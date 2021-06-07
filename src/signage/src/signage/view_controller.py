#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Python file uses the following encoding: utf-8
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot

import rospy

from autoware_api_msgs.msg import AwapiAutowareStatus
from dummy_msgs.msg import ApiDummyStation, RouteStation

class ViewControllerProperty(QObject):
    _view_mode_changed_signal = pyqtSignal(str)
    _route_name_signal = pyqtSignal(str)
    _get_departure_station_name_signal = pyqtSignal(str)
    _get_arrival_station_name_signal = pyqtSignal(str)
    _get_next_station_list_signal = pyqtSignal(list)
    _get_previous_station_list_signal = pyqtSignal(list)
    def __init__(self):
        super(ViewControllerProperty, self).__init__()
        rospy.Subscriber("/awapi/autoware/get/status", AwapiAutowareStatus, self.sub_autoware_status)
        rospy.Subscriber("/api/get/stations", ApiDummyStation, self.sub_route_station)
        rospy.Subscriber("/api/get/route", RouteStation, self.sub_route)

        self.is_auto_mode = False
        self.is_emergency_mode = False
        self.is_stopping = False
        self.is_driving = False
        self._view_mode = ""
        self._route_id = ""
        self._route_name = ""
        self._stations = {}
        self._staion_arrangement = []
        self._departure_station_id = ""
        self._arrival_station_id = ""
        self._departure_station_name = ""
        self._arrival_station_name = ""
        self._next_station_list = ["", "", ""]
        self._previous_station_list = ["", "", ""]

        rospy.Timer(rospy.Duration(0.1), self.update_view_state)


    # view mode
    @pyqtProperty(str, notify=_view_mode_changed_signal)
    def view_mode(self):
        return self._view_mode

    @view_mode.setter
    def view_mode(self, view_mode):
        self._view_mode = view_mode
        self._view_mode_changed_signal.emit(view_mode)

    def update_view_state(self, event):
        if self.is_emergency_mode:
            self.view_mode = "emergency_stopped"
        elif not self.is_auto_mode:
            self.view_mode = "manual_driving"
        elif self.is_stopping:
            self.view_mode = "stopping"
        elif self.is_driving:
            self.view_mode = "driving"
        else:
            self.view_mode = "out_of_service"


    def sub_autoware_status(self, message):
        self.is_emergency_mode = message.emergency_stopped
        self.is_auto_mode = message.control_mode == 1
        self.is_stopping = message.autoware_state != "Driving" and message.autoware_state != "InitializingVehicle"
        self.is_driving = message.autoware_state == "Driving"

    def sub_route_station(self, topic):
        if not topic:
            return True
        self._route_id = topic.id
        self.route_name = topic.name
        stations = topic.stations
        for station in stations:
            station_data = {}
            station_data["name"] = station.name
            station_data["eta"] = station.eta
            station_data["etd"] = station.eta
            self._staion_arrangement.append(station.id)
            self._stations[station.id] = station_data

    def sub_route(self, topic):
        if not topic:
            return True
        self._departure_station_id = topic.departure_station_id
        self.generate_next_previous_station_list(self._departure_station_id)
        self.departure_station_name = self._stations[self._departure_station_id]["name"]
        self._arrival_station_id = topic.arrival_station_id
        self.arrival_station_name = self._stations[self._arrival_station_id]["name"]

    def generate_next_previous_station_list(self, station_id):
        list_index = self._staion_arrangement.index(station_id)
        station_list = []
        for next_station in self._staion_arrangement[list_index:][1:4]:
            station_list.append(self._stations[next_station]["name"])
        self.next_station_list = list(station_list)

        station_list = []
        for next_station in self._staion_arrangement[:list_index][-3:][::-1]:
            station_list.append(self._stations[next_station]["name"])
        self.previous_station_list = list(station_list)

    # QMLへroute_nameを反映させる
    @pyqtProperty("QString", notify=_route_name_signal)
    def route_name(self):
        return self._route_name

    @route_name.setter
    def route_name(self, route_name):
        self._route_name = route_name
        self._route_name_signal.emit(route_name)

    # QMLへroute_nameを反映させる
    @pyqtProperty("QString", notify=_get_departure_station_name_signal)
    def departure_station_name(self):
        return self._departure_station_name

    @departure_station_name.setter
    def departure_station_name(self, departure_station_name):
        self._departure_station_name = departure_station_name
        self._get_departure_station_name_signal.emit(departure_station_name)

    # QMLへroute_nameを反映させる
    @pyqtProperty("QString", notify=_get_arrival_station_name_signal)
    def arrival_station_name(self):
        return self._arrival_station_name

    @arrival_station_name.setter
    def arrival_station_name(self, arrival_station_name):
        self._arrival_station_name = arrival_station_name
        self._get_arrival_station_name_signal.emit(arrival_station_name)

    # QMLへのsignal
    @pyqtProperty(list, notify=_get_next_station_list_signal)
    def next_station_list(self):
        return self._next_station_list

    @next_station_list.setter
    def next_station_list(self, next_station_list):
        self._next_station_list = next_station_list
        self._get_next_station_list_signal.emit(next_station_list)

    # QMLへのsignal
    @pyqtProperty(list, notify=_get_previous_station_list_signal)
    def previous_station_list(self):
        return self._previous_station_list

    @previous_station_list.setter
    def previous_station_list(self, previous_station_list):
        self._previous_station_list = previous_station_list
        self._get_previous_station_list_signal.emit(previous_station_list)