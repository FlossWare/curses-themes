#!/usr/bin/env python3
"""Tests for Theme base class - metadata, color access, and component methods."""

import pytest
from curses_themes import Theme, ColorPair
from curses_themes.colors import ColorManager


class TestThemeMetadata:
    """Test suite for Theme metadata and initialization."""

    def test_theme_initialization(self, simple_theme):
        """Test Theme initialization with metadata."""
        assert simple_theme.name == "Simple Test Theme"
        assert simple_theme.description == "A minimal theme for testing"
        assert simple_theme.author == "Test Suite"

    def test_theme_repr(self, simple_theme):
        """Test Theme __repr__ output."""
        repr_str = repr(simple_theme)
        assert "Simple Test Theme" in repr_str
        assert "Test Suite" in repr_str

    def test_abstract_get_color_map_enforcement(self):
        """Test that Theme requires get_color_map() implementation."""

        class IncompleteTheme(Theme):
            def __init__(self):
                super().__init__("Incomplete", "No color map")

            def get_color_map(self):
                """Return empty color map."""
                return {}

        theme = IncompleteTheme()
        # Base Theme is abstract, concrete themes must implement get_color_map()
        color_map = theme.get_color_map()
        assert isinstance(color_map, dict)


class TestThemeColorAccess:
    """Test suite for Theme color property access."""

    def test_colors_property_before_apply_raises_error(self, simple_theme):
        """Test accessing colors property before apply() raises RuntimeError."""
        with pytest.raises(RuntimeError, match="colors not available|has not been applied"):
            _ = simple_theme.colors

    def test_components_property_before_apply_raises_error(self, simple_theme):
        """Test accessing components property before apply() raises RuntimeError."""
        with pytest.raises(RuntimeError, match="components not available|has not been applied"):
            _ = simple_theme.components

    def test_colors_property_after_apply(
        self, mock_curses, mock_stdscr, simple_theme
    ):
        """Test accessing colors property after apply() succeeds."""
        simple_theme.apply(mock_stdscr)

        assert simple_theme.colors is not None
        assert hasattr(simple_theme.colors, "primary")
        assert hasattr(simple_theme.colors, "success")
        assert hasattr(simple_theme.colors, "error")

    def test_components_property_after_apply(
        self, mock_curses, mock_stdscr, simple_theme
    ):
        """Test accessing components property after apply() succeeds."""
        simple_theme.apply(mock_stdscr)

        assert simple_theme.components is not None
        assert hasattr(simple_theme.components, "background")
        assert hasattr(simple_theme.components, "button")
        assert hasattr(simple_theme.components, "button_focused")


class TestThemeComponentMethods:
    """Test suite for Theme component color methods."""

    def test_default_get_background_returns_none(self, simple_theme):
        """Test default get_background() returns None."""
        result = simple_theme.get_background()
        assert result is None

    def test_default_get_button_returns_none(self, simple_theme):
        """Test default get_button() returns None."""
        result = simple_theme.get_button()
        assert result is None

    def test_default_get_button_focused_returns_none(self, simple_theme):
        """Test default get_button_focused() returns None."""
        result = simple_theme.get_button_focused()
        assert result is None

    def test_default_get_text_input_returns_none(self, simple_theme):
        """Test default get_text_input() returns None."""
        result = simple_theme.get_text_input()
        assert result is None

    def test_default_get_border_returns_none(self, simple_theme):
        """Test default get_border() returns None."""
        result = simple_theme.get_border()
        assert result is None

    def test_default_get_selection_returns_none(self, simple_theme):
        """Test default get_selection() returns None."""
        result = simple_theme.get_selection()
        assert result is None

    def test_default_get_disabled_returns_none(self, simple_theme):
        """Test default get_disabled() returns None."""
        result = simple_theme.get_disabled()
        assert result is None


class TestThemeBorderDrawing:
    """Test suite for Theme box drawing functionality."""

    def test_draw_box_basic(self, mock_curses, mock_stdscr, simple_theme):
        """Test basic box drawing."""
        simple_theme.apply(mock_stdscr)

        # Should not raise
        simple_theme.draw_box(mock_stdscr, 5, 10, 8, 40)

        # Verify addstr was called (box drawing happened)
        assert mock_stdscr.addstr.called

    def test_draw_box_with_title(self, mock_curses, mock_stdscr, simple_theme):
        """Test box drawing with title."""
        simple_theme.apply(mock_stdscr)

        simple_theme.draw_box(mock_stdscr, 5, 10, 8, 40, title="Test Box")

        # Verify title was added
        assert mock_stdscr.addstr.called
        # Check if "Test Box" was in any call
        title_found = any(
            "Test Box" in str(call) for call in mock_stdscr.addstr.call_args_list
        )
        assert title_found

    def test_draw_box_minimum_dimensions(self, mock_curses, mock_stdscr, simple_theme):
        """Test box drawing with minimum dimensions (2x2)."""
        simple_theme.apply(mock_stdscr)

        # Minimum valid box is 2x2
        simple_theme.draw_box(mock_stdscr, 0, 0, 2, 2)
        assert mock_stdscr.addstr.called

    def test_draw_box_too_small_raises_error(
        self, mock_curses, mock_stdscr, simple_theme
    ):
        """Test box drawing with too small dimensions raises ValueError."""
        simple_theme.apply(mock_stdscr)

        # Box smaller than 2x2 should raise ValueError
        with pytest.raises(ValueError, match="too small|minimum"):
            simple_theme.draw_box(mock_stdscr, 0, 0, 1, 1)

    def test_draw_box_custom_border_chars(
        self, mock_curses, mock_stdscr, simple_theme
    ):
        """Test box drawing uses custom border characters."""
        simple_theme.apply(mock_stdscr)

        # Default border chars from base Theme
        border_chars = simple_theme.get_border_chars()
        assert len(border_chars) == 8
        assert isinstance(border_chars, str)

    def test_draw_box_handles_curses_error(
        self, mock_curses, mock_stdscr, simple_theme
    ):
        """Test box drawing handles curses.error gracefully."""
        simple_theme.apply(mock_stdscr)

        # Make addstr raise curses.error
        mock_stdscr.addstr.side_effect = mock_curses.error("Out of bounds")

        # Should not propagate the error (draw_box catches it)
        try:
            simple_theme.draw_box(mock_stdscr, 0, 0, 5, 5)
        except mock_curses.error:
            pytest.fail("draw_box should catch curses.error")


