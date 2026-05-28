# Autonomy Stack

A small autonomous car, built from a base RC chassis up. The hardware is intentionally cheap — the focus is the software: a clean, tested, documented autonomy stack spanning **perception → localization → planning → control**.

This is a learning-in-public project. It's built the way I'd build production software: strict module boundaries, integration tests against recorded sensor data, type-checked CI, and documentation that lets someone else reproduce it.

> **Status:** 🚧 Phase 0 — project scaffolding. Not yet driving.

---

## Goals

- Build the full autonomy pipeline (perception, localization, planning, control) on real hardware.
- Treat it as a software engineering project first and a robotics project second — tests, CI, docs, and architecture matter as much as the autonomy.
- Design v1 (plain Python) so that v2 (ROS 2) is a clean migration, not a rewrite.

## Non-goals

- Winning a race. This is about engineering quality, not lap time.
- Reinventing SLAM. Where a well-understood approach exists, I use it and cite it.

---

## Architecture

```
                 ┌─────────────┐
   camera ──────▶│ perception  │──── detections ──┐
   imu    ──────▶│             │                  │
                 └─────────────┘                  ▼
                 ┌─────────────┐           ┌─────────────┐
   imu    ──────▶│localization │── pose ──▶│  planning   │
   odom   ──────▶│             │           │             │
                 └─────────────┘           └─────────────┘
                                                  │
                                            trajectory
                                                  ▼
                                           ┌─────────────┐
                                           │   control   │── cmd ──┐
                                           └─────────────┘         │
                                           ┌─────────────┐         │
                                           │ safety node │◀────────┘
                                           └─────────────┘
                                                  │ clamped cmd
                                                  ▼
                                           motor + steering
```

Every stage publishes typed messages and runs behind an interface, so any stage can be swapped for a fake during testing. The **safety node** sits between planning/control and the hardware: it bounds every command, watchdogs the perception pipeline, and brings the car to a safe stop if anything upstream stalls.

See [`docs/architecture.md`](docs/architecture.md) for detail.

---

## Repository layout

```
autonomy-stack/              ← repo root (the git repo, hyphenated)
├── autonomy_stack/          ← the Python package (underscored, importable)
│   ├── __init__.py
│   ├── hardware/
│   ├── perception/
│   ├── localization/
│   ├── planning/
│   ├── control/
│   ├── telemetry/
│   ├── nodes/
│   └── sim/
├── tests/                   ← sibling of the package, NOT inside it
├── docs/                    ← sibling
├── scripts/                 ← sibling
├── logs/                    ← sample recorded sessions for replay/tests
├── pyproject.toml
├── README.md
├── ROADMAP.md
├── LICENSE
└── Makefile
```

This layout maps one-to-one onto ROS 2 packages for the planned v2.

---

## Tech stack

- **Language:** Python 3.11+ (v1), with a planned ROS 2 (Humble) migration for v2
- **Vision:** OpenCV, NumPy
- **Hardware:** Raspberry Pi 5, PCA9685 PWM driver, Pi Camera Module 3, BNO055 IMU, base RC chassis
- **Tooling:** ruff (lint), mypy --strict (types), pytest (tests), GitHub Actions (CI)
- **Telemetry:** structured logs (Parquet) with an offline replay tool

---

## Getting started

> Hardware bring-up instructions live in [`docs/setup.md`](docs/setup.md). The steps below get the codebase running on any machine — most modules can be exercised in tests and replay without a car attached.

```bash
git clone https://github.com/autrin/autonomy-stack.git
cd autonomy-stack

# install (editable, with dev dependencies)
pip install -e ".[dev]"

# run the checks
make lint        # ruff + mypy
make test        # pytest

# replay a recorded session through the pipeline (no hardware needed)
python -m nodes.replay --log logs/sample_session.parquet
```

On the car itself:

```bash
# drive it manually from a laptop over the network
python -m nodes.teleop

# run autonomous mode
python -m nodes.autonomy
```

---

## Safety

This is a small, low-speed indoor vehicle, but it's still a moving robot. The stack is built so that:

- Every command to the motors passes through a bounds check.
- Loss of perception for more than a short window coasts the car to a stop.
- `Ctrl-C` always brings the car to a clean, stopped state — it never leaves the motor running.

See [`docs/safety.md`](docs/safety.md) for the failure-mode analysis.

---

## Roadmap

Development happens in phases, each ending with a demoable artifact. Full detail in [`ROADMAP.md`](ROADMAP.md).

- [x] **Phase 0** — Project scaffolding, interfaces, CI
- [ ] **Phase 1** — Hardware bring-up, teleop
- [ ] **Phase 2** — Sensing + logging + replay
- [ ] **Phase 3** — Lane following (classical CV + pure pursuit)
- [ ] **Phase 4** — Obstacle detection + avoidance
- [ ] **Phase 5** — Localization (dead reckoning + AprilTags)
- [ ] **Phase 6** — Polish, tests, docs
- [ ] **Phase 7** — Writeup + demo video
- [ ] **Phase 8** *(stretch)* — ROS 2 rewrite + Gazebo simulation

---

## License

MIT. See [LICENSE](LICENSE).

## Author

Autrin Hakimi — [github.com/autrin](https://github.com/autrin) · [portfolio](https://autrin.github.io/)
