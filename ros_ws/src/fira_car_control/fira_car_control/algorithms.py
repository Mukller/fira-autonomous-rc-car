"""Pure algorithm functions, deliberately separated from rclpy plumbing.

The ROS nodes (lane_detection_node.py, steering_control_node.py,
speed_control_node.py) import from here and just wire pub/sub around these
functions. Keeping the math here means it can be unit-tested with plain
pytest, without ROS 2 installed — useful since this environment has no
rclpy available to run the nodes themselves, but the actual control logic
can and should be verified before real hardware arrives.
"""

import cv2
import numpy as np


def compute_lane_offset(frame: np.ndarray, outlier_std_threshold: float = 2.0):
    """Return the pixel offset of the lane center from the image center.

    Returns None if no lane line could be found in the frame.
    See docs/lane-detection-adaptation.md for why Otsu-based Canny
    thresholds and outlier rejection are used instead of the simulator
    code's fixed thresholds and bare polyfit.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

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

    left_x = _fit_line_x_at_bottom(left_pts, frame.shape[0], outlier_std_threshold)
    right_x = _fit_line_x_at_bottom(right_pts, frame.shape[0], outlier_std_threshold)

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


def _fit_line_x_at_bottom(segments, frame_height, outlier_std_threshold):
    if not segments:
        return None

    xs, ys = [], []
    for x1, y1, x2, y2 in segments:
        xs.extend([x1, x2])
        ys.extend([y1, y2])
    xs, ys = np.array(xs, dtype=float), np.array(ys, dtype=float)

    coeffs = np.polyfit(ys, xs, deg=1)
    fit = np.poly1d(coeffs)

    residuals = xs - fit(ys)
    std = residuals.std()
    if std > 0:
        keep = np.abs(residuals) < outlier_std_threshold * std
        if keep.sum() >= 2:
            coeffs = np.polyfit(ys[keep], xs[keep], deg=1)
            fit = np.poly1d(coeffs)

    return float(fit(frame_height))


def smooth_offset(previous: float | None, new: float, alpha: float) -> float:
    """Exponential smoothing: previous is None on the first sample."""
    if previous is None:
        return new
    return alpha * new + (1 - alpha) * previous


def steering_angle_from_offset(
        offset: float, kp: float, center_angle_deg: float,
        max_deflection_deg: float) -> float:
    """P-controller: pixel offset -> servo angle in degrees."""
    deflection = kp * offset
    deflection = max(-max_deflection_deg, min(max_deflection_deg, deflection))
    return center_angle_deg + deflection


def throttle_from_steering_angle(
        angle_deg: float, center_angle_deg: float, max_deflection_deg: float,
        max_throttle: float, min_throttle: float) -> float:
    """Linear throttle falloff: full speed straight, slower in turns."""
    deflection = abs(angle_deg - center_angle_deg)
    deflection_ratio = min(1.0, deflection / max_deflection_deg)
    return max_throttle - deflection_ratio * (max_throttle - min_throttle)
