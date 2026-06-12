#!/usr/bin/env python3
"""Tests for Unicode width handling in draw_box and draw_box_3d."""

from curses_themes.theme import _calculate_display_width


class TestDisplayWidthCalculation:
    """Test suite for _calculate_display_width utility function."""

    def test_ascii_text_width(self):
        """Test display width of ASCII text."""
        assert _calculate_display_width("Hello") == 5
        assert _calculate_display_width("Test") == 4
        assert _calculate_display_width("") == 0

    def test_japanese_hiragana_width(self):
        """Test display width of Japanese hiragana (wide characters)."""
        # こんにちは = 5 characters × 2 columns each = 10
        assert _calculate_display_width("こんにちは") == 10

    def test_japanese_katakana_width(self):
        """Test display width of Japanese katakana (wide characters)."""
        # カタカナ = 4 characters × 2 columns each = 8
        assert _calculate_display_width("カタカナ") == 8

    def test_chinese_width(self):
        """Test display width of Chinese characters (wide)."""
        # 你好世界 = 4 characters × 2 columns each = 8
        assert _calculate_display_width("你好世界") == 8
        # 中文测试 = 4 characters × 2 columns each = 8
        assert _calculate_display_width("中文测试") == 8

    def test_korean_width(self):
        """Test display width of Korean hangul (wide characters)."""
        # 한글 = 2 characters × 2 columns each = 4
        assert _calculate_display_width("한글") == 4

    def test_mixed_ascii_cjk_width(self):
        """Test display width of mixed ASCII and CJK text."""
        # 'Hello 世界' = 'Hello ' (6) + '世界' (4) = 10
        assert _calculate_display_width("Hello 世界") == 10
        # 'Test こんにちは' = 'Test ' (5) + 'こんにちは' (10) = 15
        assert _calculate_display_width("Test こんにちは") == 15

    def test_emoji_width(self):
        """Test display width of emoji (varies by type)."""
        # Note: Some emoji may be ambiguous or vary by terminal
        # Basic emoji like ☺ is typically narrow (1 column)
        text_with_emoji = "Hello ☺"
        width = _calculate_display_width(text_with_emoji)
        assert width >= 7  # At minimum the ASCII part

    def test_fullwidth_latin_width(self):
        """Test display width of fullwidth Latin characters."""
        # Fullwidth A (U+FF21) should be 2 columns
        assert _calculate_display_width("Ａ") == 2


class TestDrawBoxWithCJKTitles:
    """Test suite for draw_box with CJK titles."""

    def test_draw_box_with_japanese_title(self, mock_curses, mock_stdscr, simple_theme):
        """Test draw_box with Japanese title."""
        simple_theme.apply(mock_stdscr)

        # Japanese title 'テスト' (4 chars × 2 = 8 display width)
        # Box width 20, needs > 8 + 4 = 12, so should fit
        simple_theme.draw_box(mock_stdscr, 5, 10, 8, 20, title="テスト")

        # Verify draw was called
        assert mock_stdscr.addstr.called

    def test_draw_box_with_chinese_title(self, mock_curses, mock_stdscr, simple_theme):
        """Test draw_box with Chinese title."""
        simple_theme.apply(mock_stdscr)

        # Chinese title '测试' (2 chars × 2 = 4 display width)
        simple_theme.draw_box(mock_stdscr, 5, 10, 8, 20, title="测试")

        assert mock_stdscr.addstr.called

    def test_draw_box_with_korean_title(self, mock_curses, mock_stdscr, simple_theme):
        """Test draw_box with Korean title."""
        simple_theme.apply(mock_stdscr)

        # Korean title '테스트' (3 chars × 2 = 6 display width)
        simple_theme.draw_box(mock_stdscr, 5, 10, 8, 20, title="테스트")

        assert mock_stdscr.addstr.called

    def test_draw_box_cjk_title_too_wide(self, mock_curses, mock_stdscr, simple_theme):
        """Test draw_box skips title when CJK text is too wide."""
        simple_theme.apply(mock_stdscr)

        # Long Japanese title (10 chars × 2 = 20 display width)
        # Box width 20, needs > 20 + 4 = 24, so title should be skipped
        simple_theme.draw_box(mock_stdscr, 5, 10, 8, 20, title="こんにちはこんにちは")

        # Should still draw box (corners and borders)
        assert mock_stdscr.addstr.called

    def test_draw_box_mixed_text_title(self, mock_curses, mock_stdscr, simple_theme):
        """Test draw_box with mixed ASCII and CJK title."""
        simple_theme.apply(mock_stdscr)

        # Mixed title 'Hello 世界' = 'Hello ' (6) + '世界' (4) = 10 display width
        simple_theme.draw_box(mock_stdscr, 5, 10, 8, 30, title="Hello 世界")

        assert mock_stdscr.addstr.called


class TestDrawBox3DWithCJKTitles:
    """Test suite for draw_box_3d with CJK titles."""

    def test_draw_box_3d_with_japanese_title(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """Test draw_box_3d with Japanese title."""
        simple_3d_theme.apply(mock_stdscr)

        # Japanese title 'ボタン' (3 chars × 2 = 6 display width)
        simple_3d_theme.draw_box_3d(
            mock_stdscr, 5, 10, 5, 20, raised=True, title="ボタン"
        )

        assert mock_stdscr.addstr.called or mock_stdscr.addch.called

    def test_draw_box_3d_with_chinese_title(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """Test draw_box_3d with Chinese title."""
        simple_3d_theme.apply(mock_stdscr)

        # Chinese title '按钮' (2 chars × 2 = 4 display width)
        simple_3d_theme.draw_box_3d(
            mock_stdscr, 5, 10, 5, 20, raised=True, title="按钮"
        )

        assert mock_stdscr.addstr.called or mock_stdscr.addch.called

    def test_draw_box_3d_sunken_with_korean_title(
        self, mock_curses, mock_stdscr, simple_3d_theme
    ):
        """Test draw_box_3d sunken style with Korean title."""
        simple_3d_theme.apply(mock_stdscr)

        # Korean title '입력' (2 chars × 2 = 4 display width)
        simple_3d_theme.draw_box_3d(
            mock_stdscr, 5, 10, 5, 20, raised=False, title="입력"
        )

        assert mock_stdscr.addstr.called or mock_stdscr.addch.called
