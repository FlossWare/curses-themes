"""Lightweight movable/resizable curses windows and focus management."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

import curses

from .geometry import Rect, SizeConstraints
from .input import is_primary_click, mouse_event


class HitRegion(str, Enum):
    NONE = "none"
    BODY = "body"
    TITLE = "title"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"


@dataclass
class Window:
    """A lightweight screen-space window managed by :class:`WindowManager`."""

    title: str
    rect: Rect
    constraints: SizeConstraints = field(default_factory=SizeConstraints)
    movable: bool = True
    resizable: bool = True
    title_height: int = 1
    draw_callback: Callable[[curses.window, "Window"], None] | None = None

    focused: bool = False
    visible: bool = True
    _drag_offset: tuple[int, int] | None = field(default=None, init=False, repr=False)
    _resize_region: HitRegion = field(default=HitRegion.NONE, init=False, repr=False)
    _resize_start: tuple[int, int, Rect] | None = field(default=None, init=False, repr=False)

    def normalized(self, screen_width: int, screen_height: int) -> "Window":
        width, height = self.constraints.constrain(self.rect.width, self.rect.height)
        self.rect = Rect(self.rect.x, self.rect.y, width, height).clamp(screen_width, screen_height)
        return self

    def hit_test(self, x: int, y: int) -> HitRegion:
        if not self.visible or not self.rect.contains(x, y):
            return HitRegion.NONE
        left = x == self.rect.x
        right = x == self.rect.right - 1
        top = y == self.rect.y
        bottom = y == self.rect.bottom - 1
        if top and left:
            return HitRegion.TOP_LEFT
        if top and right:
            return HitRegion.TOP_RIGHT
        if bottom and left:
            return HitRegion.BOTTOM_LEFT
        if bottom and right:
            return HitRegion.BOTTOM_RIGHT
        # The title bar owns the top interior row. Corner cells remain resize handles.
        if top:
            return HitRegion.TITLE if self.title_height > 0 else HitRegion.TOP
        if bottom:
            return HitRegion.BOTTOM
        if left:
            return HitRegion.LEFT
        if right:
            return HitRegion.RIGHT
        if self.rect.y <= y < self.rect.y + self.title_height:
            return HitRegion.TITLE
        return HitRegion.BODY

    def begin_interaction(self, x: int, y: int) -> bool:
        region = self.hit_test(x, y)
        if region == HitRegion.TITLE and self.movable:
            self._drag_offset = (x - self.rect.x, y - self.rect.y)
            return True
        if region in {
            HitRegion.LEFT, HitRegion.RIGHT, HitRegion.TOP, HitRegion.BOTTOM,
            HitRegion.TOP_LEFT, HitRegion.TOP_RIGHT, HitRegion.BOTTOM_LEFT,
            HitRegion.BOTTOM_RIGHT,
        } and self.resizable:
            self._resize_region = region
            self._resize_start = (x, y, self.rect)
            return True
        return False

    def update_interaction(self, x: int, y: int, screen_width: int, screen_height: int) -> bool:
        if self._drag_offset is not None:
            ox, oy = self._drag_offset
            self.rect = self.rect.move(x - ox, y - oy).clamp(screen_width, screen_height)
            return True
        if self._resize_start is None:
            return False
        start_x, start_y, start_rect = self._resize_start
        dx, dy = x - start_x, y - start_y
        left, top = start_rect.x, start_rect.y
        right, bottom = start_rect.right, start_rect.bottom
        region = self._resize_region
        if region in {HitRegion.LEFT, HitRegion.TOP_LEFT, HitRegion.BOTTOM_LEFT}:
            left += dx
        if region in {HitRegion.RIGHT, HitRegion.TOP_RIGHT, HitRegion.BOTTOM_RIGHT}:
            right += dx
        if region in {HitRegion.TOP, HitRegion.TOP_LEFT, HitRegion.TOP_RIGHT}:
            top += dy
        if region in {HitRegion.BOTTOM, HitRegion.BOTTOM_LEFT, HitRegion.BOTTOM_RIGHT}:
            bottom += dy

        width, height = self.constraints.constrain(right - left, bottom - top)
        if region in {HitRegion.LEFT, HitRegion.TOP_LEFT, HitRegion.BOTTOM_LEFT}:
            left = right - width
        if region in {HitRegion.TOP, HitRegion.TOP_LEFT, HitRegion.TOP_RIGHT}:
            top = bottom - height
        self.rect = Rect(left, top, width, height).clamp(screen_width, screen_height)
        return True

    def end_interaction(self) -> None:
        self._drag_offset = None
        self._resize_region = HitRegion.NONE
        self._resize_start = None

    def interacting(self) -> bool:
        return self._drag_offset is not None or self._resize_start is not None

    def draw(self, screen: curses.window) -> None:
        if not self.visible:
            return
        try:
            win = curses.newwin(self.rect.height, self.rect.width, self.rect.y, self.rect.x)
            win.erase()
            win.box()
            if self.title and self.rect.width > 4:
                win.addnstr(0, 2, f" {self.title} ", max(1, self.rect.width - 4))
            if self.draw_callback is not None:
                self.draw_callback(win, self)
            win.noutrefresh()
        except curses.error:
            return


class WindowManager:
    """Manage windows, focus, z-order, and pointer interaction."""

    def __init__(self, screen_width: int, screen_height: int) -> None:
        if screen_width < 1 or screen_height < 1:
            raise ValueError("screen dimensions must be positive")
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._windows: list[Window] = []
        self._active: Window | None = None

    @property
    def windows(self) -> tuple[Window, ...]:
        return tuple(self._windows)

    @property
    def active(self) -> Window | None:
        return self._active

    def add(self, window: Window) -> Window:
        window.normalized(self.screen_width, self.screen_height)
        self._windows.append(window)
        self.focus(window)
        return window

    def remove(self, window: Window) -> None:
        if window not in self._windows:
            return
        self._windows.remove(window)
        window.focused = False
        window.end_interaction()
        if self._active is window:
            self._active = None
            if self._windows:
                self.focus(self._windows[-1])

    def focus(self, window: Window) -> None:
        if window not in self._windows or not window.visible:
            return
        for item in self._windows:
            item.focused = False
        window.focused = True
        self._active = window
        self._windows.remove(window)
        self._windows.append(window)

    def hit_test(self, x: int, y: int) -> Window | None:
        for window in reversed(self._windows):
            if window.visible and window.rect.contains(x, y):
                return window
        return None

    def handle_mouse(self, event: tuple[int, int, int] | None) -> bool:
        if event is None:
            return False
        x, y, button_state = event
        window = self._active if self._active and self._active.interacting() else self.hit_test(x, y)
        if window is None:
            return False
        self.focus(window)
        if window.interacting():
            released = bool(button_state & getattr(curses, "BUTTON1_RELEASED", 0))
            if released:
                window.end_interaction()
                return True
            return window.update_interaction(x, y, self.screen_width, self.screen_height)
        if is_primary_click(button_state):
            window.begin_interaction(x, y)
            return True
        return True

    def handle_key(self, key: int) -> bool:
        """Move the focused window with arrow keys.

        Applications may reserve modified keys for resizing or other commands.
        """
        window = self._active
        if window is None or not window.movable:
            return False
        keymap = {
            curses.KEY_LEFT: (-1, 0),
            curses.KEY_RIGHT: (1, 0),
            curses.KEY_UP: (0, -1),
            curses.KEY_DOWN: (0, 1),
        }
        if key not in keymap:
            return False
        dx, dy = keymap[key]
        window.rect = window.rect.move(window.rect.x + dx, window.rect.y + dy).clamp(
            self.screen_width, self.screen_height
        )
        return True

    def resize_screen(self, width: int, height: int) -> None:
        if width < 1 or height < 1:
            raise ValueError("screen dimensions must be positive")
        self.screen_width = width
        self.screen_height = height
        for window in self._windows:
            window.normalized(width, height)

    def draw(self, screen: curses.window) -> None:
        for window in self._windows:
            window.draw(screen)

    def dispatch_curses_mouse(self) -> bool:
        """Read and dispatch the current ``KEY_MOUSE`` event."""
        return self.handle_mouse(mouse_event())


__all__ = ["HitRegion", "Window", "WindowManager"]
