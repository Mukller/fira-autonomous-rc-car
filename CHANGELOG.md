# Changelog

All notable changes to this project will be documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

No hardware build exists yet — nothing has shipped, so there is no tagged
release. This section tracks work since the project started on GitHub
(2026-07-05).

### Added
- NITROUS RC car chassis model (STL/3MF, 14 parts) by TommyB, CC0-licensed,
  in `models/`
- Reference repositories attached as git submodules under `external/`:
  Pandas-Team AVIS engine code (GPL-3.0), FIRA official Gazebo simulator
  (CC0-1.0), COONEO Raspberry/Arduino ROS car (unlicensed, reference only)
- `docs/regulation-summary.md` — FIRA Physical Division rules summary,
  chassis dimensions checked against the 600x450mm limit
- `docs/electronics-bom.md` — parts list and wiring plan, chassis part
  dimensions computed directly from STL geometry (`tools/stl_bbox.py`)
- `docs/lane-detection-adaptation.md` — plan for adapting the simulator's
  lane-detection algorithm to a real camera feed
- `ros_ws/src/fira_car_control` ROS 2 package: `lane_detection_node.py`,
  `steering_control_node.py`, `speed_control_node.py`,
  `serial_bridge_node.py`, launch file
- `firmware/drive_controller/drive_controller.ino` — Arduino firmware for
  steering servo + DC motor, serial protocol, safety timeout on lost
  connection
- `tools/calibrate_camera.py`, `tools/calibrate_hsv.py` — camera intrinsics
  and HSV threshold calibration utilities
- `EXTERNAL_SOURCES.md` — extracted reference material and authorship for
  every external repository/link used, for future reuse
- Standard repo file set (`LICENSE.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`,
  `CONTRIBUTING.md`, `RELEASE_INFO.md`), `README_EN.md` mirror with
  language switcher, GitHub topics/description
- Deeper regulation research: track width (150-350mm) and wheelbase
  (200-550mm) limits, confirmation that IR line-following sensors are
  banned (camera-based detection is effectively mandatory), confirmation
  that ready-made platforms like DonkeyCar/JetRacer are allowed in Pro
  (banned only in Youth), Pro vs Youth obstacle-course difference

### Added (cont.)
- `fira_car_control/algorithms.py` — lane-offset math, smoothing, steering
  P-controller, and throttle falloff extracted from the ROS nodes into
  plain functions, plus `test/test_algorithms.py` (12 pytest cases,
  including synthetic-frame lane detection). This is the first part of the
  control stack that has actually been run and verified, not just written
  — it doesn't need rclpy or a real camera, only opencv-python/numpy/pytest

### Known limitations
- ROS nodes and firmware are untested on physical hardware — no camera,
  microcontroller, or H-bridge has been acquired yet (see open issues).
  The pixel-math in `algorithms.py` is unit-tested; the rclpy wiring
  around it (topics, timing, real camera frames) is not.
- **Critical, unresolved:** the NITROUS chassis's actual track width and
  wheelbase haven't been measured against the regulation's 150-350mm /
  200-550mm minimums — the compact chassis size raises a real risk it
  falls short of the wheelbase minimum (see `docs/regulation-summary.md`)
- 2026 season dates not found in the regulation document yet
