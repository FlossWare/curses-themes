# curses-themes API Documentation

## Overview

`curses-themes` is a lightweight theme support library for Python curses applications. It provides professional theming capabilities with zero external dependencies, inspired by the FlossWare curses-java library.

**Version:** 0.1.0  
**License:** GPL-3.0  
**Author:** FlossWare

## Installation

```bash
pip install curses-themes
```

## Quick Start

```python
import curses
from curses_themes import ThemeManager

def main(stdscr):
    # Load and apply a theme
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)
    
    # Use semantic colors
    stdscr.addstr(0, 0, "Success!", curses.color_pair(theme.colors.success))
    stdscr.addstr(1, 0, "Error!", curses.color_pair(theme.colors.error))
    
    # Draw themed boxes
    theme.draw_box(stdscr, 3, 2, 10, 40, title="My Panel")
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
```

---

## Core Classes

### Theme

Abstract base class for creating curses themes. All custom themes must inherit from this class and implement the required methods.

#### Constructor

```python
Theme(name: str, description: str = "", author: str = "")
```

**Parameters:**
- `name` (str): Human-readable theme name
- `description` (str, optional): Brief description of the theme's appearance or purpose
- `author` (str, optional): Name of the theme creator

**Example:**
```python
class MyTheme(Theme):
    def __init__(self):
        super().__init__(
            name="My Theme",
            description="A custom theme with blue accents",
            author="Your Name"
        )
```

#### Abstract Methods

##### get_color_map()

```python
def get_color_map(self) -> Dict[str, Tuple[int, int, int]]
```

**Required implementation.** Returns RGB color definitions for the theme.

**Returns:**
- `Dict[str, Tuple[int, int, int]]`: Dictionary mapping semantic color names to RGB tuples (0-255)

**Required Keys:**
- `background`: Default background color
- `foreground`: Default text color
- `primary`: Main UI color for highlights and focus
- `success`: Positive feedback and successful operations
- `error`: Error messages and critical warnings
- `warning`: Caution messages and non-critical warnings
- `info`: Informational messages and help text
- `accent`: Secondary highlight color

**Example:**
```python
def get_color_map(self):
    return {
        'background': (0, 0, 0),      # Black
        'foreground': (255, 255, 255), # White
        'primary': (0, 120, 215),      # Blue
        'success': (16, 124, 16),      # Green
        'error': (232, 17, 35),        # Red
        'warning': (193, 156, 0),      # Yellow
        'info': (0, 120, 212),         # Blue
        'accent': (142, 68, 173),      # Purple
    }
```

#### Component Color Methods

These methods define color pairs for UI components. All methods return `ColorPair` objects or `None` if not implemented.

##### get_background()

```python
def get_background(self) -> Optional[ColorPair]
```

Returns the background color pair for normal components.

**Returns:**
- `ColorPair` or `None`: Foreground and background colors for normal background

**Example:**
```python
def get_background(self) -> ColorPair:
    return ColorPair((255, 255, 255), (0, 0, 0))  # White on Black
```

##### get_button()

```python
def get_button(self) -> Optional[ColorPair]
```

Returns the color pair for buttons in normal state.

**Returns:**
- `ColorPair` or `None`: Colors for button rendering

**Example:**
```python
def get_button(self) -> ColorPair:
    return ColorPair((0, 255, 255), (0, 0, 0))  # Cyan on Black
```

##### get_button_focused()

```python
def get_button_focused(self) -> Optional[ColorPair]
```

Returns the color pair for buttons when focused.

**Returns:**
- `ColorPair` or `None`: Colors for focused button rendering

**Example:**
```python
def get_button_focused(self) -> ColorPair:
    return ColorPair((0, 0, 0), (0, 255, 255))  # Black on Cyan (inverted)
```

##### get_text_input()

```python
def get_text_input(self) -> Optional[ColorPair]
```

Returns the color pair for text input fields.

**Returns:**
- `ColorPair` or `None`: Colors for text input rendering

##### get_border()

```python
def get_border(self) -> Optional[ColorPair]
```

Returns the color pair for borders and frames.

**Returns:**
- `ColorPair` or `None`: Colors for border rendering

##### get_selection()

