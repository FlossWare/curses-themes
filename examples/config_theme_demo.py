#!/usr/bin/env python3
"""
Demonstration of loading themes from JSON, XML, and YAML config files.

This example loads three theme config files from the examples/themes/ directory
and lets the user cycle through them with a keypress. It shows how theme
definitions can live in external config files rather than Python classes.

JSON and XML parsing use only the Python standard library. YAML requires
the optional PyYAML package; the demo runs gracefully without it (the
YAML theme is simply skipped).

Usage:
    python examples/config_theme_demo.py

Controls:
    n / Right  - Next theme
    p / Left   - Previous theme
    q / Escape - Quit

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

import curses
import json
import os
import xml.etree.ElementTree as ET

from curses_themes import ColorPair, Theme

# ---------------------------------------------------------------------------
# Config-file parsers (JSON, XML, YAML)
# ---------------------------------------------------------------------------

REQUIRED_COLORS = (
    "background",
    "foreground",
    "primary",
    "success",
    "error",
    "warning",
    "info",
    "accent",
)

COMPONENT_NAMES = (
    "background",
    "button",
    "button_focused",
    "text_input",
    "border",
    "selection",
    "disabled",
)


def _parse_color_pair(data):
    """Parse a dict with 'foreground' and 'background' keys into a ColorPair."""
    return ColorPair(
        foreground=tuple(data["foreground"]),
        background=tuple(data["background"]),
    )


def _build_theme(name, description, author, color_map, components, border_chars):
    """Build a Theme from parsed config data using the Theme constructor."""
    return Theme(
        name=name,
        description=description,
        author=author,
        color_map=color_map,
        component_colors={
            cname: (cp.foreground, cp.background) for cname, cp in components.items()
        } if components else None,
        border_chars=border_chars,
    )


def load_json_theme(path):
    """Load a theme from a JSON config file."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)

    name = data["name"]
    description = data.get("description", "")
    author = data.get("author", "")

    color_map = {}
    for key in REQUIRED_COLORS:
        color_map[key] = tuple(data["colors"][key])

    components = {}
    for key in COMPONENT_NAMES:
        if key in data.get("components", {}):
            components[key] = _parse_color_pair(data["components"][key])

    border_chars = data.get("border_chars", "+-+||+-+")

    return _build_theme(name, description, author, color_map, components, border_chars)


def load_xml_theme(path):
    """Load a theme from an XML config file."""
    tree = ET.parse(path)
    root = tree.getroot()

    meta = root.find("meta")
    name = meta.findtext("name", "")
    description = meta.findtext("description", "")
    author = meta.findtext("author", "")

    color_map = {}
    colors_elem = root.find("colors")
    for key in REQUIRED_COLORS:
        elem = colors_elem.find(key)
        color_map[key] = (
            int(elem.get("r")),
            int(elem.get("g")),
            int(elem.get("b")),
        )

    components = {}
    components_elem = root.find("components")
    if components_elem is not None:
        for key in COMPONENT_NAMES:
            comp = components_elem.find(key)
            if comp is not None:
                fg = comp.find("foreground")
                bg = comp.find("background")
                components[key] = ColorPair(
                    foreground=(int(fg.get("r")), int(fg.get("g")), int(fg.get("b"))),
                    background=(int(bg.get("r")), int(bg.get("g")), int(bg.get("b"))),
                )

    border_chars_elem = root.findtext("border_chars")
    border_chars = border_chars_elem if border_chars_elem else "+-+||+-+"

    return _build_theme(name, description, author, color_map, components, border_chars)


def load_yaml_theme(path):
    """Load a theme from a YAML config file.

    Requires the optional PyYAML package (pip install pyyaml).

    Raises:
        ImportError: If PyYAML is not installed, with a helpful message.
    """
    try:
        import yaml
    except ImportError:
        raise ImportError(
            "PyYAML is required to load YAML theme files.\n"
            "Install it with:  pip install pyyaml"
        )

    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    name = data["name"]
    description = data.get("description", "")
    author = data.get("author", "")

    color_map = {}
    for key in REQUIRED_COLORS:
        color_map[key] = tuple(data["colors"][key])

    components = {}
    for key in COMPONENT_NAMES:
        if key in data.get("components", {}):
            components[key] = _parse_color_pair(data["components"][key])

    border_chars = data.get("border_chars", "+-+||+-+")

    return _build_theme(name, description, author, color_map, components, border_chars)


# ---------------------------------------------------------------------------
# Demo application
# ---------------------------------------------------------------------------


def _load_all_themes(themes_dir):
    """Load all theme config files, skipping any that fail."""
    themes = []
    errors = []

    # JSON
    json_path = os.path.join(themes_dir, "solarized.json")
    try:
        themes.append(("JSON", load_json_theme(json_path)))
    except Exception as exc:
        errors.append(f"solarized.json: {exc}")

    # XML
    xml_path = os.path.join(themes_dir, "ocean.xml")
    try:
        themes.append(("XML", load_xml_theme(xml_path)))
    except Exception as exc:
        errors.append(f"ocean.xml: {exc}")

    # YAML (optional dependency)
    yaml_path = os.path.join(themes_dir, "forest.yaml")
    try:
        themes.append(("YAML", load_yaml_theme(yaml_path)))
    except ImportError as exc:
        errors.append(f"forest.yaml skipped: {exc}")
    except Exception as exc:
        errors.append(f"forest.yaml: {exc}")

    return themes, errors


