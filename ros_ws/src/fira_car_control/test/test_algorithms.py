"""Unit tests for the pure algorithm functions in fira_car_control.algorithms.

Runs with plain pytest, no ROS 2 / rclpy required — these are the functions
extracted specifically so they could be verified without a running ROS
system or real camera. Run with:

    cd ros_ws/src/fira_car_control
    python -m pytest test/
"""

import os
import sys

import cv2
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fira_car_control.algorithms import (  # noqa: E402
    compute_lane_offset,
    smooth_offset,
    steering_angle_from_offset,
    throttle_from_steering_angle,
)


def _synthetic_frame(width=320, height=240, left_x_bottom=80, right_x_bottom=240):
    """Draw two near-vertical lane lines converging slightly toward the top,
    similar to a lane seen from a forward-facing camera."""
    frame = np.full((height, width, 3), 255, dtype=np.uint8)
    top_offset = 30
    cv2.line(frame, (left_x_bottom, height), (left_x_bottom + top_offset, 0),
             (0, 0, 0), thickness=4)
    cv2.line(frame, (right_x_bottom, height), (right_x_bottom - top_offset, 0),
             (0, 0, 0), thickness=4)
    return frame


class TestComputeLaneOffset:

    def test_centered_lane_gives_near_zero_offset(self):
        # Lines symmetric around the image center (width=320 -> center 160)
        frame = _synthetic_frame(width=320, left_x_bottom=80, right_x_bottom=240)
        offset = compute_lane_offset(frame)
        assert offset is not None
        assert abs(offset) < 15, f'expected near-zero offset, got {offset}'

    def test_lane_shifted_right_gives_positive_offset(self):
        # Both lines shifted right relative to the centered case -> lane
        # center is to the right of the image center -> positive offset.
        centered = compute_lane_offset(
            _synthetic_frame(width=320, left_x_bottom=80, right_x_bottom=240))
        shifted = compute_lane_offset(
            _synthetic_frame(width=320, left_x_bottom=140, right_x_bottom=300))
        assert centered is not None and shifted is not None
        assert shifted > centered

    def test_blank_frame_returns_none(self):
        blank = np.full((240, 320, 3), 255, dtype=np.uint8)
        assert compute_lane_offset(blank) is None


class TestSmoothOffset:

    def test_first_sample_passes_through(self):
        assert smooth_offset(None, 42.0, alpha=0.4) == 42.0

    def test_smooths_toward_new_value(self):
        result = smooth_offset(previous=0.0, new=10.0, alpha=0.5)
        assert result == pytest.approx(5.0)

    def test_alpha_zero_keeps_previous(self):
        result = smooth_offset(previous=7.0, new=100.0, alpha=0.0)
        assert result == pytest.approx(7.0)


class TestSteeringAngleFromOffset:

    def test_zero_offset_gives_center_angle(self):
        angle = steering_angle_from_offset(
            0.0, kp=0.08, center_angle_deg=90.0, max_deflection_deg=30.0)
        assert angle == pytest.approx(90.0)

    def test_positive_offset_steers_right_of_center(self):
        angle = steering_angle_from_offset(
            100.0, kp=0.08, center_angle_deg=90.0, max_deflection_deg=30.0)
        assert angle > 90.0

    def test_clamps_to_max_deflection(self):
        angle = steering_angle_from_offset(
            10_000.0, kp=0.08, center_angle_deg=90.0, max_deflection_deg=30.0)
        assert angle == pytest.approx(120.0)

        angle = steering_angle_from_offset(
            -10_000.0, kp=0.08, center_angle_deg=90.0, max_deflection_deg=30.0)
        assert angle == pytest.approx(60.0)


class TestThrottleFromSteeringAngle:

    def test_straight_ahead_gives_max_throttle(self):
        throttle = throttle_from_steering_angle(
            angle_deg=90.0, center_angle_deg=90.0, max_deflection_deg=30.0,
            max_throttle=0.6, min_throttle=0.25)
        assert throttle == pytest.approx(0.6)

    def test_full_deflection_gives_min_throttle(self):
        throttle = throttle_from_steering_angle(
            angle_deg=120.0, center_angle_deg=90.0, max_deflection_deg=30.0,
            max_throttle=0.6, min_throttle=0.25)
        assert throttle == pytest.approx(0.25)

    def test_half_deflection_gives_midpoint_throttle(self):
        throttle = throttle_from_steering_angle(
            angle_deg=105.0, center_angle_deg=90.0, max_deflection_deg=30.0,
            max_throttle=0.6, min_throttle=0.25)
        assert throttle == pytest.approx((0.6 + 0.25) / 2)