```python
def get_selection(self) -> Optional[ColorPair]
```

Returns the color pair for selected/highlighted items.

**Returns:**
- `ColorPair` or `None`: Colors for selection rendering

##### get_disabled()

```python
def get_disabled(self) -> Optional[ColorPair]
```

Returns the color pair for disabled components.

**Returns:**
- `ColorPair` or `None`: Colors for disabled component rendering

#### Border Configuration

##### get_border_chars()

```python
def get_border_chars(self) -> str
```

Returns border characters for drawing boxes. Override to provide custom border styles.

**Returns:**
- `str`: String with 8 characters representing: top-left, top, top-right, left, right, bottom-left, bottom, bottom-right

**Default:** `"+-+||+-+"` (ASCII box)  
**Unicode Example:** `"┌─┐││└─┘"` (Unicode box-drawing)

**Example:**
```python
def get_border_chars(self) -> str:
    return "┌─┐││└─┘"  # Unicode box characters
```

#### Theme Application

##### apply()

```python
def apply(self, stdscr) -> None
```

Applies the theme to a curses screen. **Must be called before using theme.colors, theme.components, or theme.draw_box().**

**Parameters:**
- `stdscr`: Curses window object (typically from `curses.wrapper`)

**Raises:**
- `RuntimeError`: If color initialization fails

**Example:**
```python
def main(stdscr):
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)
    # Now theme.colors and theme.components are available
```

#### Properties

##### colors

```python
@property
def colors(self) -> SemanticColors
```

Returns semantic color pairs for the theme. This is the legacy API maintained for backward compatibility.

**Returns:**
- `SemanticColors`: Instance with initialized color pairs

**Raises:**
- `RuntimeError`: If `apply()` has not been called

**Example:**
```python
theme.apply(stdscr)
stdscr.addstr(0, 0, "Success!", curses.color_pair(theme.colors.success))
stdscr.addstr(1, 0, "Error!", curses.color_pair(theme.colors.error))
```

##### components

```python
@property
def components(self) -> ComponentColors
```

Returns component-based color pairs for the theme. **This is the primary API** matching curses-java Theme interface.

**Returns:**
- `ComponentColors`: Instance with initialized color pairs

**Raises:**
- `RuntimeError`: If `apply()` has not been called

**Example:**
```python
theme.apply(stdscr)
stdscr.addstr(0, 0, "Button", curses.color_pair(theme.components.button))
stdscr.addstr(1, 0, "Input: ", curses.color_pair(theme.components.text_input))
```

#### Drawing Methods

##### draw_box()

```python
def draw_box(
    self,
    window,
    y: int,
    x: int,
    height: int,
    width: int,
    title: str = "",
    color_pair: Optional[int] = None
) -> None
```

Draws a themed border box on the given window.

**Parameters:**
- `window`: Curses window to draw on
- `y` (int): Top-left Y coordinate
- `x` (int): Top-left X coordinate
- `height` (int): Box height in characters
- `width` (int): Box width in characters
- `title` (str, optional): Title to display centered in top border
- `color_pair` (int, optional): Color pair number to use (defaults to border color)

**Raises:**
- `ValueError`: If box dimensions are too small (minimum 2x2)

**Example:**
```python
# Draw a box with title
theme.draw_box(stdscr, 2, 5, 10, 40, title="Settings")

# Draw a box with custom color
theme.draw_box(stdscr, 15, 5, 5, 40, 
               color_pair=theme.components.button_focused)
```

---

### ThemeManager

Singleton manager for theme registration and loading. Provides a central registry for all available themes.

**Note:** This is a singleton class. All methods are classmethods. **Do not instantiate this class.**

#### Class Methods

##### register()

```python
@classmethod
def register(cls, theme_class: Type[Theme], name: Optional[str] = None) -> None
```

Registers a theme class for use.

**Parameters:**
- `theme_class` (Type[Theme]): Theme class (subclass of Theme) to register
- `name` (str, optional): Custom name. If not provided, uses theme.name from a temporary instance

**Raises:**
- `TypeError`: If theme_class is not a Theme subclass
- `ValueError`: If a theme with this name is already registered