def _draw_color_swatch(window, y, x, label, color_pair_num, max_width):
    """Draw a labeled color swatch line."""
    text = f"  {label:<12s} Sample text in this color"
    text = text[: max_width - x - 1]
    try:
        window.addstr(y, x, text, curses.color_pair(color_pair_num))
    except curses.error:
        pass


def _draw_theme(stdscr, theme, fmt_label, index, total, errors):
    """Render a single theme's preview."""
    stdscr.clear()

    try:
        theme.apply(stdscr)
    except RuntimeError as exc:
        stdscr.addstr(0, 0, f"Cannot apply theme: {exc}")
        stdscr.addstr(2, 0, "Press any key to continue.")
        stdscr.refresh()
        return

    height, width = stdscr.getmaxyx()
    row = 0

    # Title bar
    title = f"Config Theme Demo  [{index + 1}/{total}]"
    try:
        stdscr.addstr(
            row,
            (width - len(title)) // 2,
            title,
            curses.color_pair(theme.colors.primary) | curses.A_BOLD,
        )
    except curses.error:
        pass
    row += 2

    # Theme metadata
    meta_lines = [
        f"Name:        {theme.name}",
        f"Format:      {fmt_label}",
        f"Description: {theme.description}",
        f"Author:      {theme.author}",
    ]
    for line in meta_lines:
        try:
            stdscr.addstr(
                row, 2, line[: width - 4], curses.color_pair(theme.colors.foreground)
            )
        except curses.error:
            pass
        row += 1
    row += 1

    # Semantic color swatches
    try:
        stdscr.addstr(
            row,
            2,
            "Semantic Colors:",
            curses.color_pair(theme.colors.foreground) | curses.A_BOLD,
        )
    except curses.error:
        pass
    row += 1

    color_names = [
        ("primary", theme.colors.primary),
        ("success", theme.colors.success),
        ("error", theme.colors.error),
        ("warning", theme.colors.warning),
        ("info", theme.colors.info),
        ("accent", theme.colors.accent),
    ]
    for name, pair_num in color_names:
        _draw_color_swatch(stdscr, row, 4, name, pair_num, width)
        row += 1
    row += 1

    # Component color swatches
    try:
        stdscr.addstr(
            row,
            2,
            "Component Colors:",
            curses.color_pair(theme.colors.foreground) | curses.A_BOLD,
        )
    except curses.error:
        pass
    row += 1

    component_names = [
        ("background", theme.components.background),
        ("button", theme.components.button),
        ("btn focused", theme.components.button_focused),
        ("text input", theme.components.text_input),
        ("border", theme.components.border),
        ("selection", theme.components.selection),
        ("disabled", theme.components.disabled),
    ]
    for name, pair_num in component_names:
        _draw_color_swatch(stdscr, row, 4, name, pair_num, width)
        row += 1
    row += 1

    # Themed box
    box_width = min(50, width - 8)
    box_height = 5
    if row + box_height + 4 < height and box_width >= 10:
        theme.draw_box(stdscr, row, 4, box_height, box_width, title="Themed Box")
        try:
            stdscr.addstr(
                row + 2,
                6,
                f"Border drawn with {theme.name} theme",
                curses.color_pair(theme.colors.foreground),
            )
        except curses.error:
            pass
        row += box_height + 1

    # Show any load errors
    if errors:
        row += 1
        try:
            stdscr.addstr(
                row,
                2,
                "Load notes:",
                curses.color_pair(theme.colors.warning) | curses.A_BOLD,
            )
        except curses.error:
            pass
        row += 1
        for err in errors:
            try:
                stdscr.addstr(
                    row, 4, err[: width - 6], curses.color_pair(theme.colors.warning)
                )
            except curses.error:
                pass
            row += 1

    # Footer
    footer = "n/Right: Next   p/Left: Previous   q/Esc: Quit"
    try:
        stdscr.addstr(
            height - 1,
            (width - len(footer)) // 2,
            footer,
            curses.color_pair(theme.colors.info) | curses.A_DIM,
        )
    except curses.error:
        pass

    stdscr.refresh()


def main(stdscr):
    """Main application loop: load themes and cycle through them."""
    curses.curs_set(0)

    # Locate the themes directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    themes_dir = os.path.join(script_dir, "themes")

    if not os.path.isdir(themes_dir):
        stdscr.addstr(0, 0, f"Themes directory not found: {themes_dir}")
        stdscr.addstr(2, 0, "Press any key to exit.")
        stdscr.refresh()
        stdscr.getch()
        return

    themes, errors = _load_all_themes(themes_dir)

    if not themes:
        stdscr.addstr(0, 0, "No themes could be loaded.")
        for i, err in enumerate(errors):
            stdscr.addstr(i + 1, 2, err)
        stdscr.addstr(len(errors) + 2, 0, "Press any key to exit.")
        stdscr.refresh()
        stdscr.getch()
        return

    index = 0

    while True:
        fmt_label, theme = themes[index]
        _draw_theme(stdscr, theme, fmt_label, index, len(themes), errors)

        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):  # q, Q, Escape
            break
        elif key in (ord("n"), ord("N"), curses.KEY_RIGHT):
            index = (index + 1) % len(themes)
        elif key in (ord("p"), ord("P"), curses.KEY_LEFT):
            index = (index - 1) % len(themes)


if __name__ == "__main__":
    curses.wrapper(main)
