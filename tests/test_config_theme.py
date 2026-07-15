#!/usr/bin/env python3
"""Tests for config-driven theme system -- ConfigTheme, ConfigTheme3D, and file parsers.

Covers:
    1. _parse_rgb: list, tuple, string, dict/invalid inputs, out-of-range
    2. _validate_color_pair_dict: valid dict, missing keys, non-dict
    3. validate_config: complete config, missing keys, edge cases
    4. ConfigTheme: init, get_color_map, get_border_chars, component methods
    5. ConfigTheme3D: init, get_shadow/highlight/lowlight_color, custom offsets
    6. load_theme_from_file: JSON, XML, YAML, unsupported extension, missing file
    7. load_xml: attribute-style RGB, meta tag wrapping
    8. Example theme files: solarized.json, ocean.xml, forest.yaml
    9. ThemeManager.load_from_file: integration tests
"""

import json
import os
import xml.etree.ElementTree as ET

import pytest

from curses_themes.config_theme import (
    ConfigTheme,
    ConfigTheme3D,
    _parse_rgb,
    _validate_color_pair_dict,
    _xml_extract_color_pair,
    _xml_extract_rgb,
    load_theme_from_file,
    validate_config,
)
from curses_themes.theme import ColorPair, Theme
from curses_themes.theme3d import Theme3D

# ---------------------------------------------------------------------------
# Shared test data
# ---------------------------------------------------------------------------

MINIMAL_COLORS = {
    "background": [0, 0, 0],
    "foreground": [255, 255, 255],
    "primary": [0, 120, 215],
    "success": [16, 124, 16],
    "error": [232, 17, 35],
    "warning": [193, 156, 0],
    "info": [0, 120, 212],
    "accent": [142, 68, 173],
}

MINIMAL_CONFIG = {
    "name": "Test Theme",
    "colors": dict(MINIMAL_COLORS),
}


def _make_config(
    name="Test Theme",
    description="",
    author="",
    colors=None,
    components=None,
    border_chars=None,
    three_d=None,
):
    """Build a theme config dict for testing."""
    config = {
        "name": name,
        "colors": colors if colors is not None else dict(MINIMAL_COLORS),
    }
    if description:
        config["description"] = description
    if author:
        config["author"] = author
    if components is not None:
        config["components"] = components
    if border_chars is not None:
        config["border_chars"] = border_chars
    if three_d is not None:
        config["3d"] = three_d
    return config


def _make_3d_section(
    shadow_fg=(0, 0, 0),
    shadow_bg=(0, 0, 0),
    highlight_fg=(255, 255, 255),
    highlight_bg=(200, 200, 200),
    lowlight_fg=(64, 64, 64),
    lowlight_bg=(200, 200, 200),
    shadow_offset_x=None,
    shadow_offset_y=None,
):
    """Build a 3D section dict for testing."""
    td = {
        "shadow": {
            "foreground": list(shadow_fg),
            "background": list(shadow_bg),
        },
        "highlight": {
            "foreground": list(highlight_fg),
            "background": list(highlight_bg),
        },
        "lowlight": {
            "foreground": list(lowlight_fg),
            "background": list(lowlight_bg),
        },
    }
    if shadow_offset_x is not None:
        td["shadow_offset_x"] = shadow_offset_x
    if shadow_offset_y is not None:
        td["shadow_offset_y"] = shadow_offset_y
    return td


def _color_pair_dict(fg, bg):
    """Build a component color pair dict."""
    return {
        "foreground": list(fg),
        "background": list(bg),
    }


# ---------------------------------------------------------------------------
# Tests: _parse_rgb
# ---------------------------------------------------------------------------


class TestParseRGB:
    """Tests for the _parse_rgb helper function."""

    def test_parse_from_list(self):
        """Parse RGB from a list of three integers."""
        assert _parse_rgb([128, 64, 32]) == (128, 64, 32)

    def test_parse_from_tuple(self):
        """Parse RGB from a tuple of three integers."""
        assert _parse_rgb((0, 255, 128)) == (0, 255, 128)

    def test_parse_from_string(self):
        """Parse RGB from a comma-separated string."""
        assert _parse_rgb("100, 200, 50") == (100, 200, 50)

    def test_parse_from_string_no_spaces(self):
        """Parse RGB from a comma-separated string without spaces."""
        assert _parse_rgb("100,200,50") == (100, 200, 50)

    def test_boundary_zero(self):
        """Parse RGB with all-zero values (minimum)."""
        assert _parse_rgb([0, 0, 0]) == (0, 0, 0)

    def test_boundary_max(self):
        """Parse RGB with all-255 values (maximum)."""
        assert _parse_rgb([255, 255, 255]) == (255, 255, 255)

    def test_float_values_accepted(self):
        """Float values that are whole numbers are accepted via int()."""
        assert _parse_rgb([128.0, 64.0, 32.0]) == (128, 64, 32)

    def test_wrong_length_list_raises(self):
        """A list with the wrong number of elements raises ValueError."""
        with pytest.raises(ValueError, match="3 components"):
            _parse_rgb([128, 64])

    def test_four_elements_raises(self):
        """A list with four elements raises ValueError."""
        with pytest.raises(ValueError, match="3 components"):
            _parse_rgb([128, 64, 32, 16])

    def test_empty_list_raises(self):
        """An empty list raises ValueError."""
        with pytest.raises(ValueError, match="3 components"):
            _parse_rgb([])

    def test_negative_value_raises(self):
        """A negative component value raises ValueError."""
        with pytest.raises(ValueError, match="0-255"):
            _parse_rgb([128, -1, 32])

    def test_value_above_255_raises(self):
        """A component value above 255 raises ValueError."""
        with pytest.raises(ValueError, match="0-255"):
            _parse_rgb([128, 256, 32])

    def test_invalid_type_dict_raises(self):
        """A dict raises ValueError (not a supported format in new API)."""
        with pytest.raises(ValueError, match=r"list.*tuple.*string"):
            _parse_rgb({"r": 100, "g": 200, "b": 50})

    def test_invalid_type_none_raises(self):
        """None raises ValueError."""
        with pytest.raises(ValueError, match=r"list.*tuple.*string"):
            _parse_rgb(None)

    def test_invalid_type_int_raises(self):
        """A bare integer raises ValueError."""
        with pytest.raises(ValueError, match=r"list.*tuple.*string"):
            _parse_rgb(42)

    def test_string_wrong_count_raises(self):
        """A string with wrong number of comma-separated values raises ValueError."""
        with pytest.raises(ValueError, match="3 comma-separated"):
            _parse_rgb("128,64")

    def test_string_non_integer_raises(self):
        """A string with non-integer values raises ValueError."""
        with pytest.raises(ValueError, match="non-integer"):
            _parse_rgb("abc,def,ghi")

    @pytest.mark.parametrize(
        "rgb,expected",
        [
            ([0, 0, 0], (0, 0, 0)),
            ([255, 255, 255], (255, 255, 255)),
            ([128, 64, 32], (128, 64, 32)),
            ((100, 200, 50), (100, 200, 50)),
            ("10, 20, 30", (10, 20, 30)),
        ],
    )
    def test_valid_rgb_parametrized(self, rgb, expected):
        """Various valid RGB input formats produce correct tuples."""
        assert _parse_rgb(rgb) == expected

    @pytest.mark.parametrize(
        "rgb",
        [
            [-1, 0, 0],
            [0, -1, 0],
            [0, 0, -1],
            [256, 0, 0],
            [0, 256, 0],
            [0, 0, 256],
            [1000, 0, 0],
        ],
    )
    def test_out_of_range_parametrized(self, rgb):
        """Out-of-range RGB values raise ValueError."""
        with pytest.raises(ValueError, match="0-255"):
            _parse_rgb(rgb)


