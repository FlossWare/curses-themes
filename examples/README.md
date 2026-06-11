# curses-themes Examples

This directory contains example programs demonstrating the features and capabilities of the **curses-themes** library. Examples progress from basic usage to advanced techniques, helping you learn how to build professional terminal user interfaces with themed components.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Examples by Difficulty](#examples-by-difficulty)
  - [Beginner](#beginner-examples)
  - [Intermediate](#intermediate-examples)
  - [Advanced](#advanced-examples)
- [Running Examples](#running-examples)
- [Learning Path](#learning-path)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- **Python 3.9 or higher**
- **curses-themes library installed**
  ```bash
  pip install curses-themes
  # OR install from source
  pip install -e .
  ```
- **Terminal with color support** (8, 16, or 256 colors)
- **Unix-like system** (Linux, macOS, WSL on Windows)

## Quick Start

Run any example from the project root or examples directory:

```bash
# From project root
python examples/basic_usage.py

# From examples directory
cd examples
python basic_usage.py
```

## Examples by Difficulty

### Beginner Examples

Perfect for getting started with curses-themes.

#### 1. basic_usage.py

**What it teaches:**
- Loading and applying themes
- Using semantic colors (success, error, warning, info)
- Drawing themed boxes with titles
- Proper curses initialization with `curses.wrapper()`

**Features:**
- Demonstrates all semantic color types
- Shows themed border boxes
- Clean, minimal example for reference

**Run it:**
```bash
python examples/basic_usage.py
```

**Key takeaways:**
- Theme loading: `ThemeManager.load('theme-name')`
- Applying themes: `theme.apply(stdscr)`
- Semantic colors: `theme.colors.success`, `theme.colors.error`, etc.
- Drawing boxes: `theme.draw_box(stdscr, y, x, height, width, title="...")`

---

#### 2. theme_switcher.py

**What it teaches:**
- Runtime theme switching
- Interactive keyboard controls
- Managing multiple themes
- Refreshing UI when theme changes

**Features:**
- Cycle through available themes (Next/Previous)
- Compare different color palettes side-by-side
- Interactive controls (n=next, p=previous, q=quit)
- Multiple themed boxes with different semantic colors

**Run it:**
```bash
python examples/theme_switcher.py
```

**Controls:**
- `n` - Next theme
- `p` - Previous theme  
- `q` - Quit

**Key takeaways:**
- Dynamic theme switching at runtime
- Preserving UI state across theme changes
- Using `theme.apply()` to update colors immediately

---

#### 3. custom_theme.py

**What it teaches:**
- Creating custom theme classes
- Implementing `get_color_map()` with RGB values
- Registering custom themes with ThemeManager
- Professional color palette design (Solarized example)

**Features:**
- Complete custom theme implementation (SolarizedDarkTheme)
- Theme registration and loading
- Metadata (name, description, author)
- RGB color definitions (0-255 range)

**Run it:**
```bash
python examples/custom_theme.py
```

**Key takeaways:**
- Subclass `Theme` for custom themes
- Override `get_color_map()` to define colors
- Use `ThemeManager.register(YourTheme)` to make it available
- Load custom themes by name: `ThemeManager.load('your-theme-name')`

---

### Intermediate Examples

Building practical interfaces with themed components.

#### 4. retro_themes_demo.py

**What it teaches:**
- Showcasing retro computer and database themes
- Historical context of vintage UIs
- Theme cycling in a presentation format
- Compatibility with limited Unicode terminals

**Features:**
- Demonstrates 5 retro themes: TI-99/4A, TRS-80, DOS, dBASE III, dBASE IV
- Historical descriptions for each theme
- Sample UI components (buttons, inputs, selections)
- Semantic color examples with fallback for non-Unicode terminals

**Run it:**
```bash
python examples/retro_themes_demo.py
```

**Controls:**
- `Any key` - Cycle to next theme
- `q` - Quit

**Key takeaways:**
- Loading built-in retro themes
- Displaying theme metadata (name, description)
- Unicode fallback patterns for broader compatibility
- Creating nostalgic retro aesthetics

---

#### 5. text_editor_demo.py

**What it teaches:**
- Multi-window layout design
- Building a practical text editor interface
- Status bars and line numbers
- File browser with selection highlighting
- Command palette with semantic feedback
- Modal dialog patterns

**Features:**
- Multi-pane layout: menu bar, editor area, file browser, status bar
- Line numbers with themed colors
- File browser sidebar with selection highlighting
- Status bar showing cursor position, file info, theme name
- Runtime theme switching (F1-F5 hotkeys)
- Command palette with success/error message colors
- Scrolling text viewport management
- Modal dialogs for save/open operations
- Demonstration of component colors (borders, selections, text input)

**Run it:**
```bash
python examples/text_editor_demo.py
```

**Controls:**
- `F1-F5` - Switch between themes
- `Arrow keys` - Navigate editor/file browser
- `Ctrl+S` - Save dialog (demo)
- `Ctrl+O` - Open dialog (demo)
- `q` - Quit

**Key takeaways:**
- Complex multi-window layouts
- Coordinating themed components
- Building practical editing interfaces
- Modal dialog patterns with `draw_box()`
- Runtime theme switching in real applications

---

#### 6. dialog_system_demo.py

**What it teaches:**
- Modal dialog patterns from classic UIs
- Message boxes with semantic colors
- Input dialogs with validation
- 3D effects (raised/sunken) for Borland-style UIs
- Button states and focus management
- Drop shadow effects

**Features:**
- Multiple dialog types: info, warning, error, question, custom
- Message boxes with appropriate semantic colors and icons
- Input dialogs with themed text fields and validation
- Confirmation dialogs (Yes/No/Cancel)
- Progress dialog with animated bar
- Multi-field form dialogs with tab navigation
- File picker dialog with directory tree
- 3D raised/sunken effects using `draw_box_3d()`
- Drop shadow effects for layered windows
- Keyboard shortcuts and focus indicators
- Button states: normal, focused, disabled

**Run it:**
```bash
python examples/dialog_system_demo.py
```

**Controls:**
- `1-9` - Show different dialog types
- `Tab` - Navigate form fields
- `Enter` - Confirm
- `Esc` - Cancel
- `q` - Quit

**Key takeaways:**
- Classic dialog box patterns
- Semantic color usage for message types
- 3D visual effects with themes
- Modal window management
- Focus and keyboard navigation

---

### Advanced Examples

Complex applications demonstrating sophisticated UI patterns.

#### 7. 3d_themes_demo.py

**What it teaches:**
- Borland-style 3D visual effects
- Raised windows with drop shadows
- Sunken input fields
- Overlapping window management
- Advanced 3D theme usage (Borland3DTheme, DBase4_3DTheme)

**Features:**
- Borland3DTheme with professional raised windows
- DBase4_3DTheme with Control Center style
- Side-by-side comparison of 3D themes
- Raised buttons vs sunken input fields
- Multiple overlapping windows showing shadow effects
- Interactive theme switching between 3D themes
- Fallback to 2D rendering for themes without 3D support

**Run it:**
```bash
python examples/3d_themes_demo.py
```

**Controls:**
- `n` - Next theme
- `b` - Switch to Borland3DTheme
- `d` - Switch to DBase4_3DTheme
- `q` - Quit

**Key takeaways:**
- Using `draw_box_3d()` for raised/sunken effects
- Drop shadow rendering techniques
- Managing overlapping windows with depth
- Fallback patterns for unsupported features
- Classic Borland IDE aesthetics

---

#### 8. table_browser_demo.py

**What it teaches:**
- Database-style table interfaces
- Pagination and sorting
- Column management and resizing
- Search/filter functionality
- Detail view panels
- Data-rich UI patterns perfect for retro themes

**Features:**
- Paginated table view with alternating row colors
- Column headers with sort indicators (themed arrows/symbols)
- Status bar showing record count, page numbers, filter status
- Column highlighting on hover/selection
- Search/filter bar with themed input fields
- Navigation controls (Page Up/Down, Home/End)
- Detail view panel showing selected record in themed box
- Support for multiple tables/views with tab switching
- Live theme switching to compare retro (dBASE, DOS) vs modern themes
- SQL-style command input area with syntax hints

**Run it:**
```bash
python examples/table_browser_demo.py
```

**Controls:**
- `Arrow keys` - Navigate table
- `Page Up/Down` - Page through data
- `Home/End` - Jump to first/last record
- `/` - Search/filter
- `Tab` - Switch between tables
- `F1-F5` - Switch themes
- `s` - Toggle sort column
- `q` - Quit

**Key takeaways:**
- Building data-rich interfaces
- Pagination patterns
- Column-based layouts
- Search and filtering UI
- Alternating row colors for readability
- Perfect showcase for dBASE retro themes

---

#### 9. system_monitor_demo.py

**What it teaches:**
- Real-time updating UIs
- Live data visualization with ASCII art
- Progress bars and gauges
- Semantic color usage for status indicators
- Panel-based dashboard layouts
- Time-based color changes (thresholds)

**Features:**
- Real-time updating graphs using ASCII art/block characters
- CPU usage meter with colored zones:
  - Success (green) for low usage
  - Warning (yellow) for medium usage
  - Error (red) for high usage
- Memory usage progress bar with percentage display
- Process list with sorted columns and themed selection
- Network traffic indicators with up/down arrows
- System uptime and load average displays
- Alert notifications using themed modal windows
- Panel layout with multiple bordered sections (`draw_box()`)
- Theme cycling to show how different palettes affect data visualization
- Updates every second demonstrating dynamic content handling

**Run it:**
```bash
python examples/system_monitor_demo.py
```

**Controls:**
- `Space` - Pause/resume updates
- `r` - Reset statistics
- `F1-F5` - Switch themes
- `q` - Quit

**Key takeaways:**
- Real-time UI updates without flicker
- Semantic colors for status indicators
- ASCII-based data visualization
- Dashboard-style layouts
- Threshold-based color changes
- Performance considerations for live updates

---

#### 10. theme_wizard_demo.py

**What it teaches:**
- Interactive theme creation
- Step-by-step wizard UI patterns
- Color picker implementation
- Live preview of theme changes
- Dynamic theme manipulation
- Code generation and export
- Theme configuration persistence

**Features:**
- Step-by-step wizard interface with progress indicator
- Color picker for each semantic element:
  - Background, foreground, primary
  - Success, error, warning, info, accent
- RGB value input with validation
- Live preview panel showing all theme elements in real-time
- Component showcase (buttons, inputs, borders, selections)
- Color palette suggestions (presets from popular themes)
- Side-by-side comparison with existing themes
- Export functionality generating Python `Theme` class code
- Save/load custom theme configurations to JSON
- Theme metadata editor (name, description, author)
- Border character customization preview
- Accessibility checker for color contrast ratios
- Integration demonstration with `ThemeManager.register()`

**Run it:**
```bash
python examples/theme_wizard_demo.py
```

**Controls:**
- `Arrow keys` - Navigate wizard steps
- `Tab` - Move between fields
- `Enter` - Confirm selection
- `e` - Export theme code
- `s` - Save configuration
- `p` - Preview theme
- `q` - Quit

**Key takeaways:**
- Building wizard-style interfaces
- Interactive color selection
- Live theme preview and updates
- Code generation from user input
- JSON configuration persistence
- Form validation patterns
- Advanced theme manipulation

---

## Running Examples

### From Project Root

```bash
# Run a specific example
python examples/basic_usage.py

# Run with error handling
python -u examples/text_editor_demo.py 2>&1 | tee output.log
```

### From Examples Directory

```bash
cd examples

# Run directly
./basic_usage.py  # If executable bit is set
python basic_usage.py
```

### Troubleshooting Terminal Issues

If examples don't run properly:

```bash
# Check terminal type
echo $TERM

# Should be: xterm-256color, screen-256color, or similar

# Set terminal type if needed
export TERM=xterm-256color

# Run example again
python examples/basic_usage.py
```

## Learning Path

Follow this recommended progression to master curses-themes:

### Week 1: Foundations
1. **basic_usage.py** - Learn core concepts (30 min)
2. **theme_switcher.py** - Understand theme management (30 min)
3. **custom_theme.py** - Create your first custom theme (1 hour)

**Goal:** Understand theme loading, semantic colors, and basic UI components.

### Week 2: Practical Applications
4. **retro_themes_demo.py** - Explore built-in themes (30 min)
5. **text_editor_demo.py** - Study multi-window layouts (2 hours)
6. **dialog_system_demo.py** - Master modal dialogs (1.5 hours)

**Goal:** Build practical interfaces with multiple components and layouts.

### Week 3: Advanced Techniques
7. **3d_themes_demo.py** - Learn 3D effects (1 hour)
8. **table_browser_demo.py** - Build data interfaces (2 hours)
9. **system_monitor_demo.py** - Create live dashboards (2 hours)

**Goal:** Implement advanced UI patterns and real-time updates.

### Week 4: Mastery
10. **theme_wizard_demo.py** - Advanced theme manipulation (3 hours)
11. **Build your own application** using learned patterns (ongoing)

**Goal:** Create production-quality themed applications.

## Common Patterns

### Pattern 1: Basic Theme Setup

```python
import curses
from curses_themes import ThemeManager

def main(stdscr):
    # Load and apply theme
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)
    
    # Your UI code here
    stdscr.addstr(0, 0, "Hello", theme.colors.primary)
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
```

**Used in:** basic_usage.py, theme_switcher.py, custom_theme.py

---

### Pattern 2: Runtime Theme Switching

```python
# Store current theme index
current_theme_idx = 0
theme_names = ['default', 'dark', 'light']

# In event loop
if key == ord('t'):
    current_theme_idx = (current_theme_idx + 1) % len(theme_names)
    theme = ThemeManager.load(theme_names[current_theme_idx])
    theme.apply(stdscr)
    # Redraw UI with new theme
    draw_ui(stdscr, theme)
```

**Used in:** theme_switcher.py, text_editor_demo.py, retro_themes_demo.py

---

### Pattern 3: Semantic Color Usage

```python
# Use semantic colors for UI feedback
def show_message(stdscr, y, x, msg, msg_type='info'):
    color_map = {
        'success': theme.colors.success,
        'error': theme.colors.error,
        'warning': theme.colors.warning,
        'info': theme.colors.info,
    }
    color = color_map.get(msg_type, theme.colors.foreground)
    stdscr.addstr(y, x, msg, curses.color_pair(color))
```

**Used in:** text_editor_demo.py, dialog_system_demo.py, system_monitor_demo.py

---

### Pattern 4: Modal Dialog Boxes

```python
def show_dialog(stdscr, theme, title, message, width=50):
    height, scr_width = stdscr.getmaxyx()
    
    # Calculate centered position
    dialog_h = 8
    dialog_y = (height - dialog_h) // 2
    dialog_x = (scr_width - width) // 2
    
    # Draw dialog box
    theme.draw_box(stdscr, dialog_y, dialog_x, dialog_h, width, title=title)
    
    # Add message inside
    msg_y = dialog_y + 2
    msg_x = dialog_x + 2
    stdscr.addstr(msg_y, msg_x, message, theme.colors.foreground)
    
    # Draw buttons
    btn_y = dialog_y + dialog_h - 3
    theme.draw_box(stdscr, btn_y, dialog_x + 10, 3, 12)
    stdscr.addstr(btn_y + 1, dialog_x + 14, "OK", theme.colors.button_focused)
    
    stdscr.refresh()
    return stdscr.getch()
```

**Used in:** dialog_system_demo.py, text_editor_demo.py, system_monitor_demo.py

---

### Pattern 5: Multi-Window Layouts

```python
def create_layout(stdscr, theme):
    height, width = stdscr.getmaxyx()
    
    # Menu bar at top
    menu_h = 1
    stdscr.addstr(0, 0, " File  Edit  View ", theme.colors.selection)
    
    # Main content area
    content_y = menu_h
    content_h = height - menu_h - 3  # Leave room for status
    theme.draw_box(stdscr, content_y, 0, content_h, width)
    
    # Status bar at bottom
    status_y = height - 2
    stdscr.addstr(status_y, 0, " Ready ", theme.colors.info)
    stdscr.addstr(status_y, width - 20, f"Theme: {theme.name}", 
                  theme.colors.foreground)
```

**Used in:** text_editor_demo.py, table_browser_demo.py, system_monitor_demo.py

---

### Pattern 6: Custom Theme Registration

```python
from curses_themes import Theme, ThemeManager

class MyTheme(Theme):
    def __init__(self):
        super().__init__(
            name="My Theme",
            description="Custom theme for my app",
            author="Your Name"
        )
    
    def get_color_map(self):
        return {
            'background': (0, 0, 0),
            'foreground': (255, 255, 255),
            'primary': (0, 120, 215),
            'success': (0, 200, 0),
            'error': (200, 0, 0),
            'warning': (255, 165, 0),
            'info': (100, 150, 255),
            'accent': (150, 100, 255),
        }

# Register once at startup
ThemeManager.register(MyTheme)

# Use anywhere
theme = ThemeManager.load('my-theme')
```

**Used in:** custom_theme.py, theme_wizard_demo.py

---

## Troubleshooting

### Issue: Colors don't appear correctly

**Symptoms:**
- All text appears white or default colors
- No color changes when switching themes

**Solutions:**

1. **Check terminal color support:**
   ```bash
   echo $TERM  # Should show xterm-256color or similar
   tput colors # Should show 8, 16, or 256
   ```

2. **Set proper TERM variable:**
   ```bash
   export TERM=xterm-256color
   python examples/basic_usage.py
   ```

3. **Test with simple color script:**
   ```python
   import curses
   
   def test(stdscr):
       if curses.has_colors():
           print(f"Colors available: {curses.COLORS}")
           print(f"Color pairs: {curses.COLOR_PAIRS}")
       else:
           print("No color support!")
   
   curses.wrapper(test)
   ```

---

### Issue: Unicode characters display incorrectly

**Symptoms:**
- Box drawing characters appear as `?` or garbage
- Arrows and icons don't render

**Solutions:**

1. **Check locale settings:**
   ```bash
   locale  # Should include UTF-8 encoding
   export LC_ALL=en_US.UTF-8
   export LANG=en_US.UTF-8
   ```

2. **Use ASCII fallback in your code:**
   ```python
   try:
       stdscr.addstr(y, x, "✓ Success", color)
   except UnicodeEncodeError:
       stdscr.addstr(y, x, "* Success", color)
   ```

3. **Test terminal Unicode support:**
   ```bash
   echo -e "✓ ✗ ← →"  # Should show ✓ ✗ ← →
   ```

---

### Issue: Program crashes or hangs

**Symptoms:**
- Terminal state corrupted after crash
- Cursor stays hidden
- Terminal needs reset

**Solutions:**

1. **Always use curses.wrapper():**
   ```python
   # Good - handles cleanup automatically
   if __name__ == "__main__":
       curses.wrapper(main)
   
   # Bad - can leave terminal in broken state
   if __name__ == "__main__":
       stdscr = curses.initscr()
       main(stdscr)
   ```

2. **Add exception handling:**
   ```python
   if __name__ == "__main__":
       try:
           curses.wrapper(main)
       except KeyboardInterrupt:
           print("\nProgram interrupted by user")
       except Exception as e:
           print(f"\nError: {e}")
           import traceback
           traceback.print_exc()
   ```

3. **Reset terminal manually if needed:**
   ```bash
   reset  # or 'tput reset'
   stty sane
   ```

---

### Issue: Example not found or import errors

**Symptoms:**
- `ModuleNotFoundError: No module named 'curses_themes'`
- `FileNotFoundError` when running examples

**Solutions:**

1. **Install curses-themes:**
   ```bash
   # From PyPI
   pip install curses-themes
   
   # Or from source
   cd /path/to/curses-themes
   pip install -e .
   ```

2. **Run from correct directory:**
   ```bash
   # From project root
   python examples/basic_usage.py
   
   # NOT from random directory
   ```

3. **Check Python path:**
   ```python
   import sys
   print(sys.path)  # Should include curses_themes location
   ```

---

### Issue: Screen flickers during updates

**Symptoms:**
- UI flashes when redrawing
- Text appears briefly then disappears
- Screen looks unstable

**Solutions:**

1. **Clear and redraw completely:**
   ```python
   # Clear once
   stdscr.clear()
   
   # Draw all elements
   draw_ui(stdscr, theme)
   
   # Refresh once at end
   stdscr.refresh()
   ```

2. **Use windows instead of stdscr:**
   ```python
   # Create window for stable area
   win = curses.newwin(height, width, y, x)
   win.clear()
   # Draw to win
   win.refresh()
   ```

3. **Avoid redundant clears:**
   ```python
   # Bad - clears unnecessarily
   while True:
       stdscr.clear()  # Every iteration!
       draw_ui()
   
   # Good - clear only when needed
   stdscr.clear()
   while True:
       stdscr.erase()  # Lighter than clear()
       draw_ui()
   ```

---

### Issue: Windows/WSL compatibility problems

**Symptoms:**
- curses module not available on Windows
- Examples fail on Windows Command Prompt

**Solutions:**

1. **Use WSL (Windows Subsystem for Linux):**
   ```bash
   # Install WSL if not already installed
   wsl --install
   
   # Run examples in WSL
   wsl
   cd /mnt/c/path/to/curses-themes
   python examples/basic_usage.py
   ```

2. **Use windows-curses package (fallback):**
   ```bash
   pip install windows-curses
   python examples/basic_usage.py
   ```

3. **Use a proper terminal emulator:**
   - Windows Terminal (recommended)
   - ConEmu
   - Cmder
   - Not: Command Prompt or PowerShell ISE

---

## Additional Resources

### Documentation
- **[Main README](../README.md)** - Project overview and quick start
- **[API Reference](../API.md)** - Complete API documentation
- **[Theme Guide](../THEMES.md)** - Theme creation and customization
- **[Retro Themes](../RETRO_THEMES.md)** - Historical context for vintage themes
- **[3D Effects](../3D_THEMES.md)** - Borland-style 3D theming guide

### Getting Help
- **GitHub Issues**: [Report bugs or request features](https://github.com/FlossWare/curses-themes/issues)
- **Discussions**: [Ask questions and share projects](https://github.com/FlossWare/curses-themes/discussions)
- **Contributing**: See [CONTRIBUTING.md](../CONTRIBUTING.md)

### Related Projects
- **[FlossWare/curses-java](https://github.com/FlossWare/curses-java)** - Original Java implementation

---

## License

All examples are licensed under the GNU General Public License v3.0 or later.  
See [LICENSE](../LICENSE) for details.

---

**Happy theming!** Build beautiful terminal interfaces with curses-themes.