**Example:**
```python
class MyTheme(Theme):
    def __init__(self):
        super().__init__("My Theme", "A custom theme")
    
    def get_color_map(self):
        return {...}

# Register with automatic name (derived from theme.name)
ThemeManager.register(MyTheme)

# Register with custom name
ThemeManager.register(MyTheme, 'my-custom')
```

##### load()

```python
@classmethod
def load(cls, name: str) -> Theme
```

Loads a theme by name. Creates a new instance of the requested theme.

**Parameters:**
- `name` (str): Theme name (case-insensitive, spaces/underscores converted to hyphens)

**Returns:**
- `Theme`: New Theme instance

**Raises:**
- `KeyError`: If theme is not registered

**Example:**
```python
# Load built-in theme
theme = ThemeManager.load('dark')

# Names are normalized (all equivalent)
theme = ThemeManager.load('Dark')
theme = ThemeManager.load('dark')
theme = ThemeManager.load('DARK')

# Spaces and underscores normalized to hyphens
theme = ThemeManager.load('TI 99/4A')  # Same as 'ti-99-4a'
theme = ThemeManager.load('my_custom_theme')  # Same as 'my-custom-theme'
```

##### list_themes()

```python
@classmethod
def list_themes(cls) -> Dict[str, Dict[str, str]]
```

Lists all registered themes with metadata.

**Returns:**
- `Dict[str, Dict[str, str]]`: Dictionary mapping theme names to metadata dictionaries with keys: 'name', 'description', 'author'

**Example:**
```python
themes = ThemeManager.list_themes()
for name, info in themes.items():
    print(f"{name}:")
    print(f"  Name: {info['name']}")
    print(f"  Description: {info['description']}")
    print(f"  Author: {info['author']}")

# Output:
# dark:
#   Name: Dark
#   Description: Dark theme with light text on dark background
#   Author: FlossWare
```

##### get_current()

```python
@classmethod
def get_current(cls) -> Optional[Theme]
```

Returns the currently active theme.

**Returns:**
- `Theme` or `None`: Current Theme instance, or None if no theme has been loaded

**Example:**
```python
current = ThemeManager.get_current()
if current:
    print(f"Current theme: {current.name}")
```

##### unregister()

```python
@classmethod
def unregister(cls, name: str) -> None
```

Unregisters a theme by name.

**Parameters:**
- `name` (str): Name of theme to unregister

**Raises:**
- `KeyError`: If theme is not registered

**Example:**
```python
ThemeManager.unregister('my-custom-theme')
```

##### reset()

```python
@classmethod
def reset(cls) -> None
```

Resets the theme manager state. Clears all registered themes and current theme. **This is primarily for testing purposes.**

**Warning:** This will unregister all themes, including built-in themes. They will be re-registered on next `load()` or `list_themes()` call.

---

### ColorManager

Manages color initialization and terminal capability detection. Handles the complexities of working with different terminal color capabilities (8, 16, or 256 colors).

#### Constructor

```python
ColorManager(stdscr)
```

**Parameters:**
- `stdscr`: Curses window object (typically from `curses.wrapper`)

**Raises:**
- `RuntimeError`: If the terminal doesn't support colors

**Example:**
```python
def main(stdscr):
    manager = ColorManager(stdscr)
    colors, components = manager.initialize_theme(my_theme)
    stdscr.addstr(0, 0, "Hello", curses.color_pair(colors.primary))
```

#### Attributes

- `stdscr`: The curses window object
- `color_count` (int): Number of colors supported (8, 16, or 256)

#### State Persistence

**Important:** ColorManager uses class-level state that persists across all instances.

The `_next_pair` counter and `_pair_cache` dictionary are class variables, not instance variables. This means:

- Creating multiple ColorManager instances does NOT reset color pairs
- All instances share the same color pair allocation pool
- Color pairs persist until the Python process exits
- The cache ensures identical color combinations reuse the same pair number

This design prevents duplicate color pair allocation and helps avoid exceeding the terminal's `COLOR_PAIRS` limit.

