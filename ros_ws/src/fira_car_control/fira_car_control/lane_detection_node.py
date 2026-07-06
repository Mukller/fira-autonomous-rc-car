"""Onboard lane detection for a real camera.

Architecture follows docs/lane-detection-adaptation.md: this is a fresh
implementation for a real camera feed, not a port of the GPL-3.0 simulator
code in external/pandas-team-avis-engine (Canny/Hough/HSV are generic
OpenCV techniques, not code copied from that repository).

Pipeline: undistort -> perspective warp (bird's-eye) -> adaptive Canny
(Otsu-based thresholds) -> Hough line segments -> split left/right by slope
-> robust linear fit with outlier rejection -> exponential smoothing of the
lane-center offset -> publish std_msgs/Float32 on 'lane_offset'.

Camera intrinsics/perspective matrix are placeholders until the physical
camera is mounted and calibrated (see roadmap item "calibrate_camera.py").
"""

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32


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

        offset = self._compute_lane_offset(frame)
        if offset is None:
            self.get_logger().warn('lane_detection: no lane found this frame')
            return

        if self.smoothed_offset is None:
            self.smoothed_offset = offset
        else:
            self.smoothed_offset = (
                self.alpha * offset + (1 - self.alpha) * self.smoothed_offset
            )

        self.offset_pub.publish(Float32(data=float(self.smoothed_offset)))

    def _compute_lane_offset(self, frame: np.ndarray) -> float | None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Adaptive threshold via Otsu instead of the fixed Canny(100, 250)
        # thresholds used in the simulator code — real lighting varies.
        otsu_thresh, _ = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        edges = cv2.Canny(blurred, 0.5 * otsu_thresh, otsu_thresh)

        lines = cv2.HoughLinesP(
            edges, rho=1, theta=np.pi / 180, threshold=20,
            minLineLength=frame.shape[0] // 8, maxLineGap=frame.shape[0] // 20)

        if lines is None:
            return None

        left_pts, right_pts = [], []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 == x1:
                continue
            slope = (y2 - y1) / (x2 - x1)
            if abs(slope) < 0.3:
                continue
            (left_pts if slope < 0 else right_pts).append((x1, y1, x2, y2))

        left_x = self._fit_line_x_at_bottom(left_pts, frame.shape[0])
        right_x = self._fit_line_x_at_bottom(right_pts, frame.shape[0])

        if left_x is None and right_x is None:
            return None
        if left_x is None:
            lane_center = right_x - frame.shape[1] / 4
        elif right_x is None:
            lane_center = left_x + frame.shape[1] / 4
        else:
            lane_center = (left_x + right_x) / 2

        image_center = frame.shape[1] / 2
        return float(lane_center - image_center)

    def _fit_line_x_at_bottom(self, segments, frame_height) -> float | None:
        if not segments:
            return None

        xs, ys = [], []
        for x1, y1, x2, y2 in segments:
            xs.extend([x1, x2])
            ys.extend([y1, y2])
        xs, ys = np.array(xs, dtype=float), np.array(ys, dtype=float)

        coeffs = np.polyfit(ys, xs, deg=1)
        fit = np.poly1d(coeffs)

        # Reject outliers > outlier_std_threshold std devs from the first
        # fit, then refit — a lightweight stand-in for full RANSAC.
        residuals = xs - fit(ys)
        std = residuals.std()
        if std > 0:
            keep = np.abs(residuals) < self.outlier_std_threshold * std
            if keep.sum() >= 2:
                coeffs = np.polyfit(ys[keep], xs[keep], deg=1)
                fit = np.poly1d(coeffs)

        return float(fit(frame_height))


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
