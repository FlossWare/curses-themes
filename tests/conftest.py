#!/usr/bin/env python3
"""Shared pytest fixtures for curses-themes tests."""

import pytest
from unittest.mock import MagicMock, Mock
import curses_themes
from curses_themes import Theme


class MockCurses:
    """Mock curses module for testing."""

    # Color constants
    COLOR_BLACK = 0
    COLOR_RED = 1
    COLOR_GREEN = 2
    COLOR_YELLOW = 3
    COLOR_BLUE = 4
    COLOR_MAGENTA = 5
    COLOR_CYAN = 6
    COLOR_WHITE = 7

    # Terminal capabilities
    COLORS = 256
    COLOR_PAIRS = 256

    # Attributes
    A_BOLD = 1 << 13
    A_DIM = 1 << 14

    def __init__(self):
        self.color_pairs = {}  # Track init_pair calls
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

    # Patch curses module in curses_themes.colors
    monkeypatch.setattr("curses_themes.colors.curses", mock)
    monkeypatch.setattr("curses_themes.theme.curses", mock)

    return mock


@pytest.fixture
def mock_stdscr():
    """Mock curses stdscr window object."""
    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (24, 80)
    stdscr.addstr = Mock()
    stdscr.bkgd = Mock()
    stdscr.refresh = Mock()
    stdscr.getch = Mock(return_value=ord("q"))
    stdscr.clear = Mock()
    return stdscr


class SimpleTheme(Theme):
    """Minimal concrete Theme for testing base class."""

    def __init__(self):
        super().__init__(
            name="Simple Test Theme",
            description="A minimal theme for testing",
            author="Test Suite",
        )

    def get_color_map(self):
        return {
            "background": (0, 0, 0),
            "foreground": (255, 255, 255),
            "primary": (0, 120, 215),
            "success": (16, 124, 16),
            "error": (232, 17, 35),
            "warning": (193, 156, 0),
            "info": (0, 120, 212),
            "accent": (142, 68, 173),
        }


@pytest.fixture
def simple_theme():
    """Fixture providing a minimal concrete Theme instance."""
    return SimpleTheme()


@pytest.fixture(autouse=True)
def reset_color_manager():
    """Reset ColorManager state between tests."""
    from curses_themes.colors import ColorManager

    yield
    ColorManager._next_pair = 1
    ColorManager._pair_cache.clear()


@pytest.fixture(autouse=True)
def reset_theme_manager():
    """Reset ThemeManager state between tests."""
    from curses_themes.manager import ThemeManager

    yield
    ThemeManager.reset()
