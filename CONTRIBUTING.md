# Contributing to curses-themes

Thank you for your interest in contributing to curses-themes! We welcome contributions from everyone, whether you're fixing a bug, adding a theme, improving documentation, or suggesting new features.

This document provides guidelines to help you contribute effectively to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
  - [Contributing New Themes](#contributing-new-themes)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Improving Documentation](#improving-documentation)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation Requirements](#documentation-requirements)
- [Theme Design Guidelines](#theme-design-guidelines)
- [Examples of Good Contributions](#examples-of-good-contributions)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behaviors include:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors include:**
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Enforcement

Project maintainers are responsible for clarifying standards of acceptable behavior and will take appropriate and fair corrective action in response to any instances of unacceptable behavior. Issues can be reported by contacting the project team through GitHub issues.

## Getting Started

Before contributing, please:

1. **Read the documentation** - Familiarize yourself with the [README.md](README.md) and [GUIDE.md](GUIDE.md)
2. **Check existing issues** - See if your idea or bug has already been reported
3. **Review open pull requests** - Make sure someone isn't already working on the same thing
4. **Start small** - Consider starting with a small contribution to get familiar with our workflow

## Development Setup

### Prerequisites

- **Python 3.9 or higher** - Check your version with `python3 --version`
- **Git** - For version control
- **Terminal with curses support** - Most Unix-like systems include this by default

### Initial Setup

1. **Fork the repository** on GitHub

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/curses-themes.git
   cd curses-themes
   ```

3. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/FlossWare/curses-themes.git
   ```

4. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install in development mode:**
   ```bash
   pip install -e .
   ```

6. **Install development dependencies:**
   ```bash
   pip install pytest pytest-cov
   ```

7. **Verify the installation:**
   ```bash
   python3 -c "from curses_themes import ThemeManager; print(ThemeManager.list_themes())"
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=curses_themes --cov-report=html

# Run specific test file
pytest tests/test_themes/test_dark.py

# Run tests matching a pattern
pytest -k "test_color_map"
```

### Running Examples

```bash
# Basic theme usage
python3 examples/basic_usage.py

# Interactive theme switcher
python3 examples/theme_switcher.py

# Custom theme example
python3 examples/custom_theme.py

# Retro themes demo
python3 examples/retro_themes_demo.py
```

## How to Contribute

### Contributing New Themes

Contributing a new theme is one of the most valuable contributions! Here's the complete process:

#### Theme Contribution Checklist

- [ ] Created theme class in `curses_themes/themes/your_theme_name.py`
- [ ] Implemented all required methods (`get_color_map()`, component methods)
- [ ] Optionally implemented `get_border_chars()` for custom borders
- [ ] Added comprehensive tests in `tests/test_themes/test_your_theme_name.py`
- [ ] Registered theme in `curses_themes/__init__.py`
- [ ] Registered theme in `curses_themes/manager.py`
- [ ] Updated `README.md` to list your theme
- [ ] Added example usage in `examples/` (optional but encouraged)
- [ ] Verified theme works in both 8-color and 256-color terminals
- [ ] Checked color accessibility (adequate contrast ratios)
- [ ] Added author credit and description
- [ ] Tested with all example scripts

#### Step-by-Step Theme Creation

**1. Create the theme file:** `curses_themes/themes/my_theme.py`

```python
#!/usr/bin/env python3
"""
MyTheme implementation.

Brief description of your theme, its inspiration, and design goals.

Copyright (C) 2024 Your Name

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

from typing import Dict, Tuple
from ..theme import Theme, ColorPair


class MyTheme(Theme):
    """
    A brief description of your theme.
    
    Provide more details about:
    - The inspiration (e.g., "Based on the Nord color palette")
    - The intended use case (e.g., "Designed for low-light environments")
    - Any special characteristics (e.g., "Features warm earth tones")
    
    For retro/historical themes, include:
    - Time period (e.g., "1984-1988")
    - Original system/software (e.g., "Commodore 64 BASIC")
    - Historical accuracy notes
    """
    
    # Define your color constants (RGB tuples, 0-255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    PRIMARY = (0, 120, 215)
    SUCCESS = (16, 124, 16)
    ERROR = (232, 17, 35)
    WARNING = (193, 156, 0)
    INFO = (0, 120, 212)
    ACCENT = (142, 68, 173)
    
    def __init__(self):
        """Initialize the theme with metadata."""
        super().__init__(
            name="My Theme",
            description="A brief, compelling description of your theme",
            author="Your Name"
        )
    
    def get_color_map(self) -> Dict[str, Tuple[int, int, int]]:
        """
        Get RGB color definitions for semantic colors.
        
        Returns:
            Dictionary mapping semantic color names to RGB tuples (0-255)
        """
        return {
            'background': self.BLACK,
            'foreground': self.WHITE,
            'primary': self.PRIMARY,
            'success': self.SUCCESS,
            'error': self.ERROR,
            'warning': self.WARNING,
            'info': self.INFO,
            'accent': self.ACCENT,
        }
    
    def get_background(self) -> ColorPair:
        """Get background color pair for normal components."""
        return ColorPair(self.WHITE, self.BLACK)
    
    def get_button(self) -> ColorPair:
        """Get color pair for buttons in normal state."""
        return ColorPair(self.PRIMARY, self.BLACK)
    
    def get_button_focused(self) -> ColorPair:
        """Get color pair for buttons when focused."""
        return ColorPair(self.BLACK, self.PRIMARY)
    
    def get_text_input(self) -> ColorPair:
        """Get color pair for text input fields."""
        return ColorPair(self.WHITE, self.BLACK)
    
    def get_border(self) -> ColorPair:
        """Get color pair for borders and frames."""
        return ColorPair(self.PRIMARY, self.BLACK)
    
    def get_selection(self) -> ColorPair:
        """Get color pair for selected/highlighted items."""
        return ColorPair(self.BLACK, self.ACCENT)
    
    def get_disabled(self) -> ColorPair:
        """Get color pair for disabled components."""
        return ColorPair(self.WHITE, self.BLACK)
    
    def get_border_chars(self) -> str:
        """
        Get border characters for drawing boxes.
        
        Returns:
            String with 8 characters: TL, T, TR, L, R, BL, B, BR
            
        Examples:
            ASCII box: "+-+||+-+"
            Unicode box: "┌─┐││└─┘"
            Double line: "╔═╗║║╚═╝"
        """
        return "┌─┐││└─┘"  # Unicode box drawing (recommended for modern themes)
```

**2. Create comprehensive tests:** `tests/test_themes/test_my_theme.py`

```python
#!/usr/bin/env python3
"""
Comprehensive tests for MyTheme.

Copyright (C) 2024 Your Name
"""

import pytest
from curses_themes.themes.my_theme import MyTheme
from curses_themes.theme import ColorPair


class TestMyThemeMetadata:
    """Test suite for MyTheme metadata."""
    
    def test_theme_name(self):
        """Test that theme name is correct."""
        theme = MyTheme()
        assert theme.name == "My Theme"
    
    def test_theme_description(self):
        """Test that theme has a non-empty description."""
        theme = MyTheme()
        assert theme.description
        assert isinstance(theme.description, str)
        assert len(theme.description) > 0
    
    def test_theme_author(self):
        """Test that theme has an author."""
        theme = MyTheme()
        assert theme.author == "Your Name"


class TestMyThemeColorMap:
    """Test suite for MyTheme color map."""
    
    def test_color_map_has_all_required_keys(self):
        """Test that color map contains all required semantic color keys."""
        theme = MyTheme()
        color_map = theme.get_color_map()
        
        required_keys = {
            'background', 'foreground', 'primary', 'success',
            'error', 'warning', 'info', 'accent'
        }
        
        assert set(color_map.keys()) == required_keys
    
    def test_rgb_values_are_valid(self):
        """Test that all RGB values are in valid range (0-255)."""
        theme = MyTheme()
        color_map = theme.get_color_map()
        
        for key, (r, g, b) in color_map.items():
            assert isinstance(r, int), f"{key} red component is not an integer"
            assert isinstance(g, int), f"{key} green component is not an integer"
            assert isinstance(b, int), f"{key} blue component is not an integer"
            
            assert 0 <= r <= 255, f"{key} red value {r} out of range"
            assert 0 <= g <= 255, f"{key} green value {g} out of range"
            assert 0 <= b <= 255, f"{key} blue value {b} out of range"


class TestMyThemeComponentMethods:
    """Test suite for MyTheme component color methods."""
    
    def test_all_component_methods_return_colorpairs(self):
        """Test that all component methods return ColorPair objects."""
        theme = MyTheme()
        
        component_methods = [
            'get_background',
            'get_button',
            'get_button_focused',
            'get_text_input',
            'get_border',
            'get_selection',
            'get_disabled'
        ]
        
        for method_name in component_methods:
            method = getattr(theme, method_name)
            result = method()
            assert isinstance(result, ColorPair), f"{method_name} did not return ColorPair"
            assert hasattr(result, 'foreground'), f"{method_name} ColorPair missing foreground"
            assert hasattr(result, 'background'), f"{method_name} ColorPair missing background"


class TestMyThemeBorderChars:
    """Test suite for MyTheme border characters."""
    
    def test_border_chars_length(self):
        """Test that border chars string has exactly 8 characters."""
        theme = MyTheme()
        border_chars = theme.get_border_chars()
        assert len(border_chars) == 8
```

**3. Register the theme in `curses_themes/__init__.py`:**

Add your import:
```python
from .themes import (
    DefaultTheme,
    DarkTheme,
    LightTheme,
    # ... existing themes ...
    MyTheme,  # Add this
)
```

Add to `__all__`:
```python
__all__ = [
    # ... existing exports ...
    'MyTheme',  # Add this
]
```

**4. Register the theme in `curses_themes/manager.py`:**

Add the import at the top:
```python
from .themes import (
    # ... existing imports ...
    MyTheme,
)
```

Register at the bottom:
```python
ThemeManager.register(MyTheme, 'my-theme')
```

**5. Update `README.md`:** Add your theme to the appropriate section with a brief description.

**6. Create an example (optional but encouraged):** `examples/my_theme_demo.py`

```python
#!/usr/bin/env python3
"""Example demonstrating MyTheme."""

import curses
from curses_themes import ThemeManager


def main(stdscr):
    # Load and apply your theme
    theme = ThemeManager.load('my-theme')
    theme.apply(stdscr)
    
    # Demonstrate the theme's features
    stdscr.addstr(0, 0, f"Theme: {theme.name}", theme.colors.primary)
    stdscr.addstr(2, 0, "Success message", theme.colors.success)
    stdscr.addstr(3, 0, "Error message", theme.colors.error)
    stdscr.addstr(4, 0, "Warning message", theme.colors.warning)
    
    theme.draw_box(stdscr, 6, 2, 8, 50, title="Sample Box")
    
    stdscr.addstr(16, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
```

### Reporting Bugs

Found a bug? Here's how to report it effectively:

#### Before Reporting

1. **Check existing issues** - Your bug might already be reported
2. **Test with the latest version** - The bug may already be fixed
3. **Verify it's a library bug** - Make sure the issue isn't in your code
4. **Try to reproduce it** - Can you consistently trigger the bug?

#### Bug Report Template

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Load theme '...'
2. Apply to window '...'
3. Call method '...'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Actual behavior**
What actually happened instead.

**Code Sample**
```python
# Minimal code that reproduces the issue
import curses
from curses_themes import ThemeManager

def main(stdscr):
    theme = ThemeManager.load('dark')
    # ... code that triggers the bug ...
```

**Environment:**
- OS: [e.g., Ubuntu 22.04, macOS 13.0, Windows 11]
- Python version: [e.g., 3.9.7]
- Terminal: [e.g., gnome-terminal, iTerm2, Windows Terminal]
- Color support: [e.g., 8-color, 256-color] (run `echo $TERM`)
- curses-themes version: [e.g., 0.1.0]

**Additional context**
Add any other context about the problem here.
```

### Suggesting Features

We welcome feature suggestions! Please:

1. **Check if it already exists** - Review the documentation and existing issues
2. **Describe the use case** - Why is this feature needed?
3. **Propose a solution** - How might it work?
4. **Consider alternatives** - Are there other ways to achieve the goal?

#### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
Other solutions or features you've considered.

**Code example (if applicable)**
```python
# How you envision the feature being used
theme.set_custom_color('highlight', (255, 100, 0))
```

**Additional context**
Add any other context, screenshots, or examples about the feature request.
```

### Improving Documentation

Documentation improvements are always welcome:

- **Fix typos or unclear explanations** - Submit a PR directly
- **Add examples** - Show how to accomplish common tasks
- **Improve API docs** - Add or clarify docstrings
- **Create tutorials** - Help others learn the library

## Pull Request Process

### Before Submitting

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-new-theme
   # or
   git checkout -b fix/issue-123
   ```

2. **Make your changes** following our coding standards

3. **Add or update tests** for your changes

4. **Run the test suite:**
   ```bash
   pytest
   ```

5. **Update documentation** as needed

6. **Commit with clear messages:**
   ```bash
   git commit -m "Add Nord theme with accessibility features"
   ```

### Submitting the Pull Request

1. **Push to your fork:**
   ```bash
   git push origin feature/my-new-theme
   ```

2. **Open a pull request** on GitHub

3. **Fill out the PR template** with:
   - Description of changes
   - Related issue numbers (if any)
   - Testing performed
   - Screenshots (for visual changes)

4. **Respond to feedback** - We may request changes or clarifications

### PR Review Criteria

We review PRs for:

- **Correctness** - Does it work as intended?
- **Code quality** - Does it follow our standards?
- **Test coverage** - Are new features tested?
- **Documentation** - Are changes documented?
- **Backward compatibility** - Does it break existing code?

### After Approval

Once approved and merged:

- Your contribution will be included in the next release
- You'll be added to the contributors list
- Thank you for making curses-themes better!

## Coding Standards

We follow Python community standards with some project-specific guidelines.

### Python Style Guide

**Follow PEP 8** with these specifics:

- **Indentation:** 4 spaces (no tabs)
- **Line length:** 100 characters maximum (docstrings can be longer for readability)
- **Imports:** Group in order: standard library, third-party, local
- **Naming:**
  - Classes: `PascalCase` (e.g., `DarkTheme`)
  - Functions/methods: `snake_case` (e.g., `get_color_map`)
  - Constants: `UPPER_CASE` (e.g., `DEFAULT_THEME`)
  - Private members: `_leading_underscore` (e.g., `_themes`)

### Code Organization

```python
#!/usr/bin/env python3
"""
Module docstring explaining the purpose.

Longer description if needed, including examples.

Copyright (C) 2024 Author Name

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

# Standard library imports
import curses
from typing import Dict, Tuple

# Third-party imports (if any)
# (This project has zero dependencies!)

# Local imports
from ..theme import Theme, ColorPair


class YourClass:
    """
    Class docstring with description.
    
    Attributes:
        attr_name: Description of attribute
    """
    
    def __init__(self):
        """Initialize with description of parameters."""
        pass
    
    def public_method(self) -> str:
        """
        Method docstring.
        
        Args:
            param: Description
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When something goes wrong
        """
        pass
```

### Documentation Standards

**Docstrings are required for:**
- All public classes
- All public methods and functions
- All module files

**Use Google-style docstrings:**

```python
def draw_box(self, window, y: int, x: int, height: int, width: int,
             title: str = "") -> None:
    """
    Draw a themed border box on the given window.
    
    The box uses the theme's border characters and colors. An optional
    title can be centered in the top border.
    
    Args:
        window: Curses window to draw on
        y: Top-left Y coordinate
        x: Top-left X coordinate
        height: Box height in characters
        width: Box width in characters
        title: Optional title to display in top border
        
    Raises:
        ValueError: If box dimensions are too small (minimum 2x2)
        
    Example:
        ```python
        theme.draw_box(stdscr, 5, 10, 8, 40, title="Settings")
        ```
    """
```

### Type Hints

Use type hints for better code clarity:

```python
from typing import Dict, Tuple, Optional

def get_color_map(self) -> Dict[str, Tuple[int, int, int]]:
    """Return color definitions."""
    return {...}

def get_background(self) -> Optional[ColorPair]:
    """Return background color pair or None."""
    return ColorPair(...)
```

### Error Handling

- Use specific exception types
- Provide helpful error messages
- Include context in error messages

```python
if normalized_name not in self._themes:
    available = ', '.join(sorted(self._themes.keys()))
    raise KeyError(
        f"Theme '{normalized_name}' not found. "
        f"Available themes: {available}"
    )
```

## Testing Requirements

### Test Coverage Expectations

- **New themes:** 100% coverage (all methods tested)
- **Bug fixes:** Must include a test that fails before the fix
- **New features:** Must include comprehensive tests
- **Minimum overall coverage:** 90%

### Test Organization

```
tests/
├── test_theme_manager.py        # ThemeManager tests
├── test_color_manager.py        # Color initialization tests
└── test_themes/
    ├── __init__.py
    ├── test_default.py          # DefaultTheme tests
    ├── test_dark.py             # DarkTheme tests
    └── test_my_theme.py         # Your theme tests
```

### Test Structure

Organize tests into logical classes:

```python
class TestMyThemeMetadata:
    """Test suite for theme metadata."""
    
    def test_theme_name(self):
        """Test that theme name is correct."""
        pass


class TestMyThemeColorMap:
    """Test suite for color map validation."""
    
    def test_color_map_has_all_required_keys(self):
        """Test required keys are present."""
        pass
    
    def test_rgb_values_are_valid(self):
        """Test RGB values are in range 0-255."""
        pass


class TestMyThemeComponentMethods:
    """Test suite for component color methods."""
    
    def test_get_background_returns_colorpair(self):
        """Test background method returns ColorPair."""
        pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=curses_themes --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_themes/test_my_theme.py

# Run specific test
pytest tests/test_themes/test_my_theme.py::TestMyThemeMetadata::test_theme_name

# Run tests matching pattern
pytest -k "color_map"

# Verbose output
pytest -v
```

### Test Quality Guidelines

**Good tests are:**
- **Clear:** Easy to understand what's being tested
- **Isolated:** Don't depend on other tests
- **Repeatable:** Same result every time
- **Fast:** Run quickly
- **Comprehensive:** Cover edge cases

**Each test should:**
- Test one thing
- Have a descriptive name
- Include a docstring
- Use meaningful assertions

```python
def test_rgb_values_are_valid(self):
    """Test that all RGB values are in valid range (0-255)."""
    theme = MyTheme()
    color_map = theme.get_color_map()
    
    for key, (r, g, b) in color_map.items():
        assert 0 <= r <= 255, f"{key} red value {r} out of range"
        assert 0 <= g <= 255, f"{key} green value {g} out of range"
        assert 0 <= b <= 255, f"{key} blue value {b} out of range"
```

## Documentation Requirements

### Required Documentation

When contributing, update these as appropriate:

1. **Docstrings** - All public APIs must have docstrings
2. **README.md** - Add new themes to the theme list
3. **Code comments** - Explain complex or non-obvious code
4. **Examples** - Demonstrate new features in `examples/`
5. **Tests** - Test code should be self-documenting

### Docstring Examples

**Module docstring:**
```python
"""
Theme base classes and semantic color support for curses applications.

This module provides the core Theme abstraction and SemanticColors container
that enable pluggable theming for Python curses applications.

Example:
    Basic theme usage::
    
        from curses_themes import Theme, ThemeManager
        
        theme = ThemeManager.load('dark')
        theme.apply(stdscr)
"""
```

**Class docstring:**
```python
class MyTheme(Theme):
    """
    Brief one-line description.
    
    Longer description explaining the theme's design philosophy,
    inspiration, color choices, and intended use cases.
    
    For retro themes, include historical context:
    - Time period and original system
    - Design characteristics of that era
    - Authenticity notes
    
    Attributes:
        name: Theme display name
        description: Brief description
        author: Theme creator
    
    Example:
        ```python
        theme = MyTheme()
        theme.apply(stdscr)
        stdscr.addstr(0, 0, "Hello", theme.colors.primary)
        ```
    """
```

## Theme Design Guidelines

### Color Selection Principles

**1. Accessibility First**

- Maintain adequate contrast ratios (WCAG guidelines)
- Test with color blindness simulators
- Provide both dark and light options when possible
- Consider users with visual impairments

**Minimum contrast ratios:**
- Normal text: 4.5:1
- Large text: 3:1
- UI components: 3:1

**2. Semantic Consistency**

Follow these semantic color conventions:

- **Success/Positive:** Green or cool colors
- **Error/Danger:** Red or warm alert colors
- **Warning/Caution:** Yellow, orange, or amber
- **Info/Neutral:** Blue or neutral tones
- **Primary:** Your theme's signature color
- **Accent:** Secondary highlight color

**3. Color Harmony**

Choose colors that work well together:

- Use established color palettes when possible (Solarized, Nord, Dracula, etc.)
- Maintain consistent color temperature (warm vs. cool)
- Limit the number of different hues (5-8 is typical)
- Consider the overall mood (professional, playful, retro, etc.)

### Retro/Historical Theme Guidelines

When creating themes based on historical systems or software, follow these guidelines inspired by curses-java:

**1. Historical Accuracy**

- **Research the original:** Use screenshots, manuals, or emulators
- **Document the era:** Include the time period in the theme description
- **Color fidelity:** Match the original colors as closely as possible
- **Limitations:** Respect the original system's limitations (e.g., 8 colors)

**Example:** TI-99/4A Theme (1981-1984)
```python
class TI994ATheme(Theme):
    """
    TI-99/4A home computer theme (1981-1984).
    
    Texas Instruments' iconic home computer featured a distinctive
    cyan-on-blue color scheme that became memorable to a generation
    of early computer users.
    
    Historical notes:
    - Original system: Texas Instruments TI-99/4A
    - Display: 32-column text mode
    - Colors: 16 fixed colors from TMS9918 VDP chip
    - Typical use: BASIC programming, educational software
    """
```

**2. Modern Adaptations**

Balance historical authenticity with modern usability:

- Adjust colors slightly for better readability if needed (document changes)
- Use Unicode box-drawing characters on modern terminals
- Support both 8-color and 256-color modes
- Maintain the "feel" while improving accessibility

**3. Documentation**

Include in your theme docstring:

- Original system/software name
- Time period of use
- Notable characteristics
- Any deviations from the original for modern usability

### Terminal Compatibility

**Test your theme in different environments:**

- **8-color terminals** - Basic color support
- **16-color terminals** - Extended basic colors
- **256-color terminals** - Full color palette
- **True color terminals** - 24-bit RGB (not all terminals support this)

**Color fallback strategy:**

The ColorManager handles fallbacks automatically, but design with this in mind:

1. Define colors that look good in 256-color mode
2. Ensure they're distinguishable in 16-color mode
3. Verify basic usability in 8-color mode

### Border Characters

Choose appropriate border characters for your theme:

**ASCII (universal compatibility):**
```python
def get_border_chars(self) -> str:
    return "+-+||+-+"  # TL T TR L R BL B BR
```

**Unicode box-drawing (modern terminals):**
```python
def get_border_chars(self) -> str:
    return "┌─┐││└─┘"  # Light box
    # or
    return "╔═╗║║╚═╝"  # Double box
```

**Retro/simple:**
```python
def get_border_chars(self) -> str:
    return "        "  # Spaces (for minimal themes)
    # or
    return "########"  # Hash marks (DOS-style)
```

## Examples of Good Contributions

Here are examples of high-quality contributions to inspire you:

### Example 1: Well-Designed Modern Theme

The **DarkTheme** is an excellent example of a modern theme:

**Strengths:**
- Clean, professional color palette
- Excellent documentation with clear docstrings
- Comprehensive test coverage (100%)
- Unicode border characters for modern terminals
- Good contrast ratios for accessibility
- Implements all required methods
- Matches curses-java API for consistency

**Code highlights:**
```python
class DarkTheme(Theme):
    """
    Dark theme with muted colors and dark background.
    Modern dark mode aesthetic.
    
    Matches the curses-java DarkTheme implementation exactly:
    - Background: CYAN on BLACK
    - Button: BLUE on BLACK
    - ButtonFocused: BLACK on BLUE
    - TextInput: WHITE on BLACK
    - Border: BLUE on BLACK
    - Selection: BLACK on CYAN
    - Disabled: BLUE on BLACK (muted)
    - BorderChars: "┌─┐││└─┘" (Unicode box drawing)
    """
```

### Example 2: Historically Accurate Retro Theme

The **TI-99/4A Theme** demonstrates excellent historical theme design:

**Strengths:**
- Thoroughly researched original system
- Documented time period and historical context
- Authentic color reproduction
- Educational value for users interested in computing history
- Clear explanation of design choices

**Documentation highlights:**
```python
"""
TI-99/4A home computer theme (1981-1984).

Texas Instruments' iconic home computer featured a distinctive
cyan-on-blue color scheme that became memorable to a generation
of early computer users.

Historical notes:
- Original system: Texas Instruments TI-99/4A
- Display: 32-column text mode
- Colors: 16 fixed colors from TMS9918 VDP chip
- Typical use: BASIC programming, educational software
"""
```

### Example 3: Comprehensive Test Suite

The **test_dark.py** file shows exemplary testing:

**Strengths:**
- Organized into logical test classes
- Tests all aspects (metadata, colors, components)
- Clear test names that describe what's being tested
- Comprehensive docstrings
- Validates RGB ranges
- Tests edge cases
- High readability

**Test organization:**
```python
class TestDarkThemeMetadata:
    """Test suite for DarkTheme metadata."""
    
class TestDarkThemeColorMap:
    """Test suite for DarkTheme color map."""
    
class TestDarkThemeComponentMethods:
    """Test suite for DarkTheme component color methods."""
    
class TestDarkThemeBorderChars:
    """Test suite for DarkTheme border characters."""
```

### Example 4: Helpful Example Code

The **custom_theme.py** example is a great learning resource:

**Strengths:**
- Complete, runnable example
- Detailed comments explaining each step
- Shows best practices
- Demonstrates all theme features
- Educational for contributors
- Includes proper error handling with curses.wrapper()

### Example 5: Clear Bug Report

Good bug report structure:

```markdown
**Bug:** Theme colors not applied in tmux

**Environment:**
- OS: Ubuntu 22.04
- Python: 3.10.6
- Terminal: tmux 3.2a in gnome-terminal
- Color support: 256-color (TERM=screen-256color)

**To Reproduce:**
```python
import curses
from curses_themes import ThemeManager

def main(stdscr):
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)
    stdscr.addstr(0, 0, "Test", theme.colors.primary)
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

**Expected:** Text appears in blue (primary color)
**Actual:** Text appears in default terminal color

**Additional context:**
- Works correctly outside tmux
- Works correctly with 'default' theme
- Other themes also affected
```

### What Makes These Examples Great?

1. **Clarity** - Easy to understand intent and implementation
2. **Completeness** - All necessary components included
3. **Documentation** - Well-documented with clear explanations
4. **Testing** - Comprehensive test coverage
5. **Consistency** - Follows project conventions
6. **Quality** - Attention to detail and polish
7. **Educational** - Helps others learn and contribute

## Questions?

If you have questions about contributing:

- **Check the documentation** - [README.md](README.md), [GUIDE.md](GUIDE.md)
- **Review existing code** - See how similar things are done
- **Open an issue** - Ask for clarification
- **Start small** - Begin with a simple contribution

## License

By contributing to curses-themes, you agree that your contributions will be licensed under the GNU General Public License v3.0 (GPL-3.0).

All contributions must include the GPL-3.0 license header:

```python
"""
Copyright (C) 2024 Your Name

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
```

## Thank You!

Thank you for taking the time to contribute to curses-themes! Your efforts help make terminal applications more beautiful and accessible for everyone.

Every contribution, whether it's a new theme, a bug fix, documentation improvement, or just reporting an issue, helps make this project better.

We look forward to seeing your contributions!

---

*Inspired by the excellent [curses-java](https://github.com/FlossWare/curses-java) library.*
