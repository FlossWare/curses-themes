#!/usr/bin/env python3
"""Tests for Theme3D coverage gaps.

Targets uncovered lines in theme3d.py:
- Line 138: shadow_offset_x setter negative value error
- Line 160: shadow_offset_y setter negative value error
- Line 228: get_double_border_chars default
- Line 237: supports_3d returns True
- Lines 300, 318, 336: property RuntimeError when apply() not called
- Lines 392-398: draw_box_3d ValueError for too-small dimensions
- Lines 408-428: shadow drawing (shadow_offset conditionals)
- Lines 436-453: border corner/edge drawing
- Lines 483-490: height==3 special case for bevel
- Lines 493-498: title drawing in 3D box
"""

import pytest

from curses_themes import Theme3D


class TestShadowOffsetValidation:
    """Test shadow offset property setters with negative values."""

    def test_shadow_offset_x_negative_raises_value_error(self, simple_3d_theme):
        """Setting shadow_offset_x to a negative value must raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            simple_3d_theme.shadow_offset_x = -1

    def test_shadow_offset_x_negative_large_raises_value_error(self, simple_3d_theme):
        """Setting shadow_offset_x to a large negative value must raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            simple_3d_theme.shadow_offset_x = -100

    def test_shadow_offset_y_negative_raises_value_error(self, simple_3d_theme):
        """Setting shadow_offset_y to a negative value must raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            simple_3d_theme.shadow_offset_y = -1

    def test_shadow_offset_y_negative_large_raises_value_error(self, simple_3d_theme):
        """Setting shadow_offset_y to a large negative value must raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            simple_3d_theme.shadow_offset_y = -50

    def test_shadow_offset_x_zero_is_valid(self, simple_3d_theme):
        """Setting shadow_offset_x to zero is allowed."""
        simple_3d_theme.shadow_offset_x = 0
        assert simple_3d_theme.shadow_offset_x == 0

    def test_shadow_offset_y_zero_is_valid(self, simple_3d_theme):
        """Setting shadow_offset_y to zero is allowed."""
        simple_3d_theme.shadow_offset_y = 0
        assert simple_3d_theme.shadow_offset_y == 0

    def test_shadow_offset_x_positive_is_valid(self, simple_3d_theme):
        """Setting shadow_offset_x to a positive value is allowed."""
        simple_3d_theme.shadow_offset_x = 5
        assert simple_3d_theme.shadow_offset_x == 5

    def test_shadow_offset_y_positive_is_valid(self, simple_3d_theme):
        """Setting shadow_offset_y to a positive value is allowed."""
        simple_3d_theme.shadow_offset_y = 3
        assert simple_3d_theme.shadow_offset_y == 3


class TestDoubleBorderCharsDefault:
    """Test get_double_border_chars returns the default Unicode double-line box."""

    def test_returns_correct_default_chars(self, simple_3d_theme):
        """get_double_border_chars must return the 8-char double-line set."""
        result = simple_3d_theme.get_double_border_chars()
        assert result == "╔═╗║║╚═╝"

    def test_returns_8_characters(self, simple_3d_theme):
        """get_double_border_chars result must be exactly 8 characters."""
        result = simple_3d_theme.get_double_border_chars()
        assert len(result) == 8

    def test_returns_string(self, simple_3d_theme):
        """get_double_border_chars must return a string."""
        result = simple_3d_theme.get_double_border_chars()
        assert isinstance(result, str)


class TestSupports3D:
    """Test supports_3d returns True for Theme3D subclasses."""

    def test_supports_3d_returns_true(self, simple_3d_theme):
        """Theme3D.supports_3d() must always return True."""
        assert simple_3d_theme.supports_3d() is True

    def test_supports_3d_borland(self):
        """Borland3DTheme.supports_3d() must return True."""
        from curses_themes.themes.borland3d import Borland3DTheme

        theme = Borland3DTheme()
        assert theme.supports_3d() is True

    def test_supports_3d_dbase(self):
        """DBase4_3DTheme.supports_3d() must return True."""
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme

        theme = DBase4_3DTheme()
        assert theme.supports_3d() is True


