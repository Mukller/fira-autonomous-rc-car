"""Speed control: slows the car down proportionally to steering deflection.

Starting point for a real track: full throttle in a straight line, reduced
throttle in turns. Subscribes to 'steering_angle_deg' and publishes a PWM
duty-cycle fraction (0.0-1.0) on 'motor_throttle' for the drive
microcontroller to convert into an actual PWM signal for the DC-motor 280
+ gearbox drivetrain (see docs/electronics-bom.md).

The throttle math lives in algorithms.py so it can be unit-tested without
rclpy installed. This is intentionally simple (linear falloff) — a real
speed profile will need retuning once lap-time and slip behaviour are
measured on the physical track, and the FIRA scoring gives no credit for
finishing off-track.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

from fira_car_control.algorithms import throttle_from_steering_angle


class SpeedControlNode(Node):

    def __init__(self):
        super().__init__('speed_control_node')

        self.declare_parameter('center_angle_deg', 90.0)
        self.declare_parameter('max_deflection_deg', 30.0)
        self.declare_parameter('max_throttle', 0.6)
        self.declare_parameter('min_throttle', 0.25)

        self.center_angle_deg = float(
            self.get_parameter('center_angle_deg').value)
        self.max_deflection_deg = float(
            self.get_parameter('max_deflection_deg').value)
        self.max_throttle = float(self.get_parameter('max_throttle').value)
        self.min_throttle = float(self.get_parameter('min_throttle').value)

        self.subscription = self.create_subscription(
            Float32, 'steering_angle_deg', self.on_steering_angle, 10)
        self.throttle_pub = self.create_publisher(
            Float32, 'motor_throttle', 10)

        self.get_logger().info('speed_control_node started')

    def on_steering_angle(self, msg: Float32) -> None:
        throttle = throttle_from_steering_angle(
            msg.data, self.center_angle_deg, self.max_deflection_deg,
            self.max_throttle, self.min_throttle)
        self.throttle_pub.publish(Float32(data=throttle))


def main(args=None):
    rclpy.init(args=args)
    node = SpeedControlNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
