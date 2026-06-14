"""The interface contracts are abstract - they must reject direct instantiation.

This is the Phase 0 guarantee: every concrete driver/planner is forced to
implement the full contract, because an incomplete one can't be constructed.
"""

import pytest

from autonomy_stack.control.controller import Controller
from autonomy_stack.hardware.camera import Camera
from autonomy_stack.hardware.imu import IMU
from autonomy_stack.hardware.motor import MotorDriver
from autonomy_stack.hardware.steering import SteeringServo
from autonomy_stack.planning.planner import Planner


@pytest.mark.parametrize(
    "interface",
    [MotorDriver, SteeringServo, Camera, IMU, Planner, Controller],
)
def test_interfaces_cannot_be_instantiated(interface: type) -> None:
    with pytest.raises(TypeError):
        interface()