**Example:**
```python
def main(stdscr):
    # First manager allocates pairs 1-10
    mgr1 = ColorManager(stdscr)
    semantic1, component1 = mgr1.initialize_theme(theme1)
    
    # Second manager continues from pair 11
    # (or reuses cached pairs if colors match)
    mgr2 = ColorManager(stdscr)
    semantic2, component2 = mgr2.initialize_theme(theme2)
    
    # Both managers share the same pair cache
    # Same RGB combinations return the same pair numbers
```

**Testing Note:** The `reset()` method exists primarily for test isolation. In production code, you should rarely need to call it.

#### Methods

##### initialize_theme()

```python
def initialize_theme(self, theme) -> Tuple[SemanticColors, ComponentColors]
```

Initializes all color pairs for a theme. Converts the theme's RGB color map and component colors to curses color pairs appropriate for the terminal's capabilities.

**Parameters:**
- `theme`: Theme instance with `get_color_map()` and component methods

**Returns:**
- `Tuple[SemanticColors, ComponentColors]`: Initialized color pair numbers

**Raises:**
- `ValueError`: If color map is missing required keys
- `RuntimeError`: If color initialization fails

**Example:**
```python
manager = ColorManager(stdscr)
semantic_colors, component_colors = manager.initialize_theme(my_theme)

# Use the colors
stdscr.addstr(0, 0, "Text", curses.color_pair(semantic_colors.primary))
stdscr.addstr(1, 0, "Button", curses.color_pair(component_colors.button))
```

## Understanding Color Pairs

### What Are Color Pair Numbers?

When you access `theme.colors.primary` or `theme.components.button`, you get an **integer** (the color pair number), not a curses attribute. This number is an internal identifier that curses uses to track foreground/background color combinations.

```python
theme = ThemeManager.load('dark')
theme.apply(stdscr)

print(type(theme.colors.primary))  # <class 'int'>
print(theme.colors.primary)        # 1 (or some other integer)
```

### The curses.color_pair() Wrapper

To use a color pair number with curses display functions, you **must** wrap it with `curses.color_pair()`:

```python
# CORRECT - wrap the number
stdscr.addstr(0, 0, "Text", curses.color_pair(theme.colors.primary))

# WRONG - using raw number
stdscr.addstr(0, 0, "Text", theme.colors.primary)  # May display incorrectly or crash
```

### When to Use Each Form

#### Use curses.color_pair() wrapper:

Always use `curses.color_pair()` when passing colors to **curses display functions**:

- `window.addstr(y, x, text, curses.color_pair(num))`
- `window.addch(y, x, ch, curses.color_pair(num))`
- `window.bkgd(' ', curses.color_pair(num))`
- `window.chgat(y, x, n, curses.color_pair(num))`
- `window.attrset(curses.color_pair(num))`

```python
# All correct usages
stdscr.addstr(0, 0, "Success", curses.color_pair(theme.colors.success))
stdscr.bkgd(' ', curses.color_pair(theme.components.background))
stdscr.chgat(0, 0, 10, curses.color_pair(theme.colors.error))
```

#### Use raw color pair numbers:

Use the raw integer when passing to **library methods that expect pair numbers**:

- `theme.draw_box(window, y, x, h, w, color_pair=num)` - No wrapper needed
- Storing in data structures for later use
- Comparing color pair values

```python
# Correct - draw_box expects the raw number
theme.draw_box(stdscr, 0, 0, 10, 40, color_pair=theme.components.border)

# Wrong - don't wrap when passing to library methods
theme.draw_box(stdscr, 0, 0, 10, 40, 
               color_pair=curses.color_pair(theme.components.border))  # WRONG!
```

### Common Mistakes

#### Mistake 1: Forgetting the wrapper

```python
# WRONG - missing curses.color_pair()
stdscr.addstr(0, 0, "Error", theme.colors.error)

# CORRECT
stdscr.addstr(0, 0, "Error", curses.color_pair(theme.colors.error))
```

#### Mistake 2: Double-wrapping

```python
# WRONG - draw_box internally applies curses.color_pair()
theme.draw_box(stdscr, 0, 0, 10, 40, 
               color_pair=curses.color_pair(theme.components.border))

# CORRECT - pass raw number
theme.draw_box(stdscr, 0, 0, 10, 40, 
               color_pair=theme.components.border)
```

