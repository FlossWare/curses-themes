# curses-themes

**Lightweight theme support for Python curses applications**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![codecov](https://codecov.io/gh/FlossWare/curses-themes/branch/main/graph/badge.svg)](https://codecov.io/gh/FlossWare/curses-themes)
[![Code Quality](https://github.com/FlossWare/curses-themes/workflows/Code%20Quality/badge.svg)](https://github.com/FlossWare/curses-themes/actions/workflows/quality.yml)
[![Coverage](https://github.com/FlossWare/curses-themes/workflows/Coverage/badge.svg)](https://github.com/FlossWare/curses-themes/actions/workflows/coverage.yml)

Inspired by [FlossWare curses-java](https://github.com/FlossWare/curses-java), this library brings professional theme support to Python's standard `curses` module with zero external dependencies.

## Features

- 🎨 **8 Built-in Themes**: Modern, classic IDE, and retro computer themes
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
    theme.apply(stdscr)
    
    # Use semantic colors
    stdscr.addstr(0, 0, "Success!", curses.color_pair(theme.colors.success))
    stdscr.addstr(1, 0, "Error!", curses.color_pair(theme.colors.error))
    stdscr.addstr(2, 0, "Warning!", curses.color_pair(theme.colors.warning))
    
    # Draw themed boxes
    theme.draw_box(stdscr, 4, 2, 10, 40, title="My Panel")
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
```

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

## Theme Gallery

### Modern Themes

<table>
<tr>
<td width="33%" align="center">
<img src="screenshots/default.png" width="300" alt="Default Theme"><br>
<strong>Default</strong><br>
Classic terminal aesthetic<br>
<em>Timeless</em>
</td>
<td width="33%" align="center">
<img src="screenshots/dark.png" width="300" alt="Dark Theme"><br>
<strong>Dark</strong><br>
Professional dark mode<br>
<em>Modern</em>
</td>
<td width="33%" align="center">
<img src="screenshots/light.png" width="300" alt="Light Theme"><br>
<strong>Light</strong><br>
High contrast for bright environments<br>
<em>Modern</em>
</td>
</tr>
</table>

### Retro Computer Themes

<table>
<tr>
<td width="50%" align="center">
<img src="screenshots/ti-99-4a.png" width="300" alt="TI-99/4A Theme"><br>
<strong>TI-99/4A</strong><br>
Texas Instruments home computer<br>
<em>1981-1984</em>
</td>
<td width="50%" align="center">
<img src="screenshots/trs-80.png" width="300" alt="TRS-80 Theme"><br>
<strong>TRS-80</strong><br>
Tandy/Radio Shack monochrome<br>
<em>1980-1983</em>
</td>
</tr>
</table>

### Business Software Themes

<table>
<tr>
<td width="33%" align="center">
<img src="screenshots/dos.png" width="300" alt="DOS Theme"><br>
<strong>DOS</strong><br>
Classic MS-DOS interface<br>
<em>1981-1995</em>
</td>
<td width="33%" align="center">
<img src="screenshots/dbase-iii.png" width="300" alt="dBASE III Theme"><br>
<strong>dBASE III</strong><br>
Iconic database software<br>
<em>1984-1985</em>
</td>
<td width="33%" align="center">
<img src="screenshots/dbase-iv.png" width="300" alt="dBASE IV Theme"><br>
<strong>dBASE IV</strong><br>
Windowed database interface<br>
<em>1988-1993</em>
</td>
</tr>
</table>

### 3D Effect Themes

<table>
<tr>
<td width="50%" align="center">
<img src="screenshots/borland-3d.png" width="300" alt="Borland 3D Theme"><br>
<strong>Borland 3D</strong><br>
Turbo Vision 3D look<br>
<em>1990-1997</em>
</td>
<td width="50%" align="center">
<img src="screenshots/dbase-iv-3d.png" width="300" alt="dBASE IV 3D Theme"><br>
<strong>dBASE IV 3D</strong><br>
3D windowed database UI<br>
<em>1988-1993</em>
</td>
</tr>
</table>

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

## Creating Custom Themes

```python
from curses_themes import Theme, ThemeManager

class SolarizedTheme(Theme):
    """Solarized Dark theme"""
    
    def __init__(self):
        super().__init__(
            name="Solarized Dark",
            description="Precision colors for machines and people",
            author="Ethan Schoonover"
        )
    
    def get_color_map(self):
        return {
            'background': (0, 43, 54),
            'foreground': (131, 148, 150),
            'primary': (38, 139, 210),
            'success': (133, 153, 0),
            'error': (220, 50, 47),
            'warning': (181, 137, 0),
            'info': (42, 161, 152),
            'accent': (211, 54, 130),
        }

# Register and use
ThemeManager.register(SolarizedTheme)
theme = ThemeManager.load('solarized-dark')
```

## Runtime Theme Switching

```python
import curses
from curses_themes import ThemeManager

def main(stdscr):
    themes = ['default', 'dark', 'light', 'borland3d', 'dbase3']
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

## API Reference

### ThemeManager

- `ThemeManager.load(name)` - Load theme by name
- `ThemeManager.register(theme_class, name=None)` - Register custom theme
- `ThemeManager.list_themes()` - List available themes

### Theme

- `theme.apply(stdscr)` - Apply theme to screen
- `theme.colors.primary` - Primary color
- `theme.colors.success` - Success color
- `theme.colors.error` - Error color
- `theme.colors.warning` - Warning color
- `theme.colors.info` - Info color
- `theme.colors.accent` - Accent color
- `theme.draw_box(stdscr, y, x, height, width, title="")` - Draw themed box

## Examples

See the `examples/` directory for complete demonstrations:

- `basic_usage.py` - Simple theme demonstration
- `theme_switcher.py` - Interactive theme switching
- `dashboard.py` - Full TUI dashboard with themes
- `custom_theme.py` - Creating custom themes

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Adding New Themes

1. Create theme class in `curses_themes/themes/your_theme.py`
2. Implement `get_color_map()` method
3. Optionally override `get_border_chars()`
4. Add tests in `tests/test_themes/test_your_theme.py`
5. Submit pull request

## Related Projects

- [curses-java](https://github.com/FlossWare/curses-java) - Java terminal UI library with themes (inspiration for this project)
- [Textual](https://github.com/Textualize/textual) - Modern Python TUI framework
- [Rich](https://github.com/Textualize/rich) - Rich terminal output library

## License

GPL-3.0 - See [LICENSE](LICENSE) file for details.

## Author

**FlossWare** - [https://github.com/FlossWare](https://github.com/FlossWare)

Inspired by the excellent [curses-java](https://github.com/FlossWare/curses-java) library.
