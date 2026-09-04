#!/usr/bin/env python3
"""Shared pytest fixtures for curses-tui tests."""

from unittest.mock import MagicMock, Mock

import pytest

from curses_tui import Theme


class MockCurses:
    """Mock curses module for testing."""

    COLOR_BLACK = 0
    COLOR_RED = 1
    COLOR_GREEN = 2
    COLOR_YELLOW = 3
    COLOR_BLUE = 4
    COLOR_MAGENTA = 5
    COLOR_CYAN = 6
    COLOR_WHITE = 7
    COLORS = 256
    COLOR_PAIRS = 256
    A_BOLD = 1 << 13
    A_DIM = 1 << 14

    def __init__(self):
        self.color_pairs = {}
        self.color_support = True

    def has_colors(self):
        return self.color_support

    def start_color(self):
        pass

    def use_default_colors(self):
        pass

    def init_pair(self, pair_num, fg, bg):
        self.color_pairs[pair_num] = (fg, bg)

    def color_pair(self, n):
        return n << 8

    class error(Exception):
        """Mock curses.error exception."""

        pass


@pytest.fixture
def mock_curses(monkeypatch):
    """Mock the curses module for testing."""
    mock = MockCurses()
    monkeypatch.setattr("curses_tui.colors.curses", mock)
    monkeypatch.setattr("curses_tui.theme.curses", mock)
    monkeypatch.setattr("curses_tui.theme3d.curses", mock)
    return mock


@pytest.fixture
def mock_stdscr():
    """Mock curses stdscr window object."""
    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (24, 80)
    stdscr.addstr = Mock()
    stdscr.addch = Mock()
    stdscr.bkgd = Mock()
    stdscr.refresh = Mock()
    stdscr.getch = Mock(return_value=ord("q"))
    stdscr.clear = Mock()
    return stdscr


class SimpleTheme(Theme):
    """Minimal concrete Theme for testing base class."""

    color_map = {
        "background": (0, 0, 0),
        "foreground": (255, 255, 255),
        "primary": (0, 120, 215),
        "success": (16, 124, 16),
        "error": (232, 17, 35),
        "warning": (193, 156, 0),
        "info": (0, 120, 212),
        "accent": (142, 68, 173),
    }

    def __init__(self):
        super().__init__(
            name="Simple Test Theme",
            description="A minimal theme for testing",
            author="Test Suite",
        )


@pytest.fixture
def simple_theme():
    """Fixture providing a minimal concrete Theme instance."""
    return SimpleTheme()


@pytest.fixture
def simple_3d_theme():
    """Create a minimal 3D theme for testing."""
    from curses_tui import Theme3D

    class Simple3DTheme(Theme3D):
        color_map = {
            "background": (200, 200, 200),
            "foreground": (0, 0, 0),
            "primary": (0, 120, 215),
            "success": (16, 124, 16),
            "error": (232, 17, 35),
            "warning": (193, 156, 0),
            "info": (0, 120, 212),
            "accent": (142, 68, 173),
        }
        effects_3d = {
            "shadow": ((0, 0, 0), (0, 0, 0)),
            "highlight": ((255, 255, 255), (200, 200, 200)),
            "lowlight": ((128, 128, 128), (200, 200, 200)),
        }

        def __init__(self):
            super().__init__(
                name="Simple 3D Test Theme",
                description="A minimal 3D theme for testing",
                author="Test Suite",
            )

    return Simple3DTheme()


@pytest.fixture(autouse=True)
def reset_color_manager():
    """Reset ColorManager state between tests."""
    from curses_tui.colors import ColorManager

    yield
    ColorManager._next_pair = 1
    ColorManager._pair_cache.clear()


@pytest.fixture(autouse=True)
def reset_theme_manager():
    """Reset ThemeManager state between tests."""
    from curses_tui.manager import ThemeManager

    yield
    ThemeManager.reset()
