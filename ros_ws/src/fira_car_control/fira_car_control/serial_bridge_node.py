"""Bridge between ROS 2 topics and the drive microcontroller over serial.

Subscribes to 'steering_angle_deg' and 'motor_throttle' (both
std_msgs/Float32, published by steering_control_node / speed_control_node)
and forwards them as a compact line-based protocol over UART/USB-serial to
the Arduino/ESP32 running the firmware in
firmware/drive_controller/drive_controller.ino.

Wire protocol (one line per command, newline-terminated, matches the parser
in the .ino sketch):

    S<angle_deg>\n   -- steering servo target angle, e.g. "S97.50\n"
    T<throttle>\n    -- motor throttle fraction 0.0-1.0, e.g. "T0.42\n"

This is intentionally the simplest protocol that could work: readable in a
serial monitor for debugging, no binary framing, no checksum. If USB
noise/dropped bytes turn out to be a real problem on the physical car,
that's the point to add a checksum or switch to a binary protocol — not
before, since premature framing complexity would just make debugging the
first physical test harder.

Untested against real hardware: no Arduino/ESP32 was available at the time
this was written (see roadmap issue #6). The serial device path and baud
rate are parameters so this can be pointed at whatever port shows up once
the microcontroller is wired in.
"""

import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import Float32


class SerialBridgeNode(Node):

    def __init__(self):
        super().__init__('serial_bridge_node')

        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baud_rate', 115200)

        port = self.get_parameter('serial_port').value
        baud = int(self.get_parameter('baud_rate').value)

        self.serial_conn = None
        try:
            self.serial_conn = serial.Serial(port, baud, timeout=0.1)
            self.get_logger().info(f'Opened serial port {port} @ {baud}')
        except serial.SerialException as exc:
            self.get_logger().error(
                f'Could not open serial port {port}: {exc}. '
                'Node will keep running and log dropped commands until a '
                'port becomes available.'
            )

        self.create_subscription(
            Float32, 'steering_angle_deg', self._on_steering, 10)
        self.create_subscription(
            Float32, 'motor_throttle', self._on_throttle, 10)

    def _on_steering(self, msg: Float32) -> None:
        self._send(f'S{msg.data:.2f}\n')

    def _on_throttle(self, msg: Float32) -> None:
        self._send(f'T{msg.data:.3f}\n')

    def _send(self, line: str) -> None:
        if self.serial_conn is None or not self.serial_conn.is_open:
            self.get_logger().warn(
                f'serial_bridge: dropped command, port not open: {line!r}')
            return
        try:
            self.serial_conn.write(line.encode('ascii'))
        except serial.SerialException as exc:
            self.get_logger().error(f'serial_bridge: write failed: {exc}')

    def destroy_node(self):
        if self.serial_conn is not None and self.serial_conn.is_open:
            self.serial_conn.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SerialBridgeNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
