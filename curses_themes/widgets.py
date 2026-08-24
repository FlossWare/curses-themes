"""Small, dependency-free curses widgets for FlossWare applications."""
from __future__ import annotations
import curses
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class Option:
    value: str
    label: str
    description: str = ""

class Dropdown:
    """Keyboard/mouse-friendly single-selection dropdown."""
    def __init__(self, options: Sequence[Option | str], selected: int = 0) -> None:
        self.options = [o if isinstance(o, Option) else Option(str(o), str(o)) for o in options]
        self.selected = max(0, min(selected, len(self.options) - 1)) if self.options else 0

    def choose(self, win: curses.window, y: int, x: int, width: int, title: str = "Select") -> str | None:
        if not self.options:
            return None
        current = self.selected
        while True:
            win.addnstr(y, x, f"{title}: [{self.options[current].label} ▼]", max(1, width - 1), curses.A_BOLD)
            key = win.getch()
            if key in (curses.KEY_UP, ord("k")):
                current = (current - 1) % len(self.options)
            elif key in (curses.KEY_DOWN, ord("j")):
                current = (current + 1) % len(self.options)
            elif key in (10, 13, curses.KEY_ENTER, ord(" ")):
                self.selected = current
                return self.options[current].value
            elif key in (27, ord("q")):
                return None

class Tabs:
    """Simple horizontal tab bar with keyboard and mouse support."""
    def __init__(self, labels: Sequence[str], selected: int = 0) -> None:
        self.labels = list(labels)
        self.selected = selected if self.labels else 0

    def draw(self, win: curses.window, y: int, x: int = 0) -> None:
        for i, label in enumerate(self.labels):
            attr = curses.A_REVERSE | curses.A_BOLD if i == self.selected else curses.A_NORMAL
            win.addnstr(y, x, f" {i + 1}:{label} ", max(1, win.getmaxyx()[1] - x - 1), attr)
            x += len(label) + 5

    def handle(self, key: int) -> bool:
        if not self.labels:
            return False
        if key in (curses.KEY_LEFT, ord("h")):
            self.selected = (self.selected - 1) % len(self.labels)
            return True
        if key in (curses.KEY_RIGHT, ord("l")):
            self.selected = (self.selected + 1) % len(self.labels)
            return True
        if ord("1") <= key <= ord("9"):
            index = key - ord("1")
            if index < len(self.labels):
                self.selected = index
                return True
        return False

class Table:
    """Minimal clipped table suitable for live dashboards."""
    def __init__(self, headers: Sequence[str], rows: Sequence[Sequence[object]]) -> None:
        self.headers = list(headers)
        self.rows = [list(map(str, row)) for row in rows]

    def draw(self, win: curses.window, y: int, x: int = 0, height: int | None = None) -> None:
        width = win.getmaxyx()[1]
        limit = height or max(1, win.getmaxyx()[0] - y)
        widths = [len(h) for h in self.headers]
        for row in self.rows:
            for i, value in enumerate(row[:len(widths)]):
                widths[i] = min(max(widths[i], len(value)), 36)
        def line(values):
            return "  ".join(v[:widths[i]].ljust(widths[i]) for i, v in enumerate(values))
        win.addnstr(y, x, line(self.headers), max(1, width - x - 1), curses.A_BOLD | curses.A_UNDERLINE)
        for offset, row in enumerate(self.rows[: max(0, limit - 1)], 1):
            win.addnstr(y + offset, x, line(row), max(1, width - x - 1))

__all__ = ["Dropdown", "Option", "Tabs", "Table"]
