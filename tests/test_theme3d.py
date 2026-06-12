#!/usr/bin/env python3
"""Tests for Theme3D base class - 3D box drawing."""

import pytest

from curses_themes.themes.borland3d import Borland3DTheme
from curses_themes.themes.dbase4_3d import DBase4_3DTheme


class TestTheme3DBoxDrawing:
    """Test 3D-style box drawing functionality."""

    @pytest.mark.parametrize("theme_class", [Borland3DTheme, DBase4_3DTheme])
    def test_3d_theme_initialization(self, theme_class):
        """Test 3D theme can be initialized."""
        theme = theme_class()
        assert theme is not None
        assert theme.name
        assert theme.description

    @pytest.mark.parametrize("theme_class", [Borland3DTheme, DBase4_3DTheme])
    def test_3d_theme_has_color_map(self, theme_class):
        """Test 3D theme has complete color map."""
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

    @pytest.mark.parametrize("theme_class", [Borland3DTheme, DBase4_3DTheme])
    def test_3d_theme_applies(self, mock_curses, mock_stdscr, theme_class):
        """Test 3D theme can be applied."""
        theme = theme_class()
        theme.apply(mock_stdscr)

        assert theme.colors is not None
        assert theme.components is not None

    @pytest.mark.parametrize("theme_class", [Borland3DTheme, DBase4_3DTheme])
    def test_3d_theme_has_border_chars(self, theme_class):
        """Test 3D theme has border characters."""
        theme = theme_class()
        border_chars = theme.get_border_chars()

        assert len(border_chars) == 8
        assert isinstance(border_chars, str)

    @pytest.mark.parametrize("theme_class", [Borland3DTheme, DBase4_3DTheme])
    def test_3d_theme_component_colors(self, theme_class):
        """Test 3D theme has component color definitions."""
        from curses_themes.theme import ColorPair

        theme = theme_class()

        # Test component methods exist and return ColorPair or None
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
            assert result is None or isinstance(result, ColorPair)


class TestBorland3DTheme:
    """Specific tests for Borland 3D theme."""

    def test_borland_theme_name(self):
        """Test Borland 3D theme has correct name."""
        theme = Borland3DTheme()
        assert "Borland" in theme.name or "3D" in theme.name

    def test_borland_theme_is_retro(self):
        """Test Borland 3D theme has retro styling."""
        theme = Borland3DTheme()
        # Should mention Turbo Vision or 1990s in description
        desc_lower = theme.description.lower()
        assert "turbo" in desc_lower or "borland" in desc_lower or "1990" in desc_lower

    def test_borland_theme_colors(self, mock_curses, mock_stdscr):
        """Test Borland 3D theme color palette."""
        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Borland used cyan/blue heavily
        color_map = theme.get_color_map()
        assert "primary" in color_map
        # Verify color components are valid
        r, g, b = color_map["primary"]
        assert 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255


class TestDBase4_3DTheme:
    """Specific tests for dBase IV 3D theme."""

    def test_dbase4_3d_theme_name(self):
        """Test dBase IV 3D theme has correct name."""
        theme = DBase4_3DTheme()
        assert "dBase" in theme.name or "IV" in theme.name

    def test_dbase4_3d_theme_is_retro(self):
        """Test dBase IV 3D theme has retro styling."""
        theme = DBase4_3DTheme()
        desc_lower = theme.description.lower()
        assert "dbase" in desc_lower or "database" in desc_lower or "1990" in desc_lower

    def test_dbase4_3d_theme_colors(self, mock_curses, mock_stdscr):
        """Test dBase IV 3D theme color palette."""
        theme = DBase4_3DTheme()
        theme.apply(mock_stdscr)

        color_map = theme.get_color_map()
        assert all(key in color_map for key in ["background", "foreground", "primary"])


