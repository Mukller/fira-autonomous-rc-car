"""Steering control: converts lane-center pixel offset into a servo angle.

Subscribes to 'lane_offset' (std_msgs/Float32, pixels — positive means the
lane center is to the right of the image center) and publishes a servo
command in degrees on 'steering_angle_deg' for the drive microcontroller
(Arduino/ESP32) to consume over serial (see tools/serial_bridge.py, not yet
written — roadmap item).

Starting point is a simple P controller; the plan is to add integral term
once real-world response (steering slack, servo deadband) is measured on
the physical car, and to add clamping tuned to the actual MG90s + Ackermann
linkage (Print-09_Stearing / Print-11_Bridge) throw limits.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class SteeringControlNode(Node):

    def __init__(self):
        super().__init__('steering_control_node')

        self.declare_parameter('kp', 0.08)
        self.declare_parameter('center_angle_deg', 90.0)
        self.declare_parameter('max_deflection_deg', 30.0)

        self.kp = float(self.get_parameter('kp').value)
        self.center_angle_deg = float(
            self.get_parameter('center_angle_deg').value)
        self.max_deflection_deg = float(
            self.get_parameter('max_deflection_deg').value)

        self.subscription = self.create_subscription(
            Float32, 'lane_offset', self.on_offset, 10)
        self.angle_pub = self.create_publisher(
            Float32, 'steering_angle_deg', 10)

        self.get_logger().info('steering_control_node started')

    def on_offset(self, msg: Float32) -> None:
        deflection = self.kp * msg.data
        deflection = max(
            -self.max_deflection_deg, min(self.max_deflection_deg, deflection))
        angle = self.center_angle_deg + deflection
        self.angle_pub.publish(Float32(data=angle))


def main(args=None):
    rclpy.init(args=args)
    node = SteeringControlNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
