# curses-themes

**Lightweight theme support for Python curses applications**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

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
    theme = ThemeManager.load('dracula')
    theme.apply(stdscr)
    
    # Use semantic colors
    stdscr.addstr(0, 0, "Success!", theme.colors.success)
    stdscr.addstr(1, 0, "Error!", theme.colors.error)
    stdscr.addstr(2, 0, "Warning!", theme.colors.warning)
    
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

## Built-in Themes

### Modern Themes

**Default** - Classic terminal with white text on black background  
**Dark** - Professional dark theme with comfortable blues and greens  
**Light** - Clean light theme with high contrast for well-lit environments

### Retro Computer Themes

**TI-99/4A** (1981-1984) - Texas Instruments home computer with cyan-on-blue aesthetic  
**TRS-80** (1980-1983) - Tandy/Radio Shack monochrome white-on-black display

### Business Software Themes

**DOS** (1981-1995) - Classic MS-DOS white-on-black with yellow menus  
**dBASE III** (1984-1985) - Iconic database software with cyan menus  
**dBASE IV** (1988-1993) - Windowed database interface with blue background

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
    themes = ['dark', 'light', 'dracula', 'nord', 'borland']
    current = 0
    
    while True:
        theme = ThemeManager.load(themes[current])
        theme.apply(stdscr)
        
        stdscr.clear()
        stdscr.addstr(0, 0, f"Theme: {themes[current]}", 
                     theme.colors.primary)
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