class TestTheme3DIntegration:
    """Integration tests for 3D themes."""

    def test_borland_theme_full_workflow(self, mock_curses, mock_stdscr):
        """Test complete workflow with Borland 3D theme."""
        from curses_themes import ThemeManager

        # Load theme
        theme = ThemeManager.load("borland-3d")
        assert theme is not None

        # Apply theme
        theme.apply(mock_stdscr)
        assert theme.colors is not None

        # Draw box
        theme.draw_box(mock_stdscr, 5, 10, 8, 40, title="Test")
        assert mock_stdscr.addstr.called

    def test_dbase4_3d_theme_full_workflow(self, mock_curses, mock_stdscr):
        """Test complete workflow with dBase IV 3D theme."""
        from curses_themes import ThemeManager

        # Load theme
        theme = ThemeManager.load("dbase-iv-3d")
        assert theme is not None

        # Apply theme
        theme.apply(mock_stdscr)
        assert theme.colors is not None

        # Draw box
        theme.draw_box(mock_stdscr, 5, 10, 8, 40, title="Database")
        assert mock_stdscr.addstr.called

    @pytest.mark.parametrize("theme_name", ["borland-3d", "dbase-iv-3d"])
    def test_3d_theme_metadata_complete(self, theme_name):
        """Test 3D themes have complete metadata."""
        from curses_themes import ThemeManager

        themes = ThemeManager.list_themes()
        assert theme_name in themes

        meta = themes[theme_name]
        assert "name" in meta
        assert "description" in meta
        assert "author" in meta
        assert meta["name"]
        assert meta["description"]
        assert meta["author"]


class TestTheme3DErrorMessages:
    """Test suite for Theme3D API misuse error messages."""

    def test_missing_shadow_color_error(self, mock_curses, mock_stdscr):
        """Test helpful error when get_shadow_color() calls super()."""
        from curses_themes import Theme3D, ColorPair

        class Incomplete3DTheme(Theme3D):
            def __init__(self):
                super().__init__("Incomplete 3D", "Missing methods")

            def get_color_map(self):
                return {
                    "background": (200, 200, 200),
                    "foreground": (0, 0, 0),
                    "primary": (0, 0, 255),
                    "success": (0, 255, 0),
                    "error": (255, 0, 0),
                    "warning": (255, 255, 0),
                    "info": (0, 255, 255),
                    "accent": (255, 0, 255),
                }

            def get_shadow_color(self) -> ColorPair:
                """Calls super which raises NotImplementedError."""
                return super().get_shadow_color()

            def get_highlight_color(self) -> ColorPair:
                """Calls super which raises NotImplementedError."""
                return super().get_highlight_color()

            def get_lowlight_color(self) -> ColorPair:
                """Calls super which raises NotImplementedError."""
                return super().get_lowlight_color()

        theme = Incomplete3DTheme()

        with pytest.raises(RuntimeError) as exc_info:
            theme.apply(mock_stdscr)

        error_msg = str(exc_info.value)
        assert "incomplete" in error_msg.lower() or "not implemented" in error_msg.lower()
        assert (
            "shadow" in error_msg.lower()
            or "highlight" in error_msg.lower()
            or "lowlight" in error_msg.lower()
        )
        assert "ColorPair" in error_msg


