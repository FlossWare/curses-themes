#!/usr/bin/env python3
"""
Config-driven theme support for curses-themes.

This module enables loading themes from configuration files (JSON, XML, YAML)
rather than requiring Python subclasses. Theme definitions are parsed into a
canonical dictionary format, validated, and used to construct ConfigTheme or
ConfigTheme3D instances.

Supported formats:
    - JSON (.json) -- uses stdlib ``json`` module (zero dependencies)
    - XML (.xml) -- uses stdlib ``xml.etree.ElementTree`` (zero dependencies)
    - YAML (.yaml, .yml) -- requires optional ``PyYAML`` package

Example:
    Loading a theme from a JSON file::

        from curses_themes.config_theme import load_theme_from_file

        theme = load_theme_from_file("my_theme.json")
        theme.apply(stdscr)

    Loading from a config dict directly::

        from curses_themes.config_theme import ConfigTheme

        config = {
            "name": "My Theme",
            "colors": {
                "background": [0, 0, 0],
                "foreground": [255, 255, 255],
                "primary": [0, 120, 215],
                "success": [16, 124, 16],
                "error": [232, 17, 35],
                "warning": [193, 156, 0],
                "info": [0, 120, 212],
                "accent": [142, 68, 173],
            },
        }
        theme = ConfigTheme(config)

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

import json
import pathlib
import xml.etree.ElementTree as ET
from typing import Union

try:
    import defusedxml.ElementTree as _safe_ET
except ImportError:
    _safe_ET = None

from .theme import Theme
from .theme3d import Theme3D

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The 8 required semantic color keys in a theme's color map.
REQUIRED_COLOR_KEYS = frozenset(
    {
        "background",
        "foreground",
        "primary",
        "success",
        "error",
        "warning",
        "info",
        "accent",
    }
)

#: Valid component names for the ``components`` section.
VALID_COMPONENT_KEYS = frozenset(
    {
        "background",
        "button",
        "button_focused",
        "text_input",
        "border",
        "selection",
        "disabled",
    }
)

#: Required keys when a ``3d`` section is present.
REQUIRED_3D_KEYS = frozenset({"shadow", "highlight", "lowlight"})

#: Standard ncurses color names mapped to full-brightness RGB tuples.
NCURSES_COLOR_MAP: dict[str, tuple[int, int, int]] = {
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "YELLOW": (255, 255, 0),
    "BLUE": (0, 0, 255),
    "MAGENTA": (255, 0, 255),
    "CYAN": (0, 255, 255),
    "WHITE": (255, 255, 255),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_rgb(value: Union[list, tuple, str]) -> tuple[int, int, int]:
    """
    Parse an RGB value from various formats into an ``(r, g, b)`` tuple.

    Accepts:
        - A list or tuple of 3 integers: ``[0, 255, 128]`` or ``(0, 255, 128)``
        - A comma-separated string: ``"0, 255, 128"`` or ``"0,255,128"``

    Args:
        value: RGB value in any supported format

    Returns:
        Tuple of (red, green, blue) integers, each 0-255

    Raises:
        ValueError: If the value cannot be parsed as a valid RGB color
    """
    if isinstance(value, (list, tuple)):
        if len(value) != 3:
            raise ValueError(
                f"RGB color must have exactly 3 components, got {len(value)}: {value}"
            )
        r, g, b = int(value[0]), int(value[1]), int(value[2])
    elif isinstance(value, str):
        parts = [p.strip() for p in value.split(",")]
        if len(parts) != 3:
            raise ValueError(
                f"RGB string must have 3 comma-separated values, "
                f"got {len(parts)}: {value!r}"
            )
        try:
            r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
        except ValueError as e:
            raise ValueError(
                f"RGB string contains non-integer values: {value!r}"
            ) from e
    else:
        raise ValueError(
            f"RGB color must be a list, tuple, or comma-separated string, "
            f"got {type(value).__name__}: {value!r}"
        )

    for name, component in [("red", r), ("green", g), ("blue", b)]:
        if not 0 <= component <= 255:
            raise ValueError(
                f"RGB {name} component must be 0-255, got {component} in {value}"
            )

    return (r, g, b)


def _validate_color_pair_dict(pair_dict: dict, context: str) -> list[str]:
    """
    Validate that a dict has ``foreground`` and ``background`` RGB values.

    Args:
        pair_dict: Dictionary expected to have ``foreground`` and ``background`` keys
        context: Description of where this color pair appears (for error messages)

    Returns:
        List of error message strings (empty if valid)
    """
    errors: list[str] = []
    if not isinstance(pair_dict, dict):
        errors.append(f"{context}: expected a dict, got {type(pair_dict).__name__}")
        return errors

    for key in ("foreground", "background"):
        if key not in pair_dict:
            errors.append(f"{context}: missing '{key}' key")
        else:
            try:
                _parse_rgb(pair_dict[key])
            except ValueError as e:
                errors.append(f"{context}.{key}: {e}")

    return errors


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_config(config: dict) -> None:
    """
    Validate a theme configuration dictionary.

    Checks that all required fields are present and correctly typed. Collects
    all validation errors and raises a single ``ValueError`` listing them all.

    Args:
        config: Theme configuration dictionary to validate

    Raises:
        ValueError: If any validation errors are found, with a message
            listing all problems

    Validated fields:
        - ``name``: Required, must be a non-empty string
        - ``colors``: Required dict with all 8 semantic color keys,
          each a valid RGB value
        - ``border_chars``: Optional, must be exactly 8 characters if present
        - ``components``: Optional dict; each value must have
          ``foreground``/``background`` RGB entries
        - ``3d``: Optional dict; if present, ``shadow``/``highlight``/``lowlight``
          are required ColorPair dicts
    """
    if not isinstance(config, dict):
        raise ValueError(f"Theme config must be a dict, got {type(config).__name__}")

    errors: list[str] = []

    # 1. name -- required, non-empty string
    if "name" not in config:
        errors.append("Missing required field: 'name'")
    elif not isinstance(config["name"], str):
        errors.append(f"'name' must be a string, got {type(config['name']).__name__}")
    elif not config["name"].strip():
        errors.append("'name' must be a non-empty string")

    # 2. colors -- required, dict with 8 keys
    if "colors" not in config:
        errors.append(
            "Missing required field: 'colors'. "
            "Must contain all 8 semantic colors: "
            f"{', '.join(sorted(REQUIRED_COLOR_KEYS))}"
        )
    elif not isinstance(config["colors"], dict):
        errors.append(f"'colors' must be a dict, got {type(config['colors']).__name__}")
    else:
        missing_colors = REQUIRED_COLOR_KEYS - set(config["colors"].keys())
        if missing_colors:
            errors.append(
                f"Missing required colors: {', '.join(sorted(missing_colors))}"
            )
        for key in sorted(REQUIRED_COLOR_KEYS & set(config["colors"].keys())):
            try:
                _parse_rgb(config["colors"][key])
            except ValueError as e:
                errors.append(f"colors.{key}: {e}")

    # 3. border_chars -- optional, exactly 8 characters
    if "border_chars" in config:
        bc = config["border_chars"]
        if not isinstance(bc, str):
            errors.append(f"'border_chars' must be a string, got {type(bc).__name__}")
        elif len(bc) != 8:
            errors.append(
                f"'border_chars' must be exactly 8 characters, got {len(bc)}: {bc!r}"
            )

    # 4. components -- optional, dict of color pairs
    if "components" in config:
        comps = config["components"]
        if not isinstance(comps, dict):
            errors.append(f"'components' must be a dict, got {type(comps).__name__}")
        else:
            for comp_name in sorted(comps.keys()):
                if comp_name not in VALID_COMPONENT_KEYS:
                    errors.append(
                        f"Unknown component '{comp_name}'. "
                        f"Valid components: {', '.join(sorted(VALID_COMPONENT_KEYS))}"
                    )
                else:
                    errors.extend(
                        _validate_color_pair_dict(
                            comps[comp_name], f"components.{comp_name}"
                        )
                    )

    # 5. 3d section -- optional, but shadow/highlight/lowlight required if present
    if "3d" in config:
        td = config["3d"]
        if not isinstance(td, dict):
            errors.append(f"'3d' must be a dict, got {type(td).__name__}")
        else:
            missing_3d = REQUIRED_3D_KEYS - set(td.keys())
            if missing_3d:
                errors.append(
                    f"3D section missing required keys: "
                    f"{', '.join(sorted(missing_3d))}. "
                    f"A 3D theme must define shadow, highlight, "
                    f"and lowlight color pairs."
                )
            for key in sorted(REQUIRED_3D_KEYS & set(td.keys())):
                errors.extend(_validate_color_pair_dict(td[key], f"3d.{key}"))

            # shadow offsets
            for offset_key in ("shadow_offset_x", "shadow_offset_y"):
                if offset_key in td:
                    val = td[offset_key]
                    if not isinstance(val, int):
                        errors.append(
                            f"3d.{offset_key} must be an integer, "
                            f"got {type(val).__name__}"
                        )
                    elif val < 0:
                        errors.append(
                            f"3d.{offset_key} must be non-negative, got {val}"
                        )

            # double_border_chars
            if "double_border_chars" in td:
                dbc = td["double_border_chars"]
                if not isinstance(dbc, str):
                    errors.append(
                        f"3d.double_border_chars must be a string, "
                        f"got {type(dbc).__name__}"
                    )
                elif len(dbc) != 8:
                    errors.append(
                        f"3d.double_border_chars must be exactly 8 characters, "
                        f"got {len(dbc)}: {dbc!r}"
                    )

    # Raise a single error with all problems
    if errors:
        error_list = "\n  - ".join(errors)
        raise ValueError(
            f"Theme configuration has {len(errors)} error(s):\n  - {error_list}"
        )


# ---------------------------------------------------------------------------
# ConfigTheme -- basic config-driven theme
# ---------------------------------------------------------------------------


class ConfigTheme(Theme):
    """
    Concrete Theme subclass driven by a configuration dictionary.

    Instead of subclassing Theme and hard-coding colors, ConfigTheme reads
    all values from a validated dictionary. This enables themes to be loaded
    from JSON, XML, YAML, or any other source that can produce a dict.

    The config dict must follow the canonical schema::

        {
            "name": "My Theme",                   # required
            "description": "A custom theme",       # optional, default ""
            "author": "Someone",                   # optional, default ""
            "colors": {                            # required, all 8 keys
                "background": [0, 0, 0],
                "foreground": [255, 255, 255],
                "primary": [0, 120, 215],
                "success": [16, 124, 16],
                "error": [232, 17, 35],
                "warning": [193, 156, 0],
                "info": [0, 120, 212],
                "accent": [142, 68, 173],
            },
            "border_chars": "+-+||+-+",            # optional
            "components": {                        # optional
                "background": {
                    "foreground": [255, 255, 255],
                    "background": [0, 0, 0],
                },
                ...
            },
        }

    Example:
        >>> config = {
        ...     "name": "Ocean",
        ...     "colors": {
        ...         "background": [0, 20, 40],
        ...         "foreground": [200, 220, 255],
        ...         "primary": [0, 120, 215],
        ...         "success": [16, 180, 16],
        ...         "error": [232, 60, 60],
        ...         "warning": [200, 180, 0],
        ...         "info": [100, 180, 255],
        ...         "accent": [0, 200, 200],
        ...     },
        ... }
        >>> theme = ConfigTheme(config)
        >>> theme.name
        'Ocean'

    Attributes:
        name: Human-readable theme name (from config)
        description: Theme description (from config, default "")
        author: Theme author (from config, default "")
    """

    def __init__(self, config: dict):
        """
        Initialize a config-driven theme.

        Args:
            config: Validated theme configuration dictionary. Must contain
                at minimum ``name`` and ``colors`` with all 8 required keys.

        Raises:
            ValueError: If the config is missing required fields or has
                invalid values
        """
        validate_config(config)

        color_map = {key: _parse_rgb(value) for key, value in config["colors"].items()}

        component_colors = None
        if "components" in config:
            component_colors = {
                name: (_parse_rgb(c["foreground"]), _parse_rgb(c["background"]))
                for name, c in config["components"].items()
            }

        super().__init__(
            name=config["name"],
            description=config.get("description", ""),
            author=config.get("author", ""),
            color_map=color_map,
            component_colors=component_colors,
            border_chars=config.get("border_chars"),
        )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"ConfigTheme(name='{self.name}', author='{self.author}')"


# ---------------------------------------------------------------------------
# ConfigTheme3D -- 3D config-driven theme
# ---------------------------------------------------------------------------


class ConfigTheme3D(Theme3D):
    """
    Concrete Theme3D subclass driven by a configuration dictionary.

    Extends the 3D theme system with shadow, highlight, and lowlight colors
    read from a configuration dict rather than hard-coded in a subclass.

    The config dict must include a ``"3d"`` section with at minimum
    ``shadow``, ``highlight``, and ``lowlight`` color pairs::

        {
            "name": "My 3D Theme",
            "colors": { ... },           # same as ConfigTheme
            "3d": {
                "shadow": {
                    "foreground": [0, 0, 0],
                    "background": [0, 0, 0],
                },
                "highlight": {
                    "foreground": [255, 255, 255],
                    "background": [200, 200, 200],
                },
                "lowlight": {
                    "foreground": [64, 64, 64],
                    "background": [200, 200, 200],
                },
                "shadow_offset_x": 2,    # optional, default 2
                "shadow_offset_y": 1,    # optional, default 1
                "double_border_chars": "...",  # optional
            },
        }

    Attributes:
        shadow_offset_x: Horizontal shadow offset (from config or default 2)
        shadow_offset_y: Vertical shadow offset (from config or default 1)
    """

    def __init__(self, config: dict):
        """
        Initialize a 3D config-driven theme.

        Args:
            config: Validated theme configuration dictionary. Must contain
                ``name``, ``colors``, and a ``3d`` section with ``shadow``,
                ``highlight``, and ``lowlight`` color pairs.

        Raises:
            ValueError: If the config is missing required fields, has
                invalid values, or lacks the ``3d`` section
        """
        if not isinstance(config, dict) or "3d" not in config:
            raise ValueError(
                "ConfigTheme3D requires a '3d' section in the config dict.\n"
                "The '3d' section must contain shadow, highlight, and lowlight "
                "color pairs.\n"
                "Example:\n"
                '  "3d": {\n'
                '      "shadow": {"foreground": [0,0,0], "background": [0,0,0]},\n'
                '      "highlight": {"foreground": [255,255,255], '
                '"background": [200,200,200]},\n'
                '      "lowlight": {"foreground": [64,64,64], '
                '"background": [200,200,200]}\n'
                "  }"
            )
        validate_config(config)

        color_map = {key: _parse_rgb(value) for key, value in config["colors"].items()}

        component_colors = None
        if "components" in config:
            component_colors = {
                name: (_parse_rgb(c["foreground"]), _parse_rgb(c["background"]))
                for name, c in config["components"].items()
            }

        td = config["3d"]
        effects_3d = {
            key: (_parse_rgb(td[key]["foreground"]), _parse_rgb(td[key]["background"]))
            for key in ("shadow", "highlight", "lowlight")
            if key in td
        }

        super().__init__(
            name=config["name"],
            description=config.get("description", ""),
            author=config.get("author", ""),
            color_map=color_map,
            component_colors=component_colors,
            border_chars=config.get("border_chars"),
            effects_3d=effects_3d,
            double_border_chars=td.get("double_border_chars"),
        )

        if "shadow_offset_x" in td:
            self.shadow_offset_x = td["shadow_offset_x"]
        if "shadow_offset_y" in td:
            self.shadow_offset_y = td["shadow_offset_y"]

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"ConfigTheme3D(name='{self.name}', "
            f"shadow_offset=({self.shadow_offset_x}, {self.shadow_offset_y}))"
        )


# ---------------------------------------------------------------------------
# XML parsing helpers
# ---------------------------------------------------------------------------


def _xml_extract_rgb(element: ET.Element) -> list[int]:
    """
    Extract ``[r, g, b]`` from an XML element with ``r``, ``g``, ``b`` attributes.

    Args:
        element: XML element with ``r``, ``g``, ``b`` integer attributes

    Returns:
        List of three integers ``[r, g, b]``

    Raises:
        ValueError: If any required attribute is missing or not a valid integer
    """
    missing = [attr for attr in ("r", "g", "b") if element.get(attr) is None]
    if missing:
        raise ValueError(
            f"XML element <{element.tag}> missing RGB attribute(s): "
            f"{', '.join(missing)}"
        )
    return [int(element.get("r")), int(element.get("g")), int(element.get("b"))]


def _xml_extract_color_pair(element: ET.Element) -> dict[str, list[int]]:
    """
    Extract a color pair dict from an XML element with ``<foreground>``
    and ``<background>`` children.

    Args:
        element: XML element containing ``<foreground r= g= b= />``
            and ``<background r= g= b= />`` children

    Returns:
        Dict with ``"foreground"`` and ``"background"`` keys mapping to
        ``[r, g, b]`` lists

    Raises:
        ValueError: If required children are missing or have invalid attributes
    """
    pair: dict[str, list[int]] = {}
    fg_elem = element.find("foreground")
    if fg_elem is not None:
        pair["foreground"] = _xml_extract_rgb(fg_elem)
    bg_elem = element.find("background")
    if bg_elem is not None:
        pair["background"] = _xml_extract_rgb(bg_elem)
    return pair


# ---------------------------------------------------------------------------
# Parsers -- JSON, XML, YAML
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Java curses-java format adapter
# ---------------------------------------------------------------------------


def _resolve_color(value) -> tuple[int, int, int]:
    """Resolve a color from an ncurses name string or RGB value to ``(r, g, b)``.

    Accepts ncurses color names (case-insensitive), RGB lists/tuples, or
    comma-separated RGB strings. Falls back to :func:`_parse_rgb` for
    non-name values.
    """
    if isinstance(value, str):
        upper = value.upper()
        if upper in NCURSES_COLOR_MAP:
            return NCURSES_COLOR_MAP[upper]
    return _parse_rgb(value)


def _is_java_format(data: dict) -> bool:
    """Detect if a parsed JSON dict uses the Java curses-java theme format.

    Java format has ``colors`` values as ``{"fg": "...", "bg": "..."}`` dicts,
    while Python format has ``colors`` values as ``[r, g, b]`` arrays.
    """
    if "colors" not in data or not isinstance(data["colors"], dict):
        return False
    for value in data["colors"].values():
        if isinstance(value, dict) and "fg" in value:
            return True
    return False


def _convert_java_border_chars(java_chars: str) -> str:
    """Reorder border characters from Java to Python ordering.

    Java: TL, T, TR, L, BL, B, BR, R  (positions 0-7)
    Python: TL, T, TR, L, R, BL, B, BR  (positions 0-7)
    """
    if len(java_chars) != 8:
        return java_chars
    return java_chars[0:4] + java_chars[7] + java_chars[4:7]


def _derive_semantic_colors(components: dict) -> dict:
    """Derive 8 Python semantic colors from Java component color pairs.

    Three colors are derived directly from components (100% consistent
    across all built-in themes). The remaining five use standard defaults.
    """
    bg_comp = components.get("background", {})
    btn_comp = components.get("button", {})

    background = list(bg_comp.get("background", [0, 0, 0]))
    foreground = list(bg_comp.get("foreground", [255, 255, 255]))
    primary = list(btn_comp.get("foreground", foreground))

    return {
        "background": background,
        "foreground": foreground,
        "primary": primary,
        "success": [0, 255, 0],
        "error": [255, 0, 0],
        "warning": [255, 255, 0],
        "info": list(foreground),
        "accent": list(foreground),
    }


def _convert_java_to_python(data: dict) -> dict:
    """Convert a Java curses-java theme dict to Python canonical format."""
    result = {}

    result["name"] = data.get("name", "Unnamed")
    if "description" in data:
        result["description"] = data["description"]
    if isinstance(data.get("metadata"), dict) and "author" in data["metadata"]:
        result["author"] = data["metadata"]["author"]

    java_colors = data.get("colors", {})
    components = {}
    for comp_name, pair in java_colors.items():
        if isinstance(pair, dict) and "fg" in pair:
            fg_rgb = _resolve_color(pair["fg"])
            bg_rgb = _resolve_color(pair["bg"])
            components[comp_name] = {
                "foreground": list(fg_rgb),
                "background": list(bg_rgb),
            }

    if components:
        result["components"] = components

    result["colors"] = _derive_semantic_colors(components)

    borders = data.get("borders", {})
    if "single" in borders:
        result["border_chars"] = _convert_java_border_chars(borders["single"])

    if "3d" in data:
        java_3d = data["3d"]
        python_3d = {}

        key_map = {
            "shadow_color": "shadow",
            "highlight_color": "highlight",
            "lowlight_color": "lowlight",
        }
        for java_key, python_key in key_map.items():
            if java_key in java_3d:
                pair = java_3d[java_key]
                python_3d[python_key] = {
                    "foreground": list(_resolve_color(pair["fg"])),
                    "background": list(_resolve_color(pair["bg"])),
                }

        if "shadow_offset" in java_3d:
            offset = java_3d["shadow_offset"]
            python_3d["shadow_offset_x"] = offset.get("x", 2)
            python_3d["shadow_offset_y"] = offset.get("y", 1)

        if "double" in borders:
            python_3d["double_border_chars"] = _convert_java_border_chars(
                borders["double"]
            )

        result["3d"] = python_3d

    return result


def load_json(path: Union[str, pathlib.Path]) -> dict:
    """
    Load a theme configuration from a JSON file.

    Reads and parses a JSON theme file, normalizing the ``"theme3d"`` key
    (used in JSON files) to the canonical ``"3d"`` key.

    Args:
        path: Path to the JSON theme file

    Returns:
        Parsed theme configuration dictionary

    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file contains invalid JSON

    Example:
        >>> config = load_json("dark_theme.json")
        >>> config["name"]
        'Dark'
    """
    path = pathlib.Path(path)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    # Auto-detect and convert Java curses-java format
    if _is_java_format(data):
        data = _convert_java_to_python(data)

    # Normalize JSON-specific key to canonical form
    if "theme3d" in data:
        data["3d"] = data.pop("theme3d")

    return data


def load_xml(path: Union[str, pathlib.Path]) -> dict:
    """
    Load a theme configuration from an XML file.

    Reads and parses an XML theme file, mapping the XML structure to the
    canonical dict format used by ConfigTheme and ConfigTheme3D.

    XML structure mapping:
        - ``<meta><name>`` -> ``config["name"]``
        - ``<colors><background r= g= b= />`` -> ``config["colors"]["background"]``
        - ``<components><button><foreground r= g= b= />`` -> component color pairs
        - ``<effects3d>`` -> ``config["3d"]``
        - ``<border_chars>`` -> ``config["border_chars"]``

    Args:
        path: Path to the XML theme file

    Returns:
        Parsed theme configuration dictionary in canonical format

    Raises:
        FileNotFoundError: If the file does not exist
        xml.etree.ElementTree.ParseError: If the file contains invalid XML

    Example:
        >>> config = load_xml("dark_theme.xml")
        >>> config["name"]
        'Dark'
    """
    path = pathlib.Path(path)
    if _safe_ET is not None:
        tree = _safe_ET.parse(path)
    else:
        # Disable DTD processing to mitigate entity expansion attacks
        # (billion laughs). Only load XML theme files from trusted sources.
        parser = ET.XMLParser()
        parser.entity = {}
        tree = ET.parse(path, parser=parser)
    root = tree.getroot()

    config: dict = {}

    # --- Meta section ---
    meta = root.find("meta")
    if meta is not None:
        name_elem = meta.find("name")
        if name_elem is not None and name_elem.text:
            config["name"] = name_elem.text.strip()
        desc_elem = meta.find("description")
        if desc_elem is not None and desc_elem.text:
            config["description"] = desc_elem.text.strip()
        author_elem = meta.find("author")
        if author_elem is not None and author_elem.text:
            config["author"] = author_elem.text.strip()

    # --- Colors section ---
    colors_elem = root.find("colors")
    if colors_elem is not None:
        config["colors"] = {}
        for color_elem in colors_elem:
            config["colors"][color_elem.tag] = _xml_extract_rgb(color_elem)

    # --- Components section ---
    components_elem = root.find("components")
    if components_elem is not None:
        config["components"] = {}
        for comp_elem in components_elem:
            config["components"][comp_elem.tag] = _xml_extract_color_pair(comp_elem)

    # --- Border characters ---
    border_elem = root.find("border_chars")
    if border_elem is not None and border_elem.text:
        config["border_chars"] = border_elem.text

    # --- 3D effects section ---
    effects_elem = root.find("effects3d")
    if effects_elem is not None:
        td: dict = {}

        for key in ("shadow", "highlight", "lowlight"):
            elem = effects_elem.find(key)
            if elem is not None:
                td[key] = _xml_extract_color_pair(elem)

        offset_elem = effects_elem.find("shadow_offset")
        if offset_elem is not None:
            x_val = offset_elem.get("x")
            if x_val is not None:
                td["shadow_offset_x"] = int(x_val)
            y_val = offset_elem.get("y")
            if y_val is not None:
                td["shadow_offset_y"] = int(y_val)

        dbc_elem = effects_elem.find("double_border_chars")
        if dbc_elem is not None and dbc_elem.text:
            td["double_border_chars"] = dbc_elem.text

        config["3d"] = td

    return config


def load_yaml(path: Union[str, pathlib.Path]) -> dict:
    """
    Load a theme configuration from a YAML file.

    Requires the optional ``PyYAML`` package. If PyYAML is not installed,
    raises an ``ImportError`` with installation instructions.

    Args:
        path: Path to the YAML theme file

    Returns:
        Parsed theme configuration dictionary

    Raises:
        ImportError: If PyYAML is not installed (with installation instructions)
        FileNotFoundError: If the file does not exist

    Example:
        >>> config = load_yaml("dark_theme.yaml")
        >>> config["name"]
        'Dark'
    """
    try:
        import yaml
    except ImportError:
        raise ImportError(
            "YAML theme support requires PyYAML.\n"
            "Install it with: pip install PyYAML\n"
            "Or use JSON/XML format instead (no external dependencies required)."
        )

    path = pathlib.Path(path)
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Normalize YAML-specific key to canonical form
    if isinstance(data, dict) and "theme3d" in data:
        data["3d"] = data.pop("theme3d")

    return data


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def load_theme_from_file(path: Union[str, pathlib.Path]) -> Union[Theme, Theme3D]:
    """
    Load a theme from a file, auto-detecting the format by extension.

    Parses the file, validates the configuration, and returns a
    ``ConfigTheme`` or ``ConfigTheme3D`` instance depending on whether
    the configuration includes a 3D section.

    Supported extensions:
        - ``.json`` -- JSON format (stdlib, zero dependencies)
        - ``.xml`` -- XML format (stdlib, zero dependencies)
        - ``.yaml``, ``.yml`` -- YAML format (requires PyYAML)

    Args:
        path: Path to the theme file. The file extension determines
            which parser is used.

    Returns:
        A ``ConfigTheme`` instance for basic themes, or a ``ConfigTheme3D``
        instance for themes with a 3D effects section.

    Raises:
        ValueError: If the file extension is unsupported or the config
            fails validation
        FileNotFoundError: If the file does not exist
        ImportError: If YAML format is used but PyYAML is not installed

    Example:
        >>> theme = load_theme_from_file("my_theme.json")
        >>> theme.apply(stdscr)
        >>> theme.name
        'My Theme'
    """
    path = pathlib.Path(path)
    suffix = path.suffix.lower()

    if suffix == ".json":
        config = load_json(path)
    elif suffix == ".xml":
        config = load_xml(path)
    elif suffix in (".yaml", ".yml"):
        config = load_yaml(path)
    else:
        raise ValueError(
            f"Unsupported theme file format '{suffix}'. "
            f"Supported formats: .json, .xml, .yaml, .yml"
        )

    if "3d" in config:
        return ConfigTheme3D(config)
    return ConfigTheme(config)
