from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ImuReading:
    """A single IMU sample. SI units; timestamp is a monotonic clock in seconds."""

    timestamp: float
    # Angular velocity (rad/s) in body frame: roll-rate, pitch-rate, yaw-rate.
    gyro: tuple[float, float, float]
    # Linear acceleration (m/s²) in body frame: x, y, z.
    accel: tuple[float, float, float]


class IMU(ABC):
    @abstractmethod
    def read(self) -> ImuReading:
        """Read one sample. Blocks if no sample is available yet."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Release the IMU resource."""
        ...