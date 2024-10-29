# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# This Python file uses the following encoding: utf-8

import os
import json
from datetime import datetime
import aiohttp
import asyncio
from threading import Thread

import signage.signage_utils as utils
from tier4_external_api_msgs.msg import DoorStatus
from autoware_adapi_v1_msgs.msg import (
    RouteState,
    MrmState,
    OperationModeState,
    MotionState,
    LocalizationInitializationState,
)


class RouteHandler:
    def __init__(
        self,
        node,
        viewController,
        announceController,
        autoware_interface,
        parameter_interface,
        ros_service_interface,
    ):
        self._node = node
        self._viewController = viewController
        self._announce_interface = announceController
        self._autoware = autoware_interface
        self._parameter = parameter_interface.parameter
        self._service_interface = ros_service_interface
        self.AUTOWARE_IP = os.getenv("AUTOWARE_IP", "localhost")
        self._fms_payload = {
            "method": "get",
            "url": "https://"
            + os.getenv("FMS_URL", "fms.web.auto")
            + "/v1/projects/{project_id}/environments/{environment_id}/vehicles/{vehicle_id}/active_schedule",
            "body": {},
        }
        self._schedule_details = utils.init_ScheduleDetails()
        self._display_details = utils.init_DisplayDetails()
        self._current_task_details = utils.init_CurrentTask()
        self._task_list = utils.init_TaskList()
        self._display_phrase = ""
        self._in_emergency_state = False
        self._emergency_trigger_time = self._node.get_clock().now()
        self._engage_trigger_time = self._node.get_clock().now()
        self._is_stopping = True
        self._is_driving = False
        self._previous_driving_status = False
        self._reach_final = False
        self._pre_door_announce_status = DoorStatus.UNKNOWN
        self._fms_check_time = 0
        self._prev_motion_state = 0
        self._prev_route_state = 0
        self._skip_announce = False
        self._announce_engage = False
        self._in_slow_stop_state = False
        self._in_slowing_state = False
        self._announced_depart = False
        self._announced_arrive = False
        self._trigger_external_signage = False
        self._processing_thread = False

        self.process_station_list_from_fms()

        self._node.create_timer(0.2, self.route_checker_callback)
        self._node.create_timer(0.2, self.emergency_checker_callback)
        self._node.create_timer(0.2, self.view_mode_callback)
        self._node.create_timer(0.2, self.calculate_time_callback)
        self._node.create_timer(0.2, self.door_status_callback)
        self._node.create_timer(0.2, self.announce_engage_when_starting)

    def emergency_checker_callback(self):
        if (
            self._parameter.ignore_emergency
            or self._autoware.information.operation_mode == OperationModeState.STOP
        ):
            # Ignore the emergency
            self._in_emergency_state = False
            self._in_slowing_state = False
            self._in_slow_stop_state = False
            return

        current_time = self._node.get_clock().now()
        in_emergency = self._autoware.information.mrm_behavior == MrmState.EMERGENCY_STOP
        in_comfortable_stop = self._autoware.information.mrm_behavior in [
            MrmState.COMFORTABLE_STOP,
            MrmState.PULL_OVER,
        ]

        if in_comfortable_stop:
            self._in_slowing_state = self._autoware.information.motion_state == MotionState.MOVING
            self._in_slow_stop_state = (
                self._autoware.information.motion_state == MotionState.STOPPED
            )
            self._emergency_trigger_time = self._node.get_clock().now()
        elif (
            utils.check_timeout(
                current_time, self._emergency_trigger_time, self._parameter.emergency_ignore_period
            )
            or not self._parameter.freeze_emergency
        ):
            self._in_slowing_state = False
            self._in_slow_stop_state = False

        if not in_emergency:
            if (
                self._in_emergency_state
                and utils.check_timeout(
                    current_time,
                    self._emergency_trigger_time,
                    self._parameter.emergency_ignore_period,
                )
                or not self._parameter.freeze_emergency
            ):
                # only change back to false state after the emergency is on for a specific time
                self._in_emergency_state = in_emergency
            return

        # Emergency is trigger, check whether is already trigger before
        audio = ""
        if not self._in_emergency_state:
            audio = "emergency"
        elif self._in_emergency_state and utils.check_timeout(
            current_time,
            self._emergency_trigger_time,
            self._parameter.emergency_repeat_period,
        ):
            audio = "in_emergency"

        if audio:
            self._announce_interface.announce_emergency(audio)
            self._emergency_trigger_time = self._node.get_clock().now()
            self._in_emergency_state = in_emergency

    def door_status_callback(self):
        door_status = self._autoware.information.door_status
        if self._pre_door_announce_status == door_status:
            # same announce, return
            return

        if door_status == DoorStatus.OPENING:
            # Should able to give warning everytime the door is opening
            self._announce_interface.send_announce("door_open")
        elif door_status == DoorStatus.CLOSING:
            # Should able to give warning everytime the door is closing
            self._announce_interface.send_announce("door_close")

        self._pre_door_announce_status = door_status

    def announce_engage_when_starting(self):
        try:
            if not self._parameter.signage_stand_alone:
                return

            if (
                self._autoware.information.localization_init_state
                == LocalizationInitializationState.UNINITIALIZED
                or self._autoware.information.autoware_control == False
            ):
                self._prev_motion_state = 0
                return

            if (
                self._autoware.information.motion_state
                in [MotionState.STARTING, MotionState.MOVING]
                and self._prev_motion_state == 1
            ):
                if self._announce_engage and not self._skip_announce:
                    self._skip_announce = True
                elif utils.check_timeout(
                    self._node.get_clock().now(),
                    self._engage_trigger_time,
                    self._parameter.accept_start,
                ):
                    self._announce_interface.send_announce("restart_engage")
                    self._engage_trigger_time = self._node.get_clock().now()

                if self._autoware.information.motion_state == MotionState.STARTING:
                    self._service_interface.accept_start()

            # Check to see if it has not stopped waiting for start acceptance
            if self._autoware.information.motion_state != MotionState.STARTING:
                self._accept_start_time = self._node.get_clock().now()

            # Send again when stopped in starting state for a certain period of time
            if (
                self._autoware.information.motion_state == MotionState.STARTING
                and utils.check_timeout(
                    self._node.get_clock().now(),
                    self._accept_start_time,
                    self._parameter.accept_start,
                )
            ):
                self._service_interface.accept_start()

            self._prev_motion_state = self._autoware.information.motion_state
        except Exception as e:
            self._node.get_logger().error("not able to play the announce, ERROR: {}".format(str(e)))

    def process_station_list_from_fms(self, force_update=False):
        if not self._processing_thread:
            self._processing_thread = True
            thread = Thread(target=asyncio.run(self.fms_thread()), args=(force_update,))
            thread.setDaemon(True)
            thread.start()
            self._processing_thread = False

    async def fms_thread(self, force_update=False):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"http://{self.AUTOWARE_IP}:4711/v1/services/order",
                    json=self._fms_payload,
                    timeout=10,
                ) as response:
                    data = await response.json()

            self._fms_check_time = self._node.get_clock().now()

            if not data:
                self._schedule_details = utils.init_ScheduleDetails()
                self._display_details = utils.init_DisplayDetails()
                self._current_task_details = utils.init_CurrentTask()
                raise Exception("No data from fms")
            elif utils.check_schedule_update(self._schedule_details, data) and not force_update:
                self._fms_check_time = self._node.get_clock().now()
                raise Exception("same schedule, skip")

            self._schedule_details = utils.update_schedule_details(data)

            self._display_details.route_name = utils.get_route_name(
                data.get("tags", []),
            )

            self.task_list = utils.separate_task_list(data.get("tasks", []))

            if not self.task_list.doing_list and not self.task_list.todo_list:
                self._schedule_details = utils.init_ScheduleDetails()
                self._display_details = utils.init_DisplayDetails()
                self._current_task_details = utils.init_CurrentTask()
                raise Exception("doing_list is not found, skip")

            for task in self.task_list.doing_list:
                self._current_task_details = utils.process_current_task(task)

            if force_update and self._schedule_details.schedule_type != "loop":
                # Currently loop do not provide done list for previous station so we cannot remove the it
                if not self.task_list.done_list:
                    self._display_details.previous_station = ["", ""]
                else:
                    self._display_details.previous_station = (
                        utils.get_previous_station_name_from_fms(self.task_list.done_list)
                    )

            if self._display_details.previous_station == ["", ""] and self.task_list.done_list:
                self._display_details.previous_station = utils.get_previous_station_name_from_fms(
                    self.task_list.done_list
                )

            self._display_details.next_station_list = utils.create_next_station_list(
                self._current_task_details,
                self.task_list.todo_list,
                "fms",
                self._schedule_details.schedule_type,
            )

            # Reset previous station when reach goal
            if self._reach_final and self.task_list.doing_list:
                self._reach_final = False
                self._display_details.previous_station = ["", ""]

            self._fms_check_time = self._node.get_clock().now()
        except Exception as e:
            self._node.get_logger().warning(
                "Unable to get the task from FMS, ERROR: " + str(e), throttle_duration_sec=5
            )

    def arrived_goal(self):
        try:
            self._announce_interface.announce_arrived()

            if self._current_task_details == utils.init_CurrentTask():
                raise Exception("No current task details")

            self._display_details.previous_station = self._current_task_details.departure_station

            if not self.task_list.todo_list:
                # Reach final station
                self._current_task_details.departure_station = (
                    self._current_task_details.arrival_station
                )
                self._current_task_details.arrival_station = ["", ""]
                self._reach_final = True
                return

            next_task = self.task_list.todo_list.pop(0)
            # Get the next task from todo_list
            self._current_task_details = utils.process_current_task(next_task)

            self._display_details.next_station_list = utils.create_next_station_list(
                self._current_task_details,
                self.task_list.todo_list,
                "local",
                self._schedule_details.schedule_type,
            )
        except Exception as e:
            self._node.get_logger().error("Unable to update the goal, ERROR: " + str(e))

    # ========== Timer Callback =============

    def route_checker_callback(self):
        try:
            if self._autoware.information.operation_mode == OperationModeState.AUTONOMOUS:
                # Check whether the vehicle is move in autonomous
                self._is_driving = True
                self._is_stopping = False
                self._announced_depart = False

                if (
                    not self._trigger_external_signage
                    and self._autoware.information.autoware_control
                ):
                    self._service_interface.trigger_external_signage(True)
                    self._trigger_external_signage = True
                if (
                    not self._announce_engage
                    and self._parameter.signage_stand_alone
                    and self._autoware.information.autoware_control
                ):
                    self._announce_interface.send_announce("engage")
                    self._service_interface.trigger_external_signage(True)
                    self._trigger_external_signage = True
                    self._announce_engage = True
            elif self._autoware.information.route_state in [RouteState.ARRIVED, RouteState.UNSET]:
                # Check whether the vehicle arrive to goal
                self._is_driving = False
                self._is_stopping = True
                self._skip_announce = False
                self._announce_engage = False
                self._announced_arrive = False

            if (
                self._autoware.information.operation_mode != OperationModeState.AUTONOMOUS
                or self._autoware.information.autoware_control != True
            ) and self._trigger_external_signage:
                self._service_interface.trigger_external_signage(False)
                self._trigger_external_signage = False

            if self._prev_route_state != RouteState.SET:
                if self._autoware.information.route_state == RouteState.SET:
                    self.process_station_list_from_fms(force_update=True)

            if not self._fms_check_time:
                self.process_station_list_from_fms()
            elif utils.check_timeout(
                self._node.get_clock().now(), self._fms_check_time, self._parameter.check_fms_time
            ):
                self.process_station_list_from_fms()

            if self._in_emergency_state:
                return

            if (
                not self._autoware.information.autoware_control
                and self._parameter.ignore_manual_driving
                and self._parameter.set_goal_by_distance
            ):
                if self._autoware.information.goal_distance < self._parameter.goal_distance:
                    self._is_stopping = True
                    self._is_driving = False
                    self._announced_depart = False

            if self._reach_final:
                self._previous_driving_status = False
                return

            if self._is_stopping and self._previous_driving_status:
                self.arrived_goal()
                self._previous_driving_status = False

            if self._is_driving:
                self._previous_driving_status = self._is_driving

            self._prev_route_state = self._autoware.information.route_state
        except Exception as e:
            self._node.get_logger().error("Error unable to check the route: " + str(e))

    def calculate_time_callback(self):
        try:
            if self._current_task_details == utils.init_CurrentTask():
                return

            remain_minute = utils.get_remain_minute(
                self._current_task_details.depart_time, self._node.get_clock().now().to_msg().sec
            )

            self._node.get_logger().info("_reach_final: " + str(self._reach_final))
            self._node.get_logger().info("remain_minute: " + str(remain_minute))

            if self._reach_final:
                # display arrive to final station
                self._display_phrase = utils.handle_phrase("final")
            elif self._is_stopping:
                # handle text and announce while bus is stopping
                if remain_minute > 2:
                    # display the text with the remaining time for departure
                    self._display_phrase = utils.handle_phrase(
                        "remain_minute", round(remain_minute)
                    )
                else:
                    # the departure time is close (within 1 min), announce going to depart
                    self._display_phrase = utils.handle_phrase("departing")
                    if not self._announced_depart:
                        self._announce_interface.announce_going_to_depart_and_arrive(
                            "going_to_depart"
                        )
                        self._announced_depart = True
            elif self._is_driving:
                # handle text and announce while bus is running
                if self._autoware.information.goal_distance < 100:
                    # display text and announce if the goal is within 100m
                    self._display_phrase = utils.handle_phrase("arriving")
                    if not self._announced_arrive:
                        self._announce_interface.announce_going_to_depart_and_arrive(
                            "going_to_arrive"
                        )
                        self._announced_arrive = True
                else:
                    self._display_phrase = ""
            else:
                self._display_phrase = ""
        except Exception as e:
            self._node.get_logger().error("Error in getting calculate the time: " + str(e))

    def view_mode_callback(self):
        try:
            self._viewController.clock_string = datetime.now().strftime("%H:%M")
            self._viewController.route_name = self._display_details.route_name
            self._viewController.departure_station_name = (
                self._current_task_details.departure_station
            )
            self._viewController.arrival_station_name = self._current_task_details.arrival_station
            self._viewController.previous_station_name = self._display_details.previous_station
            self._viewController.next_station_list = self._display_details.next_station_list
            self._viewController.display_phrase = self._display_phrase

            if self._autoware.is_disconnected:
                view_mode = "disconnected"
            elif (
                not self._autoware.information.autoware_control
                and not self._parameter.ignore_manual_driving
            ):
                view_mode = "manual_driving"
            elif self._in_emergency_state:
                view_mode = "emergency_stopped"
            elif self._in_slowing_state:
                view_mode = "slowing"
            elif self._in_slow_stop_state:
                view_mode = "slow_stop"
            elif self._is_stopping and self._current_task_details.departure_station != ["", ""]:
                view_mode = "stopping"
            elif self._is_driving and self._current_task_details.arrival_station != ["", ""]:
                view_mode = "driving"
            elif self._is_driving:
                view_mode = "auto_driving"
            elif self._current_task_details.departure_station != ["", ""]:
                view_mode = "stopping"
            else:
                view_mode = "out_of_service"
                self._announced_depart = False

            self._viewController.view_mode = view_mode
        except Exception as e:
            self._node.get_logger().error("Error in updating the view mode: " + str(e))