# ---------------------------------------------------------------------------
# Tests: _validate_color_pair_dict
# ---------------------------------------------------------------------------


class TestValidateColorPairDict:
    """Tests for _validate_color_pair_dict helper."""

    def test_valid_pair_dict_no_errors(self):
        """A valid dict with foreground and background produces no errors."""
        errors = _validate_color_pair_dict(
            {"foreground": [255, 255, 255], "background": [0, 0, 0]},
            "test",
        )
        assert errors == []

    def test_missing_foreground(self):
        """Missing foreground key produces an error."""
        errors = _validate_color_pair_dict(
            {"background": [0, 0, 0]},
            "test",
        )
        assert any("foreground" in e for e in errors)

    def test_missing_background(self):
        """Missing background key produces an error."""
        errors = _validate_color_pair_dict(
            {"foreground": [255, 255, 255]},
            "test",
        )
        assert any("background" in e for e in errors)

    def test_non_dict_input(self):
        """Non-dict input produces an error."""
        errors = _validate_color_pair_dict([255, 255, 255], "test")
        assert len(errors) == 1
        assert "dict" in errors[0]

    def test_invalid_rgb_value(self):
        """Invalid RGB values inside the pair produce errors."""
        errors = _validate_color_pair_dict(
            {"foreground": [300, 0, 0], "background": [0, 0, 0]},
            "test",
        )
        assert any("0-255" in e for e in errors)


# ---------------------------------------------------------------------------
# Tests: validate_config
# ---------------------------------------------------------------------------


class TestValidateConfig:
    """Tests for the validate_config function."""

    def test_valid_minimal_config(self):
        """A minimal valid config passes validation without error."""
        validate_config(MINIMAL_CONFIG)

    def test_missing_name_raises(self):
        """Missing name field raises ValueError."""
        config = {"colors": dict(MINIMAL_COLORS)}
        with pytest.raises(ValueError, match="name"):
            validate_config(config)

    def test_empty_name_raises(self):
        """Empty name string raises ValueError."""
        config = {"name": "", "colors": dict(MINIMAL_COLORS)}
        with pytest.raises(ValueError, match="non-empty"):
            validate_config(config)

    def test_missing_colors_raises(self):
        """Missing colors field raises ValueError."""
        config = {"name": "Test"}
        with pytest.raises(ValueError, match="colors"):
            validate_config(config)

    def test_missing_required_color_raises(self):
        """Missing a required color key raises ValueError."""
        colors = dict(MINIMAL_COLORS)
        del colors["primary"]
        config = {"name": "Test", "colors": colors}
        with pytest.raises(ValueError, match="primary"):
            validate_config(config)

    def test_invalid_rgb_in_colors_raises(self):
        """An out-of-range RGB value in colors raises ValueError."""
        colors = dict(MINIMAL_COLORS)
        colors["background"] = [300, 0, 0]
        config = {"name": "Test", "colors": colors}
        with pytest.raises(ValueError, match="0-255"):
            validate_config(config)

    def test_invalid_border_chars_length_raises(self):
        """Border chars with wrong length raises ValueError."""
        config = _make_config(border_chars="ABC")
        with pytest.raises(ValueError, match="8 characters"):
            validate_config(config)

    def test_valid_border_chars_pass(self):
        """Valid 8-character border_chars passes validation."""
        config = _make_config(border_chars="+-+||+-+")
        validate_config(config)

    def test_unknown_component_raises(self):
        """An unknown component name raises ValueError."""
        config = _make_config(
            components={"nonexistent_widget": _color_pair_dict((0, 0, 0), (0, 0, 0))}
        )
        with pytest.raises(ValueError, match="Unknown component"):
            validate_config(config)

    def test_valid_components_pass(self):
        """Valid components pass validation."""
        config = _make_config(
            components={
                "button": _color_pair_dict((255, 255, 255), (0, 120, 215)),
                "border": _color_pair_dict((128, 128, 128), (0, 0, 0)),
            }
        )
        validate_config(config)

    def test_valid_3d_section_pass(self):
        """A valid 3D section passes validation."""
        config = _make_config(three_d=_make_3d_section())
        validate_config(config)

    def test_3d_missing_shadow_raises(self):
        """3D section missing shadow raises ValueError."""
        td = _make_3d_section()
        del td["shadow"]
        config = _make_config(three_d=td)
        with pytest.raises(ValueError, match="shadow"):
            validate_config(config)

    def test_3d_negative_offset_raises(self):
        """Negative shadow offset in 3D section raises ValueError."""
        td = _make_3d_section(shadow_offset_x=-1)
        config = _make_config(three_d=td)
        with pytest.raises(ValueError, match="non-negative"):
            validate_config(config)

    def test_non_dict_config_raises(self):
        """Non-dict input raises ValueError."""
        with pytest.raises(ValueError, match="dict"):
            validate_config("not a dict")

    def test_name_not_string_raises(self):
        """Name that is not a string raises ValueError."""
        config = {"name": 42, "colors": dict(MINIMAL_COLORS)}
        with pytest.raises(ValueError, match="string"):
            validate_config(config)

    def test_colors_not_dict_raises(self):
        """Colors that is not a dict raises ValueError."""
        config = {"name": "Test", "colors": "not a dict"}
        with pytest.raises(ValueError, match="dict"):
            validate_config(config)

    def test_border_chars_not_string_raises(self):
        """border_chars that is not a string raises ValueError."""
        config = _make_config(border_chars=12345678)
        with pytest.raises(ValueError, match="string"):
            validate_config(config)

    def test_components_not_dict_raises(self):
        """components that is not a dict raises ValueError."""
        config = _make_config(components="not a dict")
        with pytest.raises(ValueError, match="dict"):
            validate_config(config)

    def test_3d_not_dict_raises(self):
        """3d section that is not a dict raises ValueError."""
        config = _make_config()
        config["3d"] = "not a dict"
        with pytest.raises(ValueError, match="dict"):
            validate_config(config)

    def test_3d_offset_not_int_raises(self):
        """Shadow offset that is not an integer raises ValueError."""
        td = _make_3d_section()
        td["shadow_offset_x"] = "not_int"
        config = _make_config(three_d=td)
        with pytest.raises(ValueError, match="integer"):
            validate_config(config)

    def test_3d_double_border_chars_not_string_raises(self):
        """double_border_chars that is not a string raises ValueError."""
        td = _make_3d_section()
        td["double_border_chars"] = 12345678
        config = _make_config(three_d=td)
        with pytest.raises(ValueError, match="string"):
            validate_config(config)

    def test_3d_double_border_chars_wrong_length_raises(self):
        """double_border_chars with wrong length raises ValueError."""
        td = _make_3d_section()
        td["double_border_chars"] = "ABC"
        config = _make_config(three_d=td)
        with pytest.raises(ValueError, match="8 characters"):
            validate_config(config)

    def test_3d_valid_double_border_chars(self):
        """Valid double_border_chars passes validation."""
        td = _make_3d_section()
        td["double_border_chars"] = "+-+||+-+"
        config = _make_config(three_d=td)
        validate_config(config)

    @pytest.mark.parametrize(
        "missing_color",
        [
            "background",
            "foreground",
            "primary",
            "success",
            "error",
            "warning",
            "info",
            "accent",
        ],
    )
    def test_each_required_color_missing(self, missing_color):
        """Each individual missing required color raises ValueError."""
        colors = dict(MINIMAL_COLORS)
        del colors[missing_color]
        config = {"name": "Test", "colors": colors}
        with pytest.raises(ValueError, match=missing_color):
            validate_config(config)


