from abc import ABC, abstractmethod

import numpy as np
import numpy.typing as npt


class Camera(ABC):
    @abstractmethod
    def read(self) -> npt.NDArray[np.uint8]:
        """Read one frame: an (H, W, 3) unit8 BGR image."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Release the camera resource."""
        ...
