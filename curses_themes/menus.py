"""Lightweight menus and keyboard accelerators for curses applications."""

from __future__ import annotations

import curses
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Callable

from .input import is_confirm, is_primary_click


Action = Callable[[], object]


class AcceleratorError(ValueError):
    """Raised when a menu contains duplicate accelerators."""


def normalize_accelerator(value: str) -> str:
    """Normalize an accelerator name for deterministic matching."""
    value = str(value).strip().lower()
    if not value:
        raise ValueError("accelerator must not be empty")
    aliases = {"return": "enter", "esc": "escape", "spacebar": "space"}
    parts = [aliases.get(part, part) for part in value.split("+")]
    modifiers = set(parts[:-1])
    key = parts[-1]
    valid_modifiers = {"ctrl", "alt", "shift"}
    unknown = modifiers - valid_modifiers
    if unknown:
        raise ValueError(f"unsupported accelerator modifier(s): {sorted(unknown)}")
    return "+".join([*sorted(modifiers), key])


def key_to_accelerator(
    key: int, *, alt: bool = False, ctrl: bool = False, shift: bool = False
) -> str:
    """Convert a curses key value to an accelerator string."""
    if key in (10, 13, getattr(curses, "KEY_ENTER", -1)):
        name = "enter"
    elif key == 27:
        name = "escape"
    elif key == 32:
        name = "space"
    elif 0 <= key < 256:
        name = chr(key).lower()
    else:
        function_keys = {
            getattr(curses, "KEY_F1", -1): "f1",
            getattr(curses, "KEY_F2", -1): "f2",
            getattr(curses, "KEY_F3", -1): "f3",
            getattr(curses, "KEY_F4", -1): "f4",
            getattr(curses, "KEY_F5", -1): "f5",
            getattr(curses, "KEY_F6", -1): "f6",
            getattr(curses, "KEY_F7", -1): "f7",
            getattr(curses, "KEY_F8", -1): "f8",
            getattr(curses, "KEY_F9", -1): "f9",
            getattr(curses, "KEY_F10", -1): "f10",
            getattr(curses, "KEY_F11", -1): "f11",
            getattr(curses, "KEY_F12", -1): "f12",
        }
        name = function_keys.get(key, str(key))
    modifiers = []
    if alt:
        modifiers.append("alt")
    if ctrl:
        modifiers.append("ctrl")
    if shift:
        modifiers.append("shift")
    return normalize_accelerator("+".join([*modifiers, name]))


@dataclass(frozen=True)
class MenuItem:
    """A menu item with an optional accelerator and application action."""

    label: str
    action: Action | None = None
    accelerator: str | None = None
    enabled: bool = True

    def __post_init__(self) -> None:
        if self.accelerator is not None:
            object.__setattr__(
                self, "accelerator", normalize_accelerator(self.accelerator)
            )

    def activate(self) -> object | None:
        if not self.enabled or self.action is None:
            return None
        return self.action()


class Menu:
    """A small keyboard/mouse-friendly menu."""

    def __init__(self, items: Sequence[MenuItem], selected: int = 0) -> None:
        self.items = list(items)
        self.selected = max(0, min(int(selected), max(0, len(self.items) - 1)))
        self.validate_accelerators()

    def validate_accelerators(self) -> None:
        seen: dict[str, str] = {}
        for item in self.items:
            if item.accelerator is None:
                continue
            previous = seen.get(item.accelerator)
            if previous is not None:
                raise AcceleratorError(
                    f"accelerator {item.accelerator!r} is assigned to both "
                    f"{previous!r} and {item.label!r}"
                )
            seen[item.accelerator] = item.label

    def activate(self, index: int | None = None) -> object | None:
        if not self.items:
            return None
        index = self.selected if index is None else int(index)
        if not 0 <= index < len(self.items):
            return None
        self.selected = index
        return self.items[index].activate()

    def handle_key(
        self,
        key: int,
        *,
        alt: bool = False,
        ctrl: bool = False,
        shift: bool = False,
    ) -> object | None:
        """Navigate, activate, or dispatch a menu accelerator."""
        if not self.items:
            return None
        if key == 27 and not (alt or ctrl or shift):
            return None
        if key in (getattr(curses, "KEY_DOWN", -1), ord("j")) and not (
            alt or ctrl
        ):
            self.selected = (self.selected + 1) % len(self.items)
            return None
        if key in (getattr(curses, "KEY_UP", -1), ord("k")) and not (
            alt or ctrl
        ):
            self.selected = (self.selected - 1) % len(self.items)
            return None
        if is_confirm(key) and not (alt or ctrl or shift):
            return self.activate()
        accelerator = key_to_accelerator(key, alt=alt, ctrl=ctrl, shift=shift)
        for index, item in enumerate(self.items):
            if item.enabled and item.accelerator == accelerator:
                return self.activate(index)
        return None

    def handle_mouse(
        self, event: tuple[int, int, int] | None, *, y: int, x: int = 0
    ) -> object | None:
        """Activate a menu item when its rendered row is primary-clicked."""
        if event is None:
            return None
        mouse_x, mouse_y, button_state = event
        if mouse_y != y or mouse_x < x or not is_primary_click(button_state):
            return None
        cursor = x
        for index, item in enumerate(self.items):
            width = len(item.label) + (
                len(item.accelerator or "") + 3 if item.accelerator else 1
            )
            if cursor <= mouse_x < cursor + width:
                return self.activate(index)
            cursor += width
        return None

    def rendered_labels(self) -> list[str]:
        """Return labels with accelerators formatted for display."""
        return [
            f"{item.label}  [{item.accelerator}]" if item.accelerator else item.label
            for item in self.items
        ]


__all__ = ["AcceleratorError", "Menu", "MenuItem", "key_to_accelerator", "normalize_accelerator"]
