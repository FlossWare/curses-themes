#!/usr/bin/env python3
"""
Comprehensive border character validation tests for all themes.

This test suite validates that all registered themes return properly formatted
border characters that are suitable for terminal rendering. It ensures:
1. All themes return exactly 8 characters from get_border_chars()
2. Characters are printable and valid for terminal display
3. Border characters work correctly with draw_box()
4. 3D themes return valid double border characters
"""

import pytest
from curses_themes import ThemeManager
from curses_themes.theme3d import Theme3D


class TestBorderCharsLength:
    """Test that all themes return exactly 8 border characters."""

    @pytest.fixture
    def all_theme_names(self):
        """Get all registered theme names."""
        return list(ThemeManager.list_themes().keys())

    def test_all_themes_border_chars_length(self, all_theme_names):
        """Test all themes return exactly 8 characters from get_border_chars()."""
        for theme_name in all_theme_names:
            theme = ThemeManager.load(theme_name)
            border_chars = theme.get_border_chars()
            assert len(border_chars) == 8, (
                f"Theme '{theme_name}' border_chars length is {len(border_chars)}, "
                f"expected 8. Got: {repr(border_chars)}"
            )

    def test_all_themes_border_chars_type(self, all_theme_names):
        """Test all themes return border_chars as a string."""
        for theme_name in all_theme_names:
            theme = ThemeManager.load(theme_name)
            border_chars = theme.get_border_chars()
            assert isinstance(border_chars, str), (
                f"Theme '{theme_name}' border_chars is not a string, "
                f"got type: {type(border_chars)}"
            )


class TestBorderCharsFormat:
    """Test that border characters are printable and suitable for box drawing."""

    @pytest.fixture
    def all_theme_names(self):
        """Get all registered theme names."""
        return list(ThemeManager.list_themes().keys())

    def test_border_chars_are_printable(self, all_theme_names):
        """Test border characters are printable (not control characters)."""
        for theme_name in all_theme_names:
            theme = ThemeManager.load(theme_name)
            border_chars = theme.get_border_chars()

            for i, char in enumerate(border_chars):
                # Check that character is printable (not a control character)
                # ASCII printable range: 32-126
                # Unicode characters are allowed (ord > 127)
                char_code = ord(char)
                is_printable = char_code >= 32 and char_code != 127
                assert is_printable, (
                    f"Theme '{theme_name}' border character at position {i} "
                    f"is not printable: {repr(char)} (ord={char_code})"
                )

    def test_border_chars_are_single_characters(self, all_theme_names):
        """Test each border character is a single character, not a string."""
        for theme_name in all_theme_names:
            theme = ThemeManager.load(theme_name)
            border_chars = theme.get_border_chars()

            # When iterated, each should be a single character
            chars_list = list(border_chars)
            assert len(chars_list) == 8, (
                f"Theme '{theme_name}' border_chars should iterate as 8 single "
                f"characters, got {len(chars_list)}"
            )

            for i, char in enumerate(chars_list):
                assert len(char) == 1, (
                    f"Theme '{theme_name}' border character at position {i} "
                    f"is not a single character: {repr(char)}"
                )

    def test_border_chars_valid_encoding(self, all_theme_names):
        """Test border characters can be encoded/decoded as UTF-8."""
        for theme_name in all_theme_names:
            theme = ThemeManager.load(theme_name)
            border_chars = theme.get_border_chars()

            # Should be able to encode and decode without errors
            try:
                encoded = border_chars.encode('utf-8')
                decoded = encoded.decode('utf-8')
                assert decoded == border_chars, (
                    f"Theme '{theme_name}' border_chars encoding/decoding "
                    f"mismatch: {repr(border_chars)} != {repr(decoded)}"
                )
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                pytest.fail(
                    f"Theme '{theme_name}' border_chars cannot be encoded/decoded "
                    f"as UTF-8: {repr(border_chars)} - {e}"
                )


class TestBorderCharsConsistency:
    """Test that border characters work correctly with draw_box()."""

    @pytest.fixture
    def all_theme_names(self):
        """Get all registered theme names."""
        return list(ThemeManager.list_themes().keys())

    def test_border_chars_work_with_draw_box(
        self, mock_curses, mock_stdscr, all_theme_names
    ):
        """Test border characters work correctly when used by draw_box()."""
        for theme_name in all_theme_names:
            theme = ThemeManager.load(theme_name)
            theme.apply(mock_stdscr)

            # Should not raise ValueError about border character length
            try:
                theme.draw_box(mock_stdscr, 5, 10, 8, 40, title="Test")
            except ValueError as e:
                if "8 characters" in str(e):
                    pytest.fail(
                        f"Theme '{theme_name}' draw_box() raised ValueError "
                        f"about border character count: {e}"
                    )
                else:
                    # Re-raise if it's a different ValueError
                    raise

            # Verify drawing happened
            assert mock_stdscr.addstr.called, (
                f"Theme '{theme_name}' draw_box() did not call addstr"
            )

    def test_border_chars_parse_correctly(self, all_theme_names):
        """Test border characters can be unpacked into 8 components."""
        for theme_name in all_theme_names:
            theme = ThemeManager.load(theme_name)
            border_chars = theme.get_border_chars()

            # Should be able to unpack into 8 variables
            # This is what draw_box() does internally
            try:
                (
                    top_left,
                    top,
                    top_right,
                    left,
                    right,
                    bottom_left,
                    bottom,
                    bottom_right,
                ) = tuple(border_chars)
            except ValueError as e:
                pytest.fail(
                    f"Theme '{theme_name}' border_chars cannot be unpacked into "
                    f"8 components: {repr(border_chars)} - {e}"
                )

            # Each unpacked value should be a single character
            components = [
                top_left,
                top,
                top_right,
                left,
                right,
                bottom_left,
                bottom,
                bottom_right,
            ]
            for i, char in enumerate(components):
                assert len(char) == 1, (
                    f"Theme '{theme_name}' border component {i} is not a single "
                    f"character: {repr(char)}"
                )


