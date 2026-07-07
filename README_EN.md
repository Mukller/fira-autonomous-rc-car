<div align="center">

**English** • [Русский](README.md)

</div>

# FIRA Autonomous RC Car

A 1:10-scale autonomous RC car project for the physical division of the
**FIRA Autonomous Cars League (FACL)** / RoboCup Autonomous Cars.
Brings together a 3D-printable chassis, reference autonomous-driving code
from FIRA simulation projects, and an open-source ROS stack for
Raspberry Pi + Arduino.

Status: in development. This is not a finished product — the repository
incrementally assembles and integrates components, starting July 2026.

## Competition regulation

FIRA Autonomous Cars League consists of two divisions:

- **Physical Division** — teams design, build, and program a 1:10-scale
  autonomous RC car with Ackermann steering that must drive a track without
  human intervention.
- **Simulation Division** — developing autonomous-driving software/AI in
  the **AVIS Engine** simulator (built on ROS + Gazebo).

Official regulation sources (verify against these before competing — rules
are updated yearly):

- https://firaworldcup.org/leagues/fira-challenges/autonomous-cars/
- Pro rules (Google Docs, current version): https://docs.google.com/document/d/1PgeKrsCEL-KnZFci-iQUgFKoVnY7qiXql9oOvQACfEY/
- Youth rules: https://docs.google.com/document/d/1pyhgvSQw7eaGDG0dzchA0VkbOYnGsd1_AVNhvs1iz8c/

A paraphrased summary of the key requirements (1:10 scale, 600x450mm size
limit, Ackermann steering, onboard/offboard processing score multiplier) is
in [`docs/regulation-summary.md`](docs/regulation-summary.md).

This project targets the **Physical Division** (1:10 RC car).

## Repository structure

```
models/     — chassis 3D model (STL/3MF) for printing
external/   — reference projects, attached as git submodules (see below)
docs/       — regulation, electronics, algorithm-adaptation plan
ros_ws/     — ROS 2 package fira_car_control: lane detection, steering,
              speed, and serial-bridge nodes
firmware/   — drive microcontroller firmware (servo + DC motor)
tools/      — STL bbox, camera calibration, HSV calibration
```

## Documentation

- [`docs/regulation-summary.md`](docs/regulation-summary.md) — regulation summary
- [`docs/electronics-bom.md`](docs/electronics-bom.md) — electronics plan, BOM,
  real part dimensions (computed from STL via `tools/stl_bbox.py`)
- [`docs/lane-detection-adaptation.md`](docs/lane-detection-adaptation.md) —
  plan for adapting the simulator's lane-detection algorithm to a real camera

## External material used (attribution)

### Chassis 3D model

**NITROUS — 3D Printed RC Car** by **TommyB**
- Source: https://www.printables.com/model/415497-3d-printed-rc-car
- License: Creative Commons CC0 1.0 (Public Domain) — the author marked the
  model as an original creation; attribution isn't legally required but is
  given here out of respect for the author.
- Files live in [`models/`](models/), unmodified from the original.

### Reference code (git submodules)

Code from external repositories is **not copied**, it's attached as a git
submodule — this preserves the full history, authorship, and license of
the original.

| Path | Source | License | Purpose |
|---|---|---|---|
| `external/pandas-team-avis-engine` | [Pandas-Team/Autonomous-Car-Simulation-Based-on-AVIS-Engine-FIRA-2021](https://github.com/Pandas-Team/Autonomous-Car-Simulation-Based-on-AVIS-Engine-FIRA-2021) | GPL-3.0 | Lane/sign detection, PID control — reference for simulation algorithms |
| `external/fira-autonomous-cars-simulator` | [Fira-Autonomous-Cars/FIRA-Autonomous-Cars-Simulator](https://github.com/Fira-Autonomous-Cars/FIRA-Autonomous-Cars-Simulator) | CC0-1.0 | Official FIRA simulator |
| `external/arduino-raspberry-ros-car` | [COONEO/Arduino_Raspberry_ROS_Car](https://github.com/COONEO/Arduino_Raspberry_ROS_Car) | unspecified (all rights reserved) | Reference ROS stack for Raspberry Pi + Arduino on a physical car |

Code from `COONEO/Arduino_Raspberry_ROS_Car` has no open license — used only
as read-only reference material/submodule, not copied into this
repository's own files.

### Additional material studied

- Discussion on controlling an RC car via ROS + Raspberry Pi:
  https://www.reddit.com/r/robotics/comments/alpfrj/i_controlled_a_rc_car_using_ros_and_a_raspberry/

A full extract per source (authors, licenses, architecture, what's actually
reusable) is in [`EXTERNAL_SOURCES.md`](EXTERNAL_SOURCES.md).

## Roadmap

- [x] Study the Physical Division regulation (summary in
      `docs/regulation-summary.md`, chassis dimensions checked against the
      limits — comfortably within them)
- [x] Work out the electronics plan and BOM for the NITROUS geometry
      (`docs/electronics-bom.md`, dimensions computed from STL)
- [x] Write the lane-detection adaptation plan for a real camera
      (`docs/lane-detection-adaptation.md`)
- [x] Scaffold ROS 2 steering/speed control nodes (`ros_ws/`) — needs a
      real camera and calibration to finish tuning
- [x] Write `serial_bridge_node.py` — bridges ROS topics to the
      microcontroller over UART (`S<angle>`/`T<throttle>` protocol)
- [x] Write the drive microcontroller firmware
      (`firmware/drive_controller/`) — servo+motor, safety timeout;
      untested on real hardware (no board/H-bridge on hand yet)
- [x] Write `tools/calibrate_camera.py` and `tools/calibrate_hsv.py` —
      ready to run as soon as a real camera is available
- [ ] Buy the electronics per the BOM (Raspberry Pi/Jetson, camera,
      Arduino/ESP32, H-bridge/ESC)
- [ ] Design and print a camera mount (the original model has none — the
      author never did camera-based autonomous driving)
- [ ] Assemble the physical chassis from `models/`
- [ ] Run the firmware bring-up checklist on real hardware
      (`firmware/drive_controller/README.md`)
- [ ] Tune `lane_detection_node.py` on real track footage
- [ ] Run the first test-track drive
- [x] Confirm the open regulation questions — most are resolved (see
      `docs/regulation-summary.md`): no mass limit, IR line-following
      sensors are banned (camera is mandatory, not optional), ready-made
      platforms are allowed in Pro. **One critical item remains open**:
      NITROUS chassis track width (150-350mm) and wheelbase (200-550mm)
      haven't been measured — the compact model may not meet these minimums
- [ ] Measure track width and wheelbase during chassis assembly, confirm
      regulation compliance (see the warning in `docs/regulation-summary.md`)
- [ ] Confirm 2026 season dates closer to the event
- [ ] Prepare documentation/video for competition submission

## License for original code

Code and documentation authored within this repository (outside
`external/` and `models/`) are distributed under the MIT license (see
[LICENSE.md](LICENSE.md)) unless stated otherwise.

## Additional files

- [CHANGELOG.md](CHANGELOG.md) — change history
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — project conduct rules
- [RELEASE_INFO.md](RELEASE_INFO.md) — release status
- [EXTERNAL_SOURCES.md](EXTERNAL_SOURCES.md) — attribution and extract for every external source