class TestTheme3DAbstractMethods:
    """Tests for Theme3D abstract method enforcement."""

    def test_cannot_instantiate_without_all_3d_methods(self):
        """Test that Theme3D cannot be instantiated without implementing all required methods."""
        from curses_themes.theme3d import Theme3D

        # Subclass missing all three 3D methods
        class Incomplete3DTheme(Theme3D):
            def get_color_map(self):
                return {
                    "background": (200, 200, 200),
                    "foreground": (0, 0, 0),
                    "primary": (0, 100, 200),
                    "success": (0, 200, 0),
                    "error": (200, 0, 0),
                    "warning": (200, 200, 0),
                    "info": (0, 200, 200),
                    "accent": (200, 0, 200),
                }

        # Should raise TypeError when trying to instantiate
        with pytest.raises(TypeError) as exc_info:
            Incomplete3DTheme("Incomplete", "Missing 3D methods")

        error_msg = str(exc_info.value)
        assert "abstract" in error_msg.lower()

    def test_missing_shadow_color_raises_error(self):
        """Test that missing get_shadow_color() raises TypeError."""
        from curses_themes.theme import ColorPair
        from curses_themes.theme3d import Theme3D

        # Subclass missing only get_shadow_color
        class MissingShadow(Theme3D):
            def get_color_map(self):
                return {
                    "background": (200, 200, 200),
                    "foreground": (0, 0, 0),
                    "primary": (0, 100, 200),
                    "success": (0, 200, 0),
                    "error": (200, 0, 0),
                    "warning": (200, 200, 0),
                    "info": (0, 200, 200),
                    "accent": (200, 0, 200),
                }

            def get_highlight_color(self):
                return ColorPair((255, 255, 255), (200, 200, 200))

            def get_lowlight_color(self):
                return ColorPair((64, 64, 64), (200, 200, 200))

        with pytest.raises(TypeError) as exc_info:
            MissingShadow("Missing Shadow", "No shadow color")

        error_msg = str(exc_info.value)
        assert "abstract" in error_msg.lower() or "get_shadow_color" in error_msg

    def test_missing_highlight_color_raises_error(self):
        """Test that missing get_highlight_color() raises TypeError."""
        from curses_themes.theme import ColorPair
        from curses_themes.theme3d import Theme3D

        # Subclass missing only get_highlight_color
        class MissingHighlight(Theme3D):
            def get_color_map(self):
                return {
                    "background": (200, 200, 200),
                    "foreground": (0, 0, 0),
                    "primary": (0, 100, 200),
                    "success": (0, 200, 0),
                    "error": (200, 0, 0),
                    "warning": (200, 200, 0),
                    "info": (0, 200, 200),
                    "accent": (200, 0, 200),
                }

            def get_shadow_color(self):
                return ColorPair((0, 0, 0), (0, 0, 0))

            def get_lowlight_color(self):
                return ColorPair((64, 64, 64), (200, 200, 200))

        with pytest.raises(TypeError) as exc_info:
            MissingHighlight("Missing Highlight", "No highlight color")

        error_msg = str(exc_info.value)
        assert "abstract" in error_msg.lower() or "get_highlight_color" in error_msg

    def test_missing_lowlight_color_raises_error(self):
        """Test that missing get_lowlight_color() raises TypeError."""
        from curses_themes.theme import ColorPair
        from curses_themes.theme3d import Theme3D

        # Subclass missing only get_lowlight_color
        class MissingLowlight(Theme3D):
            def get_color_map(self):
                return {
                    "background": (200, 200, 200),
                    "foreground": (0, 0, 0),
                    "primary": (0, 100, 200),
                    "success": (0, 200, 0),
                    "error": (200, 0, 0),
                    "warning": (200, 200, 0),
                    "info": (0, 200, 200),
                    "accent": (200, 0, 200),
                }

            def get_shadow_color(self):
                return ColorPair((0, 0, 0), (0, 0, 0))

            def get_highlight_color(self):
                return ColorPair((255, 255, 255), (200, 200, 200))

        with pytest.raises(TypeError) as exc_info:
            MissingLowlight("Missing Lowlight", "No lowlight color")

        error_msg = str(exc_info.value)
        assert "abstract" in error_msg.lower() or "get_lowlight_color" in error_msg

    def test_complete_implementation_succeeds(self):
        """Test that a complete Theme3D implementation can be instantiated."""
        from curses_themes.theme import ColorPair
        from curses_themes.theme3d import Theme3D

        # Complete subclass with all required methods
        class Complete3DTheme(Theme3D):
            def get_color_map(self):
                return {
                    "background": (200, 200, 200),
                    "foreground": (0, 0, 0),
                    "primary": (0, 100, 200),
                    "success": (0, 200, 0),
                    "error": (200, 0, 0),
                    "warning": (200, 200, 0),
                    "info": (0, 200, 200),
                    "accent": (200, 0, 200),
                }

            def get_shadow_color(self):
                return ColorPair((0, 0, 0), (0, 0, 0))

            def get_highlight_color(self):
                return ColorPair((255, 255, 255), (200, 200, 200))

            def get_lowlight_color(self):
                return ColorPair((64, 64, 64), (200, 200, 200))

        # Should succeed
        theme = Complete3DTheme("Complete", "All methods implemented")
        assert theme is not None
        assert theme.name == "Complete"
        assert theme.get_shadow_color() is not None
        assert theme.get_highlight_color() is not None
        assert theme.get_lowlight_color() is not None

    def test_existing_themes_still_work(self):
        """Test that existing Theme3D implementations (Borland, dBase) still work."""
        from curses_themes.themes.borland3d import Borland3DTheme
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme

        # Both should instantiate successfully
        borland = Borland3DTheme()
        assert borland is not None
        assert borland.get_shadow_color() is not None
        assert borland.get_highlight_color() is not None
        assert borland.get_lowlight_color() is not None

        dbase = DBase4_3DTheme()
        assert dbase is not None
        assert dbase.get_shadow_color() is not None
        assert dbase.get_highlight_color() is not None
        assert dbase.get_lowlight_color() is not None
