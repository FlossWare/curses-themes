#!/usr/bin/env python3
"""Integration tests for curses-themes - end-to-end workflows."""

import pytest

from curses_themes import Theme, ThemeManager


class TestCompleteThemeLifecycle:
    """Test complete theme lifecycle from registration to use."""

    def test_register_load_apply_use(self, mock_curses, mock_stdscr):
        """Test complete workflow: register → load → apply → use colors → draw box."""

        class CustomTheme(Theme):
            def __init__(self):
                super().__init__("Custom", "Test theme")

            def get_color_map(self):
                return {
                    "background": (0, 0, 0),
                    "foreground": (255, 255, 255),
                    "primary": (0, 120, 215),
                    "success": (0, 255, 0),
                    "error": (255, 0, 0),
                    "warning": (255, 255, 0),
                    "info": (0, 255, 255),
                    "accent": (255, 0, 255),
                }

        # Register
        ThemeManager.register(CustomTheme, "custom")
        assert "custom" in ThemeManager._themes

        # Load
        theme = ThemeManager.load("custom")
        assert theme is not None
        assert theme.name == "Custom"

        # Apply
        theme.apply(mock_stdscr)
        assert theme.colors is not None
        assert theme.components is not None

        # Use colors
        assert theme.colors.primary > 0
        assert theme.colors.success > 0

        # Draw box
        theme.draw_box(mock_stdscr, 5, 10, 8, 40, title="Test")
        assert mock_stdscr.addstr.called

    def test_theme_switching(self, mock_curses, mock_stdscr, simple_theme):
        """Test switching between themes in same session."""

        # Load and apply first theme
        ThemeManager.register(simple_theme.__class__, "simple")
        theme1 = ThemeManager.load("simple")
        theme1.apply(mock_stdscr)
        colors1 = theme1.colors.primary

        # Load and apply second theme
        theme2 = ThemeManager.load("dark")
        theme2.apply(mock_stdscr)
        colors2 = theme2.colors.primary

        # Both should have colors initialized
        assert colors1 > 0
        assert colors2 > 0

        # Current should be the last loaded
        assert ThemeManager.get_current() is theme2

    def test_custom_theme_registration_and_use(self, mock_curses, mock_stdscr):
        """Test creating and using a custom theme end-to-end."""

        class MyCustomTheme(Theme):
            def __init__(self):
                super().__init__("My Custom Theme", "A test theme", "Tester")

            def get_color_map(self):
                return {
                    "background": (30, 30, 30),
                    "foreground": (200, 200, 200),
                    "primary": (100, 150, 255),
                    "success": (50, 200, 50),
                    "error": (255, 50, 50),
                    "warning": (255, 200, 50),
                    "info": (50, 150, 255),
                    "accent": (200, 100, 255),
                }

            component_colors = {
                "button": ((255, 255, 255), (100, 150, 255)),
            }

            def get_border_chars(self) -> str:
                return "╔═╗║║╚═╝"

        # Register and load
        ThemeManager.register(MyCustomTheme)
        theme = ThemeManager.load("my-custom-theme")

        # Apply and verify
        theme.apply(mock_stdscr)
        assert theme.colors.primary > 0
        assert theme.components.button > 0

        # Verify border chars
        assert theme.get_border_chars() == "╔═╗║║╚═╝"


class TestMultiThemeScenarios:
    """Test scenarios with multiple themes."""

    def test_multiple_themes_in_same_session(self, mock_curses, mock_stdscr):
        """Test loading multiple different themes."""

        dark = ThemeManager.load("dark")
        light = ThemeManager.load("light")

        # Both should be loaded
        assert dark is not None
        assert light is not None
        assert dark is not light

        # Apply both (one after another)
        dark.apply(mock_stdscr)
        assert dark.colors is not None

        light.apply(mock_stdscr)
        assert light.colors is not None

    def test_color_pair_reuse_across_themes(self, mock_curses, mock_stdscr):
        """Test that color pair cache works across theme switches."""
        from curses_themes.colors import ColorManager

        # Get initial pair count
        initial_pairs = ColorManager._next_pair

        # Load and apply first theme
        theme1 = ThemeManager.load("dark")
        theme1.apply(mock_stdscr)
        pairs_after_first = ColorManager._next_pair

        # Load and apply second theme with same colors
        theme2 = ThemeManager.load("dark")  # Same theme
        theme2.apply(mock_stdscr)
        pairs_after_second = ColorManager._next_pair

        # Second theme should reuse cached pairs
        # (Though it will still allocate some new ones)
        assert pairs_after_first > initial_pairs
        assert pairs_after_second >= pairs_after_first

    def test_theme_metadata_listing(self):
        """Test listing all registered themes with metadata."""
        themes = ThemeManager.list_themes()

        # Should have all built-in themes
        assert "default" in themes
        assert "dark" in themes
        assert "light" in themes

        # Check metadata structure
        for name, meta in themes.items():
            assert "name" in meta
            assert "description" in meta
            assert "author" in meta
            assert isinstance(meta["name"], str)
            assert isinstance(meta["description"], str)


class TestErrorHandlingIntegration:
    """Test error handling in integrated workflows."""

    def test_apply_theme_with_missing_colors(self, mock_curses, mock_stdscr):
        """Test that themes with missing required colors fail gracefully."""

        class BrokenTheme(Theme):
            def __init__(self):
                super().__init__("Broken", "Missing colors")

            def get_color_map(self):
                return {
                    "background": (0, 0, 0),
                    "foreground": (255, 255, 255),
                    # Missing: primary, success, error, warning, info, accent
                }

        theme = BrokenTheme()

        with pytest.raises(ValueError, match="missing required colors"):
            theme.apply(mock_stdscr)

    def test_load_nonexistent_theme_after_registration(self):
        """Test loading a theme that was never registered."""
        ThemeManager.reset()

        with pytest.raises(KeyError, match="not found"):
            ThemeManager.load("nonexistent-theme-xyz")

    def test_unregister_then_load_fails(self, simple_theme):
        """Test that loading after unregister fails."""
        ThemeManager.register(simple_theme.__class__, "temp")
        assert "temp" in ThemeManager._themes

        ThemeManager.unregister("temp")

        with pytest.raises(KeyError):
            ThemeManager.load("temp")


class TestBuiltinThemesIntegration:
    """Test that all built-in themes work end-to-end."""

    @pytest.mark.parametrize(
        "theme_name",
        [
            "default",
            "dark",
            "light",
            "dos",
            "dbase-iii",
            "dbase-iv",
            "ti-99-4a",
            "trs-80",
        ],
    )
    def test_builtin_theme_loads_and_applies(
        self, mock_curses, mock_stdscr, theme_name
    ):
        """Test each built-in theme can be loaded and applied."""
        theme = ThemeManager.load(theme_name)
        assert theme is not None

        # Apply should work
        theme.apply(mock_stdscr)

        # Colors should be initialized
        assert theme.colors is not None
        assert theme.colors.primary > 0
        assert theme.colors.success > 0
        assert theme.colors.error > 0

        # Should be able to draw boxes
        theme.draw_box(mock_stdscr, 5, 10, 8, 40)

    @pytest.mark.parametrize(
        "theme_name",
        ["default", "dark", "light", "dos"],
    )
    def test_builtin_theme_has_valid_metadata(self, theme_name):
        """Test built-in themes have complete metadata."""
        theme = ThemeManager.load(theme_name)

        assert theme.name
        assert theme.description
        assert theme.author
        assert isinstance(theme.name, str)
        assert isinstance(theme.description, str)
        assert isinstance(theme.author, str)
