from dataclasses import dataclass


@dataclass(frozen=True)
class Detection:
    """A detected lane feature or obstacle. Refine when Phase 3 perception lands."""

    timestamp: float
    label: str         # e.g. "lane_left", "lane_right", "obstacle"
    # Bounding box in normalized image coords: (x_min, y_min, x_max, y_max), each in [0, 1].
    bbox: tuple[float, float, float, float]
    confidence: float  # [0.0, 1.0]