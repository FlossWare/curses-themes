#!/usr/bin/env python3
"""Tests for ColorManager class - RGB conversion and color pair management."""

import pytest

from curses_tui.colors import ColorManager


class TestColorManagerInit:
    """Tests for ColorManager initialization and capability detection."""

    def test_color_manager_init_success(self, mock_curses, mock_stdscr):
        """Test successful ColorManager initialization with color support."""
        # Arrange: mock_curses already configured with color support

        # Act
        manager = ColorManager(mock_stdscr)

        # Assert
        assert manager.stdscr is mock_stdscr
        assert manager.color_count == 256  # Default mock supports 256 colors
        assert ColorManager._next_pair == 1  # No pairs allocated yet
        assert len(ColorManager._pair_cache) == 0

    def test_color_manager_init_no_color_support(self, mock_curses, mock_stdscr):
        """Test ColorManager raises RuntimeError when terminal lacks color support."""
        # Arrange
        mock_curses.color_support = False

        # Act & Assert
        with pytest.raises(RuntimeError, match="Terminal does not support colors"):
            ColorManager(mock_stdscr)

    @pytest.mark.parametrize(
        "colors,expected",
        [
            (8, 8),
            (16, 16),
            (88, 16),  # Some terminals report 88, treat as 16
            (256, 256),
            (16777216, 256),  # True color still mapped to 256
        ],
    )
    def test_detect_color_capability(self, mock_curses, mock_stdscr, colors, expected):
        """Test color capability detection for various terminal types."""
        # Arrange
        mock_curses.COLORS = colors

        # Act
        manager = ColorManager(mock_stdscr)

        # Assert
        assert manager.color_count == expected


class TestRGBConversion:
    """Tests for RGB to curses color conversion algorithms."""

    def test_rgb_to_256_pure_colors(self, mock_curses, mock_stdscr):
        """Test RGB to 256-color conversion for pure RGB colors."""
        manager = ColorManager(mock_stdscr)

        # Pure red (should map to high red in 6x6x6 cube)
        color = manager._rgb_to_256(255, 0, 0)
        assert 16 <= color <= 231  # In RGB cube range

        # Pure green
        color = manager._rgb_to_256(0, 255, 0)
        assert 16 <= color <= 231

        # Pure blue
        color = manager._rgb_to_256(0, 0, 255)
        assert 16 <= color <= 231

    def test_rgb_to_256_grayscale(self, mock_curses, mock_stdscr):
        """Test RGB to 256-color grayscale ramp detection."""
        manager = ColorManager(mock_stdscr)

        # Pure black should map to color 16
        color = manager._rgb_to_256(0, 0, 0)
        assert color == 16

        # Pure white should map to color 231
        color = manager._rgb_to_256(255, 255, 255)
        assert color == 231

        # Mid-gray should use grayscale ramp (232-255)
        color = manager._rgb_to_256(128, 128, 128)
        assert 232 <= color <= 255

    def test_rgb_to_basic_color_matching(self, mock_curses, mock_stdscr):
        """Test RGB to basic 8-color matching via Euclidean distance."""
        # Arrange: Force 8-color mode
        mock_curses.COLORS = 8
        manager = ColorManager(mock_stdscr)

        # Red should map to COLOR_RED (1)
        color = manager._rgb_to_basic(255, 0, 0)
        assert color == mock_curses.COLOR_RED

        # Green should map to COLOR_GREEN (2)
        color = manager._rgb_to_basic(0, 255, 0)
        assert color == mock_curses.COLOR_GREEN

        # White should map to COLOR_WHITE (7)
        color = manager._rgb_to_basic(255, 255, 255)
        assert color == mock_curses.COLOR_WHITE


class TestColorPairManagement:
    """Tests for color pair initialization and caching."""

    def test_init_color_pair_basic(self, mock_curses, mock_stdscr):
        """Test basic color pair initialization."""
        manager = ColorManager(mock_stdscr)

        # Initialize white on black
        pair_num = manager.init_color_pair((255, 255, 255), (0, 0, 0))

        assert pair_num == 1  # First pair
        assert ColorManager._next_pair == 2  # Counter incremented
        assert len(ColorManager._pair_cache) == 1

    def test_init_color_pair_caching(self, mock_curses, mock_stdscr):
        """Test color pair cache reuses existing pairs."""
        manager = ColorManager(mock_stdscr)

        # Initialize same pair twice
        pair1 = manager.init_color_pair((255, 255, 255), (0, 0, 0))
        pair2 = manager.init_color_pair((255, 255, 255), (0, 0, 0))

        assert pair1 == pair2  # Same pair number
        assert ColorManager._next_pair == 2  # Only one pair allocated

    def test_init_color_pair_none_background(self, mock_curses, mock_stdscr):
        """Test color pair with None background (default terminal background)."""
        manager = ColorManager(mock_stdscr)

        pair_num = manager.init_color_pair((255, 255, 255), None)

        assert pair_num == 1
        # Check that bg_color was set to -1 for default background
        assert len(ColorManager._pair_cache) == 1


class TestThemeInitialization:
    """Tests for initializing themes with ColorManager."""

    def test_initialize_theme_success(self, mock_curses, mock_stdscr, simple_theme):
        """Test successful theme initialization with all required colors."""
        manager = ColorManager(mock_stdscr)

        semantic_colors, component_colors = manager.initialize_theme(simple_theme)

        # Verify semantic colors initialized
        assert semantic_colors.primary > 0
        assert semantic_colors.success > 0
        assert semantic_colors.error > 0
        assert semantic_colors.warning > 0
        assert semantic_colors.info > 0
        assert semantic_colors.background > 0
        assert semantic_colors.foreground > 0
        assert semantic_colors.accent > 0

        # Verify component colors initialized
        assert component_colors.background == 0  # None from simple_theme
        assert component_colors.button == 0
        assert component_colors.button_focused == 0

    def test_initialize_theme_missing_colors(self, mock_curses, mock_stdscr):
        """Test theme initialization fails with missing required colors."""
        from curses_tui import Theme

        class IncompleteTheme(Theme):
            def __init__(self):
                super().__init__("Incomplete", "Missing colors")

            def get_color_map(self):
                return {
                    "background": (0, 0, 0),
                    "foreground": (255, 255, 255),
                    # Missing: primary, success, error, warning, info, accent
                }

        manager = ColorManager(mock_stdscr)
        theme = IncompleteTheme()

        with pytest.raises(ValueError, match="missing required colors"):
            manager.initialize_theme(theme)

    def test_missing_colors_error_shows_all_required(self, mock_curses, mock_stdscr):
        """Test that missing colors error lists all required colors."""
        from curses_tui import Theme

        class IncompleteTheme(Theme):
            def __init__(self):
                super().__init__("Incomplete", "Missing colors")

            def get_color_map(self):
                return {
                    "background": (0, 0, 0),
                    "foreground": (255, 255, 255),
                    # Missing 6 colors
                }

        manager = ColorManager(mock_stdscr)
        theme = IncompleteTheme()

        with pytest.raises(ValueError) as exc_info:
            manager.initialize_theme(theme)

        error_msg = str(exc_info.value)
        # Should list what's missing
        assert "primary" in error_msg or "success" in error_msg
        # Should show all required colors
        assert "get_color_map" in error_msg.lower()
        # Should have example
        assert "example" in error_msg.lower() or "return" in error_msg.lower()
