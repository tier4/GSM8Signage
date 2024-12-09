from dataclasses import dataclass
import datetime
import time
import serial
import json
import os
import rclpy
from std_srvs.srv import SetBool
from std_msgs.msg import Bool
from ament_index_python.packages import get_package_share_directory
import external_signage.packet_tools as packet_tools
import uuid


@dataclass
class Display:
    address1: int
    address2: int
    height: int
    width: int
    ack_query_ack: list
    ack_data_chunk: list


class Protocol:
    SOT = 0xAA
    EOT = 0x55
    SEND_COLOR = "\x1B[34;1m"
    RECV_COLOR = "\x1B[32;1m"
    ERR_COLOR = "\x1B[31;1m"

    def __init__(self):
        self.front = Display(
            address1=0x70,
            address2=0x8F,
            height=16,
            width=128,
            ack_query_ack=[0xAA, 0x70, 0x8F, 0x07, 0x12, 0x02, 0x1A, 0x01, 0x55],
            ack_data_chunk=[0xAA, 0x70, 0x8F, 0x07, 0x20, 0x30, 0x56, 0x01, 0x55],
        )
        self.back = Display(
            address1=0x80,
            address2=0x7F,
            height=16,
            width=128,
            ack_query_ack=[0xAA, 0x80, 0x7F, 0x07, 0x12, 0x02, 0x1A, 0x01, 0x55],
            ack_data_chunk=[0xAA, 0x80, 0x7F, 0x07, 0x20, 0x30, 0x56, 0x01, 0x55],
        )
        self.side = Display(
            address1=0x90,
            address2=0x6F,
            height=24,
            width=80,
            ack_query_ack=[0xAA, 0x90, 0x6F, 0x07, 0x12, 0x02, 0x1A, 0x01, 0x55],
            ack_data_chunk=[0xAA, 0x90, 0x6F, 0x07, 0x20, 0x30, 0x56, 0x01, 0x55],
        )


class DataSender:
    def __init__(self, bus, parser, protocol, node_logger):
        self._bus = bus
        self._parser = parser
        self._protocol = protocol
        self._logger = node_logger
        self._delay_time = 0.02

    def randomname(self):
        u = uuid.uuid4()
        return u.bytes

    def _send_heartbeat(self, data, ACK_QueryACK):
        timestamp = datetime.datetime.now()
        name_time_packet = packet_tools.gen_name_time_packet(self.randomname(), timestamp, False)
        self._bus.write(name_time_packet)
        packet_tools.dump_packet(name_time_packet, None, self._protocol.SEND_COLOR)
        time.sleep(self._delay_time)
        self._bus.write(data.heartbeat_packet)
        packet_tools.dump_packet(data.heartbeat_packet, None, self._protocol.SEND_COLOR)
        buf = self._parser.wait_ack()
        if not packet_tools.lists_match(buf, ACK_QueryACK):
            if len(buf) == 0:
                self._logger.error("No ACK received for heartbeat.")
            else:
                packet_tools.dump_packet(buf, None, self._protocol.ERR_COLOR)

    def _send_data_packets(self, data, ACK_DataChunk):
        for packet in data.data_packets:
            packet_tools.dump_packet(packet, None, self._protocol.SEND_COLOR)
            self._bus.write(packet)
            buf = self._parser.wait_ack()
            if not packet_tools.lists_match(buf, ACK_DataChunk):
                if len(buf) == 0:
                    self._logger.error("No ACK received for data packet.")
                else:
                    packet_tools.dump_packet(buf, None, self._protocol.ERR_COLOR)

    def send(self, data, ACK_QueryACK, ACK_DataChunk):
        self._send_heartbeat(data, ACK_QueryACK)
        self._send_data_packets(data, ACK_DataChunk)
        return  # Exit after sending all data packets


