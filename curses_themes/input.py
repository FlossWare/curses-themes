"""Reusable keyboard and mouse input helpers for curses applications."""

from __future__ import annotations

import curses


def enable_mouse() -> bool:
    """Enable terminal mouse reporting when supported.

    Returns False when the terminal or curses build cannot report mouse
    events, allowing callers to continue in keyboard-only mode.
    """
    try:
        mask = getattr(curses, "ALL_MOUSE_EVENTS", 0)
        if hasattr(curses, "REPORT_MOUSE_POSITION"):
            mask |= curses.REPORT_MOUSE_POSITION
        if not mask:
            mask = (
                getattr(curses, "BUTTON1_PRESSED", 0)
                | getattr(curses, "BUTTON1_CLICKED", 0)
                | getattr(curses, "BUTTON1_RELEASED", 0)
            )
        if not mask:
            return False
        result = curses.mousemask(mask)
        available = result[0] if isinstance(result, tuple) else result
        if not available:
            return False
        if hasattr(curses, "mouseinterval"):
            try:
                curses.mouseinterval(200)
            except curses.error:
                pass
        return True
    except (AttributeError, curses.error, TypeError, ValueError):
        return False


def mouse_event() -> tuple[int, int, int] | None:
    """Return ``(x, y, button_state)`` for the current mouse event."""
    try:
        _id, x, y, _z, bstate = curses.getmouse()
    except (curses.error, AttributeError, TypeError, ValueError):
        return None
    return int(x), int(y), int(bstate)


def primary_button_mask() -> int:
    """Return the mask for primary-button press/click events."""
    return int(
        getattr(curses, "BUTTON1_CLICKED", 0)
        | getattr(curses, "BUTTON1_PRESSED", 0)
    )


def is_primary_click(bstate: int) -> bool:
    """Return True when *bstate* contains a primary press or click."""
    mask = primary_button_mask()
    return bool(mask and (int(bstate) & mask))


def primary_click() -> tuple[int, int] | None:
    """Return coordinates for a primary-button click/press."""
    event = mouse_event()
    if event is None:
        return None
    x, y, bstate = event
    return (x, y) if is_primary_click(bstate) else None


def mouse_position() -> tuple[int, int] | None:
    """Return coordinates for the current mouse event."""
    event = mouse_event()
    return None if event is None else event[:2]


def list_index_at(
    y: int,
    origin_y: int,
    count: int,
    *,
    scroll_offset: int = 0,
    visible: int | None = None,
) -> int | None:
    """Map a screen row to an absolute list index.

    ``origin_y`` is the screen row of the first visible item and
    ``scroll_offset`` is the absolute index of that item.
    """
    if count <= 0:
        return None
    row = int(y) - int(origin_y)
    limit = int(count) if visible is None else max(0, int(visible))
    if not 0 <= row < limit:
        return None
    index = row + int(scroll_offset)
    return index if 0 <= index < int(count) else None


def resolve_list_mouse(
    event: tuple[int, int, int] | None,
    *,
    origin_y: int,
    count: int,
    scroll_offset: int = 0,
    visible: int | None = None,
) -> tuple[str, int] | None:
    """Resolve a mouse event against a vertical list.

    Returns ``("activate", index)`` for a primary click, ``("focus", index)``
    for other mouse events over a row, and ``None`` outside the list.
    """
    if event is None or count <= 0:
        return None
    _x, y, bstate = event
    index = list_index_at(
        y,
        origin_y,
        count,
        scroll_offset=scroll_offset,
        visible=visible,
    )
    if index is None:
        return None
    return ("activate", index) if is_primary_click(bstate) else ("focus", index)


def is_confirm(key: int) -> bool:
    return key in (10, 13, curses.KEY_ENTER)


def is_cancel(key: int) -> bool:
    return key in (ord("q"), 27)


def is_up(key: int) -> bool:
    return key in (curses.KEY_UP, ord("k"))


def is_down(key: int) -> bool:
    return key in (curses.KEY_DOWN, ord("j"))


def is_mouse(key: int) -> bool:
    """Return True when *key* is the curses mouse event token."""
    return key == getattr(curses, "KEY_MOUSE", -1)


__all__ = [
    "enable_mouse",
    "is_cancel",
    "is_confirm",
    "is_down",
    "is_mouse",
    "is_primary_click",
    "is_up",
    "list_index_at",
    "mouse_event",
    "mouse_position",
    "primary_button_mask",
    "primary_click",
    "resolve_list_mouse",
]
