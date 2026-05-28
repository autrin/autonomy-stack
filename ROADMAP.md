# Roadmap

A small autonomous car, built from a base RC chassis up. The hardware is intentionally cheap — the focus is the software: a clean, tested, documented autonomy stack spanning **perception → localization → planning → control**.

Development happens in phases, each ending with a demoable artifact. The deliverable — working code, tests, docs, a demo — matters more than the timeline.

---

## Phase 0 — Project scaffolding

Set the project up with the shape of real software from day one.

- [ ] Initialize the repo: README, this roadmap, MIT license, `.gitignore`.
- [ ] Set up the Python project: `pyproject.toml`, ruff (lint), mypy (types), pytest (tests), and a `Makefile` with `make lint`, `make test`, `make run`.
- [ ] GitHub Actions CI running lint + types + tests on every push.
- [ ] Establish the module layout:
  ```
  autonomy_stack/
  ├── hardware/      # motor driver, servo, sensor interfaces (behind ABCs)
  ├── perception/    # camera processing, lane / object detection
  ├── localization/  # pose estimation
  ├── planning/      # path planning
  ├── control/       # PID, pure pursuit
  ├── telemetry/     # logging + replay
  ├── nodes/         # runnable processes
  └── sim/           # offline simulator
  ```
  This maps cleanly onto ROS 2 packages for the planned v2.
- [ ] Define the interface contracts (`MotorDriver`, `Camera`, `Planner`, etc.) as abstract base classes before implementing them. This allows real hardware to be swapped for fakes in tests.

**Artifact:** well-structured repo, green CI.

---

## Phase 1 — Hardware bring-up & teleop

A car drivable from a laptop. No autonomy yet.

- [ ] Set up the Raspberry Pi: headless boot, SSH, WiFi. Document the steps in `docs/setup.md`.
- [ ] Implement `MotorDriver` (PWM → ESC) and `SteeringServo` (PWM → servo), each with unit tests against a mock PWM interface.
- [ ] Build a `teleop` node: keyboard input on the laptop → WebSocket → Pi → car.
- [ ] Ensure clean shutdown: `Ctrl-C` always brings the car to a stopped state.

**Artifact:** drive the car from a laptop. `v0.1-teleop`.

### Hardware

| Item | Approx |
|---|---|
| 1/10-scale RC car (used Traxxas Slash 2WD or WLtoys 144001) | $70–100 |
| Raspberry Pi 5 (4GB) + case/cooling | $75 |
| Pi Camera Module 3 Wide | $35 |
| PCA9685 16-channel PWM breakout | $15 |
| BNO055 IMU breakout | $20 |
| HC-SR04 ultrasonic sensors (x2) | $10 |
| USB power bank (5V/3A) | $15 |
| MicroSD 32GB + wiring + mounting | $25 |
| **Total** | **~$265** |

---

## Phase 2 — Sensing & logging

Read every sensor reliably; log everything; replay any session offline.

- [ ] Camera capture at 30 FPS, downsampled to 640×360, timestamped.
- [ ] IMU read at 100 Hz, timestamped.
- [ ] Telemetry logger: every sensor reading, command, and state transition written to structured logs (Parquet).
- [ ] Replay tool: load a log and feed it back through the perception/planning modules offline. This is how autonomy gets debugged without driving the car.
- [ ] Web UI (Flask + single page): live camera feed + IMU plot during a session.
- [ ] Integration tests: feed a recorded log through the replay tool, assert deterministic output.

**Artifact:** capture every signal during a drive, replay it offline. `v0.2-telemetry`.

---

## Phase 3 — Lane following

The car drives itself on a marked path, using classical computer vision.

- [ ] Lay down a lane course (painter's tape on the floor).
- [ ] Classical lane detector in OpenCV: HSV threshold → ROI mask → Hough line transform → lane fit.
- [ ] Pure-pursuit steering controller.
- [ ] Constant-cruise speed controller (PID once wheel-speed feedback is available).
- [ ] Safety node: bounds-checks every command, watchdogs the perception pipeline, coasts to a stop if perception drops out.
- [ ] Perception tests using recorded camera frames as fixtures (deterministic pipeline).

**Artifact:** car follows a lane autonomously for 30+ seconds, with a perception-overlay view. `v0.3-lane-following`.

---

## Phase 4 — Obstacle detection & avoidance

The car notices obstacles and reacts.

- [ ] Front-mounted ultrasonic (or VL53L1X time-of-flight) sensing; publish detections at 20 Hz.
- [ ] Planner extension: slow at threshold distance, stop at close range.
- [ ] *(Stretch)* Add 2D LiDAR (RPLIDAR A1 / YDLIDAR X2L) and implement a "follow-the-gap" planner: find the largest open sector and steer toward it.

**Artifact:** car follows a lane and avoids obstacles. `v0.4-avoidance`.

---

## Phase 5 — Localization

The car estimates where it is, not just what it sees.

- [ ] Dead reckoning: integrate IMU + commanded velocity for a short-horizon position estimate.
- [ ] AprilTag landmarks: fixed printed tags give absolute position fixes; dead-reckon between them.
- [ ] Visualize the position estimate live on a 2D map in the web UI.
- [ ] *(Stretch)* A particle filter fusing dead reckoning with AprilTag observations, or visual odometry via feature tracking.

**Artifact:** the car maintains a live position estimate during a run. `v0.5-localization`.

---

## Phase 6 — Polish, tests, documentation

Convert a working project into a portfolio-grade one.

- [ ] Audit module boundaries; ensure integration tests cover the full perception → planning → control pipeline against recorded data.
- [ ] Type hints throughout; `mypy --strict` in CI.
- [ ] Docstrings on all public functions; API docs generated with mkdocs, hosted on GitHub Pages.
- [ ] Documentation set:
  - `docs/architecture.md` — system block diagram.
  - `docs/perception.md` — the CV pipeline, with example images.
  - `docs/control.md` — pure-pursuit math and derivation.
  - `docs/safety.md` — watchdog design and failure-mode analysis.
  - `docs/setup.md` — reproducible build instructions.
- [ ] Clean demo video: real-world view alongside a dashboard (camera overlays, position estimate, state, commands).

**Artifact:** `v1.0`. Project featured on the portfolio site.

---

## Phase 7 — Writeup

- [ ] Portfolio project card, leading with the demo video.
- [ ] One in-depth technical post (~1500–2500 words) on a single meaty topic: the pure-pursuit derivation, the safety architecture, the AprilTag localization, or the test/replay infrastructure.

---

## Phase 8 (Stretch) — ROS 2 rewrite

Migrate the stack to ROS 2 and add simulation. Turns a strong project into a very strong one for robotics-flavored roles.

- [ ] ROS 2 Humble on the Pi.
- [ ] Re-architect each module directory as a ROS 2 package.
- [ ] Define `.msg` types; replace in-process queues with topics and direct calls with services.
- [ ] Visualize with Foxglove Studio.
- [ ] Gazebo simulation: the same perception/planning/control code runs against either the real car or the simulator.
- [ ] Simulation-based regression tests in CI.

**Artifact:** `v2.0-ros2`.

---

## Design principles

- **The car is a delivery vehicle for the software.** The repo, tests, docs, and architecture are the deliverable.
- **Build for v2.** Every v1 decision should make the ROS 2 migration easier.
- **Replay over live testing.** A robust offline replay tool means iterating on autonomy code in seconds, not minutes.
- **One capability at a time.** Lane following, then obstacles, then localization.
- **The demo video is half the project.** Each phase ends by capturing footage.