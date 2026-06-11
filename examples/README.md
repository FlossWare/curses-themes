# curses-themes Examples

This directory contains example applications demonstrating the features of the `curses-themes` library.

## Requirements

- Python 3.9 or higher
- Terminal with curses support (most Linux/macOS terminals, Windows Terminal, or WSL)
- Color support (8, 16, or 256 colors recommended)

## Running the Examples

All examples can be run directly:

```bash
python3 basic_usage.py
python3 theme_switcher.py
python3 dashboard.py
python3 custom_theme.py
```

Or install the package first and run:

```bash
pip install -e ..
python3 basic_usage.py
```

## Common Keyboard Controls

Unless otherwise noted, most interactive examples use:

- **q** - Quit the application
- **ESC** - Exit or go back
- **Arrow keys** - Navigate (when applicable)
- **Enter** - Select or confirm

## Examples

### basic_usage.py

**Status**: Planned

A minimal example demonstrating core theme functionality.

**What it demonstrates**:
- Loading a built-in theme
- Applying a theme to a curses window
- Using semantic colors (success, error, warning, info)
- Drawing themed boxes
- Basic text styling with theme colors

**Usage**:
```bash
python3 basic_usage.py
```

**Controls**:
- **q** - Quit

---

### theme_switcher.py

**Status**: Planned

Interactive application for switching between all built-in themes in real-time.

**What it demonstrates**:
- Runtime theme switching
- Listing available themes
- Comparing visual appearance across themes
- Dynamic theme reloading without restart

**Usage**:
```bash
python3 theme_switcher.py
```

**Controls**:
- **n** - Next theme
- **p** - Previous theme
- **1-5** - Jump to specific theme (Dark, Light, Dracula, Nord, Borland)
- **q** - Quit

---

### dashboard.py

**Status**: Planned

Full-featured TUI dashboard showcasing advanced theme usage.

**What it demonstrates**:
- Multi-panel layouts with themed borders
- Status indicators using semantic colors
- Progress bars and gauges
- Tabbed interfaces
- Menu systems
- Modal dialogs
- Real-time updates with theme consistency

**Usage**:
```bash
python3 dashboard.py [--theme THEME_NAME]
```

**Options**:
- `--theme` - Start with specific theme (default: dark)

**Controls**:
- **Tab** - Switch between panels
- **t** - Toggle theme menu
- **Arrow keys** - Navigate menus and lists
- **Enter** - Select menu item
- **ESC** - Close dialog/menu
- **q** - Quit

---

### custom_theme.py

**Status**: Planned

Demonstrates creating and registering custom themes.

**What it demonstrates**:
- Extending the `Theme` base class
- Defining custom color palettes
- RGB to terminal color conversion
- Theme registration with `ThemeManager`
- Custom border characters (optional)
- Theme metadata (name, description, author)

**Usage**:
```bash
python3 custom_theme.py
```

**Controls**:
- **n** - Switch between custom and built-in themes
- **q** - Quit

**Example themes included**:
- Solarized Dark - Precision colors for machines and people
- Gruvbox - Retro groove color scheme
- One Dark - Atom's iconic One Dark theme
- Material - Google Material Design colors

---

## Creating Your Own Examples

When creating new examples:

1. **Include a docstring** at the top explaining what the example demonstrates
2. **Use `curses.wrapper()`** to properly initialize and clean up curses
3. **Handle terminal size gracefully** - check `curses.LINES` and `curses.COLS`
4. **Provide keyboard controls** - especially 'q' to quit
5. **Add error handling** for terminals without color support
6. **Keep it simple** - examples should be educational, not production code
7. **Comment your code** - explain what each section does

Example template:

```python
#!/usr/bin/env python3
"""
Example: Brief description

Demonstrates:
- Feature 1
- Feature 2
- Feature 3

Controls:
- q: Quit
- Other controls as needed
"""

import curses
from curses_themes import ThemeManager


def main(stdscr):
    """Main application logic"""
    # Initialize
    curses.curs_set(0)  # Hide cursor
    stdscr.timeout(100)  # Non-blocking input
    
    # Load theme
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)
    
    # Main loop
    while True:
        stdscr.clear()
        
        # Your drawing code here
        stdscr.addstr(0, 0, "Hello, themed world!", 
                     theme.colors.primary)
        
        stdscr.refresh()
        
        # Handle input
        key = stdscr.getch()
        if key == ord('q'):
            break


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass  # Clean exit on Ctrl+C
```

## Troubleshooting

### Colors not displaying correctly

- Ensure your terminal supports colors: `echo $TERM`
- Try a different terminal emulator (recommended: iTerm2, GNOME Terminal, Windows Terminal)
- Some themes require 256-color support

### Import errors

```bash
# Install the package in development mode
pip install -e ..

# Or set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."
```

### Curses initialization errors

- Ensure you're running in a real terminal, not an IDE's built-in terminal
- On Windows, use Windows Terminal or WSL
- Check that your terminal supports curses

## Additional Resources

- [Main README](../README.md) - Library overview and features
- [API Documentation](../docs/API.md) - Detailed API reference
- [curses-java](https://github.com/FlossWare/curses-java) - Original Java inspiration
- [Python curses documentation](https://docs.python.org/3/library/curses.html) - Official curses module docs

## Contributing Examples

Have an interesting use case? Consider contributing an example:

1. Create a new example following the template above
2. Test it with multiple themes
3. Add documentation to this README
4. Submit a pull request

Good example candidates:
- Form input with validation
- File browser with syntax highlighting
- Network monitoring dashboard
- Game (snake, tetris, etc.) with themed UI
- Text editor with theme support
- Calendar/agenda application
- Chart/graph visualization