#### Mistake 3: Using hardcoded numbers

```python
# WRONG - hardcoded, not theme-aware
stdscr.addstr(0, 0, "Text", curses.color_pair(1))

# CORRECT - use theme color names
stdscr.addstr(0, 0, "Text", curses.color_pair(theme.colors.primary))
```

### Complete Working Example

```python
import curses
from curses_themes import ThemeManager

def main(stdscr):
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)
    
    # Display functions - use curses.color_pair()
    stdscr.addstr(0, 0, "Title", 
                  curses.color_pair(theme.colors.primary) | curses.A_BOLD)
    stdscr.addstr(2, 0, "Success message", 
                  curses.color_pair(theme.colors.success))
    stdscr.addstr(3, 0, "[Button]", 
                  curses.color_pair(theme.components.button))
    
    # Background - use curses.color_pair()
    stdscr.bkgd(' ', curses.color_pair(theme.components.background))
    
    # Library methods - use raw number
    theme.draw_box(stdscr, 5, 0, 10, 40, 
                   title="Panel",
                   color_pair=theme.components.border)
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
```

### Why This Design?

This API design matches the standard curses model:

1. **Separation of concerns**: Color pair numbers are identifiers, `curses.color_pair()` converts them to display attributes
2. **Flexibility**: You can combine color pairs with other attributes using bitwise OR:
   ```python
   curses.color_pair(theme.colors.primary) | curses.A_BOLD | curses.A_UNDERLINE
   ```
3. **Performance**: Raw numbers can be stored and passed around efficiently
4. **Compatibility**: Works with standard curses API conventions

### Quick Reference

| Context | Use | Example |
|---------|-----|----------|
| `addstr()`, `addch()` | `curses.color_pair(num)` | `stdscr.addstr(0, 0, "Text", curses.color_pair(theme.colors.primary))` |
| `bkgd()`, `chgat()` | `curses.color_pair(num)` | `stdscr.bkgd(' ', curses.color_pair(theme.components.background))` |
| `draw_box()` | Raw number | `theme.draw_box(stdscr, 0, 0, 10, 40, color_pair=theme.components.border)` |
| Storing in variables | Raw number | `border_color = theme.components.border` |
| Combining with attributes | `curses.color_pair(num)` | `curses.color_pair(theme.colors.error) | curses.A_BOLD` |

---

##### reset()

```python
def reset(self) -> None
```

Resets the class-level color pair counter and cache. **This affects ALL ColorManager instances.**

**Warning:** This is a class-level operation. Calling `reset()` on any ColorManager instance will invalidate color pairs created by ALL instances. Previously allocated pair numbers will become invalid.

**Use Cases:**
- Test isolation (pytest fixtures)
- Never use in production code

**Example:**
```python
# In pytest conftest.py
@pytest.fixture(autouse=True)
def reset_color_manager():
    from curses_themes.colors import ColorManager
    yield
    ColorManager._next_pair = 1
    ColorManager._pair_cache.clear()
```

#### Color Conversion Methods

The following methods handle RGB-to-palette conversion and are used internally by `initialize_theme()`.

##### _rgb_to_curses_color()

```python
def _rgb_to_curses_color(self, r: int, g: int, b: int) -> int
```

Converts RGB values to a curses color number. Adapts to terminal capabilities automatically.

**Parameters:**
- `r` (int): Red component (0-255)
- `g` (int): Green component (0-255)
- `b` (int): Blue component (0-255)

**Returns:**
- `int`: Curses color number appropriate for terminal capability

---

### SemanticColors

Container for semantic color pairs used by themes. Provides named access to curses color pair numbers for common UI elements.

#### Constructor

```python
SemanticColors(
    primary: int,
    success: int,
    error: int,
    warning: int,
    info: int,
    background: int,
    foreground: int,
    accent: int
)
```

**Parameters:**
All parameters are curses color pair numbers (integers) that can be used with `curses.color_pair()`.

- `primary` (int): Main UI color for highlights and focus
- `success` (int): Positive feedback and successful operations
- `error` (int): Error messages and critical warnings
- `warning` (int): Caution messages and non-critical warnings
- `info` (int): Informational messages and help text
- `background` (int): Default background color
- `foreground` (int): Default text color
- `accent` (int): Secondary highlight color

