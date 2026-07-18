#!/usr/bin/env python3
"""Tests for 3D theme visual consistency between Java JSON exports and Python built-in themes.

Verifies that the Java curses-java 3D themes (borland3d.json, dbase4-3d.json) load
correctly as ConfigTheme3D instances and that their 3D effect colors, border
characters, component colors, and shadow offsets are structurally consistent with
the Python Borland3DTheme and DBase4_3DTheme classes.

The Java theme files live in the sibling curses-java repo at
``../../curses-java/themes/`` relative to the curses-themes repo root.  All tests
in this module are skipped when the directory is absent.
"""

import json
import os
import pathlib

import pytest

from curses_themes.config_theme import (
    NCURSES_COLOR_MAP,
    ConfigTheme,
    ConfigTheme3D,
    _convert_java_border_chars,
    _convert_java_to_python,
    load_theme_from_file,
)
from curses_themes.theme import ColorPair
from curses_themes.theme3d import Theme3D

# ---------------------------------------------------------------------------
# Path to the Java theme directory (sibling repo)
# ---------------------------------------------------------------------------

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
JAVA_THEMES_DIR = _REPO_ROOT / ".." / "curses-java" / "themes"

_java_themes_available = JAVA_THEMES_DIR.is_dir()

pytestmark = pytest.mark.skipif(
    not _java_themes_available,
    reason="curses-java themes directory not found",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ncurses_rgb(name: str) -> tuple[int, int, int]:
    """Resolve an ncurses color name to its standard RGB tuple."""
    return NCURSES_COLOR_MAP[name.upper()]


def _load_java_raw(filename: str) -> dict:
    """Load raw JSON from a Java theme file (no conversion)."""
    path = JAVA_THEMES_DIR / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Test 1: Java 3D JSON files produce ConfigTheme3D instances
# ---------------------------------------------------------------------------


class TestJava3DFilesLoadAsConfigTheme3D:
    """Verify that both Java 3D theme files load as ConfigTheme3D, not ConfigTheme."""

    def test_borland3d_loads_as_config_theme_3d(self):
        """borland3d.json must produce a ConfigTheme3D instance."""
        theme = load_theme_from_file(str(JAVA_THEMES_DIR / "borland3d.json"))
        assert isinstance(theme, ConfigTheme3D), (
            f"Expected ConfigTheme3D, got {type(theme).__name__}"
        )
        assert isinstance(theme, Theme3D)

    def test_dbase4_3d_loads_as_config_theme_3d(self):
        """dbase4-3d.json must produce a ConfigTheme3D instance."""
        theme = load_theme_from_file(str(JAVA_THEMES_DIR / "dbase4-3d.json"))
        assert isinstance(theme, ConfigTheme3D), (
            f"Expected ConfigTheme3D, got {type(theme).__name__}"
        )
        assert isinstance(theme, Theme3D)

    def test_borland3d_not_plain_config_theme(self):
        """borland3d.json must NOT be a plain ConfigTheme (it has 3D effects)."""
        theme = load_theme_from_file(str(JAVA_THEMES_DIR / "borland3d.json"))
        # ConfigTheme3D is a subclass of Theme3D, not ConfigTheme
        assert not isinstance(theme, ConfigTheme)

    def test_dbase4_3d_not_plain_config_theme(self):
        """dbase4-3d.json must NOT be a plain ConfigTheme (it has 3D effects)."""
        theme = load_theme_from_file(str(JAVA_THEMES_DIR / "dbase4-3d.json"))
        assert not isinstance(theme, ConfigTheme)

    def test_borland3d_name_matches(self):
        """borland3d.json theme name matches the Python Borland3DTheme name."""
        from curses_themes.themes.borland3d import Borland3DTheme

        java_theme = load_theme_from_file(str(JAVA_THEMES_DIR / "borland3d.json"))
        py_theme = Borland3DTheme()
        assert java_theme.name == py_theme.name

    def test_dbase4_3d_name_matches(self):
        """dbase4-3d.json theme name matches the Python DBase4_3DTheme name."""
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme

        java_theme = load_theme_from_file(str(JAVA_THEMES_DIR / "dbase4-3d.json"))
        py_theme = DBase4_3DTheme()
        assert java_theme.name == py_theme.name


# ---------------------------------------------------------------------------
# Test 2: 3D effect colors -- shadow, highlight, lowlight
# ---------------------------------------------------------------------------


class TestBorland3DEffectColors:
    """Compare 3D effect colors between Java borland3d.json and Python Borland3DTheme."""

    @pytest.fixture
    def java_theme(self):
        return load_theme_from_file(str(JAVA_THEMES_DIR / "borland3d.json"))

    @pytest.fixture
    def py_theme(self):
        from curses_themes.themes.borland3d import Borland3DTheme
        return Borland3DTheme()

    def test_both_have_shadow_highlight_lowlight(self, java_theme, py_theme):
        """Both themes define all three required 3D effect keys."""
        java_3d = java_theme.get_3d_colors()
        py_3d = py_theme.get_3d_colors()

        for key in ("shadow", "highlight", "lowlight"):
            assert key in java_3d, f"Java theme missing 3D key: {key}"
            assert key in py_3d, f"Python theme missing 3D key: {key}"

    def test_shadow_colors_match(self, java_theme, py_theme):
        """Shadow color is BLACK/BLACK in both Java and Python Borland 3D themes."""
        java_shadow = java_theme.get_3d_colors()["shadow"]
        py_shadow = py_theme.get_3d_colors()["shadow"]

        assert java_shadow.foreground == py_shadow.foreground, (
            f"Shadow fg mismatch: Java {java_shadow.foreground} vs Python {py_shadow.foreground}"
        )
        assert java_shadow.background == py_shadow.background, (
            f"Shadow bg mismatch: Java {java_shadow.background} vs Python {py_shadow.background}"
        )

    def test_highlight_foreground_matches(self, java_theme, py_theme):
        """Highlight foreground is WHITE in both (255, 255, 255)."""
        java_hl = java_theme.get_3d_colors()["highlight"]
        py_hl = py_theme.get_3d_colors()["highlight"]

        assert java_hl.foreground == py_hl.foreground, (
            f"Highlight fg mismatch: Java {java_hl.foreground} vs Python {py_hl.foreground}"
        )

    def test_lowlight_foreground_matches(self, java_theme, py_theme):
        """Lowlight foreground is BLACK in both (0, 0, 0)."""
        java_ll = java_theme.get_3d_colors()["lowlight"]
        py_ll = py_theme.get_3d_colors()["lowlight"]

        assert java_ll.foreground == py_ll.foreground, (
            f"Lowlight fg mismatch: Java {java_ll.foreground} vs Python {py_ll.foreground}"
        )

    def test_3d_colors_are_color_pairs(self, java_theme, py_theme):
        """All 3D effect values are ColorPair instances for both themes."""
        for name, theme in [("Java", java_theme), ("Python", py_theme)]:
            colors_3d = theme.get_3d_colors()
            for key in ("shadow", "highlight", "lowlight"):
                assert isinstance(colors_3d[key], ColorPair), (
                    f"{name} 3D color '{key}' is not a ColorPair"
                )

    def test_java_highlight_bg_is_ncurses_cyan(self, java_theme):
        """Java highlight bg uses ncurses CYAN (0, 255, 255) from the JSON."""
        java_hl = java_theme.get_3d_colors()["highlight"]
        assert java_hl.background == _ncurses_rgb("CYAN")

    def test_java_lowlight_bg_is_ncurses_cyan(self, java_theme):
        """Java lowlight bg uses ncurses CYAN (0, 255, 255) from the JSON."""
        java_ll = java_theme.get_3d_colors()["lowlight"]
        assert java_ll.background == _ncurses_rgb("CYAN")


class TestDBase4_3DEffectColors:
    """Compare 3D effect colors between Java dbase4-3d.json and Python DBase4_3DTheme."""

    @pytest.fixture
    def java_theme(self):
        return load_theme_from_file(str(JAVA_THEMES_DIR / "dbase4-3d.json"))

    @pytest.fixture
    def py_theme(self):
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme
        return DBase4_3DTheme()

    def test_both_have_shadow_highlight_lowlight(self, java_theme, py_theme):
        """Both themes define all three required 3D effect keys."""
        java_3d = java_theme.get_3d_colors()
        py_3d = py_theme.get_3d_colors()

        for key in ("shadow", "highlight", "lowlight"):
            assert key in java_3d, f"Java theme missing 3D key: {key}"
            assert key in py_3d, f"Python theme missing 3D key: {key}"

    def test_shadow_colors_match(self, java_theme, py_theme):
        """Shadow color is BLACK/BLACK in both Java and Python dBASE IV 3D themes."""
        java_shadow = java_theme.get_3d_colors()["shadow"]
        py_shadow = py_theme.get_3d_colors()["shadow"]

        assert java_shadow.foreground == py_shadow.foreground, (
            f"Shadow fg mismatch: Java {java_shadow.foreground} vs Python {py_shadow.foreground}"
        )
        assert java_shadow.background == py_shadow.background, (
            f"Shadow bg mismatch: Java {java_shadow.background} vs Python {py_shadow.background}"
        )

    def test_highlight_foreground_is_white(self, java_theme, py_theme):
        """Highlight foreground is WHITE in both Java and Python."""
        java_hl = java_theme.get_3d_colors()["highlight"]
        py_hl = py_theme.get_3d_colors()["highlight"]

        assert java_hl.foreground == (255, 255, 255)
        assert py_hl.foreground == (255, 255, 255)

    def test_lowlight_foreground_is_black(self, java_theme, py_theme):
        """Lowlight foreground is BLACK in both Java and Python."""
        java_ll = java_theme.get_3d_colors()["lowlight"]
        py_ll = py_theme.get_3d_colors()["lowlight"]

        assert java_ll.foreground == (0, 0, 0)
        assert py_ll.foreground == (0, 0, 0)

    def test_3d_colors_are_color_pairs(self, java_theme, py_theme):
        """All 3D effect values are ColorPair instances for both themes."""
        for name, theme in [("Java", java_theme), ("Python", py_theme)]:
            colors_3d = theme.get_3d_colors()
            for key in ("shadow", "highlight", "lowlight"):
                assert isinstance(colors_3d[key], ColorPair), (
                    f"{name} 3D color '{key}' is not a ColorPair"
                )


# ---------------------------------------------------------------------------
# Test 3: Border character consistency
# ---------------------------------------------------------------------------


class TestBorderCharConsistency:
    """Verify border characters are correctly converted between Java and Python."""

    def test_borland3d_single_border_conversion(self):
        """Java borland3d.json single border converts to a valid 8-char Python string."""
        raw = _load_java_raw("borland3d.json")
        java_single = raw["borders"]["single"]
        converted = _convert_java_border_chars(java_single)

        assert len(converted) == 8, (
            f"Converted border must be 8 chars, got {len(converted)}: {converted!r}"
        )

    def test_borland3d_double_border_conversion(self):
        """Java borland3d.json double border converts to a valid 8-char Python string."""
        raw = _load_java_raw("borland3d.json")
        java_double = raw["borders"]["double"]
        converted = _convert_java_border_chars(java_double)

        assert len(converted) == 8
        assert converted == "╔═╗║║╚═╝"

    def test_dbase4_3d_single_border_conversion(self):
        """Java dbase4-3d.json single border converts to a valid 8-char Python string."""
        raw = _load_java_raw("dbase4-3d.json")
        java_single = raw["borders"]["single"]
        converted = _convert_java_border_chars(java_single)

        assert len(converted) == 8

    def test_dbase4_3d_double_border_conversion(self):
        """Java dbase4-3d.json double border converts to a valid 8-char Python string."""
        raw = _load_java_raw("dbase4-3d.json")
        java_double = raw["borders"]["double"]
        converted = _convert_java_border_chars(java_double)

        assert len(converted) == 8
        assert converted == "╔═╗║║╚═╝"

    def test_borland3d_loaded_border_chars_valid(self):
        """Loaded borland3d.json has valid 8-char border_chars after full conversion."""
        theme = load_theme_from_file(str(JAVA_THEMES_DIR / "borland3d.json"))
        border = theme.get_border_chars()
        assert len(border) == 8

    def test_dbase4_3d_loaded_border_chars_valid(self):
        """Loaded dbase4-3d.json has valid 8-char border_chars after full conversion."""
        theme = load_theme_from_file(str(JAVA_THEMES_DIR / "dbase4-3d.json"))
        border = theme.get_border_chars()
        assert len(border) == 8

    def test_dbase4_3d_borders_match_python(self):
        """dBASE IV 3D borders match between Java (converted) and Python."""
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme

        java_theme = load_theme_from_file(str(JAVA_THEMES_DIR / "dbase4-3d.json"))
        py_theme = DBase4_3DTheme()

        assert java_theme.get_border_chars() == py_theme.get_border_chars(), (
            f"Border mismatch: Java {java_theme.get_border_chars()!r} vs "
            f"Python {py_theme.get_border_chars()!r}"
        )

    def test_dbase4_3d_double_borders_match_python(self):
        """dBASE IV 3D double borders match between Java (converted) and Python."""
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme

        java_theme = load_theme_from_file(str(JAVA_THEMES_DIR / "dbase4-3d.json"))
        py_theme = DBase4_3DTheme()

        assert java_theme.get_double_border_chars() == py_theme.get_double_border_chars()


# ---------------------------------------------------------------------------
# Test 4: Component color consistency
# ---------------------------------------------------------------------------


class TestBorland3DComponentColors:
    """Compare component colors between Java borland3d.json and Python Borland3DTheme."""

    @pytest.fixture
    def java_theme(self):
        return load_theme_from_file(str(JAVA_THEMES_DIR / "borland3d.json"))

    @pytest.fixture
    def py_theme(self):
        from curses_themes.themes.borland3d import Borland3DTheme
        return Borland3DTheme()

    def test_java_has_all_component_keys(self, java_theme):
        """Java borland3d.json has all expected component keys after conversion."""
        comps = java_theme.get_components()
        expected_keys = {"background", "button", "button_focused", "text_input",
                         "border", "selection", "disabled"}
        assert set(comps.keys()) == expected_keys

    def test_python_has_all_component_keys(self, py_theme):
        """Python Borland3DTheme has all expected component keys."""
        expected_keys = {"background", "button", "button_focused", "text_input",
                         "border", "selection", "disabled"}
        assert set(py_theme.component_colors.keys()) == expected_keys

    def test_same_component_keys(self, java_theme, py_theme):
        """Both Java and Python Borland 3D define the same set of component keys."""
        java_keys = set(java_theme.get_components().keys())
        py_keys = set(py_theme.component_colors.keys())
        assert java_keys == py_keys

    def test_component_colors_are_valid_rgb(self, java_theme):
        """All Java-loaded component colors are valid RGB tuples (0-255)."""
        comps = java_theme.get_components()
        for comp_name, pair in comps.items():
            for channel_name, color in [("fg", pair.foreground), ("bg", pair.background)]:
                assert len(color) == 3, (
                    f"{comp_name}.{channel_name} must have 3 components"
                )
                for i, val in enumerate(color):
                    assert 0 <= val <= 255, (
                        f"{comp_name}.{channel_name}[{i}] = {val} out of range"
                    )

    def test_button_focused_fg_matches(self, java_theme, py_theme):
        """button_focused foreground is BLACK in both Java and Python."""
        java_pair = java_theme.get_components()["button_focused"]
        py_fg, py_bg = py_theme.component_colors["button_focused"]

        assert java_pair.foreground == py_fg, (
            f"button_focused fg: Java {java_pair.foreground} vs Python {py_fg}"
        )

    def test_selection_fg_matches(self, java_theme, py_theme):
        """selection foreground is BLACK in both Java and Python."""
        java_pair = java_theme.get_components()["selection"]
        py_fg, py_bg = py_theme.component_colors["selection"]

        assert java_pair.foreground == py_fg


class TestDBase4_3DComponentColors:
    """Compare component colors between Java dbase4-3d.json and Python DBase4_3DTheme."""

    @pytest.fixture
    def java_theme(self):
        return load_theme_from_file(str(JAVA_THEMES_DIR / "dbase4-3d.json"))

    @pytest.fixture
    def py_theme(self):
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme
        return DBase4_3DTheme()

    def test_same_component_keys(self, java_theme, py_theme):
        """Both Java and Python dBASE IV 3D define the same component keys."""
        java_keys = set(java_theme.get_components().keys())
        py_keys = set(py_theme.component_colors.keys())
        assert java_keys == py_keys

    def test_component_colors_are_valid_rgb(self, java_theme):
        """All Java-loaded component colors are valid RGB tuples (0-255)."""
        comps = java_theme.get_components()
        for comp_name, pair in comps.items():
            for channel_name, color in [("fg", pair.foreground), ("bg", pair.background)]:
                assert len(color) == 3
                for val in color:
                    assert 0 <= val <= 255

    def test_background_component_fg_matches(self, java_theme, py_theme):
        """background component foreground is WHITE in both."""
        java_pair = java_theme.get_components()["background"]
        py_fg, _py_bg = py_theme.component_colors["background"]

        assert java_pair.foreground == py_fg, (
            f"background fg: Java {java_pair.foreground} vs Python {py_fg}"
        )

    def test_background_component_bg_matches(self, java_theme, py_theme):
        """background component background is BLUE in both.

        Java ncurses BLUE is (0, 0, 255) while Python uses (0, 0, 238).
        Both are "blue" but differ in exact shade due to palette choices.
        """
        java_pair = java_theme.get_components()["background"]
        _py_fg, py_bg = py_theme.component_colors["background"]

        # Both should be a shade of blue (r=0, g=0, b>200)
        assert java_pair.background[0] == 0
        assert java_pair.background[1] == 0
        assert java_pair.background[2] > 200
        assert py_bg[0] == 0
        assert py_bg[1] == 0
        assert py_bg[2] > 200

    def test_button_fg_is_yellow(self, java_theme, py_theme):
        """button foreground is YELLOW in both Java and Python."""
        java_pair = java_theme.get_components()["button"]
        py_fg, _py_bg = py_theme.component_colors["button"]

        assert java_pair.foreground == py_fg, (
            f"button fg: Java {java_pair.foreground} vs Python {py_fg}"
        )

    def test_disabled_colors_match(self, java_theme, py_theme):
        """disabled component uses BLUE/BLUE in both Java and Python.

        Verifies both fg and bg are blue, though the exact shade may differ.
        """
        java_pair = java_theme.get_components()["disabled"]
        py_fg, py_bg = py_theme.component_colors["disabled"]

        # Both fg and bg should be blue (r=0, g=0, b>200)
        for label, java_color, py_color in [
            ("fg", java_pair.foreground, py_fg),
            ("bg", java_pair.background, py_bg),
        ]:
            assert java_color[0] == 0, f"disabled {label} red channel should be 0"
            assert java_color[1] == 0, f"disabled {label} green channel should be 0"
            assert java_color[2] > 200, f"disabled {label} blue channel should be high"
            assert py_color[0] == 0
            assert py_color[1] == 0
            assert py_color[2] > 200


# ---------------------------------------------------------------------------
# Test 5: Shadow offset consistency
# ---------------------------------------------------------------------------


class TestShadowOffsetConsistency:
    """Verify shadow offsets are consistent between Java and Python 3D themes."""

    def test_borland3d_shadow_offset_x_matches(self):
        """borland3d shadow_offset_x is 2 in both Java and Python."""
        from curses_themes.themes.borland3d import Borland3DTheme

        java_theme = load_theme_from_file(str(JAVA_THEMES_DIR / "borland3d.json"))
        py_theme = Borland3DTheme()

        assert java_theme.shadow_offset_x == py_theme.shadow_offset_x == 2

    def test_borland3d_shadow_offset_y_matches(self):
        """borland3d shadow_offset_y is 1 in both Java and Python."""
        from curses_themes.themes.borland3d import Borland3DTheme

        java_theme = load_theme_from_file(str(JAVA_THEMES_DIR / "borland3d.json"))
        py_theme = Borland3DTheme()

        assert java_theme.shadow_offset_y == py_theme.shadow_offset_y == 1

    def test_dbase4_3d_shadow_offset_x_matches(self):
        """dbase4-3d shadow_offset_x is 2 in both Java and Python."""
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme

        java_theme = load_theme_from_file(str(JAVA_THEMES_DIR / "dbase4-3d.json"))
        py_theme = DBase4_3DTheme()

        assert java_theme.shadow_offset_x == py_theme.shadow_offset_x == 2

    def test_dbase4_3d_shadow_offset_y_matches(self):
        """dbase4-3d shadow_offset_y is 1 in both Java and Python."""
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme

        java_theme = load_theme_from_file(str(JAVA_THEMES_DIR / "dbase4-3d.json"))
        py_theme = DBase4_3DTheme()

        assert java_theme.shadow_offset_y == py_theme.shadow_offset_y == 1

    def test_borland3d_shadow_offset_from_json(self):
        """borland3d.json raw shadow_offset matches converted theme values."""
        raw = _load_java_raw("borland3d.json")
        theme = load_theme_from_file(str(JAVA_THEMES_DIR / "borland3d.json"))

        assert raw["3d"]["shadow_offset"]["x"] == theme.shadow_offset_x
        assert raw["3d"]["shadow_offset"]["y"] == theme.shadow_offset_y

    def test_dbase4_3d_shadow_offset_from_json(self):
        """dbase4-3d.json raw shadow_offset matches converted theme values."""
        raw = _load_java_raw("dbase4-3d.json")
        theme = load_theme_from_file(str(JAVA_THEMES_DIR / "dbase4-3d.json"))

        assert raw["3d"]["shadow_offset"]["x"] == theme.shadow_offset_x
        assert raw["3d"]["shadow_offset"]["y"] == theme.shadow_offset_y


# ---------------------------------------------------------------------------
# Test 6: Full conversion pipeline -- Java JSON to Python ConfigTheme3D
# ---------------------------------------------------------------------------


class TestConversionPipelineIntegrity:
    """Verify the full Java-to-Python conversion pipeline for 3D themes."""

    @pytest.mark.parametrize("filename", ["borland3d.json", "dbase4-3d.json"])
    def test_java_3d_json_roundtrip_has_all_3d_keys(self, filename):
        """Converted Java 3D JSON has shadow, highlight, and lowlight in 3d section."""
        raw = _load_java_raw(filename)
        converted = _convert_java_to_python(raw)

        assert "3d" in converted, f"{filename} missing '3d' section after conversion"
        for key in ("shadow", "highlight", "lowlight"):
            assert key in converted["3d"], (
                f"{filename} missing '3d.{key}' after conversion"
            )

    @pytest.mark.parametrize("filename", ["borland3d.json", "dbase4-3d.json"])
    def test_java_3d_json_has_valid_color_pairs(self, filename):
        """Each 3D color in converted output has foreground and background lists."""
        raw = _load_java_raw(filename)
        converted = _convert_java_to_python(raw)

        for key in ("shadow", "highlight", "lowlight"):
            pair = converted["3d"][key]
            assert "foreground" in pair, f"{filename} 3d.{key} missing foreground"
            assert "background" in pair, f"{filename} 3d.{key} missing background"
            assert len(pair["foreground"]) == 3
            assert len(pair["background"]) == 3

    @pytest.mark.parametrize("filename", ["borland3d.json", "dbase4-3d.json"])
    def test_java_3d_json_has_shadow_offsets(self, filename):
        """Converted Java 3D JSON preserves shadow offset values."""
        raw = _load_java_raw(filename)
        converted = _convert_java_to_python(raw)

        assert "shadow_offset_x" in converted["3d"]
        assert "shadow_offset_y" in converted["3d"]
        assert converted["3d"]["shadow_offset_x"] == raw["3d"]["shadow_offset"]["x"]
        assert converted["3d"]["shadow_offset_y"] == raw["3d"]["shadow_offset"]["y"]

    @pytest.mark.parametrize("filename", ["borland3d.json", "dbase4-3d.json"])
    def test_java_3d_json_has_double_border_chars(self, filename):
        """Converted Java 3D JSON includes double_border_chars from borders.double."""
        raw = _load_java_raw(filename)
        converted = _convert_java_to_python(raw)

        assert "double_border_chars" in converted["3d"]
        assert len(converted["3d"]["double_border_chars"]) == 8

    @pytest.mark.parametrize("filename", ["borland3d.json", "dbase4-3d.json"])
    def test_java_3d_json_has_eight_semantic_colors(self, filename):
        """Converted Java 3D JSON has all 8 required semantic color keys."""
        raw = _load_java_raw(filename)
        converted = _convert_java_to_python(raw)

        required = {"background", "foreground", "primary", "success",
                    "error", "warning", "info", "accent"}
        assert set(converted["colors"].keys()) == required

    @pytest.mark.parametrize("filename", ["borland3d.json", "dbase4-3d.json"])
    def test_full_load_apply_succeeds(self, filename, mock_curses, mock_stdscr):
        """Fully loaded and applied Java 3D theme initializes all color pairs."""
        theme = load_theme_from_file(str(JAVA_THEMES_DIR / filename))
        theme.apply(mock_stdscr)

        assert theme.shadow_color_pair > 0
        assert theme.highlight_color_pair > 0
        assert theme.lowlight_color_pair > 0
        assert theme.colors.primary > 0

    @pytest.mark.parametrize("filename", ["borland3d.json", "dbase4-3d.json"])
    def test_draw_box_3d_succeeds_after_apply(self, filename, mock_curses, mock_stdscr):
        """draw_box_3d works on Java-loaded 3D themes after apply."""
        theme = load_theme_from_file(str(JAVA_THEMES_DIR / filename))
        theme.apply(mock_stdscr)
        theme.draw_box_3d(mock_stdscr, 2, 2, 6, 20, raised=True, title="Test")
        assert mock_stdscr.addstr.called
