"""The interface contracts are abstract - they must reject direct instantiation.

This is the Phase 0 guarantee: every concrete driver/planner is forced to
implement the full contract, because an incomplete one can't be constructed.
"""

import pytest

from autonomy_stack.hardware.camera import Camera
from autonomy_stack.hardware.motor import MotorDriver


@pytest.mark.parametrize("interface", [MotorDriver, Camera])
def test_interfaces_cannot_be_instantiated(interface: type) -> None:
    with pytest.raises(TypeError):
        interface()