class TestTheme3DDoubleBorderChars:
    """Test 3D themes' double border character validation."""

    @pytest.fixture
    def theme_3d_names(self):
        """Get all 3D theme names."""
        all_themes = ThemeManager.list_themes()
        theme_3d_names = []

        for theme_name in all_themes.keys():
            theme = ThemeManager.load(theme_name)
            if isinstance(theme, Theme3D):
                theme_3d_names.append(theme_name)

        return theme_3d_names

    def test_3d_themes_have_double_border_chars(self, theme_3d_names):
        """Test 3D themes implement get_double_border_chars()."""
        if not theme_3d_names:
            pytest.skip("No 3D themes registered")

        for theme_name in theme_3d_names:
            theme = ThemeManager.load(theme_name)
            assert hasattr(theme, 'get_double_border_chars'), (
                f"3D theme '{theme_name}' does not have get_double_border_chars() "
                "method"
            )

    def test_3d_themes_double_border_chars_length(self, theme_3d_names):
        """Test 3D themes return exactly 8 characters from get_double_border_chars()."""
        if not theme_3d_names:
            pytest.skip("No 3D themes registered")

        for theme_name in theme_3d_names:
            theme = ThemeManager.load(theme_name)
            double_border_chars = theme.get_double_border_chars()
            assert len(double_border_chars) == 8, (
                f"3D theme '{theme_name}' double_border_chars length is "
                f"{len(double_border_chars)}, expected 8. "
                f"Got: {repr(double_border_chars)}"
            )

    def test_3d_themes_double_border_chars_type(self, theme_3d_names):
        """Test 3D themes return double_border_chars as a string."""
        if not theme_3d_names:
            pytest.skip("No 3D themes registered")

        for theme_name in theme_3d_names:
            theme = ThemeManager.load(theme_name)
            double_border_chars = theme.get_double_border_chars()
            assert isinstance(double_border_chars, str), (
                f"3D theme '{theme_name}' double_border_chars is not a string, "
                f"got type: {type(double_border_chars)}"
            )

    def test_3d_themes_double_border_chars_printable(self, theme_3d_names):
        """Test 3D themes' double border characters are printable."""
        if not theme_3d_names:
            pytest.skip("No 3D themes registered")

        for theme_name in theme_3d_names:
            theme = ThemeManager.load(theme_name)
            double_border_chars = theme.get_double_border_chars()

            for i, char in enumerate(double_border_chars):
                char_code = ord(char)
                is_printable = char_code >= 32 and char_code != 127
                assert is_printable, (
                    f"3D theme '{theme_name}' double border character at "
                    f"position {i} is not printable: {repr(char)} "
                    f"(ord={char_code})"
                )


class TestBorderCharsExpectedFormat:
    """Test border characters follow expected format conventions."""

    @pytest.fixture
    def all_theme_names(self):
        """Get all registered theme names."""
        return list(ThemeManager.list_themes().keys())

    def test_border_chars_order_documented(self, all_theme_names):
        """
        Verify border characters are in documented order:
        top-left, top, top-right, left, right, bottom-left, bottom, bottom-right.
        """
        for theme_name in all_theme_names:
            theme = ThemeManager.load(theme_name)
            border_chars = theme.get_border_chars()

            # We can't know what the actual characters should be, but we can
            # verify they unpack in the expected order without error
            try:
                # This is the documented format from Theme.get_border_chars()
                (
                    top_left,
                    top,
                    top_right,
                    left,
                    right,
                    bottom_left,
                    bottom,
                    bottom_right,
                ) = tuple(border_chars)

                # Just verify we got 8 values
                assert all(
                    isinstance(c, str) for c in [
                        top_left, top, top_right, left, right,
                        bottom_left, bottom, bottom_right
                    ]
                ), (
                    f"Theme '{theme_name}' border_chars unpacked values are not "
                    "all strings"
                )
            except (ValueError, TypeError) as e:
                pytest.fail(
                    f"Theme '{theme_name}' border_chars cannot be unpacked in "
                    f"documented format: {e}"
                )

    def test_border_chars_no_newlines_or_tabs(self, all_theme_names):
        """Test border characters don't contain newlines or tabs."""
        for theme_name in all_theme_names:
            theme = ThemeManager.load(theme_name)
            border_chars = theme.get_border_chars()

            for i, char in enumerate(border_chars):
                assert char not in ['\n', '\r', '\t', '\v', '\f'], (
                    f"Theme '{theme_name}' border character at position {i} "
                    f"contains whitespace control character: {repr(char)}"
                )
