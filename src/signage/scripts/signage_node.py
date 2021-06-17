#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Python file uses the following encoding: utf-8
import sys
import os

import rospy, rospkg
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

from signage.view_controller import ViewControllerProperty
from signage.autoware_state_interface import AutowareStateInterface

def main(args=None):
    rospy.init_node('signage', anonymous=True)

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    autoware_state_interface = AutowareStateInterface()
    viewController = ViewControllerProperty(autoware_state_interface)

    ctx = engine.rootContext()
    ctx.setContextProperty("viewController", viewController)
    engine.load(os.path.join(rospkg.RosPack().get_path('signage'), 'resource', 'page', 'main.qml'))

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