# ---------------------------------------------------------------------------
# Tests: ConfigTheme
# ---------------------------------------------------------------------------


class TestConfigThemeInit:
    """Tests for ConfigTheme initialization."""

    def test_minimal_config(self):
        """Create a ConfigTheme with only required fields."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        assert theme.name == "Test Theme"
        assert theme.description == ""
        assert theme.author == ""

    def test_full_metadata(self):
        """Create a ConfigTheme with all metadata fields."""
        config = _make_config(
            name="Full Theme",
            description="A fully described theme",
            author="Jane Doe",
        )
        theme = ConfigTheme(config)
        assert theme.name == "Full Theme"
        assert theme.description == "A fully described theme"
        assert theme.author == "Jane Doe"

    def test_missing_required_color_raises(self):
        """Missing required color raises ValueError."""
        colors = dict(MINIMAL_COLORS)
        del colors["error"]
        config = {"name": "Bad", "colors": colors}
        with pytest.raises(ValueError, match="error"):
            ConfigTheme(config)

    def test_is_theme_subclass(self):
        """ConfigTheme is a proper Theme subclass."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        assert isinstance(theme, Theme)

    def test_repr(self):
        """__repr__ includes name and author."""
        config = _make_config(name="MyTheme", author="Author")
        theme = ConfigTheme(config)
        r = repr(theme)
        assert "MyTheme" in r
        assert "Author" in r


class TestConfigThemeColorMap:
    """Tests for ConfigTheme.get_color_map()."""

    def test_returns_correct_tuples(self):
        """get_color_map returns correct (r, g, b) tuples."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        color_map = theme.get_color_map()
        assert color_map["background"] == (0, 0, 0)
        assert color_map["foreground"] == (255, 255, 255)
        assert color_map["primary"] == (0, 120, 215)

    def test_returns_all_8_keys(self):
        """get_color_map returns all 8 required keys."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        color_map = theme.get_color_map()
        expected = {
            "background",
            "foreground",
            "primary",
            "success",
            "error",
            "warning",
            "info",
            "accent",
        }
        assert set(color_map.keys()) == expected


class TestConfigThemeBorderChars:
    """Tests for ConfigTheme border character handling."""

    def test_default_border_chars(self):
        """Default border chars are ASCII box characters."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        assert theme.get_border_chars() == "+-+||+-+"

    def test_custom_border_chars(self):
        """Custom border characters are returned correctly."""
        config = _make_config(border_chars="+-+||+-+")
        theme = ConfigTheme(config)
        assert theme.get_border_chars() == "+-+||+-+"

    def test_unicode_border_chars(self):
        """Unicode box-drawing characters work correctly."""
        config = _make_config(border_chars="┌─┐││└─┘")
        theme = ConfigTheme(config)
        assert len(theme.get_border_chars()) == 8


class TestConfigThemeComponents:
    """Tests for ConfigTheme component color methods."""

    def test_no_components_returns_none(self):
        """All component methods return None when not configured."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        assert theme.get_background() is None
        assert theme.get_button() is None
        assert theme.get_button_focused() is None
        assert theme.get_text_input() is None
        assert theme.get_border() is None
        assert theme.get_selection() is None
        assert theme.get_disabled() is None

    def test_configured_button_returns_color_pair(self):
        """A configured button component returns ColorPair."""
        config = _make_config(
            components={
                "button": _color_pair_dict((255, 255, 255), (0, 120, 215)),
            }
        )
        theme = ConfigTheme(config)
        result = theme.get_button()
        assert isinstance(result, ColorPair)
        assert result.foreground == (255, 255, 255)
        assert result.background == (0, 120, 215)

    def test_all_components_configured(self):
        """Theme with all component colors configured returns correct values."""
        comps = {
            "background": _color_pair_dict((200, 200, 200), (0, 0, 0)),
            "button": _color_pair_dict((255, 255, 255), (0, 120, 215)),
            "button_focused": _color_pair_dict((0, 0, 0), (255, 255, 0)),
            "text_input": _color_pair_dict((0, 0, 0), (255, 255, 255)),
            "border": _color_pair_dict((128, 128, 128), (0, 0, 0)),
            "selection": _color_pair_dict((255, 255, 255), (0, 0, 128)),
            "disabled": _color_pair_dict((128, 128, 128), (64, 64, 64)),
        }
        config = _make_config(components=comps)
        theme = ConfigTheme(config)

        assert theme.get_background() is not None
        assert theme.get_button().foreground == (255, 255, 255)
        assert theme.get_button_focused().foreground == (0, 0, 0)
        assert theme.get_text_input().background == (255, 255, 255)
        assert theme.get_border() is not None
        assert theme.get_selection() is not None
        assert theme.get_disabled() is not None

    def test_partial_components(self):
        """Theme with only some components: configured ones return values, others None."""
        config = _make_config(
            components={
                "button": _color_pair_dict((255, 255, 255), (0, 120, 215)),
            }
        )
        theme = ConfigTheme(config)
        assert theme.get_button() is not None
        assert theme.get_button_focused() is None
        assert theme.get_background() is None