#### Attributes

All constructor parameters are available as instance attributes.

#### Usage Example

```python
theme = ThemeManager.load('dark')
theme.apply(stdscr)

# Access semantic colors
stdscr.addstr(0, 0, "Success!", curses.color_pair(theme.colors.success))
stdscr.addstr(1, 0, "Error!", curses.color_pair(theme.colors.error))
stdscr.addstr(2, 0, "Warning!", curses.color_pair(theme.colors.warning))
stdscr.addstr(3, 0, "Info", curses.color_pair(theme.colors.info))
stdscr.addstr(4, 0, "Primary", curses.color_pair(theme.colors.primary))
stdscr.addstr(5, 0, "Accent", curses.color_pair(theme.colors.accent))
```

---

### ComponentColors

Container for component-based color pairs used by themes. This is the primary API matching curses-java Theme interface.

#### Constructor

```python
ComponentColors(
    background: int,
    button: int,
    button_focused: int,
    text_input: int,
    border: int,
    selection: int,
    disabled: int
)
```

**Parameters:**
All parameters are curses color pair numbers (integers) that can be used with `curses.color_pair()`.

- `background` (int): Normal background color pair
- `button` (int): Button in normal state
- `button_focused` (int): Button when focused
- `text_input` (int): Text input fields
- `border` (int): Borders and frames
- `selection` (int): Selected/highlighted items
- `disabled` (int): Disabled components

#### Attributes

All constructor parameters are available as instance attributes.

#### Usage Example

```python
theme = ThemeManager.load('dark')
theme.apply(stdscr)

# Access component colors
stdscr.addstr(0, 0, "Background", curses.color_pair(theme.components.background))
stdscr.addstr(1, 0, "[Button]", curses.color_pair(theme.components.button))
stdscr.addstr(2, 0, "[Focused]", curses.color_pair(theme.components.button_focused))
stdscr.addstr(3, 0, "Input: ", curses.color_pair(theme.components.text_input))
stdscr.addstr(4, 0, "Border", curses.color_pair(theme.components.border))
stdscr.addstr(5, 0, "Selected", curses.color_pair(theme.components.selection))
stdscr.addstr(6, 0, "Disabled", curses.color_pair(theme.components.disabled))
```

---

### ColorPair

Represents a foreground/background color pair with RGB values.

#### Constructor

```python
ColorPair(foreground: Tuple[int, int, int], background: Tuple[int, int, int])
```

**Parameters:**
- `foreground` (Tuple[int, int, int]): RGB tuple for foreground color (0-255)
- `background` (Tuple[int, int, int]): RGB tuple for background color (0-255)

#### Attributes

- `foreground` (Tuple[int, int, int]): Foreground RGB values
- `background` (Tuple[int, int, int]): Background RGB values

#### Usage Example

```python
# Define a color pair
pair = ColorPair((255, 255, 255), (0, 0, 0))  # White on Black

# Use in theme component methods
def get_background(self) -> ColorPair:
    return ColorPair((255, 255, 255), (0, 0, 0))
```

---

## Built-in Themes

The library includes 8 built-in themes:

### 1. Default Theme

Classic terminal appearance with white text on black background.

**Load with:** `ThemeManager.load('default')`

**Color Scheme:**
- Background: White on Black
- Button: Cyan on Black
- Button Focused: Black on Cyan
- Text Input: Green on Black
- Border: White on Black
- Selection: Black on White
- Disabled: White on Black

### 2. Dark Theme

Modern dark theme with light text on dark background.

**Load with:** `ThemeManager.load('dark')`

### 3. Light Theme

Clean light theme with dark text on light background.

**Load with:** `ThemeManager.load('light')`

### 4. TI-99/4A Theme

Vintage TI-99/4A computer theme with characteristic color scheme.

**Load with:** `ThemeManager.load('ti-99-4a')`

### 5. TRS-80 Theme

Classic TRS-80 computer theme with green on black appearance.

**Load with:** `ThemeManager.load('trs-80')`

### 6. DOS Theme

MS-DOS inspired theme with blue background.

