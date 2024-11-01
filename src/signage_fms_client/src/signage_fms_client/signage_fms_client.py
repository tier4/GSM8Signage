# This Python file uses the following encoding: utf-8
import os

import rclpy
from rclpy.node import Node

import requests
from std_msgs.msg import String


class FMSClient(Node):
    def __init__(self, node):
        self._node = node
        node.declare_parameter("post_request_time", 8.0)
        self._post_request_time = (
            node.get_parameter("post_request_time").get_parameter_value().double_value
        )
        self._fms_payload = {
            "method": "get",
            "url": "https://"
            + os.getenv("FMS_URL", "fms.web.auto")
            + "/v1/projects/{project_id}/environments/{environment_id}/vehicles/{vehicle_id}/active_schedule",
            "body": {},
        }
        self.AUTOWARE_IP = os.getenv("AUTOWARE_IP", "localhost")
        self.schedule_pub_ = node.create_publisher(String, "/signage/active_schedule", 10)
        self.timer = node.create_timer(self._post_request_time + 0.5, self.pub_schedule)

    def pub_schedule(self):
        try:
            msg = String()
            respond = requests.post(
                "http://{}:4711/v1/services/order".format(self.AUTOWARE_IP),
                json=self._fms_payload,
                timeout=self._post_request_time,
            )
            msg.data = respond.text
            self.schedule_pub_.publish(msg)
        except Exception as e:
            self._node.get_logger().warning(
                "Unable to get the task from FMS, ERROR: " + str(e), throttle_duration_sec=5
            )


def main(args=None):

    rclpy.init(args=args)
    node = Node("signage_fms_client")

    signage_fms_client = FMSClient(node)

    while True:
        rclpy.spin_once(node, timeout_sec=0.01)


if __name__ == "__main__":
    main()
