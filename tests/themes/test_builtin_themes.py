#!/usr/bin/env python3
"""Smoke tests for all built-in themes."""

import pytest
from curses_themes.themes.default import DefaultTheme
from curses_themes.themes.dark import DarkTheme
from curses_themes.themes.light import LightTheme
from curses_themes.themes.dos import DOSTheme
from curses_themes.themes.dbase3 import DBase3Theme
from curses_themes.themes.dbase4 import DBase4Theme
from curses_themes.themes.ti994a import TI994ATheme
from curses_themes.themes.trs80 import TRS80Theme


# Parametrized test for all lazy-registered built-in themes
# Note: 3D themes (Borland3DTheme, DBase4_3DTheme) are registered at module load
# but not included in lazy registration, so they're tested separately
ALL_BUILTIN_THEMES = [
    DefaultTheme,
    DarkTheme,
    LightTheme,
    DOSTheme,
    DBase3Theme,
    DBase4Theme,
    TI994ATheme,
    TRS80Theme,
]


class TestBuiltinThemeColorMaps:
    """Test that all built-in themes have valid color maps."""

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_has_all_required_colors(self, theme_class):
        """Test theme has all required semantic colors."""
        theme = theme_class()
        color_map = theme.get_color_map()

        required_colors = {
            "background",
            "foreground",
            "primary",
            "success",
            "error",
            "warning",
            "info",
            "accent",
        }

        assert set(color_map.keys()) == required_colors

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_rgb_values_valid(self, theme_class):
        """Test all RGB values are in valid range (0-255)."""
        theme = theme_class()
        color_map = theme.get_color_map()

        for color_name, (r, g, b) in color_map.items():
            assert (
                isinstance(r, int) and 0 <= r <= 255
            ), f"{theme_class.__name__} {color_name} red out of range: {r}"
            assert (
                isinstance(g, int) and 0 <= g <= 255
            ), f"{theme_class.__name__} {color_name} green out of range: {g}"
            assert (
                isinstance(b, int) and 0 <= b <= 255
            ), f"{theme_class.__name__} {color_name} blue out of range: {b}"


class TestBuiltinThemeMetadata:
    """Test that all built-in themes have complete metadata."""

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_has_name(self, theme_class):
        """Test theme has a non-empty name."""
        theme = theme_class()
        assert theme.name
        assert isinstance(theme.name, str)
        assert len(theme.name) > 0

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_has_description(self, theme_class):
        """Test theme has a non-empty description."""
        theme = theme_class()
        assert theme.description
        assert isinstance(theme.description, str)
        assert len(theme.description) > 0

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_has_author(self, theme_class):
        """Test theme has an author."""
        theme = theme_class()
        assert theme.author
        assert isinstance(theme.author, str)


class TestBuiltinThemeComponentColors:
    """Test that built-in themes handle component colors correctly."""

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_component_methods_return_colorpair_or_none(self, theme_class):
        """Test component methods return ColorPair or None."""
        from curses_themes.theme import ColorPair

        theme = theme_class()

        component_methods = [
            "get_background",
            "get_button",
            "get_button_focused",
            "get_text_input",
            "get_border",
            "get_selection",
            "get_disabled",
        ]

        for method_name in component_methods:
            method = getattr(theme, method_name)
            result = method()
            assert result is None or isinstance(
                result, ColorPair
            ), f"{theme_class.__name__}.{method_name}() returned invalid type: {type(result)}"


class TestBuiltinThemeBorderChars:
    """Test border characters for built-in themes."""

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_border_chars_length(self, theme_class):
        """Test border chars have exactly 8 characters."""
        theme = theme_class()
        border_chars = theme.get_border_chars()
        assert (
            len(border_chars) == 8
        ), f"{theme_class.__name__} border_chars length is {len(border_chars)}, expected 8"

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_border_chars_type(self, theme_class):
        """Test border chars are a string."""
        theme = theme_class()
        border_chars = theme.get_border_chars()
        assert isinstance(
            border_chars, str
        ), f"{theme_class.__name__} border_chars is not a string"


class TestBuiltinThemeApplication:
    """Test that built-in themes can be applied to a window."""

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_applies_without_error(
        self, mock_curses, mock_stdscr, theme_class
    ):
        """Test theme can be applied to stdscr."""
        theme = theme_class()

        # Should not raise
        theme.apply(mock_stdscr)

        # Colors should be initialized
        assert theme.colors is not None
        assert theme.components is not None

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_draw_box_works(self, mock_curses, mock_stdscr, theme_class):
        """Test theme can draw boxes after apply."""
        theme = theme_class()
        theme.apply(mock_stdscr)

        # Should not raise
        theme.draw_box(mock_stdscr, 5, 10, 8, 40, title="Test")

        # Verify drawing happened
        assert mock_stdscr.addstr.called


class TestSpecificThemeCharacteristics:
    """Test specific characteristics of individual themes."""

    def test_default_theme_has_expected_name(self):
        """Test DefaultTheme has correct name."""
        theme = DefaultTheme()
        assert theme.name == "Default"

    def test_dark_theme_has_expected_name(self):
        """Test DarkTheme has correct name."""
        theme = DarkTheme()
        assert theme.name == "Dark"

    def test_dos_theme_is_retro(self):
        """Test DOS theme has retro characteristics."""
        theme = DOSTheme()
        # DOS theme should mention its era or characteristics
        assert "DOS" in theme.name or "dos" in theme.description.lower()

    def test_ti994a_theme_is_retro(self):
        """Test TI-99/4A theme has retro characteristics."""
        theme = TI994ATheme()
        assert "TI-99" in theme.name or "ti-99" in theme.description.lower()


class TestThemeColorContrast:
    """Basic contrast checks for themes."""

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_foreground_background_different(self, theme_class):
        """Test foreground and background colors are different."""
        theme = theme_class()
        color_map = theme.get_color_map()

        fg = color_map["foreground"]
        bg = color_map["background"]

        # Colors should be different (at least one component differs)
        assert fg != bg, f"{theme_class.__name__} foreground equals background"

    @pytest.mark.parametrize("theme_class", ALL_BUILTIN_THEMES)
    def test_theme_semantic_colors_are_distinct(self, theme_class):
        """Test that semantic colors are reasonably distinct."""
        theme = theme_class()
        color_map = theme.get_color_map()

        # Success, error, and warning should all be different
        success = color_map["success"]
        error = color_map["error"]
        warning = color_map["warning"]

        # At least one should differ from the others
        # (Some themes may use similar colors, but not all identical)
        all_same = success == error == warning
        assert (
            not all_same
        ), f"{theme_class.__name__} success/error/warning are all identical"