**Load with:** `ThemeManager.load('dos')`

### 7. dBASE III Theme

Retro dBASE III database application theme.

**Load with:** `ThemeManager.load('dbase-iii')`

### 8. dBASE IV Theme

Classic dBASE IV database application theme.

**Load with:** `ThemeManager.load('dbase-iv')`

---

## Advanced Usage Patterns

### Creating a Custom Theme

```python
from curses_themes import Theme, ThemeManager, ColorPair

class CyberpunkTheme(Theme):
    """Custom cyberpunk-inspired theme."""
    
    def __init__(self):
        super().__init__(
            name="Cyberpunk",
            description="Neon cyberpunk theme with electric colors",
            author="Your Name"
        )
    
    def get_color_map(self):
        return {
            'background': (10, 10, 30),       # Dark blue
            'foreground': (0, 255, 255),      # Cyan
            'primary': (255, 0, 255),         # Magenta
            'success': (0, 255, 128),         # Bright green
            'error': (255, 0, 128),           # Hot pink
            'warning': (255, 255, 0),         # Yellow
            'info': (0, 200, 255),            # Light blue
            'accent': (255, 128, 0),          # Orange
        }
    
    def get_background(self) -> ColorPair:
        return ColorPair((0, 255, 255), (10, 10, 30))
    
    def get_button(self) -> ColorPair:
        return ColorPair((255, 0, 255), (10, 10, 30))
    
    def get_button_focused(self) -> ColorPair:
        return ColorPair((10, 10, 30), (255, 0, 255))
    
    def get_text_input(self) -> ColorPair:
        return ColorPair((0, 255, 128), (10, 10, 30))
    
    def get_border(self) -> ColorPair:
        return ColorPair((0, 255, 255), (10, 10, 30))
    
    def get_selection(self) -> ColorPair:
        return ColorPair((10, 10, 30), (255, 0, 255))
    
    def get_disabled(self) -> ColorPair:
        return ColorPair((100, 100, 120), (10, 10, 30))
    
    def get_border_chars(self) -> str:
        # Use Unicode box-drawing characters
        return "┌─┐││└─┘"

# Register and use
ThemeManager.register(CyberpunkTheme)
theme = ThemeManager.load('cyberpunk')
```

### Listing Available Themes

```python
import curses
from curses_themes import ThemeManager

def show_theme_menu(stdscr):
    """Display a menu of available themes."""
    themes = ThemeManager.list_themes()
    
    stdscr.clear()
    stdscr.addstr(0, 0, "Available Themes:", curses.A_BOLD)
    
    row = 2
    for name, info in themes.items():
        stdscr.addstr(row, 2, f"- {info['name']}")
        stdscr.addstr(row + 1, 4, f"{info['description']}")
        row += 3
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(show_theme_menu)
```

### Dynamic Theme Switching

```python
import curses
from curses_themes import ThemeManager

def main(stdscr):
    theme_names = ['default', 'dark', 'light', 'ti-99-4a']
    current_theme_idx = 0
    
    while True:
        # Load and apply current theme
        theme = ThemeManager.load(theme_names[current_theme_idx])
        theme.apply(stdscr)
        
        # Clear and redraw
        stdscr.clear()
        stdscr.addstr(0, 0, f"Current Theme: {theme.name}", 
                      curses.color_pair(theme.components.border))
        stdscr.addstr(2, 0, "Press 'n' for next theme, 'q' to quit",
                      curses.color_pair(theme.components.text_input))
        
        # Draw a sample box
        theme.draw_box(stdscr, 4, 2, 8, 40, title="Sample Box")
        
        stdscr.refresh()
        
        # Handle input
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('n'):
            current_theme_idx = (current_theme_idx + 1) % len(theme_names)

if __name__ == "__main__":
    curses.wrapper(main)
```

### Drawing Complex UIs

