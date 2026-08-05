# curses-themes

**Lightweight theme support for Python curses applications**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![codecov](https://codecov.io/gh/FlossWare/curses-themes/branch/main/graph/badge.svg)](https://codecov.io/gh/FlossWare/curses-themes)
[![Code Quality](https://github.com/FlossWare/curses-themes/workflows/Code%20Quality/badge.svg)](https://github.com/FlossWare/curses-themes/actions/workflows/quality.yml)


Inspired by [FlossWare curses-java](https://github.com/FlossWare/curses-java), this library brings professional theme support to Python's standard `curses` module with zero external dependencies.

## Features

- 🎨 **16 Built-in Themes**: Modern developer palettes, classic IDE, and retro computer themes
- 🔌 **Pluggable Architecture**: Easy custom theme creation
- 🎯 **Semantic Colors**: `primary`, `success`, `error`, `warning`, `info`
- 🔄 **Runtime Theme Switching**: Change themes on-the-fly
- 🖥️ **Terminal Aware**: Auto-detects 8/16/256 color support with fallbacks
- 📦 **Zero Dependencies**: Only uses Python standard library `curses`
- 🧪 **Thoroughly Tested**: Comprehensive test coverage
- 📚 **Well Documented**: API reference, examples, and guides

## Quick Start

```python
#!/usr/bin/env python3
import curses
from curses_themes import ThemeManager

def main(stdscr):
    # Load and apply a theme
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)  # REQUIRED before using colors
    
    # Semantic colors - general-purpose coloring by intent
    stdscr.addstr(0, 0, "Success!", curses.color_pair(theme.colors.success))
    stdscr.addstr(1, 0, "Error!", curses.color_pair(theme.colors.error))
    stdscr.addstr(2, 0, "Warning!", curses.color_pair(theme.colors.warning))
    
    # Component colors - UI widget styling
    stdscr.addstr(3, 0, "[ Save ]", curses.color_pair(theme.components.button))
    
    # Draw themed boxes
    theme.draw_box(stdscr, 5, 2, 10, 40, title="My Panel")
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
```

**Important**: You must call `theme.apply(stdscr)` before accessing `theme.colors` or `theme.components`, or a `RuntimeError` is raised. Color attributes return integers that must be wrapped with `curses.color_pair()` when used with curses display functions. See the [API Documentation](API.md#understanding-color-pairs) for details.

## Installation

```bash
pip install curses-themes
```

Or install from source:

```bash
git clone https://github.com/FlossWare/curses-themes.git
cd curses-themes
pip install -e .
```

### Windows

Python on Windows doesn't include the `curses` module. Install with Windows support:

```bash
pip install curses-themes[windows]
```

Or install `windows-curses` separately:

```bash
pip install windows-curses
```

Use [Windows Terminal](https://aka.ms/terminal) for best color support.

## Theme Gallery

### Modern Themes

<table>
<tr>
<td width="33%" align="center">
<img src="https://raw.githubusercontent.com/FlossWare/curses-themes/main/screenshots/default.png" width="300" alt="Default Theme"><br>
<strong>Default</strong><br>
Classic terminal aesthetic
</td>
<td width="33%" align="center">
<img src="https://raw.githubusercontent.com/FlossWare/curses-themes/main/screenshots/dark.png" width="300" alt="Dark Theme"><br>
<strong>Dark</strong><br>
Professional dark mode
</td>
<td width="33%" align="center">
<img src="https://raw.githubusercontent.com/FlossWare/curses-themes/main/screenshots/light.png" width="300" alt="Light Theme"><br>
<strong>Light</strong><br>
High contrast light mode
</td>
</tr>
</table>

### Modern Developer Themes

| Theme | Load name | Style | Best For |
|-------|-----------|-------|----------|
| **Dracula** | `dracula` | Dark purple accents | Popular developer dark mode |
| **Nord** | `nord` | Arctic blue-gray | Calm, elegant UIs |
| **Solarized Dark** | `solarized-dark` | Precision muted dark | Long coding sessions |
| **Solarized Light** | `solarized-light` | Precision muted light | Bright environments |
| **Monokai** | `monokai` | Vibrant warm dark | Classic editor aesthetic |
| **Catppuccin** | `catppuccin` | Soft pastel dark | Modern, soothin' TUIs |

```python
theme = ThemeManager.load('dracula')  # or nord, solarized-dark, monokai, catppuccin, ...
theme.apply(stdscr)
```

### Theme Comparison

| Theme | Era | Style | Colors | Best For |
|-------|-----|-------|--------|----------|
| Default | Timeless | Minimal | B/W | Universal compatibility |
| Dark | Modern | Professional | Blues/Greens | Low-light coding |
| Light | Modern | Clean | High contrast | Bright environments |
| TI-99/4A | 1981-1984 | Retro | Cyan/Blue | Nostalgia, gaming UIs |
| TRS-80 | 1980-1983 | Monochrome | White/Black | Authentic retro feel |
| DOS | 1981-1995 | Classic | White/Yellow | System utilities |
| dBASE III | 1984-1985 | Business | Cyan menus | Database applications |
| dBASE IV | 1988-1993 | Windowed | Blue background | Modern database UIs |
| Borland 3D | 1990-1997 | 3D Effect | Gray/Blue shadows | IDE-style applications |
| dBASE IV 3D | 1988-1993 | 3D Windowed | Blue with depth | Sophisticated database UIs |
| Dracula | Modern | Dark purple | Soft pastels | Popular dark coding |
| Nord | Modern | Arctic | Blue-gray | Calm professional UIs |
| Solarized Dark | Modern | Muted dark | Precision | Long coding sessions |
| Solarized Light | Modern | Muted light | Precision | Bright environments |
| Monokai | Classic editor | Vibrant dark | Warm tones | TextMate/Sublime feel |
| Catppuccin | Modern | Pastel dark | Soft pastels | Contemporary TUIs |

## Runtime Theme Switching

```python
import curses
from curses_themes import ThemeManager

def main(stdscr):
    themes = ['default', 'dark', 'dracula', 'nord', 'catppuccin', 'borland-3d']
    current = 0
    
    while True:
        theme = ThemeManager.load(themes[current])
        theme.apply(stdscr)
        
        stdscr.clear()
        stdscr.addstr(0, 0, f"Theme: {themes[current]}", 
                     curses.color_pair(theme.colors.primary))
        stdscr.addstr(2, 0, "Press 'n' for next, 'q' to quit")
        
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('n'):
            current = (current + 1) % len(themes)

curses.wrapper(main)
```

## Creating Custom Themes

```python
from curses_themes import Theme, ThemeManager

class SolarizedTheme(Theme):
    color_map = {
        'background': (0, 43, 54),
        'foreground': (131, 148, 150),
        'primary': (38, 139, 210),
        'success': (133, 153, 0),
        'error': (220, 50, 47),
        'warning': (181, 137, 0),
        'info': (42, 161, 152),
        'accent': (211, 54, 130),
    }
    component_colors = {
        'background': ((131, 148, 150), (0, 43, 54)),
        'button': ((38, 139, 210), (0, 43, 54)),
        'button_focused': ((0, 43, 54), (38, 139, 210)),
        'border': ((131, 148, 150), (0, 43, 54)),
    }
    border_chars = "\u250c\u2500\u2510\u2502\u2502\u2514\u2500\u2518"

    def __init__(self):
        super().__init__(
            name="Solarized Dark",
            description="Precision colors for machines and people",
            author="Ethan Schoonover",
        )

ThemeManager.register(SolarizedTheme)
theme = ThemeManager.load('solarized-dark')
```

## API Reference

### ThemeManager

- `ThemeManager.load(name)` - Load theme by name
- `ThemeManager.register(theme_class, name=None)` - Register custom theme
- `ThemeManager.list_themes()` - List available themes

### Theme

- `theme.apply(stdscr)` - Apply theme to screen (must call before using colors)
- `theme.draw_box(stdscr, y, x, height, width, title="")` - Draw themed box

#### Semantic Colors (`theme.colors.*`)

- `primary`, `success`, `error`, `warning`, `info`, `accent`, `background`, `foreground`

#### Component Colors (`theme.components.*`)

- `background`, `button`, `button_focused`, `text_input`, `border`, `selection`, `disabled`

## Examples

See the `examples/` directory for complete demonstrations.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT - See [LICENSE](LICENSE).

## Author

**FlossWare** - https://github.com/FlossWare
