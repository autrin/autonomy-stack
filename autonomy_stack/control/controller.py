from abc import ABC, abstractmethod
from dataclasses import dataclass

from autonomy_stack.localization.pose import Pose
from autonomy_stack.planning.planner import Trajectory


@dataclass(frozen=True)
class Command:
    """A combined throttle + steering command. Both fields in [-1.0, 1.0]."""

    timestamp: float
    throttle: float    # -1 full reverse, +1 full forward
    steering: float    # -1 full left,    +1 full right


class Controller(ABC):
    @abstractmethod
    def step(self, trajectory: Trajectory, pose: Pose) -> Command:
        """Compute the next actuator command tracking the given trajectory."""
        ...