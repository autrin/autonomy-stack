from abc import ABC, abstractmethod


class MotorDriver(ABC):
    @abstractmethod
    def set_throttle(self, value: float) -> None:
        """Set drive throttle in [-1.0, 1.0]. -1 full reverse, +1 full forward."""
        ...

    @abstractmethod
    def stop(self) -> None:
        """Stop the motor. Either successful or raise an exception."""
        ...