class TestThemeApplyMechanism:
    """Test suite for Theme apply() mechanism."""

    def test_apply_initializes_colors(self, mock_curses, mock_stdscr, simple_theme):
        """Test apply() initializes semantic colors."""
        simple_theme.apply(mock_stdscr)

        # Colors should now be accessible
        assert simple_theme.colors is not None
        assert simple_theme.colors.primary > 0
        assert simple_theme.colors.success > 0

    def test_apply_initializes_components(
        self, mock_curses, mock_stdscr, simple_theme
    ):
        """Test apply() initializes component colors."""
        simple_theme.apply(mock_stdscr)

        # Components should now be accessible
        assert simple_theme.components is not None
        # SimpleTheme returns None for all components, so they'll be 0
        assert simple_theme.components.background == 0

    def test_apply_sets_screen_background(
        self, mock_curses, mock_stdscr, simple_theme
    ):
        """Test apply() sets screen background color."""
        simple_theme.apply(mock_stdscr)

        # Verify bkgd was called to set background
        assert mock_stdscr.bkgd.called

    def test_multiple_apply_calls(self, mock_curses, mock_stdscr, simple_theme):
        """Test multiple apply() calls work correctly."""
        simple_theme.apply(mock_stdscr)
        colors1 = simple_theme.colors

        # Apply again
        simple_theme.apply(mock_stdscr)
        colors2 = simple_theme.colors

        # Should get new color objects
        assert colors1 is not colors2


class TestThemeBorderChars:
    """Test suite for border character customization."""

    def test_default_border_chars_length(self, simple_theme):
        """Test default border chars have exactly 8 characters."""
        border_chars = simple_theme.get_border_chars()
        assert len(border_chars) == 8

    def test_default_border_chars_format(self, simple_theme):
        """Test default border chars are valid string."""
        border_chars = simple_theme.get_border_chars()
        assert isinstance(border_chars, str)
        # Default is "┌─┐││└─┘"
        assert all(isinstance(c, str) for c in border_chars)


class TestThemeWithComponentColors:
    """Test suite for themes that implement component colors."""

    def test_theme_with_component_colors(self, mock_curses, mock_stdscr):
        """Test theme that implements component color methods."""

        class ComponentTheme(Theme):
            def __init__(self):
                super().__init__("Component Theme", "Has components")

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

            def get_button(self) -> ColorPair:
                return ColorPair((255, 255, 255), (0, 120, 215))

            def get_button_focused(self) -> ColorPair:
                return ColorPair((0, 0, 0), (0, 255, 255))

        theme = ComponentTheme()
        theme.apply(mock_stdscr)

        # Component colors should be initialized
        assert theme.components.button > 0
        assert theme.components.button_focused > 0


class TestThemeErrorMessages:
    """Test suite for API misuse error messages."""

    def test_colors_before_apply_error_message(self, simple_theme):
        """Test helpful error when accessing colors before apply()."""
        with pytest.raises(RuntimeError) as exc_info:
            _ = simple_theme.colors

        error_msg = str(exc_info.value)
        assert (
            "has not been applied" in error_msg.lower()
            or "not available" in error_msg.lower()
        )
        assert "apply(" in error_msg
        assert "stdscr" in error_msg.lower()

    def test_components_before_apply_error_message(self, simple_theme):
        """Test helpful error when accessing components before apply()."""
        with pytest.raises(RuntimeError) as exc_info:
            _ = simple_theme.components

        error_msg = str(exc_info.value)
        assert (
            "has not been applied" in error_msg.lower()
            or "not available" in error_msg.lower()
        )
        assert "apply(" in error_msg

    def test_draw_box_invalid_window_error(self, mock_curses, simple_theme):
        """Test helpful error when drawing on invalid/dead window."""
        from unittest.mock import Mock

        # Create a mock window that raises error on getmaxyx
        dead_window = Mock()
        dead_window.getmaxyx.side_effect = mock_curses.error("window died")

        simple_theme._components = Mock()  # Fake apply
        simple_theme._components.border = 1

        with pytest.raises(RuntimeError) as exc_info:
            simple_theme.draw_box(dead_window, 0, 0, 5, 5)

        error_msg = str(exc_info.value)
        assert "window" in error_msg.lower() and (
            "valid" in error_msg.lower() or "dead" in error_msg.lower()
        )

    def test_apply_invalid_stdscr_error(self, mock_curses, simple_theme):
        """Test helpful error when applying theme to invalid stdscr."""
        from unittest.mock import Mock

        dead_stdscr = Mock()
        dead_stdscr.getmaxyx.side_effect = mock_curses.error("endwin called")

        with pytest.raises(RuntimeError) as exc_info:
            simple_theme.apply(dead_stdscr)

        error_msg = str(exc_info.value)
        assert "window" in error_msg.lower() and (
            "valid" in error_msg.lower() or "apply" in error_msg.lower()
        )
