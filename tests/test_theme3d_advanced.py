#!/usr/bin/env python3
"""Advanced tests for Theme3D - shadow effects and 3D drawing."""

import pytest

from curses_themes.themes.borland3d import Borland3DTheme


class TestTheme3DShadowEffects:
    """Test 3D shadow and highlight effects."""

    def test_3d_theme_draw_box_with_title(self, mock_curses, mock_stdscr):
        """Test 3D box drawing with title."""
        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Draw box with title
        theme.draw_box(mock_stdscr, 5, 10, 10, 50, title="3D Window")

        # Verify addstr was called for drawing
        assert mock_stdscr.addstr.called
        assert mock_stdscr.addstr.call_count > 10  # Multiple drawing calls

    def test_3d_theme_draw_box_minimum_size(self, mock_curses, mock_stdscr):
        """Test 3D box with minimum size."""
        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Minimum 2x2 box
        theme.draw_box(mock_stdscr, 0, 0, 2, 2)
        assert mock_stdscr.addstr.called

    def test_3d_theme_draw_box_large_size(self, mock_curses, mock_stdscr):
        """Test 3D box with large dimensions."""
        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Large box
        theme.draw_box(mock_stdscr, 1, 1, 20, 70, title="Large Window")
        assert mock_stdscr.addstr.called

    def test_3d_theme_draw_box_at_various_positions(self, mock_curses, mock_stdscr):
        """Test 3D boxes at different screen positions."""
        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Top-left
        theme.draw_box(mock_stdscr, 0, 0, 5, 20)

        # Bottom-right (within 24x80 screen)
        theme.draw_box(mock_stdscr, 15, 50, 5, 20)

        # Center
        theme.draw_box(mock_stdscr, 10, 30, 5, 20)

        assert mock_stdscr.addstr.called

    def test_3d_theme_multiple_boxes(self, mock_curses, mock_stdscr):
        """Test drawing multiple 3D boxes."""
        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Draw several boxes
        theme.draw_box(mock_stdscr, 1, 5, 6, 30, title="Box 1")
        theme.draw_box(mock_stdscr, 8, 5, 6, 30, title="Box 2")
        theme.draw_box(mock_stdscr, 15, 5, 6, 30, title="Box 3")

        assert mock_stdscr.addstr.called
        assert mock_stdscr.addstr.call_count > 30  # Many drawing calls


class TestTheme3DColorPairs:
    """Test 3D theme color pair usage."""

    def test_3d_theme_uses_component_colors(self, mock_curses, mock_stdscr):
        """Test that 3D theme initializes component colors."""
        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Component colors should be set
        assert theme.components is not None
        assert theme.components.background >= 0
        assert theme.components.button >= 0

    def test_3d_theme_semantic_colors(self, mock_curses, mock_stdscr):
        """Test 3D theme semantic color initialization."""
        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # All semantic colors should be initialized
        assert theme.colors.primary > 0
        assert theme.colors.success > 0
        assert theme.colors.error > 0
        assert theme.colors.warning > 0
        assert theme.colors.info > 0
        assert theme.colors.accent > 0


class TestTheme3DEdgeCases:
    """Test edge cases for 3D themes."""

    def test_3d_theme_empty_title(self, mock_curses, mock_stdscr):
        """Test 3D box with empty title."""
        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Empty title should work
        theme.draw_box(mock_stdscr, 5, 10, 8, 40, title="")
        assert mock_stdscr.addstr.called

    def test_3d_theme_long_title(self, mock_curses, mock_stdscr):
        """Test 3D box with very long title."""
        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Long title (should be truncated to fit)
        long_title = "This is a very long title that exceeds the box width"
        theme.draw_box(mock_stdscr, 5, 10, 8, 30, title=long_title)
        assert mock_stdscr.addstr.called

    def test_3d_theme_curses_error_handling(self, mock_curses, mock_stdscr):
        """Test 3D box handles curses errors gracefully."""
        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Make addstr raise curses.error for out of bounds
        mock_stdscr.addstr.side_effect = mock_curses.error("Out of bounds")

        # Should not propagate error
        try:
            theme.draw_box(mock_stdscr, 5, 10, 8, 40)
        except mock_curses.error:
            pytest.fail("draw_box should catch curses.error")

    def test_3d_theme_border_characters(self, mock_curses, mock_stdscr):
        """Test 3D theme uses correct border characters."""
        theme = Borland3DTheme()

        border_chars = theme.get_border_chars()
        assert len(border_chars) == 8
        assert isinstance(border_chars, str)


class TestTheme3DWithDifferentScreenSizes:
    """Test 3D themes work with different terminal sizes."""

    def test_3d_theme_small_terminal(self, mock_curses, mock_stdscr):
        """Test 3D theme on small terminal."""
        mock_stdscr.getmaxyx.return_value = (10, 40)

        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Small box on small terminal
        theme.draw_box(mock_stdscr, 1, 1, 3, 10)
        assert mock_stdscr.addstr.called

    def test_3d_theme_large_terminal(self, mock_curses, mock_stdscr):
        """Test 3D theme on large terminal."""
        mock_stdscr.getmaxyx.return_value = (50, 200)

        theme = Borland3DTheme()
        theme.apply(mock_stdscr)

        # Large box on large terminal
        theme.draw_box(mock_stdscr, 5, 10, 30, 150)
        assert mock_stdscr.addstr.called


class TestBothTheme3DImplementations:
    """Test both Borland3D and DBase4_3D themes side by side."""

    def test_both_themes_have_different_color_palettes(self):
        """Test that Borland and dBase themes have different colors."""
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme

        borland = Borland3DTheme()
        dbase = DBase4_3DTheme()

        borland_map = borland.get_color_map()
        dbase_map = dbase.get_color_map()

        # At least some colors should differ
        differences = sum(
            1
            for key in borland_map
            if borland_map[key] != dbase_map.get(key, (999, 999, 999))
        )
        assert differences > 0, "Themes should have some different colors"

    def test_both_themes_work_independently(self, mock_curses, mock_stdscr):
        """Test both 3D themes can be used in same session."""
        from curses_themes.themes.dbase4_3d import DBase4_3DTheme

        # Use Borland
        borland = Borland3DTheme()
        borland.apply(mock_stdscr)
        assert borland.colors is not None

        # Switch to dBase
        dbase = DBase4_3DTheme()
        dbase.apply(mock_stdscr)
        assert dbase.colors is not None

        # Both should work
        borland.draw_box(mock_stdscr, 1, 1, 5, 30)
        dbase.draw_box(mock_stdscr, 7, 1, 5, 30)
        assert mock_stdscr.addstr.called
