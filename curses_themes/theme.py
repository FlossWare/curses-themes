#!/usr/bin/env python3
"""
Theme base classes and semantic color support for curses applications.

This module provides the core Theme abstraction and SemanticColors container
that enable pluggable theming for Python curses applications.

Copyright (C) 2024 FlossWare

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import contextlib
import curses
import unicodedata
from abc import ABC, abstractmethod
from typing import Optional


def _calculate_display_width(text: str) -> int:
    """Calculate the display width of text accounting for CJK characters.

    Uses unicodedata.east_asian_width() to properly handle double-width
    CJK (Chinese, Japanese, Korean) characters and other wide Unicode
    characters that occupy two terminal columns.

    Args:
        text: The text string to measure

    Returns:
        Display width in terminal columns

    Example:
        >>> _calculate_display_width('Hello')  # ASCII
        5
        >>> _calculate_display_width('こんにちは')  # Japanese
        10
        >>> _calculate_display_width('你好世界')  # Chinese
        8
    """
    width = 0
    for char in text:
        ea_width = unicodedata.east_asian_width(char)
        # 'F' (Fullwidth) and 'W' (Wide) take 2 columns
        # 'H' (Halfwidth), 'Na' (Narrow), 'N' (Neutral), 'A' (Ambiguous) take 1 column
        if ea_width in ("F", "W"):
            width += 2
        else:
            width += 1
    return width


class ColorPair:
    """Represents a foreground/background color pair."""

    def __init__(
        self, foreground: tuple[int, int, int], background: tuple[int, int, int]
    ):
        self.foreground = foreground
        self.background = background

    def __repr__(self):
        return f"ColorPair(fg={self.foreground}, bg={self.background})"


class ComponentColors:
    """
    Container for component-based color pairs used by themes.

    Provides the component-based API that matches curses-java Theme interface.
    This is the primary API for widget rendering.

    Attributes:
        background: Normal background color pair
        button: Button in normal state
        button_focused: Button when focused
        text_input: Text input fields
        border: Borders and frames
        selection: Selected/highlighted items
        disabled: Disabled components
    """

    def __init__(
        self,
        background: int,
        button: int,
        button_focused: int,
        text_input: int,
        border: int,
        selection: int,
        disabled: int,
    ):
        """
        Initialize component color pairs.

        Args:
            background: Curses color pair number for normal background
            button: Curses color pair number for buttons
            button_focused: Curses color pair number for focused buttons
            text_input: Curses color pair number for text input
            border: Curses color pair number for borders
            selection: Curses color pair number for selections
            disabled: Curses color pair number for disabled components
        """
        self.background = background
        self.button = button
        self.button_focused = button_focused
        self.text_input = text_input
        self.border = border
        self.selection = selection
        self.disabled = disabled

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"ComponentColors(background={self.background}, button={self.button}, "
            f"button_focused={self.button_focused}, text_input={self.text_input}, "
            f"border={self.border}, selection={self.selection}, disabled={self.disabled})"
        )


class SemanticColors:
    """
    Container for semantic color pairs used by themes.

    Provides named access to curses color pair numbers for common UI elements.
    This allows themes to define colors by purpose (e.g., 'error', 'success')
    rather than by arbitrary pair numbers.

    Attributes:
        primary: Main UI color for highlights and focus
        success: Positive feedback and successful operations
        error: Error messages and critical warnings
        warning: Caution messages and non-critical warnings
        info: Informational messages and help text
        background: Default background color
        foreground: Default text color
        accent: Secondary highlight color
    """

    def __init__(
        self,
        primary: int,
        success: int,
        error: int,
        warning: int,
        info: int,
        background: int,
        foreground: int,
        accent: int,
    ):
        """
        Initialize semantic color pairs.

        Args:
            primary: Curses color pair number for primary UI elements
            success: Curses color pair number for success messages
            error: Curses color pair number for error messages
            warning: Curses color pair number for warning messages
            info: Curses color pair number for info messages
            background: Curses color pair number for default background
            foreground: Curses color pair number for default foreground
            accent: Curses color pair number for accent elements
        """
        self.primary = primary
        self.success = success
        self.error = error
        self.warning = warning
        self.info = info
        self.background = background
        self.foreground = foreground
        self.accent = accent

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"SemanticColors(primary={self.primary}, success={self.success}, "
            f"error={self.error}, warning={self.warning}, info={self.info}, "
            f"background={self.background}, foreground={self.foreground}, "
            f"accent={self.accent})"
        )


class Theme(ABC):
    """
    Abstract base class for curses themes.

    Themes define the visual appearance of a curses application by mapping
    semantic colors to RGB values. Subclasses must implement get_color_map()
    to provide the color definitions.

    Example:
        ```python
        class MyTheme(Theme):
            def __init__(self):
                super().__init__(
                    name="My Theme",
                    description="A custom theme",
                    author="Your Name"
                )

            def get_color_map(self):
                return {
                    'background': (0, 0, 0),
                    'foreground': (255, 255, 255),
                    'primary': (0, 120, 215),
                    'success': (16, 124, 16),
                    'error': (232, 17, 35),
                    'warning': (193, 156, 0),
                    'info': (0, 120, 212),
                    'accent': (142, 68, 173),
                }
        ```

    Attributes:
        name: Human-readable theme name
        description: Brief description of the theme
        author: Theme creator's name
        colors: SemanticColors instance (available after apply())
    """

    def __init__(self, name: str, description: str = "", author: str = ""):
        """
        Initialize theme metadata.

        Args:
            name: Human-readable theme name
            description: Brief description of the theme's appearance or purpose
            author: Name of the theme creator
        """
        self.name = name
        self.description = description
        self.author = author
        self._colors: Optional[SemanticColors] = None
        self._components: Optional[ComponentColors] = None

    @abstractmethod
    def get_color_map(self) -> dict[str, tuple[int, int, int]]:
        """
        Get RGB color definitions for this theme.

        Must return a dictionary mapping semantic color names to RGB tuples.
        Required keys: background, foreground, primary, success, error,
        warning, info, accent.

        Returns:
            Dictionary mapping color names to (R, G, B) tuples where each
            component is 0-255

        Example:
            ```python
            {
                'background': (0, 0, 0),
                'foreground': (255, 255, 255),
                'primary': (0, 120, 215),
                'success': (16, 124, 16),
                'error': (232, 17, 35),
                'warning': (193, 156, 0),
                'info': (0, 120, 212),
                'accent': (142, 68, 173),
            }
            ```
        """
        pass

    def get_background(self) -> Optional[ColorPair]:
        """
        Get the background color pair for normal components.

        Returns:
            ColorPair with foreground and background RGB values, or None if not implemented
        """
        return None

    def get_button(self) -> Optional[ColorPair]:
        """
        Get the color pair for buttons in normal state.

        Returns:
            ColorPair for button rendering, or None if not implemented
        """
        return None

    def get_button_focused(self) -> Optional[ColorPair]:
        """
        Get the color pair for buttons when focused.

        Returns:
            ColorPair for focused button rendering, or None if not implemented
        """
        return None

    def get_text_input(self) -> Optional[ColorPair]:
        """
        Get the color pair for text input fields.

        Returns:
            ColorPair for text input rendering, or None if not implemented
        """
        return None

    def get_border(self) -> Optional[ColorPair]:
        """
        Get the color pair for borders and frames.

        Returns:
            ColorPair for border rendering, or None if not implemented
        """
        return None

    def get_selection(self) -> Optional[ColorPair]:
        """
        Get the color pair for selected/highlighted items.

        Returns:
            ColorPair for selection rendering, or None if not implemented
        """
        return None

    def get_disabled(self) -> Optional[ColorPair]:
        """
        Get the color pair for disabled components.

        Returns:
            ColorPair for disabled component rendering, or None if not implemented
        """
        return None

    def get_border_chars(self) -> str:
        """
        Get border characters for drawing boxes.

        Override this method to provide custom border styles (e.g., Unicode
        box-drawing characters for modern terminals).

        Returns:
            String with 8 characters in order:
            top-left, top, top-right, left, right, bottom-left, bottom, bottom-right
            Default: "+-+||+-+" (ASCII box)
            Unicode example: "┌─┐│└─┘│"

        Note:
            This matches the Java Theme.getBorderChars() format for API compatibility.
        """
        return "+-+||+-+"

    def _validate_stdscr(self, stdscr, operation: str) -> None:
        """
        Validate stdscr is alive and usable.

        Args:
            stdscr: The curses window to validate
            operation: Description of operation for error message

        Raises:
            RuntimeError: If stdscr appears to be dead/ended
        """
        try:
            # Try to get window size - will fail if stdscr is dead
            stdscr.getmaxyx()
        except (AttributeError, curses.error) as e:
            raise RuntimeError(
                f"Cannot {operation} - curses window is no longer valid.\n"
                f"This usually happens after curses.endwin() or when used outside curses.wrapper().\n"
                f"Ensure theme operations happen within the curses.wrapper() callback.\n"
                f"Original error: {e}"
            )

    def apply(self, stdscr) -> None:
        """
        Apply this theme to a curses screen.

        Initializes color pairs and sets up the theme for use. Must be called
        before using theme.colors, theme.components, or theme.draw_box().

        Args:
            stdscr: Curses window object (typically from curses.wrapper)

        Raises:
            RuntimeError: If color initialization fails
        """
        from .colors import ColorManager

        # Validate stdscr is alive
        self._validate_stdscr(stdscr, "apply theme")

        # Initialize colors using the color manager
        color_manager = ColorManager(stdscr)
        self._colors, self._components = color_manager.initialize_theme(self)

        # Set default screen colors
        stdscr.bkgd(" ", curses.color_pair(self._components.background))

    @property
    def colors(self) -> SemanticColors:
        """
        Get semantic color pairs for this theme.

        This is the legacy API maintained for backward compatibility.
        New code should use the component-based methods instead.

        Returns:
            SemanticColors instance with initialized color pair numbers.
            Each attribute (primary, success, error, etc.) is an integer that
            must be wrapped with curses.color_pair() when used with curses
            display functions.

        Raises:
            RuntimeError: If apply() has not been called yet

        Example:
            >>> theme.apply(stdscr)
            >>> # Correct usage - wrap with curses.color_pair()
            >>> stdscr.addstr(0, 0, "Success!", curses.color_pair(theme.colors.success))
            >>> # Wrong - missing wrapper will not display correctly
            >>> stdscr.addstr(0, 0, "Error!", theme.colors.error)  # DON'T DO THIS
        """
        if self._colors is None:
            raise RuntimeError(
                f"Theme '{self.name}' colors not available - apply() must be called first.\n"
                f"Correct usage:\n"
                f"  theme = ThemeManager.load('{self.name.lower()}')\n"
                f"  theme.apply(stdscr)  # Initialize colors\n"
                f"  stdscr.addstr(0, 0, 'text', curses.color_pair(theme.colors.primary))"
            )
        return self._colors

    @property
    def components(self) -> ComponentColors:
        """
        Get component-based color pairs for this theme.

        This is the primary API matching curses-java Theme interface.

        Returns:
            ComponentColors instance with initialized color pair numbers.
            Each attribute (button, border, text_input, etc.) is an integer that
            must be wrapped with curses.color_pair() when used with curses
            display functions.

        Raises:
            RuntimeError: If apply() has not been called yet

        Example:
            >>> theme.apply(stdscr)
            >>> # Correct usage - wrap with curses.color_pair()
            >>> stdscr.addstr(0, 0, "[OK]", curses.color_pair(theme.components.button))
            >>> # Wrong - missing wrapper will not display correctly
            >>> stdscr.addstr(0, 0, "[OK]", theme.components.button)  # DON'T DO THIS
        """
        if self._components is None:
            raise RuntimeError(
                f"Theme '{self.name}' components not available - apply() must be called first.\n"
                f"Correct usage:\n"
                f"  theme = ThemeManager.load('{self.name.lower()}')\n"
                f"  theme.apply(stdscr)  # Initialize components\n"
                f"  stdscr.addstr(0, 0, 'Button', curses.color_pair(theme.components.button))"
            )
        return self._components

    def draw_box(
        self,
        window,
        y: int,
        x: int,
        height: int,
        width: int,
        title: str = "",
        color_pair: Optional[int] = None,
    ) -> None:
        """
        Draw a themed border box on the given window.

        Args:
            window: Curses window to draw on
            y: Top-left Y coordinate
            x: Top-left X coordinate
            height: Box height in characters
            width: Box width in characters
            title: Optional title to display centered in top border
            color_pair: Color pair number to use (defaults to border color)

        Raises:
            ValueError: If box dimensions are too small
        """
        # Validate window is alive
        self._validate_stdscr(window, "draw box")

        if height < 2 or width < 2:
            raise ValueError(
                f"Box dimensions too small: {height}x{width}. Minimum is 2x2."
            )

        # Use border color if none specified
        if color_pair is None:
            color_pair = self.components.border

        border_chars = self.get_border_chars()
        if len(border_chars) != 8:
            raise ValueError(
                f"get_border_chars() must return 8 characters, got {len(border_chars)}"
            )

        # Parse border characters: TL T TR L R BL B BR
        top_left, top, top_right, left, right, bottom_left, bottom, bottom_right = (
            tuple(border_chars)
        )

        attr = curses.color_pair(color_pair)

        # Draw corners
        try:
            window.addstr(y, x, top_left, attr)
            window.addstr(y, x + width - 1, top_right, attr)
            window.addstr(y + height - 1, x, bottom_left, attr)
            window.addstr(y + height - 1, x + width - 1, bottom_right, attr)
        except curses.error:
            # Ignore errors at screen boundaries
            pass

        # Draw horizontal borders
        for i in range(1, width - 1):
            try:
                window.addstr(y, x + i, top, attr)
                window.addstr(y + height - 1, x + i, bottom, attr)
            except curses.error:
                pass

        # Draw vertical borders
        for i in range(1, height - 1):
            try:
                window.addstr(y + i, x, left, attr)
                window.addstr(y + i, x + width - 1, right, attr)
            except curses.error:
                pass

        # Draw title if provided
        if title:
            # Calculate display width accounting for CJK/wide characters
            title_display_width = _calculate_display_width(title)
            if width > title_display_width + 4:
                title_x = x + (width - title_display_width - 2) // 2
                with contextlib.suppress(curses.error):
                    window.addstr(y, title_x, f" {title} ", attr)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Theme(name='{self.name}', author='{self.author}')"