class TestConfigThemeApply:
    """Tests for ConfigTheme.apply() with mock curses."""

    def test_apply_initializes_colors(self, mock_curses, mock_stdscr):
        """apply() initializes semantic colors."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        theme.apply(mock_stdscr)
        assert theme.colors is not None
        assert theme.colors.primary > 0

    def test_apply_initializes_components(self, mock_curses, mock_stdscr):
        """apply() initializes component colors."""
        config = _make_config(
            components={
                "button": _color_pair_dict((255, 255, 255), (0, 120, 215)),
            }
        )
        theme = ConfigTheme(config)
        theme.apply(mock_stdscr)
        assert theme.components is not None
        assert theme.components.button > 0

    def test_apply_sets_screen_background(self, mock_curses, mock_stdscr):
        """apply() sets the screen background."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        theme.apply(mock_stdscr)
        assert mock_stdscr.bkgd.called

    def test_draw_box_after_apply(self, mock_curses, mock_stdscr):
        """Drawing a box works after applying a config theme."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        theme.apply(mock_stdscr)
        theme.draw_box(mock_stdscr, 2, 2, 5, 20, title="Config Box")
        assert mock_stdscr.addstr.called

    def test_colors_before_apply_raises(self):
        """Accessing colors before apply raises RuntimeError."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        with pytest.raises(RuntimeError):
            _ = theme.colors

    def test_components_before_apply_raises(self):
        """Accessing components before apply raises RuntimeError."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        with pytest.raises(RuntimeError):
            _ = theme.components


# ---------------------------------------------------------------------------
# Tests: ConfigTheme3D
# ---------------------------------------------------------------------------


class TestConfigTheme3DInit:
    """Tests for ConfigTheme3D initialization."""

    def test_minimal_3d_config(self):
        """Create a ConfigTheme3D with required 3D properties."""
        config = _make_config(three_d=_make_3d_section())
        theme = ConfigTheme3D(config)
        assert theme.name == "Test Theme"
        assert isinstance(theme, Theme3D)
        assert isinstance(theme, Theme)

    def test_3d_color_methods(self):
        """3D color methods return ColorPair with correct values."""
        config = _make_config(three_d=_make_3d_section())
        theme = ConfigTheme3D(config)

        shadow = theme.get_shadow_color()
        assert isinstance(shadow, ColorPair)
        assert shadow.foreground == (0, 0, 0)
        assert shadow.background == (0, 0, 0)

        highlight = theme.get_highlight_color()
        assert highlight.foreground == (255, 255, 255)
        assert highlight.background == (200, 200, 200)

        lowlight = theme.get_lowlight_color()
        assert lowlight.foreground == (64, 64, 64)
        assert lowlight.background == (200, 200, 200)

    def test_default_shadow_offsets(self):
        """Default shadow offsets are 2 and 1."""
        config = _make_config(three_d=_make_3d_section())
        theme = ConfigTheme3D(config)
        assert theme.shadow_offset_x == 2
        assert theme.shadow_offset_y == 1

    def test_custom_shadow_offsets(self):
        """Custom shadow offsets from config are applied."""
        config = _make_config(
            three_d=_make_3d_section(shadow_offset_x=4, shadow_offset_y=3)
        )
        theme = ConfigTheme3D(config)
        assert theme.shadow_offset_x == 4
        assert theme.shadow_offset_y == 3

    def test_missing_3d_section_raises(self):
        """Missing 3D section raises ValueError."""
        with pytest.raises(ValueError, match="3d"):
            ConfigTheme3D(MINIMAL_CONFIG)

    def test_3d_theme_color_map(self):
        """ConfigTheme3D inherits base color map behavior."""
        config = _make_config(three_d=_make_3d_section())
        theme = ConfigTheme3D(config)
        color_map = theme.get_color_map()
        assert color_map["background"] == (0, 0, 0)
        assert color_map["primary"] == (0, 120, 215)
        assert len(color_map) == 8

    def test_3d_theme_with_components(self):
        """ConfigTheme3D with component colors configured."""
        config = _make_config(
            components={
                "button": _color_pair_dict((255, 255, 255), (0, 120, 215)),
            },
            three_d=_make_3d_section(),
        )
        theme = ConfigTheme3D(config)
        assert theme.get_button() is not None
        assert theme.get_button_focused() is None

    def test_3d_no_components_all_none(self):
        """A 3D theme with no components returns None for all."""
        config = _make_config(three_d=_make_3d_section())
        theme = ConfigTheme3D(config)
        assert theme.get_background() is None
        assert theme.get_button() is None
        assert theme.get_button_focused() is None
        assert theme.get_text_input() is None
        assert theme.get_border() is None
        assert theme.get_selection() is None
        assert theme.get_disabled() is None

    def test_3d_all_components_configured(self):
        """A 3D theme with all component colors returns correct values."""
        comps = {
            "background": _color_pair_dict((200, 200, 200), (0, 0, 0)),
            "button": _color_pair_dict((255, 255, 255), (0, 120, 215)),
            "button_focused": _color_pair_dict((0, 0, 0), (255, 255, 0)),
            "text_input": _color_pair_dict((0, 0, 0), (255, 255, 255)),
            "border": _color_pair_dict((128, 128, 128), (0, 0, 0)),
            "selection": _color_pair_dict((255, 255, 255), (0, 0, 128)),
            "disabled": _color_pair_dict((128, 128, 128), (64, 64, 64)),
        }
        config = _make_config(components=comps, three_d=_make_3d_section())
        theme = ConfigTheme3D(config)
        assert theme.get_background() is not None
        assert theme.get_button() is not None
        assert theme.get_button_focused() is not None
        assert theme.get_text_input() is not None
        assert theme.get_border() is not None
        assert theme.get_selection() is not None
        assert theme.get_disabled() is not None

    def test_3d_theme_border_chars(self):
        """ConfigTheme3D with custom border characters."""
        config = _make_config(
            border_chars="+-+||+-+",
            three_d=_make_3d_section(),
        )
        theme = ConfigTheme3D(config)
        assert theme.get_border_chars() == "+-+||+-+"

    def test_3d_theme_default_border_chars(self):
        """ConfigTheme3D default border characters."""
        config = _make_config(three_d=_make_3d_section())
        theme = ConfigTheme3D(config)
        assert theme.get_border_chars() == "+-+||+-+"

    def test_3d_theme_double_border_chars(self):
        """ConfigTheme3D returns default double border chars."""
        config = _make_config(three_d=_make_3d_section())
        theme = ConfigTheme3D(config)
        result = theme.get_double_border_chars()
        assert len(result) == 8

    def test_3d_theme_repr(self):
        """__repr__ includes name and shadow offset."""
        config = _make_config(
            name="My3D",
            three_d=_make_3d_section(shadow_offset_x=3, shadow_offset_y=2),
        )
        theme = ConfigTheme3D(config)
        r = repr(theme)
        assert "My3D" in r
        assert "3" in r
        assert "2" in r


class TestConfigTheme3DApply:
    """Tests for ConfigTheme3D.apply() with mock curses."""

    def test_apply_initializes_3d_colors(self, mock_curses, mock_stdscr):
        """apply() initializes 3D color pairs."""
        config = _make_config(three_d=_make_3d_section())
        theme = ConfigTheme3D(config)
        theme.apply(mock_stdscr)

        assert theme.shadow_color_pair > 0
        assert theme.highlight_color_pair > 0
        assert theme.lowlight_color_pair > 0

    def test_apply_initializes_semantic_colors(self, mock_curses, mock_stdscr):
        """apply() also initializes semantic colors from base."""
        config = _make_config(three_d=_make_3d_section())
        theme = ConfigTheme3D(config)
        theme.apply(mock_stdscr)
        assert theme.colors.primary > 0
        assert theme.colors.success > 0

    def test_draw_box_3d_after_apply(self, mock_curses, mock_stdscr):
        """Drawing a 3D box works after applying theme."""
        config = _make_config(three_d=_make_3d_section())
        theme = ConfigTheme3D(config)
        theme.apply(mock_stdscr)
        theme.draw_box_3d(mock_stdscr, 2, 2, 5, 20, raised=True, title="3D Box")
        assert mock_stdscr.addstr.called


# ---------------------------------------------------------------------------
# Tests: JSON parsing
# ---------------------------------------------------------------------------


class TestJSONParser:
    """Tests for JSON theme file loading."""

    def test_load_json_from_file(self, tmp_path):
        """Load a theme from a JSON file."""
        config = _make_config(name="JSON File Theme")
        json_path = tmp_path / "theme.json"
        json_path.write_text(json.dumps(config), encoding="utf-8")

        theme = load_theme_from_file(str(json_path))
        assert isinstance(theme, ConfigTheme)
        assert theme.name == "JSON File Theme"

    def test_load_json_with_all_fields(self, tmp_path):
        """Load a JSON file with all optional fields."""
        config = _make_config(
            name="Full JSON",
            description="Fully specified JSON theme",
            author="JSON Author",
            border_chars="+-+||+-+",
            components={
                "button": _color_pair_dict((255, 255, 255), (0, 120, 215)),
                "border": _color_pair_dict((128, 128, 128), (0, 0, 0)),
            },
        )
        json_path = tmp_path / "full_theme.json"
        json_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

        theme = load_theme_from_file(str(json_path))
        assert theme.name == "Full JSON"
        assert theme.description == "Fully specified JSON theme"
        assert theme.author == "JSON Author"
        assert theme.get_border_chars() == "+-+||+-+"
        assert theme.get_button() is not None
        assert theme.get_border() is not None

    def test_load_json_3d_theme(self, tmp_path):
        """Load a 3D theme from JSON."""
        config = _make_config(
            name="JSON 3D",
            three_d=_make_3d_section(),
        )
        json_path = tmp_path / "3d_theme.json"
        json_path.write_text(json.dumps(config), encoding="utf-8")

        theme = load_theme_from_file(str(json_path))
        assert isinstance(theme, ConfigTheme3D)
        assert theme.get_shadow_color().foreground == (0, 0, 0)

    def test_load_json_theme3d_key_normalized(self, tmp_path):
        """JSON 'theme3d' key is normalized to '3d'."""
        config = _make_config(name="Normalized 3D")
        config["theme3d"] = _make_3d_section()
        json_path = tmp_path / "theme3d_key.json"
        json_path.write_text(json.dumps(config), encoding="utf-8")

        theme = load_theme_from_file(str(json_path))
        assert isinstance(theme, ConfigTheme3D)

    def test_load_json_invalid_json_raises(self, tmp_path):
        """Invalid JSON file raises an error."""
        json_path = tmp_path / "bad.json"
        json_path.write_text("not valid json {{{", encoding="utf-8")

        with pytest.raises(json.JSONDecodeError):
            load_theme_from_file(str(json_path))

    def test_load_json_missing_colors_raises(self, tmp_path):
        """JSON file missing colors raises ValueError."""
        config = {"name": "No Colors"}
        json_path = tmp_path / "no_colors.json"
        json_path.write_text(json.dumps(config), encoding="utf-8")

        with pytest.raises(ValueError, match="colors"):
            load_theme_from_file(str(json_path))

    def test_load_json_nonexistent_file_raises(self):
        """Loading a nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_theme_from_file("/tmp/does_not_exist_theme.json")