```python
import curses
from curses_themes import ThemeManager

def draw_ui(stdscr):
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)
    
    # Draw main window
    height, width = stdscr.getmaxyx()
    
    # Title bar
    stdscr.addstr(0, 0, " My Application ".center(width), 
                  curses.color_pair(theme.components.border) | curses.A_BOLD)
    
    # Menu panel
    theme.draw_box(stdscr, 2, 2, 10, 20, title="Menu")
    menu_items = ["File", "Edit", "View", "Help"]
    for idx, item in enumerate(menu_items):
        if idx == 0:  # Highlight first item
            attr = curses.color_pair(theme.components.selection)
        else:
            attr = curses.color_pair(theme.components.button)
        stdscr.addstr(4 + idx, 4, f" {item} ", attr)
    
    # Content panel
    theme.draw_box(stdscr, 2, 24, 10, width - 26, title="Content")
    stdscr.addstr(4, 26, "Welcome to the application!", 
                  curses.color_pair(theme.components.background))
    stdscr.addstr(5, 26, "Status: OK", 
                  curses.color_pair(theme.colors.success))
    
    # Status bar
    stdscr.addstr(height - 1, 0, " Press 'q' to quit ".center(width),
                  curses.color_pair(theme.components.border))
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(draw_ui)
```

---

## Terminal Compatibility

The library automatically adapts to terminal capabilities:

- **256-color terminals**: Full RGB color support with 6x6x6 color cube
- **16-color terminals**: Maps to extended ANSI colors
- **8-color terminals**: Maps to basic ANSI colors

Color conversion is handled automatically by `ColorManager` using Euclidean distance in RGB space for the best visual match.

---

## Error Handling

### Common Exceptions

#### RuntimeError

Raised when:
- Terminal doesn't support colors
- `theme.colors` or `theme.components` accessed before `apply()`
- Color initialization fails
- Maximum color pairs exceeded

```python
try:
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)
except RuntimeError as e:
    print(f"Failed to apply theme: {e}")
```

#### KeyError

Raised when:
- Loading a non-existent theme
- Unregistering a non-existent theme

```python
try:
    theme = ThemeManager.load('nonexistent')
except KeyError as e:
    print(f"Theme not found: {e}")
    # Fall back to default
    theme = ThemeManager.load('default')
```

#### ValueError

Raised when:
- Theme color map is missing required keys
- Box dimensions are too small in `draw_box()`
- Theme already registered with same name

```python
try:
    theme.draw_box(stdscr, 0, 0, 1, 1)  # Too small
except ValueError as e:
    print(f"Invalid dimensions: {e}")
```

#### TypeError

Raised when:
- Attempting to instantiate `ThemeManager`
- Registering a non-Theme class

---

## Best Practices

### 1. Always Apply Themes Before Use

```python
# Good
theme = ThemeManager.load('dark')
theme.apply(stdscr)
stdscr.addstr(0, 0, "Text", curses.color_pair(theme.colors.primary))

# Bad - will raise RuntimeError
theme = ThemeManager.load('dark')
stdscr.addstr(0, 0, "Text", curses.color_pair(theme.colors.primary))
```

### 2. Use Component Colors for Widgets

Component colors provide better semantic meaning for UI elements:

```python
# Good - clear intent
stdscr.addstr(0, 0, "[OK]", curses.color_pair(theme.components.button))
stdscr.addstr(1, 0, "Name: ", curses.color_pair(theme.components.text_input))

# Less clear
stdscr.addstr(0, 0, "[OK]", curses.color_pair(theme.colors.primary))
```

### 3. Handle Terminal Limitations

```python
import curses
from curses_themes import ThemeManager, ColorManager

def main(stdscr):
    try:
        manager = ColorManager(stdscr)
        theme = ThemeManager.load('dark')
        theme.apply(stdscr)
        
        # Check capabilities
        if manager.color_count < 256:
            stdscr.addstr(0, 0, "Limited colors - display may vary")
        
    except RuntimeError as e:
        stdscr.addstr(0, 0, f"Color support error: {e}")
        return
```

### 4. Normalize Theme Names

Theme names are automatically normalized (lowercase, hyphens), but it's good practice to use consistent naming:

```python
# All equivalent, but be consistent
ThemeManager.load('dark')        # Preferred
ThemeManager.load('Dark')
ThemeManager.load('DARK')
```

---

## License

This library is licensed under the GNU General Public License v3.0.

Copyright (C) 2024 FlossWare

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See <https://www.gnu.org/licenses/> for details.
