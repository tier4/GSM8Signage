# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

import rclpy
from rclpy.node import Node

from signage.heartbeat import Heartbeat
from signage.view_controller import ViewControllerProperty
from signage.announce_controller import AnnounceControllerProperty
from signage.autoware_interface import AutowareInterface
from signage.parameter_interface import ParameterInterface
from signage.route_handler import RouteHandler
from signage.ros_service_interface import RosServiceInterface
from ament_index_python.packages import get_package_share_directory


def main(args=None):
    package_path = get_package_share_directory("signage")

    rclpy.init(args=args)
    node = Node("signage")

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    heartbeat = Heartbeat(node)
    autoware_interface = AutowareInterface(node)
    autoware_interface = AutowareInterface(node)
    parameter_interface = ParameterInterface(node)
    ros_service_interface = RosServiceInterface(node, parameter_interface)
    viewController = ViewControllerProperty(node, parameter_interface)
    announceController = AnnounceControllerProperty(node, autoware_interface, parameter_interface)
    route_handler = RouteHandler(
        node,
        viewController,
        announceController,
        autoware_interface,
        parameter_interface,
        ros_service_interface,
    )

    ctx = engine.rootContext()
    ctx.setContextProperty("viewController", viewController)
    ctx.setContextProperty("announceController", announceController)
    engine.load(package_path + "/resource/page/main.qml")

    if not engine.rootObjects():
        rclpy.shutdown()
        sys.exit(-1)

    while True:
        app.processEvents()
        rclpy.spin_once(node, timeout_sec=0.01)


if __name__ == "__main__":
    main()
