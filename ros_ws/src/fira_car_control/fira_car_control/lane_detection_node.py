"""Onboard lane detection for a real camera.

Architecture follows docs/lane-detection-adaptation.md: this is a fresh
implementation for a real camera feed, not a port of the GPL-3.0 simulator
code in external/pandas-team-avis-engine (Canny/Hough/HSV are generic
OpenCV techniques, not code copied from that repository).

The actual pixel math lives in algorithms.py (kept free of rclpy so it can
be unit-tested with plain pytest, see ros_ws/src/fira_car_control/test/).
This module is just the ROS 2 wiring around it.

Camera intrinsics/perspective matrix are placeholders until the physical
camera is mounted and calibrated (see roadmap item "calibrate_camera.py").
"""

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32

from fira_car_control.algorithms import compute_lane_offset, smooth_offset


class LaneDetectionNode(Node):

    def __init__(self):
        super().__init__('lane_detection_node')

        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('smoothing_alpha', 0.4)
        self.declare_parameter('outlier_std_threshold', 2.0)

        image_topic = self.get_parameter('image_topic').value
        self.alpha = float(self.get_parameter('smoothing_alpha').value)
        self.outlier_std_threshold = float(
            self.get_parameter('outlier_std_threshold').value)

        self.bridge = CvBridge()
        self.smoothed_offset = None

        # TODO(roadmap): fill in from tools/calibrate_camera.py output.
        self.camera_matrix = None
        self.dist_coeffs = None
        # TODO(roadmap): fill in from a one-time perspective calibration
        # once the camera is physically mounted on Print-01_Main-body.
        self.perspective_matrix = None

        self.subscription = self.create_subscription(
            Image, image_topic, self.on_image, 10)
        self.offset_pub = self.create_publisher(Float32, 'lane_offset', 10)

        self.get_logger().info(
            f'lane_detection_node listening on {image_topic}')

    def on_image(self, msg: Image) -> None:
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        if self.camera_matrix is not None:
            frame = cv2.undistort(frame, self.camera_matrix, self.dist_coeffs)

        if self.perspective_matrix is not None:
            h, w = frame.shape[:2]
            frame = cv2.warpPerspective(frame, self.perspective_matrix, (w, h))

        offset = compute_lane_offset(frame, self.outlier_std_threshold)
        if offset is None:
            self.get_logger().warn('lane_detection: no lane found this frame')
            return

        self.smoothed_offset = smooth_offset(
            self.smoothed_offset, offset, self.alpha)
        self.offset_pub.publish(Float32(data=float(self.smoothed_offset)))


def main(args=None):
    rclpy.init(args=args)
    node = LaneDetectionNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
