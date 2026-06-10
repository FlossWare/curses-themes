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

from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional
import curses


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
        accent: int
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

    @abstractmethod
    def get_color_map(self) -> Dict[str, Tuple[int, int, int]]:
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

    def get_border_chars(self) -> Dict[str, str]:
        """
        Get border characters for drawing boxes.

        Override this method to provide custom border styles (e.g., Unicode
        box-drawing characters for modern terminals).

        Returns:
            Dictionary with keys: horizontal, vertical, top_left, top_right,
            bottom_left, bottom_right. Default uses ASCII characters.
        """
        return {
            'horizontal': '-',
            'vertical': '|',
            'top_left': '+',
            'top_right': '+',
            'bottom_left': '+',
            'bottom_right': '+',
        }

    def apply(self, stdscr) -> None:
        """
        Apply this theme to a curses screen.

        Initializes color pairs and sets up the theme for use. Must be called
        before using theme.colors or theme.draw_box().

        Args:
            stdscr: Curses window object (typically from curses.wrapper)

        Raises:
            RuntimeError: If color initialization fails
        """
        from .colors import ColorManager

        # Initialize colors using the color manager
        color_manager = ColorManager(stdscr)
        self._colors = color_manager.initialize_theme(self)

        # Set default screen colors
        stdscr.bkgd(' ', curses.color_pair(self._colors.background))

    @property
    def colors(self) -> SemanticColors:
        """
        Get semantic color pairs for this theme.

        Returns:
            SemanticColors instance with initialized color pairs

        Raises:
            RuntimeError: If apply() has not been called yet
        """
        if self._colors is None:
            raise RuntimeError(
                f"Theme '{self.name}' has not been applied. "
                "Call theme.apply(stdscr) first."
            )
        return self._colors

    def draw_box(
        self,
        window,
        y: int,
        x: int,
        height: int,
        width: int,
        title: str = "",
        color_pair: Optional[int] = None
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
            color_pair: Color pair number to use (defaults to primary)

        Raises:
            ValueError: If box dimensions are too small
        """
        if height < 2 or width < 2:
            raise ValueError(
                f"Box dimensions too small: {height}x{width}. "
                "Minimum is 2x2."
            )

        # Use primary color if none specified
        if color_pair is None:
            color_pair = self.colors.primary

        chars = self.get_border_chars()
        attr = curses.color_pair(color_pair)

        # Draw corners
        try:
            window.addstr(y, x, chars['top_left'], attr)
            window.addstr(y, x + width - 1, chars['top_right'], attr)
            window.addstr(y + height - 1, x, chars['bottom_left'], attr)
            window.addstr(y + height - 1, x + width - 1, chars['bottom_right'], attr)
        except curses.error:
            # Ignore errors at screen boundaries
            pass

        # Draw horizontal borders
        for i in range(1, width - 1):
            try:
                window.addstr(y, x + i, chars['horizontal'], attr)
                window.addstr(y + height - 1, x + i, chars['horizontal'], attr)
            except curses.error:
                pass

        # Draw vertical borders
        for i in range(1, height - 1):
            try:
                window.addstr(y + i, x, chars['vertical'], attr)
                window.addstr(y + i, x + width - 1, chars['vertical'], attr)
            except curses.error:
                pass

        # Draw title if provided
        if title and width > len(title) + 4:
            title_x = x + (width - len(title) - 2) // 2
            try:
                window.addstr(y, title_x, f" {title} ", attr)
            except curses.error:
                pass

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Theme(name='{self.name}', author='{self.author}')"