# ---------------------------------------------------------------------------
# Tests: XML parsing
# ---------------------------------------------------------------------------


class TestXMLParser:
    """Tests for XML theme file loading."""

    def _write_xml_theme(self, tmp_path, filename, xml_content):
        """Write XML content to a temp file and return the path."""
        xml_path = tmp_path / filename
        xml_path.write_text(xml_content, encoding="utf-8")
        return str(xml_path)

    def test_load_xml_basic(self, tmp_path):
        """Load a basic theme from an XML file."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <theme>
            <meta>
                <name>XML Theme</name>
                <description>Test XML theme</description>
                <author>Tester</author>
            </meta>
            <colors>
                <background r="0" g="0" b="0" />
                <foreground r="255" g="255" b="255" />
                <primary r="0" g="120" b="215" />
                <success r="16" g="124" b="16" />
                <error r="232" g="17" b="35" />
                <warning r="193" g="156" b="0" />
                <info r="0" g="120" b="212" />
                <accent r="142" g="68" b="173" />
            </colors>
        </theme>"""
        path = self._write_xml_theme(tmp_path, "basic.xml", xml)
        theme = load_theme_from_file(path)
        assert isinstance(theme, ConfigTheme)
        assert theme.name == "XML Theme"
        assert theme.description == "Test XML theme"
        assert theme.author == "Tester"

    def test_load_xml_attribute_style_rgb(self, tmp_path):
        """XML with r/g/b as element attributes (attribute-style RGB)."""
        xml = """<theme>
            <meta><name>Attr RGB</name></meta>
            <colors>
                <background r="10" g="25" b="47" />
                <foreground r="176" g="210" b="224" />
                <primary r="30" g="120" b="180" />
                <success r="46" g="174" b="120" />
                <error r="210" g="60" b="70" />
                <warning r="224" g="175" b="50" />
                <info r="64" g="190" b="200" />
                <accent r="120" g="85" b="195" />
            </colors>
        </theme>"""
        path = self._write_xml_theme(tmp_path, "attr.xml", xml)
        theme = load_theme_from_file(path)
        color_map = theme.get_color_map()
        assert color_map["background"] == (10, 25, 47)
        assert color_map["foreground"] == (176, 210, 224)

    def test_load_xml_meta_tag_wrapping(self, tmp_path):
        """XML with name/description/author inside a <meta> tag."""
        xml = """<theme type="basic">
            <meta>
                <name>Meta Theme</name>
                <description>Wrapped in meta</description>
                <author>Meta Author</author>
            </meta>
            <colors>
                <background r="0" g="0" b="0" />
                <foreground r="255" g="255" b="255" />
                <primary r="0" g="120" b="215" />
                <success r="16" g="124" b="16" />
                <error r="232" g="17" b="35" />
                <warning r="193" g="156" b="0" />
                <info r="0" g="120" b="212" />
                <accent r="142" g="68" b="173" />
            </colors>
        </theme>"""
        path = self._write_xml_theme(tmp_path, "meta.xml", xml)
        theme = load_theme_from_file(path)
        assert theme.name == "Meta Theme"
        assert theme.description == "Wrapped in meta"
        assert theme.author == "Meta Author"

    def test_load_xml_with_components(self, tmp_path):
        """Load XML with component color pairs."""
        xml = """<theme>
            <meta><name>Comp XML</name></meta>
            <colors>
                <background r="0" g="0" b="0" />
                <foreground r="255" g="255" b="255" />
                <primary r="0" g="120" b="215" />
                <success r="16" g="124" b="16" />
                <error r="232" g="17" b="35" />
                <warning r="193" g="156" b="0" />
                <info r="0" g="120" b="212" />
                <accent r="142" g="68" b="173" />
            </colors>
            <components>
                <button>
                    <foreground r="255" g="255" b="255" />
                    <background r="0" g="120" b="215" />
                </button>
            </components>
        </theme>"""
        path = self._write_xml_theme(tmp_path, "comp.xml", xml)
        theme = load_theme_from_file(path)
        assert theme.get_button() is not None
        assert theme.get_button().foreground == (255, 255, 255)

    def test_load_xml_with_border_chars(self, tmp_path):
        """Load XML with custom border characters."""
        xml = """<theme>
            <meta><name>Border XML</name></meta>
            <colors>
                <background r="0" g="0" b="0" />
                <foreground r="255" g="255" b="255" />
                <primary r="0" g="120" b="215" />
                <success r="16" g="124" b="16" />
                <error r="232" g="17" b="35" />
                <warning r="193" g="156" b="0" />
                <info r="0" g="120" b="212" />
                <accent r="142" g="68" b="173" />
            </colors>
            <border_chars>+-+||+-+</border_chars>
        </theme>"""
        path = self._write_xml_theme(tmp_path, "border.xml", xml)
        theme = load_theme_from_file(path)
        assert theme.get_border_chars() == "+-+||+-+"

    def test_load_xml_3d_theme(self, tmp_path):
        """Load a 3D theme from XML with effects3d section."""
        xml = """<theme>
            <meta><name>XML 3D</name></meta>
            <colors>
                <background r="0" g="0" b="0" />
                <foreground r="255" g="255" b="255" />
                <primary r="0" g="120" b="215" />
                <success r="16" g="124" b="16" />
                <error r="232" g="17" b="35" />
                <warning r="193" g="156" b="0" />
                <info r="0" g="120" b="212" />
                <accent r="142" g="68" b="173" />
            </colors>
            <effects3d>
                <shadow>
                    <foreground r="0" g="0" b="0" />
                    <background r="0" g="0" b="0" />
                </shadow>
                <highlight>
                    <foreground r="255" g="255" b="255" />
                    <background r="200" g="200" b="200" />
                </highlight>
                <lowlight>
                    <foreground r="64" g="64" b="64" />
                    <background r="200" g="200" b="200" />
                </lowlight>
                <shadow_offset x="3" y="2" />
            </effects3d>
        </theme>"""
        path = self._write_xml_theme(tmp_path, "3d.xml", xml)
        theme = load_theme_from_file(path)
        assert isinstance(theme, ConfigTheme3D)
        assert theme.shadow_offset_x == 3
        assert theme.shadow_offset_y == 2

    def test_load_xml_rgb_missing_attribute_raises(self, tmp_path):
        """XML with missing RGB attribute raises ValueError."""
        xml = """<theme>
            <meta><name>Bad RGB</name></meta>
            <colors>
                <background r="0" g="0" />
            </colors>
        </theme>"""
        path = self._write_xml_theme(tmp_path, "bad_rgb.xml", xml)
        with pytest.raises(ValueError, match="RGB"):
            load_theme_from_file(path)

    def test_load_xml_no_meta_no_colors(self, tmp_path):
        """XML with no meta and no colors loads an empty config dict."""
        xml = """<theme></theme>"""
        path = self._write_xml_theme(tmp_path, "empty.xml", xml)
        # This should parse but fail validation when creating a theme
        with pytest.raises(ValueError, match="name"):
            load_theme_from_file(path)

    def test_load_xml_3d_with_double_border_chars(self, tmp_path):
        """Load XML 3D theme with double_border_chars inside effects3d."""
        xml = """<theme>
            <meta><name>3D DBC</name></meta>
            <colors>
                <background r="0" g="0" b="0" />
                <foreground r="255" g="255" b="255" />
                <primary r="0" g="120" b="215" />
                <success r="16" g="124" b="16" />
                <error r="232" g="17" b="35" />
                <warning r="193" g="156" b="0" />
                <info r="0" g="120" b="212" />
                <accent r="142" g="68" b="173" />
            </colors>
            <effects3d>
                <shadow>
                    <foreground r="0" g="0" b="0" />
                    <background r="0" g="0" b="0" />
                </shadow>
                <highlight>
                    <foreground r="255" g="255" b="255" />
                    <background r="200" g="200" b="200" />
                </highlight>
                <lowlight>
                    <foreground r="64" g="64" b="64" />
                    <background r="200" g="200" b="200" />
                </lowlight>
                <double_border_chars>+-+||+-+</double_border_chars>
            </effects3d>
        </theme>"""
        path = self._write_xml_theme(tmp_path, "3d_dbc.xml", xml)
        theme = load_theme_from_file(path)
        assert isinstance(theme, ConfigTheme3D)
        assert theme.get_double_border_chars() == "+-+||+-+"

    def test_load_xml_3d_no_shadow_offset(self, tmp_path):
        """Load XML 3D theme without shadow_offset element (uses defaults)."""
        xml = """<theme>
            <meta><name>3D NoOffset</name></meta>
            <colors>
                <background r="0" g="0" b="0" />
                <foreground r="255" g="255" b="255" />
                <primary r="0" g="120" b="215" />
                <success r="16" g="124" b="16" />
                <error r="232" g="17" b="35" />
                <warning r="193" g="156" b="0" />
                <info r="0" g="120" b="212" />
                <accent r="142" g="68" b="173" />
            </colors>
            <effects3d>
                <shadow>
                    <foreground r="0" g="0" b="0" />
                    <background r="0" g="0" b="0" />
                </shadow>
                <highlight>
                    <foreground r="255" g="255" b="255" />
                    <background r="200" g="200" b="200" />
                </highlight>
                <lowlight>
                    <foreground r="64" g="64" b="64" />
                    <background r="200" g="200" b="200" />
                </lowlight>
            </effects3d>
        </theme>"""
        path = self._write_xml_theme(tmp_path, "3d_nooffset.xml", xml)
        theme = load_theme_from_file(path)
        assert isinstance(theme, ConfigTheme3D)
        assert theme.shadow_offset_x == 2  # default
        assert theme.shadow_offset_y == 1  # default

    def test_load_xml_color_pair_partial_fg_only(self, tmp_path):
        """XML component with only foreground still loads (bg missing from pair)."""
        xml = """<theme>
            <meta><name>Partial FG</name></meta>
            <colors>
                <background r="0" g="0" b="0" />
                <foreground r="255" g="255" b="255" />
                <primary r="0" g="120" b="215" />
                <success r="16" g="124" b="16" />
                <error r="232" g="17" b="35" />
                <warning r="193" g="156" b="0" />
                <info r="0" g="120" b="212" />
                <accent r="142" g="68" b="173" />
            </colors>
            <components>
                <button>
                    <foreground r="255" g="255" b="255" />
                </button>
            </components>
        </theme>"""
        path = self._write_xml_theme(tmp_path, "partial.xml", xml)
        # This should parse XML but fail validation due to missing background
        with pytest.raises(ValueError, match="background"):
            load_theme_from_file(path)

    def test_load_xml_nonexistent_file_raises(self):
        """Loading a nonexistent XML file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_theme_from_file("/tmp/does_not_exist_theme.xml")


# ---------------------------------------------------------------------------
# Tests: XML helper functions
# ---------------------------------------------------------------------------


class TestXMLExtractRGB:
    """Tests for _xml_extract_rgb helper."""

    def test_valid_attributes(self):
        """Extract RGB from valid r/g/b attributes."""
        elem = ET.fromstring('<color r="10" g="20" b="30" />')
        result = _xml_extract_rgb(elem)
        assert result == [10, 20, 30]

    def test_missing_attribute_raises(self):
        """Missing RGB attribute raises ValueError."""
        elem = ET.fromstring('<color r="10" g="20" />')
        with pytest.raises(ValueError, match="missing RGB"):
            _xml_extract_rgb(elem)


class TestXMLExtractColorPair:
    """Tests for _xml_extract_color_pair helper."""

    def test_valid_color_pair(self):
        """Extract a valid color pair from XML element."""
        xml = '<button><foreground r="255" g="255" b="255"/><background r="0" g="0" b="0"/></button>'
        elem = ET.fromstring(xml)
        result = _xml_extract_color_pair(elem)
        assert result["foreground"] == [255, 255, 255]
        assert result["background"] == [0, 0, 0]

    def test_partial_color_pair(self):
        """Color pair with only foreground returns partial dict."""
        xml = '<button><foreground r="255" g="255" b="255"/></button>'
        elem = ET.fromstring(xml)
        result = _xml_extract_color_pair(elem)
        assert "foreground" in result
        assert "background" not in result


# ---------------------------------------------------------------------------
# Tests: YAML parsing
# ---------------------------------------------------------------------------


class TestYAMLParser:
    """Tests for YAML theme file loading."""

    @pytest.fixture
    def yaml_available(self):
        """Skip tests if PyYAML is not installed."""
        try:
            import yaml  # noqa: F401

            return True
        except ImportError:
            pytest.skip("PyYAML not installed")

    def test_load_yaml_from_file(self, tmp_path, yaml_available):
        """Load a theme from a YAML file."""
        import yaml

        config = _make_config(name="YAML Theme")
        yaml_path = tmp_path / "theme.yaml"
        yaml_path.write_text(yaml.dump(config), encoding="utf-8")

        theme = load_theme_from_file(str(yaml_path))
        assert isinstance(theme, ConfigTheme)
        assert theme.name == "YAML Theme"

    def test_load_yml_extension(self, tmp_path, yaml_available):
        """Load a theme from a .yml file (alternate extension)."""
        import yaml

        config = _make_config(name="YML Theme")
        yml_path = tmp_path / "theme.yml"
        yml_path.write_text(yaml.dump(config), encoding="utf-8")

        theme = load_theme_from_file(str(yml_path))
        assert isinstance(theme, ConfigTheme)
        assert theme.name == "YML Theme"

    def test_load_yaml_3d_theme(self, tmp_path, yaml_available):
        """Load a 3D theme from YAML."""
        import yaml

        config = _make_config(name="YAML 3D", three_d=_make_3d_section())
        yaml_path = tmp_path / "3d_theme.yaml"
        yaml_path.write_text(yaml.dump(config), encoding="utf-8")

        theme = load_theme_from_file(str(yaml_path))
        assert isinstance(theme, ConfigTheme3D)

    def test_load_yaml_with_components(self, tmp_path, yaml_available):
        """Load YAML with component colors."""
        import yaml

        config = _make_config(
            name="YAML Components",
            components={
                "button": _color_pair_dict((255, 255, 255), (0, 120, 215)),
            },
        )
        yaml_path = tmp_path / "components.yaml"
        yaml_path.write_text(yaml.dump(config), encoding="utf-8")

        theme = load_theme_from_file(str(yaml_path))
        assert theme.get_button() is not None

    def test_yaml_import_error_message(self, tmp_path, monkeypatch):
        """Importing YAML without PyYAML gives a helpful message."""
        import builtins

        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "yaml":
                raise ImportError("No module named 'yaml'")
            return real_import(name, *args, **kwargs)

        yaml_path = tmp_path / "theme.yaml"
        yaml_path.write_text("name: test", encoding="utf-8")

        monkeypatch.setattr(builtins, "__import__", mock_import)

        with pytest.raises(ImportError, match="PyYAML"):
            load_theme_from_file(str(yaml_path))

    def test_yaml_theme3d_key_normalized(self, tmp_path, yaml_available):
        """YAML 'theme3d' key is normalized to '3d'."""
        import yaml

        config = _make_config(name="Normalized 3D")
        config["theme3d"] = _make_3d_section()
        yaml_path = tmp_path / "theme3d_key.yaml"
        yaml_path.write_text(yaml.dump(config), encoding="utf-8")

        theme = load_theme_from_file(str(yaml_path))
        assert isinstance(theme, ConfigTheme3D)


# ---------------------------------------------------------------------------
# Tests: load_theme_from_file format detection
# ---------------------------------------------------------------------------


class TestLoadThemeFromFileFormatDetection:
    """Tests for auto-detection of file format by extension."""

    def test_json_extension_detected(self, tmp_path):
        """The .json extension is properly detected."""
        config = _make_config(name="JSON Detect")
        path = tmp_path / "test.json"
        path.write_text(json.dumps(config), encoding="utf-8")

        theme = load_theme_from_file(str(path))
        assert theme.name == "JSON Detect"

    def test_xml_extension_detected(self, tmp_path):
        """The .xml extension is properly detected."""
        xml = """<theme>
            <meta><name>XML Detect</name></meta>
            <colors>
                <background r="0" g="0" b="0" />
                <foreground r="255" g="255" b="255" />
                <primary r="0" g="120" b="215" />
                <success r="16" g="124" b="16" />
                <error r="232" g="17" b="35" />
                <warning r="193" g="156" b="0" />
                <info r="0" g="120" b="212" />
                <accent r="142" g="68" b="173" />
            </colors>
        </theme>"""
        path = tmp_path / "test.xml"
        path.write_text(xml, encoding="utf-8")

        theme = load_theme_from_file(str(path))
        assert theme.name == "XML Detect"

    def test_unsupported_extension_raises(self, tmp_path):
        """An unsupported file extension raises ValueError."""
        path = tmp_path / "theme.txt"
        path.write_text("not a theme", encoding="utf-8")

        with pytest.raises(ValueError, match="Unsupported"):
            load_theme_from_file(str(path))

    def test_unsupported_extension_ini_raises(self, tmp_path):
        """The .ini extension raises ValueError."""
        path = tmp_path / "theme.ini"
        path.write_text("[theme]\nname=test", encoding="utf-8")

        with pytest.raises(ValueError, match="Unsupported"):
            load_theme_from_file(str(path))

    def test_nonexistent_file_raises(self):
        """A nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_theme_from_file("/tmp/absolutely_does_not_exist.json")

    def test_case_insensitive_extension(self, tmp_path):
        """Extension detection is case-insensitive."""
        config = _make_config(name="Upper JSON")
        path = tmp_path / "test.JSON"
        path.write_text(json.dumps(config), encoding="utf-8")

        theme = load_theme_from_file(str(path))
        assert theme.name == "Upper JSON"


