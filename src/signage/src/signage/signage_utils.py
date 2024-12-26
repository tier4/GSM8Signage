# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# This Python file uses the following encoding: utf-8

DEFAULT_ROUTE_NAME = ["自動運転中", "Auto Driving"]
DEFAULT_DEPARTURE_NAME = "出発点; Start"
DEFAULT_ARRIVAL_NAME = "終点; Last Stop"
PREVIOUS_STATION_INDEX = -1  # TODO: check whether is -1 or 0
NEXT_STATION_DISPLAY_AMOUNT = 6

from dataclasses import dataclass
from datetime import datetime
from dateutil import parser
from itertools import cycle
from rclpy.duration import Duration


@dataclass
class TaskList:
    doing_list: list
    todo_list: list
    done_list: list


@dataclass
class CurrentTask:
    departure_station: list
    arrival_station: list
    depart_time: int


@dataclass
class ScheduleDetails:
    updated_time: str
    schedule_id: str
    schedule_type: str


@dataclass
class DisplayDetails:
    route_name: list
    previous_station: list
    next_station_list: list


def init_TaskList():
    return TaskList([], [], [])


def init_CurrentTask():
    return CurrentTask(["", ""], ["", ""], 0)


def init_ScheduleDetails():
    return ScheduleDetails("", "", "")


def init_DisplayDetails():
    return DisplayDetails(DEFAULT_ROUTE_NAME, ["", ""], [["", ""] * 5])


def check_schedule_update(schedule_details, data):
    return (
        schedule_details.updated_time == data["updated_at"]
        and schedule_details.schedule_id == data["schedule_id"]
    )


def update_schedule_details(data):
    return ScheduleDetails(data["updated_at"], data["schedule_id"], data["schedule_type"])


def process_tag(tags_list, key):
    for item in tags_list:
        if item["key"] == key:
            return item["value"]
    return ""


def split_name(name_string):
    name_list = name_string.split(";")
    if len(name_list) < 2:
        name_list.append("")
    return name_list


def get_route_name(tag_list):
    route_name = process_tag(tag_list, "route_name")
    if not route_name:
        return DEFAULT_ROUTE_NAME
    return split_name(route_name)


def separate_task_list(task_list):
    doing_list = []
    todo_list = []
    done_list = []
    for task in task_list:
        if task["task_type"] == "move":
            if task["status"] in ["doing"]:
                doing_list.append(task)
            elif task["status"] in ["todo"]:
                todo_list.append(task)
            elif task["status"] in ["done"]:
                done_list.append(task)
    return TaskList(doing_list, todo_list, done_list)


def process_current_task(task):
    if task.get("origin", "").get("name", ""):
        departure_station = split_name(task.get("origin", "").get("name", ""))
    else:
        departure_station = split_name(DEFAULT_DEPARTURE_NAME)

    if task.get("destination", "").get("name", ""):
        arrival_station = split_name(task.get("destination", "").get("name", ""))
    else:
        arrival_station = split_name(DEFAULT_ARRIVAL_NAME)

    try:
        date_time_obj = parser.parse(task["plan_start_time"])
        depart_time = datetime.timestamp(date_time_obj)
    except:
        depart_time = 0

    return CurrentTask(departure_station, arrival_station, depart_time)


def get_previous_station_name_from_fms(done_list):
    previous_station_task = done_list[PREVIOUS_STATION_INDEX]
    return split_name(previous_station_task.get("origin", "").get("name", DEFAULT_DEPARTURE_NAME))


def repeat_task_for_loop(station_list):
    station_cycle = cycle(station_list)
    for _ in range(NEXT_STATION_DISPLAY_AMOUNT - len(station_list)):
        station_list.append(next(station_cycle))
    return station_list


def auto_add_empty_list(station_list):
    for _ in range(NEXT_STATION_DISPLAY_AMOUNT - len(station_list)):
        station_list.append(["", ""])


def create_next_station_list(current_task_details, todo_list, call_type, schedule_type=""):
    station_list = [current_task_details.arrival_station]

    for task in todo_list:
        station_list.append(
            split_name(task.get("destination", "").get("name", DEFAULT_ARRIVAL_NAME))
        )

    if call_type == "local" and schedule_type == "loop":
        # Need this condition, because FMS will not include the departure_station in the task
        if current_task_details.departure_station[1] != "Start":
            station_list.append(current_task_details.departure_station)

    if len(station_list) < NEXT_STATION_DISPLAY_AMOUNT and schedule_type == "loop":
        station_list = repeat_task_for_loop(station_list)

    auto_add_empty_list(station_list)

    return station_list[: NEXT_STATION_DISPLAY_AMOUNT - 1]


def get_remain_minute(depart_time, current_time):
    return (depart_time - current_time) / 60


def handle_phrase(phrase_type, remain_minute=0):
    return {
        "final": "終点です。\nご乗車ありがとうございました",
        "remain_minute": "このバスはあと{}分程で出発します".format(str(remain_minute)),
        "departing": "間もなく発車時刻です",
        "arriving": "間もなく到着します",
    }.get(phrase_type, "")


def check_timeout(current_time, trigger_time, duration):
    return current_time - trigger_time > Duration(seconds=duration)
