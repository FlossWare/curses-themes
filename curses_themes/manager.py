#!/usr/bin/env python3
"""
Theme management and registration system.

This module provides the ThemeManager singleton for loading, registering,
and managing available themes.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from pathlib import Path
from typing import Callable, Optional

from .theme import Theme


class ThemeManager:
    """
    Singleton manager for theme registration and loading.

    Provides a central registry for all available themes, including built-in
    themes and custom user themes. Themes are registered by name and can be
    loaded on demand.

    Example:
        ```python
        # Load a built-in theme
        theme = ThemeManager.load('dark')
        theme.apply(stdscr)

        # Register a custom theme
        ThemeManager.register(MyCustomTheme)
        theme = ThemeManager.load('my-custom-theme')

        # List all available themes
        for name, info in ThemeManager.list_themes().items():
            print(f"{name}: {info['description']}")
        ```

    Note:
        This is a singleton class. All methods are classmethods and operate
        on shared state. Do not instantiate this class.
    """

    # Registry of theme factories by normalized name (classes or callables)
    _themes: dict[str, Callable[[], Theme]] = {}

    # Cache of theme metadata (name, description, author) by normalized name
    _theme_metadata: dict[str, dict[str, str]] = {}

    # Currently active theme instance
    _current_theme: Optional[Theme] = None

    # Flag to track if built-in themes have been registered
    _builtin_registered: bool = False

    def __init__(self):
        """
        Prevent instantiation of singleton.

        Raises:
            TypeError: Always - this class should not be instantiated
        """
        raise TypeError(
            "ThemeManager is a singleton and should not be instantiated. "
            "Use ThemeManager.load(), ThemeManager.register(), etc."
        )

    @classmethod
    def _normalize_name(cls, name: str) -> str:
        """
        Normalize theme name for consistent lookup.

        Converts to lowercase and replaces spaces/underscores with hyphens.

        Args:
            name: Theme name to normalize

        Returns:
            Normalized theme name
        """
        return name.lower().replace(" ", "-").replace("_", "-")

    @classmethod
    def _register_builtin_themes(cls) -> None:
        """
        Register all built-in themes.

        This is called automatically on first use of load() or list_themes().
        Built-in themes are lazily loaded from the themes package.
        """
        if cls._builtin_registered:
            return

        # Import built-in themes
        # This is done lazily to avoid circular imports and to defer
        # loading themes until they're actually needed
        try:
            from .themes.borland3d import Borland3DTheme
            from .themes.catppuccin import CatppuccinTheme
            from .themes.dark import DarkTheme
            from .themes.dbase3 import DBase3Theme
            from .themes.dbase4 import DBase4Theme
            from .themes.dbase4_3d import DBase4_3DTheme
            from .themes.default import DefaultTheme
            from .themes.dos import DOSTheme
            from .themes.dracula import DraculaTheme
            from .themes.light import LightTheme
            from .themes.monokai import MonokaiTheme
            from .themes.nord import NordTheme
            from .themes.solarized_dark import SolarizedDarkTheme
            from .themes.solarized_light import SolarizedLightTheme
            from .themes.ti994a import TI994ATheme
            from .themes.trs80 import TRS80Theme
        except ImportError:
            pass
        else:
            cls.register(DefaultTheme, "default")
            cls.register(DarkTheme, "dark")
            cls.register(LightTheme, "light")
            cls.register(TI994ATheme, "ti-99-4a")
            cls.register(TRS80Theme, "trs-80")
            cls.register(DOSTheme, "dos")
            cls.register(DBase3Theme, "dbase-iii")
            cls.register(DBase4Theme, "dbase-iv")
            cls.register(Borland3DTheme, "borland-3d")
            cls.register(DBase4_3DTheme, "dbase-iv-3d")
            # Popular modern developer palettes
            cls.register(DraculaTheme, "dracula")
            cls.register(NordTheme, "nord")
            cls.register(SolarizedDarkTheme, "solarized-dark")
            cls.register(SolarizedLightTheme, "solarized-light")
            cls.register(MonokaiTheme, "monokai")
            cls.register(CatppuccinTheme, "catppuccin")

        cls._builtin_registered = True

    @classmethod
    def register(cls, theme_class: type[Theme], name: Optional[str] = None) -> None:
        """
        Register a theme class for use.

        Args:
            theme_class: Theme class (subclass of Theme) to register
            name: Optional custom name. If not provided, uses theme.name
                 from a temporary instance.

        Raises:
            TypeError: If theme_class is not a Theme subclass
            ValueError: If a theme with this name is already registered
        """
        if not isinstance(theme_class, type):
            raise TypeError(
                f"Expected a Theme class, got an instance of {type(theme_class).__name__}. "
                "Pass the class itself, not an instance: "
                f"ThemeManager.register({type(theme_class).__name__})"
            )

        if not issubclass(theme_class, Theme):
            raise TypeError(
                f"{theme_class.__name__} is not a Theme subclass. "
                "All themes must inherit from Theme."
            )

        if name is None:
            temp_instance = theme_class()  # type: ignore[call-arg]
            name = temp_instance.name
            cls._theme_metadata[cls._normalize_name(name)] = {
                "name": temp_instance.name,
                "description": temp_instance.description,
                "author": temp_instance.author,
            }
        else:
            normalized_name = cls._normalize_name(name)
            if normalized_name not in cls._theme_metadata:
                temp_instance = theme_class()  # type: ignore[call-arg]
                cls._theme_metadata[normalized_name] = {
                    "name": temp_instance.name,
                    "description": temp_instance.description,
                    "author": temp_instance.author,
                }

        normalized_name = cls._normalize_name(name)

        if normalized_name in cls._themes:
            existing = cls._themes[normalized_name]
            if existing != theme_class:
                raise ValueError(
                    f"Theme '{normalized_name}' is already registered. "
                    f"Use a different name or "
                    f"unregister the existing theme first."
                )
            return

        cls._themes[normalized_name] = theme_class

    @classmethod
    def unregister(cls, name: str) -> None:
        """Unregister a theme by name."""
        normalized_name = cls._normalize_name(name)

        if normalized_name not in cls._themes:
            raise KeyError(
                f"Theme '{normalized_name}' is not registered. "
                f"Available themes: {', '.join(cls._themes.keys())}"
            )

        factory = cls._themes[normalized_name]
        del cls._themes[normalized_name]

        if normalized_name in cls._theme_metadata:
            del cls._theme_metadata[normalized_name]

        if cls._current_theme is not None and (
            (isinstance(factory, type) and isinstance(cls._current_theme, factory))
            or cls._normalize_name(cls._current_theme.name) == normalized_name
        ):
            cls._current_theme = None

    @classmethod
    def load(cls, name: str) -> Theme:
        """Load a theme by name."""
        cls._register_builtin_themes()

        normalized_name = cls._normalize_name(name)

        if normalized_name not in cls._themes:
            available = ", ".join(sorted(cls._themes.keys()))
            raise KeyError(
                f"Theme '{normalized_name}' not found. Available themes: {available}"
            )

        factory = cls._themes[normalized_name]
        theme_instance = factory()  # type: ignore[call-arg]
        cls._current_theme = theme_instance
        return theme_instance

    @classmethod
    def load_from_file(cls, path: str, name: Optional[str] = None) -> Theme:
        """Load a theme from a configuration file and register it."""
        from .config_theme import load_theme_from_file

        theme = load_theme_from_file(path)

        registration_name = name if name is not None else theme.name
        normalized = cls._normalize_name(registration_name)

        cls._theme_metadata[normalized] = {
            "name": theme.name,
            "description": theme.description,
            "author": theme.author,
        }

        _path = path
        cls._themes[normalized] = lambda: load_theme_from_file(_path)
        cls._current_theme = theme
        return theme

    @classmethod
    def load_themes_from_directory(
        cls, directory: str, pattern: str = "*.json"
    ) -> int:
        """Load all matching theme files from a directory."""
        dir_path = Path(directory)
        count = 0

        for path in sorted(dir_path.glob(pattern)):
            if path.name == "schema.json":
                continue
            try:
                cls.load_from_file(str(path))
                count += 1
            except Exception:
                pass

        return count

    @classmethod
    def create(
        cls,
        name: str,
        color_map: dict[str, tuple[int, int, int]],
        *,
        component_colors: Optional[
            dict[str, tuple[tuple[int, int, int], tuple[int, int, int]]]
        ] = None,
        border_chars: Optional[str] = None,
        description: str = "",
        author: str = "",
        effects_3d: Optional[
            dict[str, tuple[tuple[int, int, int], tuple[int, int, int]]]
        ] = None,
        double_border_chars: Optional[str] = None,
        register: bool = True,
    ) -> Theme:
        """Create a theme from data and optionally register it."""
        if effects_3d is not None:
            from .theme3d import Theme3D

            theme = Theme3D(
                name,
                description,
                author,
                color_map=color_map,
                component_colors=component_colors,
                border_chars=border_chars,
                effects_3d=effects_3d,
                double_border_chars=double_border_chars,
            )
        else:
            theme = Theme(
                name,
                description,
                author,
                color_map=color_map,
                component_colors=component_colors,
                border_chars=border_chars,
            )

        if register:
            normalized = cls._normalize_name(name)
            cls._theme_metadata[normalized] = {
                "name": name,
                "description": description,
                "author": author,
            }
            cls._themes[normalized] = lambda: type(theme)(
                name,
                description,
                author,
                color_map=color_map,
                component_colors=component_colors,
                border_chars=border_chars,
                **(
                    {
                        "effects_3d": effects_3d,
                        "double_border_chars": double_border_chars,
                    }
                    if effects_3d is not None
                    else {}
                ),
            )

        cls._current_theme = theme
        return theme

    @classmethod
    def list_themes(cls) -> dict[str, dict[str, str]]:
        """List all registered themes with metadata."""
        cls._register_builtin_themes()

        result = {}
        for normalized_name in sorted(cls._themes.keys()):
            if normalized_name in cls._theme_metadata:
                result[normalized_name] = cls._theme_metadata[normalized_name].copy()
            else:
                theme_class = cls._themes[normalized_name]
                temp_instance = theme_class()  # type: ignore[call-arg]
                metadata = {
                    "name": temp_instance.name,
                    "description": temp_instance.description,
                    "author": temp_instance.author,
                }
                cls._theme_metadata[normalized_name] = metadata
                result[normalized_name] = metadata.copy()

        return result

    @classmethod
    def get_current(cls) -> Optional[Theme]:
        """Get the currently active theme."""
        return cls._current_theme

    @classmethod
    def reset(cls) -> None:
        """Reset the theme manager state."""
        cls._themes.clear()
        cls._theme_metadata.clear()
        cls._current_theme = None
        cls._builtin_registered = False

    @classmethod
    def __repr__(cls) -> str:
        """String representation for debugging."""
        theme_count = len(cls._themes)
        current = cls._current_theme.name if cls._current_theme else "None"
        return f"ThemeManager(themes={theme_count}, current='{current}')"