# ---------------------------------------------------------------------------
# Tests: Loading actual example theme files
# ---------------------------------------------------------------------------


class TestExampleThemeFiles:
    """Tests loading the actual example theme files shipped with the project."""

    @pytest.fixture
    def examples_dir(self):
        """Return the path to the examples/themes directory."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, "examples", "themes")

    def test_load_solarized_json(self, examples_dir):
        """Load the solarized.json example and verify key properties."""
        path = os.path.join(examples_dir, "solarized.json")
        theme = load_theme_from_file(path)

        assert isinstance(theme, ConfigTheme)
        assert theme.name == "Solarized Dark"
        assert theme.author == "FlossWare"
        assert theme.description != ""

        color_map = theme.get_color_map()
        assert color_map["background"] == (0, 43, 54)
        assert color_map["foreground"] == (131, 148, 150)
        assert len(color_map) >= 8

        # Verify components are loaded
        assert theme.get_button() is not None
        assert theme.get_button_focused() is not None
        assert theme.get_border() is not None
        assert theme.get_selection() is not None
        assert theme.get_disabled() is not None
        assert theme.get_background() is not None
        assert theme.get_text_input() is not None

    def test_load_ocean_xml(self, examples_dir):
        """Load the ocean.xml example and verify key properties."""
        path = os.path.join(examples_dir, "ocean.xml")
        theme = load_theme_from_file(path)

        assert isinstance(theme, ConfigTheme)
        assert theme.name == "Ocean"
        assert theme.author == "FlossWare"

        color_map = theme.get_color_map()
        assert color_map["background"] == (10, 25, 47)
        assert color_map["foreground"] == (176, 210, 224)
        assert len(color_map) >= 8

        # Verify components are loaded
        assert theme.get_button() is not None
        assert theme.get_border() is not None

    def test_load_forest_yaml(self, examples_dir):
        """Load the forest.yaml example (skip if no PyYAML)."""
        try:
            import yaml  # noqa: F401
        except ImportError:
            pytest.skip("PyYAML not installed")

        path = os.path.join(examples_dir, "forest.yaml")
        theme = load_theme_from_file(path)

        assert isinstance(theme, ConfigTheme)
        assert theme.name == "Forest"
        assert theme.author == "FlossWare"

        color_map = theme.get_color_map()
        assert color_map["background"] == (20, 30, 18)
        assert color_map["foreground"] == (190, 210, 170)
        assert len(color_map) >= 8

        # Verify components are loaded
        assert theme.get_button() is not None
        assert theme.get_border() is not None

    def test_solarized_apply(self, examples_dir, mock_curses, mock_stdscr):
        """Load solarized.json, apply it, verify colors initialized."""
        path = os.path.join(examples_dir, "solarized.json")
        theme = load_theme_from_file(path)
        theme.apply(mock_stdscr)

        assert theme.colors.primary > 0
        assert theme.colors.success > 0
        assert theme.colors.error > 0
        assert theme.components.button > 0

    def test_ocean_apply(self, examples_dir, mock_curses, mock_stdscr):
        """Load ocean.xml, apply it, verify colors initialized."""
        path = os.path.join(examples_dir, "ocean.xml")
        theme = load_theme_from_file(path)
        theme.apply(mock_stdscr)

        assert theme.colors.primary > 0
        assert theme.components.border > 0


# ---------------------------------------------------------------------------
# Tests: ThemeManager.load_from_file integration
# ---------------------------------------------------------------------------


class TestThemeManagerLoadFromFile:
    """Integration tests for ThemeManager.load_from_file method."""

    def test_load_from_json_file(self, tmp_path):
        """ThemeManager.load_from_file loads a JSON theme."""
        from curses_themes.manager import ThemeManager

        config = _make_config(name="Manager JSON")
        json_path = tmp_path / "manager_theme.json"
        json_path.write_text(json.dumps(config), encoding="utf-8")

        theme = ThemeManager.load_from_file(str(json_path))
        assert theme.name == "Manager JSON"
        assert isinstance(theme, ConfigTheme)

    def test_load_from_file_custom_name(self, tmp_path):
        """ThemeManager.load_from_file with custom registration name."""
        from curses_themes.manager import ThemeManager

        config = _make_config(name="Original Name")
        json_path = tmp_path / "custom_name.json"
        json_path.write_text(json.dumps(config), encoding="utf-8")

        theme = ThemeManager.load_from_file(str(json_path), name="custom-alias")
        assert theme.name == "Original Name"

    def test_load_from_xml_file(self, tmp_path):
        """ThemeManager.load_from_file loads an XML theme."""
        from curses_themes.manager import ThemeManager

        xml = """<theme>
            <meta><name>Manager XML</name></meta>
            <colors>
                <background r="0" g="0" b="0" />
                <foreground r="255" g="255" b="255" />
                <primary r="0" g="120" b="215" />
                <success r="16" g="124" b="16" />
                <error r="232" g="17" b="35" />
                <warning r="193" g="156" b="0" />
                <info r="0" g="120" b="212" />
                <accent r="142" g="68" b="173" />
            </colors>
        </theme>"""
        xml_path = tmp_path / "manager_theme.xml"
        xml_path.write_text(xml, encoding="utf-8")

        theme = ThemeManager.load_from_file(str(xml_path))
        assert theme.name == "Manager XML"
        assert isinstance(theme, ConfigTheme)

    def test_load_from_file_nonexistent_raises(self):
        """load_from_file with a nonexistent path raises FileNotFoundError."""
        from curses_themes.manager import ThemeManager

        with pytest.raises(FileNotFoundError):
            ThemeManager.load_from_file("/tmp/absolutely_nonexistent_theme.json")

    def test_load_from_file_and_apply(self, mock_curses, mock_stdscr, tmp_path):
        """Load via ThemeManager.load_from_file and apply to mock stdscr."""
        from curses_themes.manager import ThemeManager

        config = _make_config(
            name="Manager Apply Test",
            components={
                "button": _color_pair_dict((255, 255, 255), (0, 120, 215)),
            },
        )
        json_path = tmp_path / "manager_apply.json"
        json_path.write_text(json.dumps(config), encoding="utf-8")

        theme = ThemeManager.load_from_file(str(json_path))
        theme.apply(mock_stdscr)

        assert theme.colors is not None
        assert theme.colors.primary > 0
        assert theme.components.button > 0


# ---------------------------------------------------------------------------
# Tests: Edge cases and error handling
# ---------------------------------------------------------------------------


class TestEdgeCasesAndErrors:
    """Edge cases and error handling for the config theme system."""

    def test_extra_colors_in_map_preserved(self):
        """Extra (non-required) colors in the map are preserved."""
        colors = dict(MINIMAL_COLORS)
        colors["custom_color"] = [100, 200, 50]
        config = {"name": "Extra", "colors": colors}
        theme = ConfigTheme(config)
        color_map = theme.get_color_map()
        assert "custom_color" in color_map
        assert color_map["custom_color"] == (100, 200, 50)

    def test_config_theme_multiple_applies(self, mock_curses, mock_stdscr):
        """Applying the same config theme multiple times is valid."""
        theme = ConfigTheme(MINIMAL_CONFIG)
        theme.apply(mock_stdscr)
        colors1 = theme.colors.primary
        theme.apply(mock_stdscr)
        colors2 = theme.colors.primary
        assert colors1 > 0
        assert colors2 > 0

    def test_empty_components_dict_valid(self):
        """An empty components dict in config is valid."""
        config = _make_config(components={})
        theme = ConfigTheme(config)
        assert theme.get_button() is None
        assert theme.get_border() is None

    def test_3d_config_missing_highlight_raises(self):
        """3D config missing highlight key raises ValueError."""
        td = _make_3d_section()
        del td["highlight"]
        config = _make_config(three_d=td)
        with pytest.raises(ValueError, match="highlight"):
            ConfigTheme3D(config)

    def test_3d_config_missing_lowlight_raises(self):
        """3D config missing lowlight key raises ValueError."""
        td = _make_3d_section()
        del td["lowlight"]
        config = _make_config(three_d=td)
        with pytest.raises(ValueError, match="lowlight"):
            ConfigTheme3D(config)

    def test_roundtrip_json_apply_verify(self, mock_curses, mock_stdscr, tmp_path):
        """Round-trip: create JSON, load, apply, verify all colors."""
        config = _make_config(
            name="Roundtrip",
            description="Full round-trip test",
            author="Roundtrip Tester",
        )
        json_path = tmp_path / "roundtrip.json"
        json_path.write_text(json.dumps(config), encoding="utf-8")

        theme = load_theme_from_file(str(json_path))
        theme.apply(mock_stdscr)

        assert theme.colors.primary > 0
        assert theme.colors.success > 0
        assert theme.colors.error > 0
        assert theme.colors.warning > 0
        assert theme.colors.info > 0
        assert theme.colors.accent > 0

        color_map = theme.get_color_map()
        assert color_map["background"] == (0, 0, 0)
        assert color_map["foreground"] == (255, 255, 255)

    def test_roundtrip_3d_json(self, mock_curses, mock_stdscr, tmp_path):
        """Round-trip for a 3D theme loaded from JSON."""
        config = _make_config(
            name="3D Roundtrip",
            three_d=_make_3d_section(shadow_offset_x=3, shadow_offset_y=2),
        )
        json_path = tmp_path / "3d_roundtrip.json"
        json_path.write_text(json.dumps(config), encoding="utf-8")

        theme = load_theme_from_file(str(json_path))
        assert isinstance(theme, ConfigTheme3D)

        theme.apply(mock_stdscr)
        assert theme.shadow_color_pair > 0
        assert theme.highlight_color_pair > 0
        assert theme.lowlight_color_pair > 0
        assert theme.shadow_offset_x == 3
        assert theme.shadow_offset_y == 2

        theme.draw_box_3d(mock_stdscr, 1, 1, 5, 20, raised=True)
        assert mock_stdscr.addstr.called