class ExternalSignage:
    def __init__(self, node):
        self.node = node
        self.protocol = Protocol()

        package_path = get_package_share_directory("external_signage") + "/resource/td5_file/"
        node.declare_parameter("serial_port", "/dev/ttyS0")
        self._serial_port = node.get_parameter("serial_port").get_parameter_value().string_value

        try:
            self.bus = serial.Serial(
                self._serial_port,
                baudrate=38400,
                parity=serial.PARITY_EVEN,
                timeout=0.2,
                exclusive=False,
            )
            self.parser = packet_tools.Parser(self.bus)
            self._external_signage_available = True
        except Exception as e:
            self.node.get_logger().error(str(e))
            self._external_signage_available = False

        self.displays = {
            "front": self._load_display_data(self.protocol.front, package_path),
            "back": self._load_display_data(self.protocol.back, package_path),
            "side": self._load_display_data(self.protocol.side, package_path),
        }

        api_qos = rclpy.qos.QoSProfile(
            history=rclpy.qos.QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=rclpy.qos.QoSReliabilityPolicy.RELIABLE,
            durability=rclpy.qos.QoSDurabilityPolicy.TRANSIENT_LOCAL,
        )

        node.create_service(SetBool, "/signage/trigger_external", self.trigger_external_signage)
        node.create_service(SetBool, "/signage/mode_change", self.experiment_set)
        self.mode_status_pub_ = node.create_publisher(Bool, "/signage/mode_status", api_qos)

        self._settings_file = "/home/" + os.environ.get("USER") + "/settings.json"
        if os.path.exists(self._settings_file):
            with open(self._settings_file, "r") as f:
                self._settings = json.load(f)
        else:
            self._settings = {"in_experiment": False}
            with open(self._settings_file, "w") as f:
                json.dump(self._settings, f, indent=4)

        if self._settings.get("in_experiment", False):
            self.pub_mode_status(True)
            self.display_signage("experiment")
        else:
            self.pub_mode_status(False)

    def pub_mode_status(self, status):
        msg = Bool()
        msg.data = status

    def _load_display_data(self, display, package_path):
        auto_path = package_path + f"automatic_{display.width}x{display.height}.td5"
        experiment_path = package_path + f"experiment_{display.width}x{display.height}.td5"
        null_path = package_path + f"null_{display.width}x{display.height}.td5"
        return {
            "auto": packet_tools.TD5Data(
                auto_path, display.address1, display.address2, display.height, display.width
            ),
            "experiment": packet_tools.TD5Data(
                experiment_path, display.address1, display.address2, display.height, display.width
            ),
            "null": packet_tools.TD5Data(
                null_path, display.address1, display.address2, display.height, display.width
            ),
        }

    def send_data(self, display_key, data_key):
        display = self.displays[display_key]
        data = display[data_key]
        ack_query_ack = self.protocol.__dict__[display_key].ack_query_ack
        ack_data_chunk = self.protocol.__dict__[display_key].ack_data_chunk
        sender = DataSender(self.bus, self.parser, self.protocol, self.node.get_logger())
        sender.send(data, ack_query_ack, ack_data_chunk)

    def trigger_external_signage(self, request, response):
        if self._settings["in_experiment"]:
            return response

        try:
            if request.data:
                self.display_signage("auto")
            else:
                self.display_signage("null")
            response.success = True
        except Exception as e:
            self.node.get_logger().error(str(e))
        return response

    def experiment_set(self, request, response):
        try:
            if request.data:
                self.pub_mode_status(True)
                self._settings["in_experiment"] = True
                self.display_signage("experiment")
            else:
                self.pub_mode_status(False)
                self._settings["in_experiment"] = False
                self.display_signage("null")

            with open(self._settings_file, "w") as f:
                json.dump(self._settings, f, indent=4)
            response.success = True
        except Exception as e:
            self.node.get_logger().error(str(e))
        return response

    def display_signage(self, display_file):
        if not self._external_signage_available:
            return

        for display_key in self.displays:
            self.send_data(display_key, display_file)
            time.sleep(1)
