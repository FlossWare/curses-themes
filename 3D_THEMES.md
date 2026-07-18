# 3D Themes for curses-themes

This document describes the 3D theme system for creating text-mode user interfaces with shadow and highlight effects reminiscent of early GUI applications from the late 1980s and early 1990s.

## Table of Contents

- [Introduction to 3D Themes](#introduction-to-3d-themes)
- [Historical Context](#historical-context)
- [How 3D Effects Work in Text Mode](#how-3d-effects-work-in-text-mode)
- [Theme3D Base Class](#theme3d-base-class)
- [Borland3DTheme](#borland3dtheme)
- [DBase4_3DTheme](#dbase4_3dtheme)
- [Usage Examples](#usage-examples)
- [Comparison Table](#comparison-table)
- [Terminal Compatibility](#terminal-compatibility)

---

## Introduction to 3D Themes

3D themes bring depth and dimensionality to terminal user interfaces by simulating raised buttons, sunken input fields, and drop shadows using carefully coordinated color combinations and box-drawing characters. These effects create visual hierarchy and tactile feedback in text mode applications, making interfaces more intuitive and visually appealing.

**What are 3D themes in terminal UI?**

In graphical user interfaces, 3D effects are created using shading, gradients, and anti-aliasing. In text mode, we achieve similar effects through:

- **Shadow colors**: Darker colors placed on the right and bottom edges
- **Highlight colors**: Lighter colors placed on the left and top edges  
- **Asymmetric borders**: Different characters or colors for opposing edges
- **Color gradients**: Strategic use of foreground/background combinations
- **Offset shadows**: L-shaped shadows positioned to the right and below elements

The result is a pseudo-3D appearance that simulates light coming from the upper-left corner, casting shadows to the lower-right.

---

## Historical Context

### Borland Turbo Vision (1990-1995)

**Era:** 1990-1995  
**Developer:** Borland International  
**Platform:** DOS, 16-bit text mode applications

Turbo Vision was a revolutionary text-mode application framework introduced by Borland in 1990 for Turbo Pascal 6.0. It brought sophisticated GUI-like interfaces to DOS applications, featuring:

- **3D shadowed windows**: Windows appeared to float above the background with L-shaped drop shadows
- **Raised buttons**: Buttons used highlight/shadow edges to appear raised from the surface
- **Sunken input fields**: Text inputs appeared recessed with inverted highlight/shadow
- **Menu bars and pull-down menus**: With 3D effects for visual depth
- **Dialog boxes**: Sophisticated layouts with consistent 3D styling

Turbo Vision was used in Borland's flagship products:
- Turbo Pascal 6.0+ IDE (1990)
- Turbo C++ IDE (1990)
- Borland C++ IDE (1991)
- Quattro Pro for DOS (1992)

The framework's color scheme became iconic: cyan/teal backgrounds with white and yellow text, using carefully chosen shadow and highlight colors to create the illusion of depth. The 3D effects made text-mode applications feel modern and professional, competing with early Windows applications.

### dBASE IV Control Center (1988-1993)

**Era:** 1988-1993  
**Developer:** Ashton-Tate (acquired by Borland 1991)  
**Platform:** DOS database management system

dBASE IV introduced a revolutionary windowed interface called the Control Center in 1988, two years before Turbo Vision. This marked a significant departure from dBASE III's command-line interface:

- **Multi-window interface**: Multiple overlapping windows with 3D effects
- **Pull-down menus**: Menu bar with drop-down selections
- **Mouse support**: Point-and-click interface in text mode
- **3D window frames**: Windows with shadow effects for depth
- **Paneled interface**: Catalog panels appearing as raised surfaces

The Control Center used a blue background (departing from the traditional black) with white and yellow text. Windows featured 3D shadowing to appear as floating panels above the blue workspace. This interface influenced database tools throughout the 1990s and represented the bridge between command-line and GUI database management.

**Historical Significance:**

Both systems demonstrated that sophisticated, usable interfaces could be created in text mode using clever color combinations and box-drawing characters. They influenced:

- Norton Commander and Norton Utilities (3D file manager interface)
- DOS Navigator (dual-pane file manager with 3D effects)
- Midnight Commander (Unix clone with similar aesthetics)
- Many custom business applications of the DOS era

---

## How 3D Effects Work in Text Mode

### Light Source Model

3D effects in text mode simulate a light source positioned at the **upper-left** of the screen. This creates:

- **Bright edges** on the top and left (facing the light)
- **Dark edges** on the bottom and right (in shadow)

```
    Light Source (↖)
    ┌─────────┐  ← Top edge: BRIGHT (highlight)
    │         │
    │  Box    │← Left edge: BRIGHT
    │         │
    └─────────┘  ← Bottom edge: DARK (shadow)
              ↑
         Right edge: DARK
```

### Drop Shadows

Drop shadows create the illusion that UI elements float above the background. They are rendered as:

- **Offset positioning**: Shadow appears 1-2 characters to the right and below
- **L-shaped pattern**: Shadow only on right and bottom edges
- **Darker color**: Shadow uses dark gray or black on the background color
- **Consistent direction**: All shadows fall the same way (lower-right)

```
Normal window:              3D window with shadow:
┌──────────┐               ┌──────────┐
│  Window  │               │  Window  │▓
│          │               │          │▓
└──────────┘               └──────────┘▓
                            ▓▓▓▓▓▓▓▓▓▓▓▓
```

### Raised vs Sunken Rendering

**Raised elements** (buttons, panels):
- Top/left edges: Use highlight color (white, bright yellow, bright cyan)
- Bottom/right edges: Use shadow color (dark gray, dark blue)
- Center: Normal component color
- Effect: Appears to protrude toward the user

```
Raised Button:
╔═══════════╗  ← Top: highlight (white/bright)
║  [ OK ]   ║  ← Sides: normal color
╚═══════════╝  ← Bottom: shadow (dark gray/black)
```

**Sunken elements** (input fields, recessed panels):
- Top/left edges: Use shadow color (dark gray, dark blue)
- Bottom/right edges: Use highlight color (white, bright cyan)
- Center: Input field color (often different from background)
- Effect: Appears to recede away from the user

```
Sunken Input Field:
┌───────────┐  ← Top: shadow (dark)
│ Input___  │  ← Interior: input color
└───────────┘  ← Bottom: highlight (bright)
```

### Color Combinations for 3D Effects

**Borland Turbo Vision palette:**
- Highlight: White (RGB: 255, 255, 255)
- Normal: Yellow or cyan on teal/blue background
- Shadow: Dark gray (RGB: 128, 128, 128)
- Deep shadow: Black (RGB: 0, 0, 0)

**dBASE IV Control Center palette:**
- Highlight: Bright white (RGB: 255, 255, 255)
- Normal: White or yellow on blue background
- Shadow: Dark blue (RGB: 0, 0, 128)
- Deep shadow: Black (RGB: 0, 0, 0)

---

## Theme3D Base Class

The `Theme3D` class extends the standard `Theme` class with additional methods and properties for rendering 3D effects.

### Class Definition

```python
from curses_themes import Theme, ColorPair

class Theme3D(Theme):
    """
    Base class for themes with 3D shadow and highlight effects.
    
    Extends the standard Theme class with 3D rendering support for
    raised buttons, sunken input fields, and drop shadows using
    highlight and shadow colors.
    
    Subclasses must define:
    - effects_3d: dict mapping 'shadow', 'highlight', and optionally
      'lowlight' to (fg_rgb_tuple, bg_rgb_tuple) pairs
    """
```

### Required Class Attribute

#### `effects_3d`

A dict mapping effect names to `(fg_rgb_tuple, bg_rgb_tuple)` pairs. Required keys are `'shadow'` and `'highlight'`; `'lowlight'` is optional.

**Example:**
```python
class MyTheme(Theme3D):
    effects_3d = {
        'shadow': ((0, 0, 0), (64, 64, 64)),
        'highlight': ((255, 255, 255), (0, 128, 128)),
        'lowlight': ((64, 64, 64), (0, 128, 128)),
    }
```

### Method

#### `get_3d_colors() -> dict[str, ColorPair]`

Returns the resolved 3D effect colors as a dict of `str -> ColorPair`. The keys match the `effects_3d` class attribute (`'shadow'`, `'highlight'`, `'lowlight'`).

**Example:**
```python
colors_3d = theme.get_3d_colors()
highlight_pair = colors_3d['highlight']
shadow_pair = colors_3d['shadow']
```

### 3D Drawing Methods

#### `draw_box_3d(window, y, x, height, width, title="", raised=True)`

Draws a 3D box with highlight and shadow edges.

**Parameters:**
- `window`: Curses window to draw on
- `y` (int): Top-left Y coordinate
- `x` (int): Top-left X coordinate
- `height` (int): Box height in characters
- `width` (int): Box width in characters
- `title` (str): Optional title centered in top border
- `raised` (bool): If True, renders raised (button-like); if False, renders sunken (input-like)

**Raises:**
- `ValueError`: If box dimensions are too small (minimum 3x3 for 3D effects)
- `RuntimeError`: If theme has not been applied with `theme.apply(stdscr)`

**Example:**
```python
# Draw a raised button
theme.draw_box_3d(stdscr, 5, 10, 3, 15, title="OK", raised=True)

# Draw a sunken input field
theme.draw_box_3d(stdscr, 10, 10, 3, 30, raised=False)
```

**Rendering:**

Raised box (button):
```
╔═══════════╗  ← Highlight color (bright)
║  Content  ║  ← Border color
╚═══════════╝  ← Shadow color (dark)
```

Sunken box (input):
```
┌───────────┐  ← Shadow color (dark)
│  Content  │  ← Border color
└───────────┘  ← Highlight color (bright)
```

#### `draw_window_with_shadow(window, y, x, height, width, title="")`

Draws a window with a drop shadow (L-shaped shadow offset to right and bottom).

**Parameters:**
- `window`: Curses window to draw on
- `y` (int): Top-left Y coordinate  
- `x` (int): Top-left X coordinate
- `height` (int): Window height in characters
- `width` (int): Window width in characters
- `title` (str): Optional title centered in top border

**Shadow offset:** 1 character right, 1 character down

**Example:**
```python
# Draw a floating dialog with shadow
theme.draw_window_with_shadow(stdscr, 5, 10, 12, 50, title="Settings")
```

**Rendering:**
```
┌──────────────┐
│   Window     │▓  ← Shadow (right edge)
│              │▓
│  [ OK ]      │▓
└──────────────┘▓
 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ← Shadow (bottom edge)
```

### Properties

After calling `theme.apply(stdscr)`, the following properties are available:

- `theme.components.highlight`: Color pair number for highlight edges
- `theme.components.shadow`: Color pair number for shadow edges  
- `theme.components.deep_shadow`: Color pair number for drop shadows (if implemented)

---

## Borland3DTheme

Recreates the iconic Turbo Vision 3D interface from Borland's DOS-era IDEs (1990-1995).

### Historical Context

The Borland3DTheme captures the sophisticated text-mode interface introduced with Turbo Vision in Turbo Pascal 6.0 (1990). This framework revolutionized DOS application development by providing:

- Object-oriented architecture for text-mode UIs
- Sophisticated 3D window effects with shadows
- Consistent visual language across Borland products
- Professional appearance rivaling early Windows applications

The color scheme became iconic: teal/cyan backgrounds with white and yellow text, using carefully coordinated highlight and shadow colors to create convincing 3D effects in text mode.

### Visual Identity

**Color Palette:**
- Background: Teal/cyan (RGB: 0, 128, 128) - the signature Turbo Vision color
- Text: White (RGB: 255, 255, 255) - high contrast on teal
- Highlight: Bright white (RGB: 255, 255, 255) - top/left edges of raised elements
- Shadow: Dark gray (RGB: 128, 128, 128) - bottom/right edges
- Deep shadow: Black (RGB: 0, 0, 0) - drop shadows behind windows
- Button: Yellow (RGB: 255, 255, 0) on teal - menu items and buttons
- Focused: Black (RGB: 0, 0, 0) on yellow - inverted selection
- Input: White on blue (RGB: 0, 0, 160) - data entry fields

### Color Scheme Details

```python
class Borland3DTheme(Theme3D):
    """Borland Turbo Vision theme (1990-1995)."""
    
    # Turbo Vision color palette
    TEAL = (0, 128, 128)         # Background
    WHITE = (255, 255, 255)       # Text and highlights
    YELLOW = (255, 255, 0)        # Buttons and menus
    BLUE = (0, 0, 160)            # Input fields
    BLACK = (0, 0, 0)             # Shadows
    DARK_GRAY = (128, 128, 128)   # Shadow edges
    LIGHT_GRAY = (192, 192, 192)  # Disabled items
```

**Component Colors:**
- Background: White on teal
- Button: Yellow on teal (normal state)
- Button Focused: Black on yellow (inverted)
- Text Input: White on dark blue (distinguishes input fields)
- Border: White on teal
- Selection: Black on cyan (highlighted items)
- Disabled: Light gray on teal (muted but visible)
- Highlight: White on teal (bright edges)
- Shadow: Dark gray on teal (dark edges)
- Deep Shadow: Black on dark gray (window drop shadows)

### Visual Appearance

**Windows:** Appear to float above the teal background with black drop shadows offset to the right and bottom. Window frames use white for top/left borders and dark gray for bottom/right borders.

**Buttons:** Raised appearance with white highlight on top/left edges and dark gray shadow on bottom/right edges. Yellow text provides high visibility. When focused, colors invert to black-on-yellow.

**Input Fields:** Sunken appearance with dark gray shadow on top/left edges and white highlight on bottom/right edges. Dark blue background distinguishes input areas from display text.

**Menus:** Yellow text on teal background with 3D raised appearance. Drop-down menus cast shadows on the content below.

### When to Use

- **Retro DOS applications**: Recreating the look of 1990s Borland tools
- **IDE-style interfaces**: Code editors, development tools, text-mode debuggers
- **Professional business applications**: Database frontends, administration tools
- **Nostalgia projects**: Evoking the classic Turbo Pascal/C++ era
- **High-contrast needs**: Teal background provides better readability than black in some lighting

### Loading the Theme

```python
from curses_themes import ThemeManager
import curses

def main(stdscr):
    # Load Borland 3D theme
    theme = ThemeManager.load('borland-3d')
    theme.apply(stdscr)
    
    # Use 3D components
    theme.draw_window_with_shadow(stdscr, 2, 5, 15, 60, title="Turbo Pascal")
    theme.draw_box_3d(stdscr, 5, 10, 3, 12, title="OK", raised=True)
    theme.draw_box_3d(stdscr, 10, 10, 3, 40, raised=False)
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

### Border Characters

Uses Unicode box-drawing characters for authentic Borland appearance:

**Standard borders:** `┌─┐││└─┘` (single-line)  
**Raised elements:** `╔═╗║╚═╝` (double-line for emphasis)  
**Fallback (ASCII):** `+-+||+-+` (when Unicode unavailable)

---

## DBase4_3DTheme

Recreates the dBASE IV Control Center windowed interface with 3D effects (1988-1993).

### Historical Context

The DBase4_3DTheme captures the revolutionary Control Center interface introduced in dBASE IV (1988), which predated Turbo Vision by two years. This marked Ashton-Tate's bold move from command-line to GUI-inspired database management:

- **Control Center**: Visual catalog of database objects (files, queries, reports, forms)
- **Windowed interface**: Multiple overlapping windows with 3D shadows
- **Blue workspace**: Departure from traditional black background
- **Pull-down menus**: Menu bar with cascading selections
- **Mouse support**: Point-and-click in text mode (revolutionary for 1988)

Despite initial technical problems that hurt dBASE IV's reputation, the interface design was ahead of its time. When Borland acquired Ashton-Tate in 1991, the Control Center's windowed approach influenced Borland's database tools throughout the 1990s.

### Visual Identity

**Color Palette:**
- Background: Blue (RGB: 0, 0, 238) - the Control Center workspace color
- Text: White (RGB: 255, 255, 255) - primary text
- Highlight: Bright white (RGB: 255, 255, 255) - top/left edges
- Shadow: Dark blue (RGB: 0, 0, 128) - bottom/right edges
- Deep shadow: Black (RGB: 0, 0, 0) - window drop shadows
- Button: Yellow (RGB: 255, 255, 0) on blue - menu items
- Focused: Blue on yellow - inverted selection
- Input: Cyan (RGB: 0, 255, 255) on blue - data entry fields

### Color Scheme Details

```python
class DBase4_3DTheme(Theme3D):
    """dBASE IV Control Center theme (1988-1993)."""
    
    # Control Center color palette
    BLUE = (0, 0, 238)            # Background
    WHITE = (255, 255, 255)       # Text and highlights
    YELLOW = (255, 255, 0)        # Buttons and menus
    CYAN = (0, 255, 255)          # Input fields
    BLACK = (0, 0, 0)             # Shadows
    DARK_BLUE = (0, 0, 128)       # Shadow edges
    LIGHT_GRAY = (192, 192, 192)  # Disabled items
```

**Component Colors:**
- Background: White on blue
- Button: Yellow on blue (menu items)
- Button Focused: Blue on yellow (inverted)
- Text Input: Cyan on blue (data entry)
- Border: White on blue
- Selection: Blue on white (highlighted records)
- Disabled: Blue on blue (muted, subtle)
- Highlight: White on blue (bright edges)
- Shadow: Dark blue on blue (dark edges)
- Deep Shadow: Black on dark gray (window shadows)

### Difference from Flat dBASE IV

**Flat dBASE IV theme** (`dbase-iv`):
- No 3D effects
- Simple single-line borders
- No shadows or highlights
- Flat color scheme throughout

**dBASE IV 3D theme** (`dbase-iv-3d`):
- 3D raised panels for catalog sections
- Sunken input fields in forms
- Drop shadows on windows and dialogs
- Highlight/shadow borders on all elements
- Creates visual hierarchy through depth

### Visual Appearance

**Control Center panels:** Raised 3D panels containing database object catalogs (Data, Queries, Forms, Reports, Labels, Applications). Each panel appears elevated above the blue workspace.

**Windows:** Floating windows with white borders and black drop shadows. Window frames use white for top/left edges and dark blue for bottom/right edges.

**Menus:** Yellow menu bar with 3D raised appearance. Drop-down menus cast shadows and appear to overlay the content.

**Input Fields:** Cyan text in sunken fields, creating the impression of typing into a recessed surface.

**Browse Mode:** Records displayed with blue-on-white selection bar, maintaining high contrast for data visibility.

### When to Use

- **Database applications**: SQL clients, table browsers, data entry forms
- **Record management interfaces**: Any application displaying tabular data
- **Catalog-style UIs**: Applications organizing items into categories
- **Blue color scheme preference**: Some users find blue less harsh than black
- **Historical accuracy**: Recreating dBASE IV or Clipper-era applications

### Loading the Theme

```python
from curses_themes import ThemeManager
import curses

def main(stdscr):
    # Load dBASE IV 3D theme
    theme = ThemeManager.load('dbase-iv-3d')
    theme.apply(stdscr)
    
    # Draw Control Center-style panels
    theme.draw_box_3d(stdscr, 3, 2, 8, 20, title="Data", raised=True)
    theme.draw_box_3d(stdscr, 3, 24, 8, 20, title="Queries", raised=True)
    theme.draw_box_3d(stdscr, 3, 46, 8, 20, title="Forms", raised=True)
    
    # Draw input field
    theme.draw_box_3d(stdscr, 13, 10, 3, 40, raised=False)
    
    # Draw window with shadow
    theme.draw_window_with_shadow(stdscr, 6, 15, 12, 50, title="Edit Record")
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

### Border Characters

Uses Unicode box-drawing characters matching the Control Center style:

**Window frames:** `┌─┐││└─┘` (single-line)  
**Panel borders:** `╔═╗║╚═╝` (double-line for catalog panels)  
**Fallback (ASCII):** `+-+||+-+` (maximum compatibility)

---

## Usage Examples

### Basic 3D Box Drawing

Drawing raised and sunken boxes with 3D effects:

```python
import curses
from curses_themes import ThemeManager

def main(stdscr):
    theme = ThemeManager.load('borland-3d')
    theme.apply(stdscr)
    
    # Draw a raised button
    theme.draw_box_3d(
        window=stdscr,
        y=5,
        x=10,
        height=3,
        width=15,
        title="OK",
        raised=True
    )
    
    # Draw a sunken input field
    theme.draw_box_3d(
        window=stdscr,
        y=10,
        x=10,
        height=3,
        width=40,
        raised=False
    )
    
    # Add text inside the input field
    stdscr.addstr(11, 12, "Enter your name:", 
                  curses.color_pair(theme.components.text_input))
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

### Raised Buttons

Creating a dialog with multiple raised buttons:

```python
import curses
from curses_themes import ThemeManager

def main(stdscr):
    theme = ThemeManager.load('dbase-iv-3d')
    theme.apply(stdscr)
    
    # Draw dialog window with shadow
    theme.draw_window_with_shadow(stdscr, 5, 15, 12, 50, title="Confirmation")
    
    # Add message
    stdscr.addstr(8, 20, "Save changes before closing?",
                  curses.color_pair(theme.components.background))
    
    # Draw three raised buttons
    buttons = [
        (15, 18, "  Yes  "),
        (15, 28, "  No   "),
        (15, 38, " Cancel ")
    ]
    
    for x, y, label in buttons:
        theme.draw_box_3d(stdscr, 10, x, 3, len(label) + 4, raised=True)
        # Add button text
        stdscr.addstr(11, x + 2, label,
                      curses.color_pair(theme.components.button))
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

### Sunken Input Fields

Creating a form with multiple input fields:

```python
import curses
from curses_themes import ThemeManager

def main(stdscr):
    theme = ThemeManager.load('borland-3d')
    theme.apply(stdscr)
    
    # Draw form window
    theme.draw_window_with_shadow(stdscr, 3, 10, 18, 60, title="User Registration")
    
    # Define form fields
    fields = [
        (5, 15, "Name:", 30),
        (8, 15, "Email:", 30),
        (11, 15, "Phone:", 20),
        (14, 15, "Address:", 40)
    ]
    
    for row, col, label, width in fields:
        # Draw label
        stdscr.addstr(row, col, label,
                      curses.color_pair(theme.components.background))
        
        # Draw sunken input field
        theme.draw_box_3d(stdscr, row, col + len(label) + 2, 3, width, raised=False)
    
    # Draw submit button
    theme.draw_box_3d(stdscr, 18, 35, 3, 12, title="Submit", raised=True)
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

### Multiple Windows with Shadows

Creating a multi-window interface with overlapping 3D windows:

```python
import curses
from curses_themes import ThemeManager

def main(stdscr):
    theme = ThemeManager.load('dbase-iv-3d')
    theme.apply(stdscr)
    
    # Background window (Control Center)
    stdscr.addstr(1, 2, "dBASE IV CONTROL CENTER",
                  curses.color_pair(theme.components.button))
    
    # Draw catalog panels (raised)
    panels = [
        (3, 2, 10, 18, "Data"),
        (3, 22, 10, 18, "Queries"),
        (3, 42, 10, 18, "Forms"),
        (14, 2, 10, 18, "Reports"),
        (14, 22, 10, 18, "Labels"),
        (14, 42, 10, 18, "Applications")
    ]
    
    for y, x, h, w, title in panels:
        theme.draw_box_3d(stdscr, y, x, h, w, title=title, raised=True)
    
    # Overlapping window (floating on top)
    theme.draw_window_with_shadow(stdscr, 8, 25, 14, 45, title="Database Properties")
    
    # Add content to floating window
    stdscr.addstr(10, 28, "Database: CUSTOMER.DBF",
                  curses.color_pair(theme.components.background))
    stdscr.addstr(12, 28, "Records: 1,247",
                  curses.color_pair(theme.components.background))
    stdscr.addstr(14, 28, "Last Update: 1992-03-15",
                  curses.color_pair(theme.components.background))
    
    # OK button in dialog
    theme.draw_box_3d(stdscr, 18, 45, 3, 12, title="OK", raised=True)
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

### Creating Custom 3D Themes

Extending Theme3D for your own color scheme:

```python
from curses_themes import Theme3D, ThemeManager

class Custom3DTheme(Theme3D):
    """Custom 3D theme with purple color scheme."""

    color_map = {
        'background': (128, 0, 128),
        'foreground': (255, 255, 255),
        'primary': (230, 230, 250),
        'success': (0, 255, 0),
        'error': (255, 0, 0),
        'warning': (255, 255, 0),
        'info': (0, 255, 255),
        'accent': (230, 230, 250),
    }

    component_colors = {
        'background': ((255, 255, 255), (128, 0, 128)),
        'button': ((230, 230, 250), (128, 0, 128)),
        'button_focused': ((128, 0, 128), (230, 230, 250)),
        'text_input': ((255, 255, 255), (64, 0, 64)),
        'border': ((255, 255, 255), (128, 0, 128)),
        'selection': ((128, 0, 128), (230, 230, 250)),
        'disabled': ((96, 96, 96), (128, 0, 128)),
    }

    effects_3d = {
        'shadow': ((96, 96, 96), (128, 0, 128)),
        'highlight': ((255, 255, 255), (128, 0, 128)),
        'lowlight': ((0, 0, 0), (96, 96, 96)),
    }

    border_chars = "┌─┐││└─┘"
    double_border_chars = "╔═╗║║╚═╝"

    def __init__(self):
        super().__init__(
            name="Custom 3D Purple",
            description="Purple 3D theme with lavender accents",
            author="Your Name"
        )

# Register and use custom theme
ThemeManager.register(Custom3DTheme)

import curses

def main(stdscr):
    theme = ThemeManager.load('custom-3d-purple')
    theme.apply(stdscr)
    
    theme.draw_window_with_shadow(stdscr, 5, 10, 12, 50, title="Custom Theme")
    theme.draw_box_3d(stdscr, 8, 20, 3, 15, title="OK", raised=True)
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

---

## Comparison Table

| Feature | Borland3DTheme | DBase4_3DTheme |
|---------|----------------|----------------|
| **Era** | 1990-1995 | 1988-1993 |
| **Origin** | Turbo Vision framework | dBASE IV Control Center |
| **Background** | Teal (0, 128, 128) | Blue (0, 0, 238) |
| **Text** | White | White |
| **Buttons** | Yellow on teal | Yellow on blue |
| **Focused** | Black on yellow | Blue on yellow |
| **Input Fields** | White on dark blue | Cyan on blue |
| **Highlight** | White | White |
| **Shadow** | Dark gray | Dark blue |
| **Deep Shadow** | Black | Black |
| **Selection** | Black on cyan | Blue on white |
| **Disabled** | Light gray on teal | Blue on blue (subtle) |
| **Border Style** | Unicode ┌─┐, ╔═╗ | Unicode ┌─┐, ╔═╗ |
| **ASCII Fallback** | +-+\|\|+-+ | +-+\|\|+-+ |
| **Primary Use** | IDEs, development tools | Database applications |
| **Visual Style** | Professional, technical | Business-oriented |
| **Contrast** | High (white on teal) | Very high (white on blue) |
| **Color Mood** | Cool, analytical | Formal, trustworthy |
| **Best For** | Code editors, debuggers | Data entry, forms, records |

### Aesthetic Differences

**Borland3DTheme:**
- **Cooler tones**: Teal background is less saturated than dBASE blue
- **Softer appearance**: Dark gray shadows are gentler than dark blue
- **Technical feel**: Associated with programming and development
- **Yellow emphasis**: Bright yellow buttons stand out strongly on teal
- **IDE heritage**: Evokes Turbo Pascal, Borland C++, professional tools

**DBase4_3DTheme:**
- **Warmer tones**: Brighter blue background is more saturated
- **Higher contrast**: White-on-blue provides maximum readability
- **Business feel**: Associated with database and data management
- **Cyan input fields**: Distinctive cyan separates input from display text
- **Database heritage**: Evokes Control Center, Clipper, xBase applications

### Performance Considerations

Both themes have similar performance characteristics:

- **Color pairs**: Each theme uses 10-12 color pairs (minimal terminal resources)
- **Rendering speed**: 3D effects add minimal overhead (just extra border drawing)
- **Memory footprint**: Negligible difference from flat themes
- **Terminal compatibility**: Both require 16+ color support for full fidelity

---

## Terminal Compatibility

### Unicode Box-Drawing Requirements

3D themes look best with Unicode box-drawing characters:

**Required characters:**
- `┌ ─ ┐ │ └ ┘` - Single-line boxes (U+250x range)
- `╔ ═ ╗ ║ ╚ ╝` - Double-line boxes (U+255x range)
- `▓` - Medium shade for drop shadows (U+2593)

**Terminal support:**
- ✅ Modern terminals: xterm, gnome-terminal, konsole, Windows Terminal, iTerm2
- ✅ macOS Terminal.app (with UTF-8 encoding)
- ✅ Most Linux console terminals
- ⚠️ Some older terminals may require Unicode configuration

**Fallback to ASCII:**

If Unicode is unavailable, themes automatically fall back to ASCII:

```python
def get_border_chars(self) -> str:
    """
    Returns Unicode if supported, ASCII otherwise.
    
    Unicode: "┌─┐││└─┘" or "╔═╗║╚═╝"
    ASCII:   "+-+||+-+"
    """
    if self.unicode_supported():
        return "┌─┐││└─┘"  # Single-line
    return "+-+||+-+"       # ASCII fallback
```

### Color Support Requirements

**Minimum:** 16-color terminal (8 standard + 8 bright colors)

**Recommended:** 256-color terminal for full RGB color fidelity

**Checking color support:**

```python
import curses

def main(stdscr):
    num_colors = curses.COLORS
    can_change_color = curses.can_change_color()
    
    if num_colors < 16:
        print("Warning: 3D themes require at least 16 colors")
        print(f"Your terminal supports {num_colors} colors")
    elif num_colors >= 256:
        print("Excellent: 256+ color support detected")
    else:
        print(f"Good: {num_colors} color support (3D themes will work)")

curses.wrapper(main)
```

### Terminal Configuration

**For best results:**

1. **Set TERM variable:**
   ```bash
   export TERM=xterm-256color
   ```

2. **Enable UTF-8:**
   ```bash
   export LANG=en_US.UTF-8
   export LC_ALL=en_US.UTF-8
   ```

3. **Test Unicode support:**
   ```bash
   echo -e "Box chars: ┌─┐\n│ │\n└─┘"
   echo -e "Shade: ▓▓▓"
   ```

### Graceful Degradation

The 3D themes handle limited terminal capabilities gracefully:

**8-color terminals:**
- Map RGB colors to nearest standard color
- Reduce highlight/shadow distinction
- Maintain usability with reduced visual fidelity

**Monochrome terminals:**
- Use intensity variations (normal/bold)
- Rely on box-drawing characters for structure
- 3D effects minimal but borders remain functional

**No Unicode support:**
- Fall back to ASCII borders: `+-+||+-+`
- Use spacing and layout to imply depth
- Core functionality preserved

---

## Advanced Topics

### Customizing Shadow Offset

Default shadow offset is 1 character right and 1 down. You can customize:

```python
class CustomShadowTheme(Theme3D):
    def get_shadow_offset(self) -> Tuple[int, int]:
        """Returns (x_offset, y_offset) for drop shadows."""
        return (2, 1)  # 2 chars right, 1 char down
```

### Double vs Single Borders

Choose border style based on emphasis:

```python
def get_border_chars(self) -> str:
    """Override to select border style."""
    # Double-line for high emphasis (dialogs, important panels)
    return "╔═╗║╚═╝║"
    
    # Single-line for standard windows
    # return "┌─┐││└─┘"
    
    # ASCII for maximum compatibility
    # return "+-+||+-+"
```

### Nested 3D Elements

Creating depth hierarchy with multiple shadow levels:

```python
# Background window (deepest)
theme.draw_window_with_shadow(stdscr, 2, 2, 20, 70, title="Main")

# Mid-level panel (raised)
theme.draw_box_3d(stdscr, 5, 5, 10, 30, title="Panel", raised=True)

# Foreground button (most raised)
theme.draw_box_3d(stdscr, 8, 10, 3, 12, title="OK", raised=True)
```

### Performance Optimization

For applications with many 3D elements:

```python
# Cache color pairs after theme.apply()
bg_pair = theme.components.background
border_pair = theme.components.border
highlight_pair = theme.components.highlight
shadow_pair = theme.components.shadow

# Reuse in tight loops
for i in range(100):
    stdscr.addstr(i, 0, "Item", curses.color_pair(bg_pair))
```

---

## References

### Historical Documentation

- **Borland Turbo Vision Programmer's Guide** (1990) - Original documentation for Turbo Vision framework
- **dBASE IV User's Guide** (1988) - Ashton-Tate's Control Center documentation
- **Turbo Pascal 6.0 User's Guide** - First release with Turbo Vision
- **Borland C++ Programmer's Guide** - Turbo Vision in C++

### Related Projects

- [Turbo Vision (Open Source)](https://github.com/magiblot/tvision) - Modern C++ port of Turbo Vision
- [Free Vision](https://github.com/set-soft/tvision) - Free Pascal port
- [RHIDE](http://www.rhide.com/) - IDE using Turbo Vision for DJGPP

### Further Reading

- "The Art of Text Mode Graphics" - Terminal UI design principles
- "DOS Application Development" - 1990s software development techniques
- "Borland: The Rise and Fall" - History of Borland International

---

## License

The curses-themes 3D theme system is released under the MIT License.

Borland3DTheme and DBase4_3DTheme are clean-room implementations based on visual observation of historical software and publicly available screenshots. These implementations do not use any proprietary Borland or Ashton-Tate code.

**Trademarks:**
- Turbo Vision, Turbo Pascal, Turbo C++, Borland C++ are trademarks of Micro Focus International
- dBASE is a trademark of dBASE LLC
- MS-DOS, PC-DOS are trademarks of Microsoft Corporation and IBM Corporation

All theme implementations are original works by FlossWare, created for historical preservation and educational purposes.

---

**Documentation Version:** 1.0  
**Last Updated:** June 2026  
**Author:** FlossWare  
**Project:** [curses-themes](https://github.com/FlossWare/curses-themes)