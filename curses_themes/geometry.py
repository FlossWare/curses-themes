"""Small geometry primitives for reusable curses UI components."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Rect:
    """A screen-space rectangle using ``x, y, width, height``."""

    x: int
    y: int
    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width < 1 or self.height < 1:
            raise ValueError("rectangle dimensions must be positive")

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height

    def contains(self, x: int, y: int) -> bool:
        return self.x <= x < self.right and self.y <= y < self.bottom

    def move(self, x: int, y: int) -> "Rect":
        return Rect(x, y, self.width, self.height)

    def resize(self, width: int, height: int) -> "Rect":
        return Rect(width=width, height=height, x=self.x, y=self.y)

    def clamp(self, screen_width: int, screen_height: int) -> "Rect":
        if screen_width < 1 or screen_height < 1:
            raise ValueError("screen dimensions must be positive")
        width = min(self.width, screen_width)
        height = min(self.height, screen_height)
        x = min(max(0, self.x), screen_width - width)
        y = min(max(0, self.y), screen_height - height)
        return Rect(x, y, width, height)


@dataclass(frozen=True)
class SizeConstraints:
    """Minimum and optional maximum dimensions for a window."""

    min_width: int = 10
    min_height: int = 3
    max_width: int | None = None
    max_height: int | None = None

    def __post_init__(self) -> None:
        if self.min_width < 1 or self.min_height < 1:
            raise ValueError("minimum dimensions must be positive")
        if self.max_width is not None and self.max_width < self.min_width:
            raise ValueError("max_width must be >= min_width")
        if self.max_height is not None and self.max_height < self.min_height:
            raise ValueError("max_height must be >= min_height")

    def constrain(self, width: int, height: int) -> tuple[int, int]:
        width = max(self.min_width, int(width))
        height = max(self.min_height, int(height))
        if self.max_width is not None:
            width = min(width, self.max_width)
        if self.max_height is not None:
            height = min(height, self.max_height)
        return width, height


__all__ = ["Rect", "SizeConstraints"]
