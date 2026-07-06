# Release Information

## Latest Release: none yet

**Status:** Active development, pre-hardware

No version has been tagged. This project is a software/planning scaffold
until the physical car exists — see the roadmap checklist in
[README.md](README.md) and open
[issues](https://github.com/Mukller/fira-autonomous-rc-car/issues).

The first tagged release (`v0.1.0`) will follow the project's own
convention ([[feedback_releases]] — every version gets a git tag and a
GitHub release) once there is something a release actually represents:
either a working ROS 2 stack validated on the physical car, or a stable
snapshot of the design/planning docs. Right now the design docs
(`docs/`, `EXTERNAL_SOURCES.md`) are further along than the hardware, so
tagging a release before a real test run would overstate readiness.

### What exists today

- ✅ 3D-printable chassis model, dimensions verified against FIRA size limits
- ✅ Electronics BOM and wiring plan
- ✅ ROS 2 node scaffold (lane detection, steering, speed, serial bridge)
- ✅ Arduino firmware for the drive microcontroller
- ✅ Camera/HSV calibration tooling
- ⬜ Physical hardware assembled
- ⬜ Any node tested against a real camera or motor
- ⬜ A completed test track run