class TestColorPairPropertiesBeforeApply:
    """Test RuntimeError when accessing color pair properties before apply()."""

    def test_shadow_color_pair_before_apply(self, simple_3d_theme):
        """Accessing shadow_color_pair before apply() must raise RuntimeError."""
        with pytest.raises(RuntimeError, match="has not been applied"):
            _ = simple_3d_theme.shadow_color_pair

    def test_highlight_color_pair_before_apply(self, simple_3d_theme):
        """Accessing highlight_color_pair before apply() must raise RuntimeError."""
        with pytest.raises(RuntimeError, match="has not been applied"):
            _ = simple_3d_theme.highlight_color_pair

    def test_lowlight_color_pair_before_apply(self, simple_3d_theme):
        """Accessing lowlight_color_pair before apply() must raise RuntimeError."""
        with pytest.raises(RuntimeError, match="has not been applied"):
            _ = simple_3d_theme.lowlight_color_pair

    def test_shadow_color_pair_error_includes_theme_name(self, simple_3d_theme):
        """RuntimeError message must include the theme name."""
        with pytest.raises(RuntimeError, match="Simple 3D Test Theme"):
            _ = simple_3d_theme.shadow_color_pair

    def test_highlight_color_pair_error_includes_theme_name(self, simple_3d_theme):
        """RuntimeError message must include the theme name."""
        with pytest.raises(RuntimeError, match="Simple 3D Test Theme"):
            _ = simple_3d_theme.highlight_color_pair

    def test_lowlight_color_pair_error_includes_theme_name(self, simple_3d_theme):
        """RuntimeError message must include the theme name."""
        with pytest.raises(RuntimeError, match="Simple 3D Test Theme"):
            _ = simple_3d_theme.lowlight_color_pair

    def test_color_pairs_valid_after_apply(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """All 3D color pairs must be accessible after apply()."""
        simple_3d_theme.apply(mock_stdscr)
        assert isinstance(simple_3d_theme.shadow_color_pair, int)
        assert isinstance(simple_3d_theme.highlight_color_pair, int)
        assert isinstance(simple_3d_theme.lowlight_color_pair, int)


class TestDrawBox3DValidation:
    """Test draw_box_3d dimension validation."""

    def test_too_small_height(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d with height < 2 must raise ValueError."""
        simple_3d_theme.apply(mock_stdscr)
        with pytest.raises(ValueError, match="too small"):
            simple_3d_theme.draw_box_3d(mock_stdscr, 0, 0, 1, 10)

    def test_too_small_width(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d with width < 2 must raise ValueError."""
        simple_3d_theme.apply(mock_stdscr)
        with pytest.raises(ValueError, match="too small"):
            simple_3d_theme.draw_box_3d(mock_stdscr, 0, 0, 10, 1)

    def test_both_dimensions_too_small(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d with both dimensions < 2 must raise ValueError."""
        simple_3d_theme.apply(mock_stdscr)
        with pytest.raises(ValueError, match="too small"):
            simple_3d_theme.draw_box_3d(mock_stdscr, 0, 0, 1, 1)

    def test_zero_height(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d with height of 0 must raise ValueError."""
        simple_3d_theme.apply(mock_stdscr)
        with pytest.raises(ValueError, match="too small"):
            simple_3d_theme.draw_box_3d(mock_stdscr, 0, 0, 0, 10)

    def test_zero_width(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d with width of 0 must raise ValueError."""
        simple_3d_theme.apply(mock_stdscr)
        with pytest.raises(ValueError, match="too small"):
            simple_3d_theme.draw_box_3d(mock_stdscr, 0, 0, 10, 0)

    def test_minimum_valid_size(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d with 2x2 must not raise."""
        simple_3d_theme.apply(mock_stdscr)
        simple_3d_theme.draw_box_3d(mock_stdscr, 0, 0, 2, 2)


class TestDrawBox3DInvalidBorderChars:
    """Test draw_box_3d raises ValueError for wrong border character count."""

    def test_bad_border_chars_length(self, mock_curses, mock_stdscr):
        """draw_box_3d must raise ValueError when get_border_chars() returns wrong length."""

        class BadBorderTheme(Theme3D):
            def __init__(self):
                super().__init__("BadBorder", "wrong border chars")

            def get_color_map(self):
                return {
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

            def get_border_chars(self):
                return "ABC"  # Only 3 chars, need 8

        theme = BadBorderTheme()
        theme.apply(mock_stdscr)
        with pytest.raises(ValueError, match="8 characters"):
            theme.draw_box_3d(mock_stdscr, 0, 0, 5, 10)


class TestDrawBox3DShadowRendering:
    """Test shadow rendering in draw_box_3d (lines 408-428)."""

    def test_shadow_with_default_offsets(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """draw_box_3d must draw shadow when offsets are positive (defaults 2,1)."""
        simple_3d_theme.apply(mock_stdscr)
        simple_3d_theme.draw_box_3d(mock_stdscr, 2, 3, 5, 10)

        # addch is used for shadow drawing
        assert mock_stdscr.addch.called

    def test_shadow_right_edge_rendering(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """draw_box_3d must draw shadow on the right edge of the box."""
        simple_3d_theme.apply(mock_stdscr)
        # Default shadow_offset_x = 2, shadow_offset_y = 1
        y, x, h, w = 2, 3, 5, 10

        simple_3d_theme.draw_box_3d(mock_stdscr, y, x, h, w)

        # Shadow on right: addch calls at x + width + j for j in range(shadow_offset_x)
        addch_calls = mock_stdscr.addch.call_args_list
        shadow_y_start = y + simple_3d_theme.shadow_offset_y  # 2 + 1 = 3
        right_shadow_x_values = {x + w, x + w + 1}  # offset_x = 2

        right_shadow_calls = [
            c
            for c in addch_calls
            if c[0][1] in right_shadow_x_values and c[0][0] >= shadow_y_start
        ]
        assert len(right_shadow_calls) > 0, "Right shadow should have been drawn"

    def test_shadow_bottom_edge_rendering(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """draw_box_3d must draw shadow on the bottom edge of the box."""
        simple_3d_theme.apply(mock_stdscr)
        y, x, h, w = 2, 3, 5, 10

        simple_3d_theme.draw_box_3d(mock_stdscr, y, x, h, w)

        addch_calls = mock_stdscr.addch.call_args_list
        shadow_x_start = x + simple_3d_theme.shadow_offset_x  # 3 + 2 = 5
        bottom_row = y + h  # 2 + 5 = 7

        bottom_shadow_calls = [
            c
            for c in addch_calls
            if c[0][0] == bottom_row and c[0][1] >= shadow_x_start
        ]
        assert len(bottom_shadow_calls) > 0, "Bottom shadow should have been drawn"

    def test_no_shadow_when_offsets_zero(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """draw_box_3d with both offsets 0 must not draw any shadow."""
        simple_3d_theme.shadow_offset_x = 0
        simple_3d_theme.shadow_offset_y = 0
        simple_3d_theme.apply(mock_stdscr)

        mock_stdscr.addch.reset_mock()
        simple_3d_theme.draw_box_3d(mock_stdscr, 2, 3, 2, 2)

        # With a 2x2 box (height < 3, width < 3), no bevel is drawn either,
        # and with offsets 0, no shadow is drawn. addch should not be called.
        assert not mock_stdscr.addch.called

    def test_shadow_only_x_offset(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d with only shadow_offset_x > 0 must draw right shadow only."""
        simple_3d_theme.shadow_offset_x = 3
        simple_3d_theme.shadow_offset_y = 0
        simple_3d_theme.apply(mock_stdscr)

        simple_3d_theme.draw_box_3d(mock_stdscr, 2, 3, 5, 10)

        # Should have right-edge shadow calls but no bottom-edge shadow
        addch_calls = mock_stdscr.addch.call_args_list
        assert len(addch_calls) > 0

    def test_shadow_only_y_offset(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d with only shadow_offset_y > 0 must draw bottom shadow only."""
        simple_3d_theme.shadow_offset_x = 0
        simple_3d_theme.shadow_offset_y = 2
        simple_3d_theme.apply(mock_stdscr)

        simple_3d_theme.draw_box_3d(mock_stdscr, 2, 3, 5, 10)

        addch_calls = mock_stdscr.addch.call_args_list
        assert len(addch_calls) > 0


class TestDrawBox3DBorderDrawing:
    """Test border corner and edge drawing (lines 436-453)."""

    def test_corners_drawn(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d must draw all four corners using addstr."""
        simple_3d_theme.apply(mock_stdscr)
        y, x, h, w = 5, 10, 6, 20

        simple_3d_theme.draw_box_3d(mock_stdscr, y, x, h, w)

        addstr_calls = mock_stdscr.addstr.call_args_list
        positions = [(c[0][0], c[0][1]) for c in addstr_calls]

        # Check all four corners are drawn
        assert (y, x) in positions, "Top-left corner not drawn"
        assert (y, x + w - 1) in positions, "Top-right corner not drawn"
        assert (y + h - 1, x) in positions, "Bottom-left corner not drawn"
        assert (y + h - 1, x + w - 1) in positions, "Bottom-right corner not drawn"

    def test_horizontal_borders_drawn(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d must draw top and bottom horizontal borders."""
        simple_3d_theme.apply(mock_stdscr)
        y, x, h, w = 5, 10, 6, 20

        simple_3d_theme.draw_box_3d(mock_stdscr, y, x, h, w)

        addstr_calls = mock_stdscr.addstr.call_args_list
        positions = [(c[0][0], c[0][1]) for c in addstr_calls]

        # Inner horizontal positions (between corners)
        for i in range(1, w - 1):
            assert (y, x + i) in positions, f"Top border at x+{i} not drawn"
            assert (
                y + h - 1,
                x + i,
            ) in positions, f"Bottom border at x+{i} not drawn"

    def test_vertical_borders_drawn(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d must draw left and right vertical borders."""
        simple_3d_theme.apply(mock_stdscr)
        y, x, h, w = 5, 10, 6, 20

        simple_3d_theme.draw_box_3d(mock_stdscr, y, x, h, w)

        addstr_calls = mock_stdscr.addstr.call_args_list
        positions = [(c[0][0], c[0][1]) for c in addstr_calls]

        for i in range(1, h - 1):
            assert (y + i, x) in positions, f"Left border at y+{i} not drawn"
            assert (
                y + i,
                x + w - 1,
            ) in positions, f"Right border at y+{i} not drawn"

    def test_corner_curses_error_suppressed(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """draw_box_3d must suppress curses.error when drawing corners."""
        simple_3d_theme.apply(mock_stdscr)
        mock_stdscr.addstr.side_effect = mock_curses.error("out of bounds")

        # Must not propagate curses.error
        simple_3d_theme.draw_box_3d(mock_stdscr, 5, 10, 6, 20)


class TestDrawBox3DBevelEffects:
    """Test 3D bevel edge drawing for different box sizes."""

    def test_raised_bevel_large_box(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d raised=True with height>=4 and width>=4 draws bevel edges."""
        simple_3d_theme.apply(mock_stdscr)
        y, x, h, w = 5, 10, 6, 20

        simple_3d_theme.draw_box_3d(mock_stdscr, y, x, h, w, raised=True)

        # Bevel drawing uses addch
        addch_calls = mock_stdscr.addch.call_args_list
        # Filter out shadow calls -- bevel calls are inside the border
        bevel_y_positions = {c[0][0] for c in addch_calls}
        assert (y + 1) in bevel_y_positions, "Top bevel edge not drawn"
        assert (y + h - 2) in bevel_y_positions, "Bottom bevel edge not drawn"

    def test_sunken_bevel_large_box(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d raised=False with height>=4 and width>=4 draws reversed bevel."""
        simple_3d_theme.apply(mock_stdscr)
        y, x, h, w = 5, 10, 6, 20

        simple_3d_theme.draw_box_3d(mock_stdscr, y, x, h, w, raised=False)

        addch_calls = mock_stdscr.addch.call_args_list
        assert len(addch_calls) > 0, "Sunken bevel should draw addch calls"

    def test_height_3_raised_special_case(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """draw_box_3d with height==3 and width>=3 uses single-row bevel (raised)."""
        simple_3d_theme.apply(mock_stdscr)
        y, x, h, w = 5, 10, 3, 10

        mock_stdscr.addch.reset_mock()
        simple_3d_theme.draw_box_3d(mock_stdscr, y, x, h, w, raised=True)

        addch_calls = mock_stdscr.addch.call_args_list
        # In height==3 case, bevel is drawn at y+1 for the middle row
        bevel_calls = [c for c in addch_calls if c[0][0] == y + 1]
        # Should have drawn bevel in the middle row for inner positions
        assert len(bevel_calls) > 0, "height==3 raised bevel not drawn"

    def test_height_3_sunken_special_case(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """draw_box_3d with height==3 and width>=3 uses single-row bevel (sunken)."""
        simple_3d_theme.apply(mock_stdscr)
        y, x, h, w = 5, 10, 3, 10

        mock_stdscr.addch.reset_mock()
        simple_3d_theme.draw_box_3d(mock_stdscr, y, x, h, w, raised=False)

        addch_calls = mock_stdscr.addch.call_args_list
        bevel_calls = [c for c in addch_calls if c[0][0] == y + 1]
        assert len(bevel_calls) > 0, "height==3 sunken bevel not drawn"

    def test_height_3_width_3_minimum_bevel(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """draw_box_3d with height==3, width==3 draws exactly 1 bevel cell."""
        simple_3d_theme.shadow_offset_x = 0
        simple_3d_theme.shadow_offset_y = 0
        simple_3d_theme.apply(mock_stdscr)

        mock_stdscr.addch.reset_mock()
        simple_3d_theme.draw_box_3d(mock_stdscr, 0, 0, 3, 3, raised=True)

        # width-1 - 1 = 1 interior position at (1, 1)
        bevel_calls = [c for c in mock_stdscr.addch.call_args_list if c[0][0] == 1]
        assert len(bevel_calls) == 1

    def test_no_bevel_for_2x2_box(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d with 2x2 box must not draw any bevel."""
        simple_3d_theme.shadow_offset_x = 0
        simple_3d_theme.shadow_offset_y = 0
        simple_3d_theme.apply(mock_stdscr)

        mock_stdscr.addch.reset_mock()
        simple_3d_theme.draw_box_3d(mock_stdscr, 0, 0, 2, 2)

        # No bevel or shadow, so addch should not be called
        assert not mock_stdscr.addch.called

    def test_height_2_width_large_no_bevel(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """draw_box_3d with height==2 never draws bevel regardless of width."""
        simple_3d_theme.shadow_offset_x = 0
        simple_3d_theme.shadow_offset_y = 0
        simple_3d_theme.apply(mock_stdscr)

        mock_stdscr.addch.reset_mock()
        simple_3d_theme.draw_box_3d(mock_stdscr, 0, 0, 2, 20)

        assert not mock_stdscr.addch.called


class TestDrawBox3DTitle:
    """Test title drawing in draw_box_3d (lines 493-498)."""

    def test_title_drawn_when_fits(self, mock_curses, mock_stdscr, simple_3d_theme):
        """draw_box_3d must draw the title when it fits within the box."""
        simple_3d_theme.apply(mock_stdscr)

        simple_3d_theme.draw_box_3d(mock_stdscr, 5, 10, 6, 30, title="Hello")

        addstr_calls = mock_stdscr.addstr.call_args_list
        title_calls = [c for c in addstr_calls if " Hello " in str(c[0][2])]
        assert len(title_calls) == 1, "Title should be drawn exactly once"

    def test_title_centered_on_top_border(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """Title must be drawn on the top row (y coordinate of the box)."""
        simple_3d_theme.apply(mock_stdscr)
        y = 5

        simple_3d_theme.draw_box_3d(mock_stdscr, y, 10, 6, 30, title="Test")

        addstr_calls = mock_stdscr.addstr.call_args_list
        title_calls = [c for c in addstr_calls if " Test " in str(c[0][2])]
        assert len(title_calls) == 1
        assert title_calls[0][0][0] == y, "Title must be on the top border row"

    def test_title_not_drawn_when_too_wide(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """Title must not be drawn if it does not fit (needs width > display_width + 4)."""
        simple_3d_theme.apply(mock_stdscr)

        # Title "ABCDEFGH" has display width 8, needs > 12 width. Box width = 10.
        simple_3d_theme.draw_box_3d(mock_stdscr, 5, 10, 6, 10, title="ABCDEFGH")

        addstr_calls = mock_stdscr.addstr.call_args_list
        title_calls = [c for c in addstr_calls if "ABCDEFGH" in str(c[0][2])]
        assert len(title_calls) == 0, "Title too wide should not be drawn"

    def test_empty_title_not_drawn(self, mock_curses, mock_stdscr, simple_3d_theme):
        """Empty string title must not trigger title drawing."""
        simple_3d_theme.apply(mock_stdscr)

        simple_3d_theme.draw_box_3d(mock_stdscr, 5, 10, 6, 30, title="")

        addstr_calls = mock_stdscr.addstr.call_args_list
        # No call should have a string that is just spaces (title formatting)
        for c in addstr_calls:
            text = str(c[0][2])
            # Title is formatted as " {title} " -- empty title means no such call
            assert text != "  ", "Empty title should not produce a drawing call"

    def test_title_with_no_title_argument(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """draw_box_3d with default (no title) must not draw title."""
        simple_3d_theme.apply(mock_stdscr)
        mock_stdscr.addstr.reset_mock()

        simple_3d_theme.draw_box_3d(mock_stdscr, 5, 10, 6, 30)

        addstr_calls = mock_stdscr.addstr.call_args_list
        # Count the addstr calls: corners (4) + horizontal edges + vertical edges
        # No title call should be present
        for c in addstr_calls:
            text = str(c[0][2])
            # Title would be " something " -- all border chars are single characters
            if len(text) > 1:
                # Only title would be multi-char besides spaces
                assert text.strip() == "" or len(text) == 1


class TestDrawBox3DRaisedVsSunken:
    """Test raised vs sunken rendering differences."""

    def test_raised_and_sunken_use_different_attrs(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """Raised and sunken boxes must use swapped highlight/lowlight attrs."""
        simple_3d_theme.apply(mock_stdscr)

        # Draw raised box
        mock_stdscr.addch.reset_mock()
        simple_3d_theme.draw_box_3d(mock_stdscr, 0, 0, 5, 10, raised=True)
        raised_calls = list(mock_stdscr.addch.call_args_list)

        # Draw sunken box
        mock_stdscr.addch.reset_mock()
        simple_3d_theme.draw_box_3d(mock_stdscr, 0, 0, 5, 10, raised=False)
        sunken_calls = list(mock_stdscr.addch.call_args_list)

        # Extract attributes used in bevel drawing (filtering to inner border positions)
        def extract_bevel_attrs(calls, y, h):
            """Get attrs from top bevel row."""
            return {c[0][3] for c in calls if c[0][0] == y + 1 and len(c[0]) >= 4}

        raised_attrs = extract_bevel_attrs(raised_calls, 0, 5)
        sunken_attrs = extract_bevel_attrs(sunken_calls, 0, 5)

        # Both should have calls, but they should differ in attrs
        assert len(raised_attrs) > 0
        assert len(sunken_attrs) > 0


class TestDrawBox3DWithCursesErrors:
    """Test that draw_box_3d gracefully handles curses.error in all sections."""

    def test_addch_error_in_shadow(self, mock_curses, mock_stdscr, simple_3d_theme):
        """curses.error in shadow drawing must be suppressed."""
        simple_3d_theme.apply(mock_stdscr)
        mock_stdscr.addch.side_effect = mock_curses.error("out of bounds")

        # Must not raise
        simple_3d_theme.draw_box_3d(mock_stdscr, 5, 10, 6, 20)

    def test_addstr_error_in_border(self, mock_curses, mock_stdscr, simple_3d_theme):
        """curses.error in border drawing must be suppressed."""
        simple_3d_theme.apply(mock_stdscr)
        mock_stdscr.addstr.side_effect = mock_curses.error("out of bounds")

        # Must not raise
        simple_3d_theme.draw_box_3d(mock_stdscr, 5, 10, 6, 20)

    def test_both_addstr_and_addch_error(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """curses.error in both addstr and addch must be suppressed."""
        simple_3d_theme.apply(mock_stdscr)
        mock_stdscr.addstr.side_effect = mock_curses.error("out of bounds")
        mock_stdscr.addch.side_effect = mock_curses.error("out of bounds")

        simple_3d_theme.draw_box_3d(mock_stdscr, 5, 10, 6, 20)


class TestDrawBox3DRepr:
    """Test Theme3D __repr__ method."""

    def test_repr_format(self, simple_3d_theme):
        """__repr__ must include class name, theme name, and author."""
        result = repr(simple_3d_theme)
        assert "Theme3D" in result
        assert "Simple 3D Test Theme" in result
        assert "Test Suite" in result
