"""Runtime adapter from the language-neutral TUI Schema 1.0 contract."""

from __future__ import annotations

import curses
from collections.abc import Callable

from .geometry import Rect, SizeConstraints
from .menus import Menu, MenuItem
from .schema import validate
from .windows import Window, WindowManager

ActionHandler = Callable[[str], object]


def build_menus(document: dict) -> dict[str, Menu]:
    """Build reusable menus while preserving action identifiers."""
    validate(document)
    menus: dict[str, Menu] = {}
    for definition in document.get("menus", []):
        items = [
            MenuItem(
                item["label"],
                action=(lambda action=item["action"]: action),
                accelerator=item.get("accelerator"),
                enabled=item.get("enabled", True),
            )
            for item in definition["items"]
            if item.get("type") != "separator" and item.get("visible", True)
        ]
        menus[definition["id"]] = Menu(items)
    return menus


def build_window_manager(
    document: dict,
    screen_width: int,
    screen_height: int,
    *,
    on_action: ActionHandler | None = None,
) -> WindowManager:
    """Create windows from a validated 1.0 document.

    The adapter renders the declarative controls and returns action identifiers
    through ``on_action``. It never executes schema-provided code.
    """
    validate(document)
    manager = WindowManager(screen_width, screen_height)
    for definition in document["windows"]:
        layout = definition.get("layout", {})
        width = layout.get("width", max(20, screen_width // 2))
        height = layout.get("height", max(6, screen_height // 2))
        x = layout.get("x", 0)
        y = layout.get("y", 0)
        constraints = SizeConstraints(
            min_width=layout.get("minWidth", 10),
            min_height=layout.get("minHeight", 3),
            max_width=layout.get("maxWidth"),
            max_height=layout.get("maxHeight"),
        )
        window = Window(
            definition.get("title", ""),
            Rect(x, y, width, height),
            constraints=constraints,
            movable=definition.get("movable", True),
            resizable=definition.get("resizable", True),
            draw_callback=_make_draw_callback(definition, on_action),
        )
        manager.add(window)
    return manager


def _make_draw_callback(
    definition: dict, on_action: ActionHandler | None
) -> Callable[[curses.window, Window], None]:
    content = definition.get("content", [])

    def draw(win: curses.window, _window: Window) -> None:
        cursor_y = 1
        for widget in content:
            cursor_y = _draw_widget(win, widget, cursor_y, 1, on_action)

    return draw


def _draw_widget(
    win: curses.window,
    widget: dict,
    y: int,
    x: int,
    on_action: ActionHandler | None,
) -> int:
    if not widget.get("visible", True):
        return y
    kind = widget["type"]
    label = widget.get("label", "")
    enabled = widget.get("enabled", True)
    attr = curses.A_NORMAL if enabled else curses.A_DIM
    width = max(1, win.getmaxyx()[1] - x - 1)
    try:
        if kind == "label":
            win.addnstr(y, x, label, width, attr)
            return y + 1
        if kind == "text-input":
            text = f"{label}: {widget.get('value', '')}" if label else widget.get("value", "")
            win.addnstr(y, x, text, width, attr)
            return y + 1
        if kind == "checkbox":
            mark = "[x]" if widget.get("value", False) else "[ ]"
            win.addnstr(y, x, f"{mark} {label}".rstrip(), width, attr)
            return y + 1
        if kind == "list":
            if label:
                win.addnstr(y, x, label, width, curses.A_BOLD)
                y += 1
            selected = widget.get("selected")
            for item in widget.get("items", []):
                prefix = "> " if item.get("id") == selected else "  "
                item_attr = attr if item.get("enabled", True) else curses.A_DIM
                win.addnstr(y, x, prefix + item["label"], width, item_attr)
                y += 1
            return y
        if kind == "button":
            win.addnstr(y, x, f"[ {label} ]", width, attr | curses.A_BOLD)
            return y + 1
        if kind == "separator":
            win.addnstr(y, x, "-" * max(1, width), width, attr)
            return y + 1
        if kind == "group":
            if label:
                win.addnstr(y, x, label, width, curses.A_BOLD)
                y += 1
            for child in widget.get("children", []):
                y = _draw_widget(win, child, y, x + 2, on_action)
            return y
    except curses.error:
        return y + 1
    return y


def dispatch_action(action: str, handler: ActionHandler | None) -> object | None:
    """Dispatch an action identifier through the application-owned handler."""
    if handler is None:
        return action
    return handler(action)


__all__ = ["ActionHandler", "build_menus", "build_window_manager", "dispatch_action"]
