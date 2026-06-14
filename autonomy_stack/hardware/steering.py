from abc import ABC, abstractmethod


class SteeringServo(ABC):
    @abstractmethod
    def set_angle(self, value: float) -> None:
        """Set steering in [-1.0, 1.0]. -1 full left, +1 full right, 0 centered."""
        ...

    @abstractmethod
    def center(self) -> None:
        """Return steering to center. Either successful or raise an exception."""
        ...