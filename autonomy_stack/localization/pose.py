from dataclasses import dataclass


@dataclass(frozen=True)
class Pose:
    """2D pose of the car in the world frame."""

    timestamp: float
    x: float           # meters
    y: float           # meters
    heading: float     # radians; 0 = +x axis, CCW positive