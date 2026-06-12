# curses-themes User Guide

**Complete guide to using the curses-themes library for Python terminal applications**

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Working with Themes](#working-with-themes)
- [Creating Custom Themes](#creating-custom-themes)
- [Advanced Usage](#advanced-usage)
- [Windows Support](#windows-support)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Installation

### From PyPI (when published)

```bash
pip install curses-themes
```

### From Source

```bash
git clone https://github.com/FlossWare/curses-themes.git
cd curses-themes
pip install -e .
```

### Requirements

- Python 3.9 or higher
- Terminal with curses support
- Color-capable terminal (8, 16, or 256 colors)

### Platform-Specific Notes

**Linux/macOS**: Works out of the box  
**Windows**: Requires `windows-curses` package:

```bash
pip install windows-curses
pip install curses-themes
```

---

## Quick Start

### Minimal Example

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
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
```

### Available Themes

```python
from curses_themes import ThemeManager

# List all themes
themes = ThemeManager.list_themes()
for name, info in themes.items():
    print(f"{name}: {info['description']}")

# Output:
# default: Default theme with white text on black background
# dark: Dark theme with muted colors and dark background
# light: Light theme with bright background and dark text
# ti-99-4a: Texas Instruments TI-99/4A home computer theme
# trs-80: Tandy/Radio Shack TRS-80 monochrome theme
# dos: Classic MS-DOS and PC-DOS theme
# dbase-iii: Ashton-Tate dBASE III theme
# dbase-iv: Ashton-Tate/Borland dBASE IV theme
```

---

## Core Concepts

### 1. Theme Architecture

curses-themes provides two complementary color systems:

#### Semantic Colors
Purpose-based colors for UI state:
- `primary` - Main UI highlights and focus
- `success` - Positive feedback
- `error` - Error messages
- `warning` - Caution messages
- `info` - Informational messages
- `accent` - Secondary highlights

#### Component Colors
Widget-specific colors matching curses-java API:
- `background` - Default background
- `foreground` - Default text
- `button` - Normal button state
- `button_focused` - Focused button state
- `text_input` - Input fields
- `border` - Borders and frames
- `selection` - Selected items
- `disabled` - Disabled elements

### 2. Terminal Compatibility

The `ColorManager` automatically detects terminal capabilities:

- **256-color terminals**: Full RGB palette with accurate color mapping
- **16-color terminals**: Maps to closest ANSI colors
- **8-color terminals**: Maps to basic 8-color palette

Your themes work everywhere without code changes!

### ColorManager Best Practices

**Understanding State Persistence**

ColorManager uses class-level state that persists across instances:

```python
import curses
from curses_themes import ColorManager

def demo1(stdscr):
    mgr = ColorManager(stdscr)
    pair1 = mgr.init_color_pair((255, 0, 0), (0, 0, 0))  # Returns 1
    print(f"Allocated pair: {pair1}")

def demo2(stdscr):
    mgr = ColorManager(stdscr)  # New instance!
    # Same colors return cached pair number
    pair2 = mgr.init_color_pair((255, 0, 0), (0, 0, 0))  # Returns 1 (cached)
    # New colors continue allocation
    pair3 = mgr.init_color_pair((0, 255, 0), (0, 0, 0))  # Returns 2
    print(f"Cached: {pair2}, New: {pair3}")

curses.wrapper(demo1)
curses.wrapper(demo2)
# Output: Allocated pair: 1
#         Cached: 1, New: 2
```

**Why This Design?**

1. **Prevents duplicate pairs**: Same colors always get the same pair number
2. **Conserves COLOR_PAIRS**: Terminals have limited color pairs (often 256)
3. **Works with theme switching**: Multiple themes can coexist without conflicts

**What NOT to do:**

```python
# DON'T call reset() in production code
mgr = ColorManager(stdscr)
mgr.reset()  # This breaks ALL active color pairs!

# DON'T assume new instance = fresh state
mgr1 = ColorManager(stdscr)
mgr2 = ColorManager(stdscr)  # Shares state with mgr1
```

### 3. Color Pair API Usage

**Important**: Theme color attributes return **integers** (color pair numbers), not curses attributes.

```python
theme.colors.primary        # Returns: 1 (an integer)
theme.components.button     # Returns: 2 (an integer)
```

**Always wrap with `curses.color_pair()` for display functions**:

```python
# CORRECT
stdscr.addstr(0, 0, "Text", curses.color_pair(theme.colors.primary))

# WRONG - missing wrapper
stdscr.addstr(0, 0, "Text", theme.colors.primary)
```

**Exception**: Library methods like `draw_box()` expect raw numbers:

```python
# CORRECT - no wrapper for draw_box
theme.draw_box(stdscr, 0, 0, 10, 40, color_pair=theme.components.border)
```

See [API Documentation - Understanding Color Pairs](API.md#understanding-color-pairs) for complete details.

### 4. Theme Registration

Themes are registered with `ThemeManager` by name:

```python
from curses_themes import ThemeManager, Theme

# Built-in themes are auto-registered
theme = ThemeManager.load('dark')

# Register a custom theme
class MyTheme(Theme):
    # ... implementation ...

ThemeManager.register(MyTheme, 'my-theme')
theme = ThemeManager.load('my-theme')
```

---

## Working with Themes

### Loading Themes

```python
from curses_themes import ThemeManager

# Load by name (case-insensitive)
theme = ThemeManager.load('dark')
theme = ThemeManager.load('DARK')  # Same result
theme = ThemeManager.load('Dark')  # Same result

# Names normalize: spaces/underscores → hyphens
theme = ThemeManager.load('ti_99_4a')    # Works
theme = ThemeManager.load('ti-99-4a')    # Same theme
theme = ThemeManager.load('TI 99 4A')    # Same theme
```

### Applying Themes

```python
def main(stdscr):
    # Load theme
    theme = ThemeManager.load('dos')
    
    # Apply to screen - REQUIRED before using colors
    theme.apply(stdscr)
    
    # Now you can use theme colors
    stdscr.addstr(0, 0, "Hello!", curses.color_pair(theme.colors.primary))
```

### Using Semantic Colors

```python
def main(stdscr):
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)
    
    # Status messages
    stdscr.addstr(0, 0, "✓ File saved", 
                 curses.color_pair(theme.colors.success))
    stdscr.addstr(1, 0, "✗ Connection failed", 
                 curses.color_pair(theme.colors.error))
    stdscr.addstr(2, 0, "⚠ Low disk space", 
                 curses.color_pair(theme.colors.warning))
    stdscr.addstr(3, 0, "ℹ Press F1 for help", 
                 curses.color_pair(theme.colors.info))
```

### Using Component Colors

```python
def draw_button(window, y, x, text, focused, theme):
    """Draw a themed button"""
    if focused:
        color = theme.components.button_focused
        attr = curses.A_BOLD
    else:
        color = theme.components.button
        attr = curses.A_NORMAL
    
    window.addstr(y, x, f"[ {text} ]", 
                 curses.color_pair(color) | attr)

def main(stdscr):
    theme = ThemeManager.load('ti-99-4a')
    theme.apply(stdscr)
    
    draw_button(stdscr, 5, 10, "Save", focused=False, theme=theme)
    draw_button(stdscr, 7, 10, "Cancel", focused=True, theme=theme)
```

### Drawing Themed Boxes

```python
def main(stdscr):
    theme = ThemeManager.load('borland')
    theme.apply(stdscr)
    
    # Draw a bordered panel
    theme.draw_box(
        window=stdscr,
        y=2,          # Top-left Y
        x=5,          # Top-left X
        height=10,    # Height in characters
        width=40,     # Width in characters
        title="Settings"  # Optional title
    )
    
    # Content inside the box
    stdscr.addstr(3, 7, "Volume: 75%", 
                 curses.color_pair(theme.components.foreground))
```

### Runtime Theme Switching

```python
def main(stdscr):
    themes = ['dark', 'light', 'ti-99-4a', 'dos', 'dbase-iii']
    current = 0
    
    while True:
        # Load and apply new theme
        theme = ThemeManager.load(themes[current])
        theme.apply(stdscr)
        
        # Redraw UI
        stdscr.clear()
        stdscr.addstr(0, 0, f"Theme: {theme.name}", 
                     curses.color_pair(theme.components.button_focused))
        stdscr.addstr(2, 0, "Press 'n' for next, 'q' to quit")
        stdscr.refresh()
        
        # Handle input
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('n'):
            current = (current + 1) % len(themes)
```

---

## Creating Custom Themes

### Basic Custom Theme

```python
from curses_themes import Theme, ColorPair
from typing import Dict, Tuple

class MyTheme(Theme):
    """My custom terminal theme"""
    
    def __init__(self):
        super().__init__(
            name="My Theme",
            description="A personalized color scheme",
            author="Your Name"
        )
    
    # Define RGB colors (0-255)
    BG = (20, 20, 30)       # Dark blue-gray
    FG = (220, 220, 220)    # Light gray
    PRIMARY = (100, 180, 255)  # Sky blue
    
    # Component color pairs
    def get_background(self) -> ColorPair:
        return ColorPair(self.FG, self.BG)
    
    def get_button(self) -> ColorPair:
        return ColorPair(self.PRIMARY, self.BG)
    
    def get_button_focused(self) -> ColorPair:
        return ColorPair(self.BG, self.PRIMARY)
    
    def get_text_input(self) -> ColorPair:
        return ColorPair((150, 255, 150), self.BG)  # Light green
    
    def get_border(self) -> ColorPair:
        return ColorPair(self.FG, self.BG)
    
    def get_selection(self) -> ColorPair:
        return ColorPair(self.BG, self.FG)
    
    def get_disabled(self) -> ColorPair:
        return ColorPair((100, 100, 100), self.BG)  # Dark gray
    
    # Semantic color map
    def get_color_map(self) -> Dict[str, Tuple[int, int, int]]:
        return {
            'background': self.BG,
            'foreground': self.FG,
            'primary': self.PRIMARY,
            'success': (80, 200, 80),    # Green
            'error': (255, 80, 80),      # Red
            'warning': (255, 200, 80),   # Orange
            'info': (100, 180, 255),     # Blue
            'accent': (200, 100, 255),   # Purple
        }

# Register and use
from curses_themes import ThemeManager
ThemeManager.register(MyTheme, 'my-theme')

# Later...
theme = ThemeManager.load('my-theme')
```

### Custom Border Characters

```python
class UnicodeTheme(Theme):
    # ... other methods ...
    
    def get_border_chars(self) -> str:
        """
        Returns 8 characters: TL, T, TR, L, R, BL, B, BR
        """
        # Unicode single-line box
        return "┌─┐│└─┘│"
        
        # Or double-line box
        # return "╔═╗║╚═╝║"
        
        # Or rounded corners
        # return "╭─╮│╰─╯│"
        
        # Or ASCII for compatibility
        # return "+-+||+-+"
```

---

## Advanced Usage

### Multi-Panel Layouts

```python
def draw_layout(stdscr, theme):
    height, width = stdscr.getmaxyx()
    
    # Header
    theme.draw_box(stdscr, 0, 0, 3, width, title="Application")
    stdscr.addstr(1, 2, "Status: Running", 
                 curses.color_pair(theme.colors.success))
    
    # Left sidebar
    sidebar_width = width // 3
    theme.draw_box(stdscr, 3, 0, height - 6, sidebar_width, title="Menu")
    
    # Main content
    theme.draw_box(stdscr, 3, sidebar_width, height - 6, 
                  width - sidebar_width, title="Content")
    
    # Footer
    theme.draw_box(stdscr, height - 3, 0, 3, width)
    stdscr.addstr(height - 2, 2, "Press 'q' to quit", 
                 curses.color_pair(theme.components.foreground))
```

### Theme-Aware Widgets

```python
class Button:
    """A themed button widget"""
    def __init__(self, text, y, x, theme):
        self.text = text
        self.y = y
        self.x = x
        self.theme = theme
        self.focused = False
    
    def draw(self, window):
        if self.focused:
            color = self.theme.components.button_focused
            attr = curses.A_BOLD
        else:
            color = self.theme.components.button
            attr = curses.A_NORMAL
        
        window.addstr(self.y, self.x, f"[ {self.text} ]",
                     curses.color_pair(color) | attr)
    
    def set_focus(self, focused):
        self.focused = focused

# Usage
def main(stdscr):
    theme = ThemeManager.load('dbase-iv')
    theme.apply(stdscr)
    
    buttons = [
        Button("Save", 5, 10, theme),
        Button("Cancel", 7, 10, theme),
        Button("Help", 9, 10, theme),
    ]
    
    current = 0
    buttons[current].set_focus(True)
    
    while True:
        stdscr.clear()
        for btn in buttons:
            btn.draw(stdscr)
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_DOWN:
            buttons[current].set_focus(False)
            current = (current + 1) % len(buttons)
            buttons[current].set_focus(True)
```

### Configuration File Support

```python
import json
from pathlib import Path

def load_user_theme():
    """Load theme from user config"""
    config_file = Path.home() / '.config' / 'myapp' / 'config.json'
    
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
            return config.get('theme', 'dark')
    
    return 'dark'  # Default

def main(stdscr):
    theme_name = load_user_theme()
    theme = ThemeManager.load(theme_name)
    theme.apply(stdscr)
    # ... rest of app
```

---

## Windows Support

### Installation

```bash
# Install windows-curses first
pip install windows-curses

# Then install curses-themes
pip install curses-themes
```

### Terminal Recommendations

- **Windows Terminal** (best compatibility)
- **WSL** with any Linux terminal
- **ConEmu** or **Cmder**

Avoid: Old Command Prompt (cmd.exe) - limited color support

### Known Limitations

- 256-color support varies by terminal
- Unicode box-drawing may not render perfectly
- Some terminals only support 16 colors well

The library automatically adapts to your terminal's capabilities.

---

## Troubleshooting

### Colors Not Displaying

**Problem**: Colors appear wrong or not at all

**Solutions**:
1. Check terminal support: `echo $TERM`
2. Use a modern terminal (iTerm2, GNOME Terminal, Windows Terminal)
3. Try a different theme (some require 256 colors)
4. Verify curses initialization: `curses.has_colors()`

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'curses_themes'`

**Solutions**:
```bash
# Install the package
pip install -e .

# Or set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Theme Not Found

**Problem**: `KeyError: Theme 'xyz' not found`

**Solutions**:
```python
# List available themes
from curses_themes import ThemeManager
themes = ThemeManager.list_themes()
print(list(themes.keys()))

# Use exact name from the list
theme = ThemeManager.load('ti-99-4a')  # Not 'ti994a'
```

### Windows Curses Errors

**Problem**: `No module named '_curses'` on Windows

**Solution**:
```bash
pip install windows-curses
```

### Border Characters Not Displaying

**Problem**: Box borders show as `?` or garbage characters

**Solutions**:
1. Use ASCII borders: create theme with `get_border_chars() -> "+-+||+-+"`
2. Ensure UTF-8 encoding: `export LANG=en_US.UTF-8`
3. Use a Unicode-compatible terminal

---

## Best Practices

### 1. Always Use `curses.wrapper()`

```python
# GOOD
def main(stdscr):
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)
    # ... your code

if __name__ == "__main__":
    curses.wrapper(main)

# BAD - can leave terminal in broken state
stdscr = curses.initscr()
# ... your code
curses.endwin()
```

### 2. Apply Theme Before Using Colors

```python
# GOOD
theme = ThemeManager.load('dark')
theme.apply(stdscr)  # Must call before using theme.colors
stdscr.addstr(0, 0, "Text", curses.color_pair(theme.colors.primary))

# BAD - will raise RuntimeError
theme = ThemeManager.load('dark')
stdscr.addstr(0, 0, "Text", curses.color_pair(theme.colors.primary))
```

### 3. Use Semantic Colors for Flexibility

```python
# GOOD - adapts to theme changes
stdscr.addstr(0, 0, "Success", curses.color_pair(theme.colors.success))

# LESS FLEXIBLE - hardcoded to green
stdscr.addstr(0, 0, "Success", curses.color_pair(2))
```

### 4. Handle Terminal Size Changes

```python
import signal

def handle_resize(signum, frame):
    """Handle terminal resize"""
    curses.endwin()
    stdscr.refresh()

def main(stdscr):
    signal.signal(signal.SIGWINCH, handle_resize)
    # ... rest of code
```

### 5. Provide Theme Selection UI

```python
def select_theme(stdscr):
    """Let user choose a theme"""
    themes = list(ThemeManager.list_themes().keys())
    current = 0
    
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select Theme:")
        
        for i, name in enumerate(themes):
            if i == current:
                stdscr.addstr(i + 2, 2, f"> {name}", curses.A_BOLD)
            else:
                stdscr.addstr(i + 2, 2, f"  {name}")
        
        key = stdscr.getch()
        if key == curses.KEY_UP:
            current = max(0, current - 1)
        elif key == curses.KEY_DOWN:
            current = min(len(themes) - 1, current + 1)
        elif key == ord('\n'):
            return themes[current]
```

---

## Next Steps

- Browse the [Examples](examples/) directory for complete demos
- Read the [API Documentation](API.md) for detailed reference
- Check out [RETRO_THEMES.md](RETRO_THEMES.md) for retro computing themes
- See [CONTRIBUTING.md](CONTRIBUTING.md) to add your own themes

---

**Happy theming! 🎨**
