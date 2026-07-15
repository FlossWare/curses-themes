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

        # Test get_components() returns dict of ColorPair values
        components = theme.get_components()
        assert isinstance(components, dict)

        component_names = [
            "background",
            "button",
            "button_focused",
            "text_input",
            "border",
            "selection",
            "disabled",
        ]

        for name in component_names:
            if name in components:
                assert isinstance(components[name], ColorPair)


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

    def test_missing_3d_colors_error(self, mock_curses, mock_stdscr):
        """Test helpful error when effects_3d is not provided."""
        from curses_themes import Theme3D

        class Incomplete3DTheme(Theme3D):
            def __init__(self):
                super().__init__("Incomplete 3D", "Missing effects_3d")

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

        theme = Incomplete3DTheme()

        with pytest.raises(NotImplementedError) as exc_info:
            theme.apply(mock_stdscr)

        error_msg = str(exc_info.value)
        assert "effects_3d" in error_msg
        assert "Incomplete 3D" in error_msg


class TestTheme3DAbstractMethods:
    """Tests for Theme3D abstract method enforcement."""

    def test_missing_effects_3d_raises_not_implemented(self):
        """Test that Theme3D without effects_3d raises NotImplementedError on get_3d_colors()."""
        from curses_themes.theme3d import Theme3D

        # Subclass missing effects_3d
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

        # Instantiation succeeds, but get_3d_colors() raises NotImplementedError
        theme = Incomplete3DTheme("Incomplete", "Missing effects_3d")
        with pytest.raises(NotImplementedError) as exc_info:
            theme.get_3d_colors()

        error_msg = str(exc_info.value)
        assert "effects_3d" in error_msg

    def test_missing_shadow_in_effects_3d_raises_error(self, mock_curses, mock_stdscr):
        """Test that missing 'shadow' key in effects_3d raises RuntimeError on apply()."""
        from curses_themes.theme3d import Theme3D

        # Subclass with effects_3d missing 'shadow'
        class MissingShadow(Theme3D):
            color_map = {
                "background": (200, 200, 200),
                "foreground": (0, 0, 0),
                "primary": (0, 100, 200),
                "success": (0, 200, 0),
                "error": (200, 0, 0),
                "warning": (200, 200, 0),
                "info": (0, 200, 200),
                "accent": (200, 0, 200),
            }

            effects_3d = {
                "highlight": ((255, 255, 255), (200, 200, 200)),
                "lowlight": ((64, 64, 64), (200, 200, 200)),
            }

        theme = MissingShadow("Missing Shadow", "No shadow color")
        with pytest.raises(RuntimeError) as exc_info:
            theme.apply(mock_stdscr)

        error_msg = str(exc_info.value)
        assert "shadow" in error_msg.lower()

    def test_missing_highlight_in_effects_3d_raises_error(
        self, mock_curses, mock_stdscr
    ):
        """Test that missing 'highlight' key in effects_3d raises RuntimeError on apply()."""
        from curses_themes.theme3d import Theme3D

        # Subclass with effects_3d missing 'highlight'
        class MissingHighlight(Theme3D):
            color_map = {
                "background": (200, 200, 200),
                "foreground": (0, 0, 0),
                "primary": (0, 100, 200),
                "success": (0, 200, 0),
                "error": (200, 0, 0),
                "warning": (200, 200, 0),
                "info": (0, 200, 200),
                "accent": (200, 0, 200),
            }

            effects_3d = {
                "shadow": ((0, 0, 0), (0, 0, 0)),
                "lowlight": ((64, 64, 64), (200, 200, 200)),
            }

        theme = MissingHighlight("Missing Highlight", "No highlight color")
        with pytest.raises(RuntimeError) as exc_info:
            theme.apply(mock_stdscr)

        error_msg = str(exc_info.value)
        assert "highlight" in error_msg.lower()

    def test_missing_lowlight_in_effects_3d_raises_error(
        self, mock_curses, mock_stdscr
    ):
        """Test that missing 'lowlight' key in effects_3d raises RuntimeError on apply()."""
        from curses_themes.theme3d import Theme3D

        # Subclass with effects_3d missing 'lowlight'
        class MissingLowlight(Theme3D):
            color_map = {
                "background": (200, 200, 200),
                "foreground": (0, 0, 0),
                "primary": (0, 100, 200),
                "success": (0, 200, 0),
                "error": (200, 0, 0),
                "warning": (200, 200, 0),
                "info": (0, 200, 200),
                "accent": (200, 0, 200),
            }

            effects_3d = {
                "shadow": ((0, 0, 0), (0, 0, 0)),
                "highlight": ((255, 255, 255), (200, 200, 200)),
            }

        theme = MissingLowlight("Missing Lowlight", "No lowlight color")
        with pytest.raises(RuntimeError) as exc_info:
            theme.apply(mock_stdscr)

        error_msg = str(exc_info.value)
        assert "lowlight" in error_msg.lower()

    def test_complete_implementation_succeeds(self):
        """Test that a complete Theme3D implementation can be instantiated."""
        from curses_themes.theme import ColorPair
        from curses_themes.theme3d import Theme3D

        # Complete subclass with effects_3d class attribute
        class Complete3DTheme(Theme3D):
            color_map = {
                "background": (200, 200, 200),
                "foreground": (0, 0, 0),
                "primary": (0, 100, 200),
                "success": (0, 200, 0),
                "error": (200, 0, 0),
                "warning": (200, 200, 0),
                "info": (0, 200, 200),
                "accent": (200, 0, 200),
            }

            effects_3d = {
                "shadow": ((0, 0, 0), (0, 0, 0)),
                "highlight": ((255, 255, 255), (200, 200, 200)),
                "lowlight": ((64, 64, 64), (200, 200, 200)),
            }

        # Should succeed
        theme = Complete3DTheme("Complete", "All effects_3d provided")
        assert theme is not None
        assert theme.name == "Complete"
        colors_3d = theme.get_3d_colors()
        assert "shadow" in colors_3d
        assert "highlight" in colors_3d
        assert "lowlight" in colors_3d
        assert isinstance(colors_3d["shadow"], ColorPair)
        assert isinstance(colors_3d["highlight"], ColorPair)
        assert isinstance(colors_3d["lowlight"], ColorPair)

    def test_existing_themes_still_work(self):
        """Test that existing Theme3D implementations (Borland, dBase) still work."""
        from curses_themes.theme import ColorPair
        from curses_themes.themes.borland3d import Borland3DTheme
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme

        # Both should instantiate successfully
        borland = Borland3DTheme()
        assert borland is not None
        borland_3d = borland.get_3d_colors()
        assert isinstance(borland_3d["shadow"], ColorPair)
        assert isinstance(borland_3d["highlight"], ColorPair)
        assert isinstance(borland_3d["lowlight"], ColorPair)

        dbase = DBase4_3DTheme()
        assert dbase is not None
        dbase_3d = dbase.get_3d_colors()
        assert isinstance(dbase_3d["shadow"], ColorPair)
        assert isinstance(dbase_3d["highlight"], ColorPair)
        assert isinstance(dbase_3d["lowlight"], ColorPair)
