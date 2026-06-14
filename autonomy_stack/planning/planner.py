from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass

from autonomy_stack.localization.pose import Pose
from autonomy_stack.perception.detection import Detection


@dataclass(frozen=True)
class Waypoint:
    """A single trajectory point in the world frame."""

    x: float           # meters
    y: float           # meters
    speed: float       # m/s, target speed at this waypoint


@dataclass(frozen=True)
class Trajectory:
    """A planned path: a time-ordered sequence of waypoints."""

    timestamp: float
    waypoints: Sequence[Waypoint]


class Planner(ABC):
    @abstractmethod
    def plan(self, pose: Pose, detections: Sequence[Detection]) -> Trajectory:
        """Compute the next trajectory given current pose and latest detections."""
        ...