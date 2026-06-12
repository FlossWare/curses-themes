# curses-themes Example Best Practices

This document outlines the best practices for writing examples using the curses-themes library.

## Theme Lifecycle Management

### 1. Registration → Load → Apply Pattern

Always follow this sequence when working with themes:

```python
# 1. Register custom theme (if needed)
ThemeManager.register(MyCustomTheme)

# 2. Load theme by slug
theme = ThemeManager.load("my-custom-theme")

# 3. Apply theme to window
theme.apply(stdscr)
```

**Important**: Registration must happen before loading. The `register()` method makes the theme class available to `ThemeManager`.

### 2. Error Handling for Theme Operations

Always wrap theme loading and application in try/except blocks:

```python
try:
    theme = ThemeManager.load("theme-name")
    theme.apply(stdscr)
except RuntimeError as e:
    # Terminal doesn't support colors or theme initialization failed
    stdscr.addstr(0, 0, f"Theme error: {e}")
    stdscr.addstr(1, 0, "This terminal may not support colors.")
    stdscr.refresh()
    stdscr.getch()
    return
except Exception as e:
    # Unknown error - try fallback theme
    try:
        theme = ThemeManager.load("default")
        theme.apply(stdscr)
    except Exception:
        stdscr.addstr(0, 0, f"Error loading theme: {e}")
        stdscr.refresh()
        stdscr.getch()
        return
```

**Why**: Theme operations can fail if:
- Terminal doesn't support colors
- Theme doesn't exist
- Color initialization fails
- Terminal has insufficient color pairs available

## Color Pair Usage

### Understanding theme.colors Values

**Critical Concept**: `theme.colors.X` returns a color pair NUMBER, not a color attribute you can use directly.

```python
# ❌ INCORRECT - Missing curses.color_pair() wrapper
stdscr.addstr(y, x, "Text", theme.colors.primary)

# ✅ CORRECT - Wrap in curses.color_pair()
stdscr.addstr(y, x, "Text", curses.color_pair(theme.colors.primary))
```

### When to Use curses.color_pair()

Use `curses.color_pair()` when passing theme colors to:
- `addstr()` and `addch()` - text rendering functions
- `bkgd()` - background color setting
- Any curses function expecting a color attribute

**Exception**: Some theme methods handle color_pair wrapping internally:
- `theme.draw_box()` - automatically handles color pair
- `theme.draw_box_3d()` - automatically handles color pair

### Combining with Attributes

You can combine color pairs with text attributes using bitwise OR:

```python
# Combine primary color with bold attribute
stdscr.addstr(y, x, "Bold Text", 
              curses.color_pair(theme.colors.primary) | curses.A_BOLD)

# Combine info color with dim attribute
stdscr.addstr(y, x, "Dimmed Text",
              curses.color_pair(theme.colors.info) | curses.A_DIM)
```

## Exception Handling Patterns

### 1. Boundary Errors with curses.error

It's acceptable to ignore `curses.error` for boundary conditions, but **always include an explanatory comment**:

```python
try:
    stdscr.addstr(height - 1, width - 1, "X")
except curses.error:
    # Ignore errors when drawing at screen boundaries
    pass
```

**Why Comment**: The next developer needs to know this is intentional, not a bug.

### 2. Specific Exception Types

Always catch specific exception types, not bare `except:`:

```python
# ❌ BAD - Catches everything, including KeyboardInterrupt
try:
    theme.apply(stdscr)
except:
    pass

# ✅ GOOD - Catches specific exception
try:
    theme.apply(stdscr)
except RuntimeError as e:
    handle_theme_error(e)

# ✅ ALSO GOOD - Catches all exceptions except system exits
try:
    theme.apply(stdscr)
except Exception as e:
    handle_theme_error(e)
```

**Why**: Bare `except:` catches `KeyboardInterrupt` and `SystemExit`, preventing graceful shutdown.

### 3. Unicode Handling

For Unicode characters, catch `UnicodeEncodeError` specifically:

```python
try:
    stdscr.addstr(y, x, "✓ Success")
except UnicodeEncodeError:
    # Fallback for terminals without Unicode support
    stdscr.addstr(y, x, "* Success")
```

## Resource Management

### Use curses.wrapper()

Always use `curses.wrapper()` for automatic cleanup:

```python
def main(stdscr):
    # Your application code here
    pass

if __name__ == "__main__":
    curses.wrapper(main)
```

**What it does**:
- Initializes curses properly
- Automatically restores terminal state on exit
- Handles exceptions and cleanup
- No manual cleanup needed

### Hide Cursor Safely

```python
try:
    curses.curs_set(0)  # Hide cursor
except curses.error:
    # Some terminals don't support cursor visibility control
    pass
```

## Theme Validation

### Check Theme Components

Before using theme components, verify they exist:

```python
# Check if theme has 3D drawing capability
if hasattr(theme, "draw_box_3d"):
    theme.draw_box_3d(stdscr, y, x, height, width, raised=True)
else:
    # Fallback to regular box
    theme.draw_box(stdscr, y, x, height, width)
```

### Accessing Theme Properties

Safe pattern for accessing theme properties:

```python
# Get theme description safely
if hasattr(theme, "description") and theme.description:
    stdscr.addstr(y, x, theme.description[:width-4])
```

## Documentation Standards

### Module Docstrings

Every example should start with a docstring explaining:

```python
#!/usr/bin/env python3
"""
Brief description of what this example demonstrates.

This example shows how to:
- Feature 1
- Feature 2
- Feature 3

Copyright (C) 2024 FlossWare
[... license text ...]
"""
```

### Function Docstrings

Document all functions with clear parameter and return descriptions:

```python
def draw_demo_ui(stdscr, theme):
    """
    Draw the demonstration UI using the current theme.

    Args:
        stdscr: Curses window object
        theme: Current Theme instance

    Returns:
        None
    """
```

### Inline Comments for Non-Obvious Code

Add comments explaining:
- Why exceptions are caught/ignored
- What color pair numbers represent
- Why certain patterns are used

```python
# theme.colors.primary is a color pair NUMBER - must wrap in curses.color_pair()
stdscr.addstr(y, x, "Text", curses.color_pair(theme.colors.primary))
```

## Common Patterns

### Theme Switching in Interactive Apps

```python
def switch_theme(stdscr, theme_name):
    """Switch to a new theme with error handling."""
    try:
        theme = ThemeManager.load(theme_name)
        theme.apply(stdscr)
        return theme
    except Exception as e:
        # Log error but keep current theme
        return None
```

### Error Display with Theme Colors

```python
try:
    theme = ThemeManager.load("dark")
    theme.apply(stdscr)
except RuntimeError as e:
    # Use default terminal colors for error message
    stdscr.addstr(0, 0, f"Error: {e}")
    stdscr.refresh()
    return
```

### Screen Size Validation

```python
height, width = stdscr.getmaxyx()

# Only draw complex UI if screen is large enough
if height > 20 and width > 60:
    draw_detailed_ui(stdscr, theme)
else:
    draw_simple_ui(stdscr, theme)
```

## Testing Your Example

Before submitting your example, verify:

1. **No bare except clauses** - Use `except Exception:` or specific types
2. **Theme loading has error handling** - Wrap in try/except
3. **Color pairs are wrapped** - Use `curses.color_pair(theme.colors.X)`
4. **Uses curses.wrapper()** - For proper cleanup
5. **Has module docstring** - Explaining what it demonstrates
6. **Comments explain non-obvious code** - Especially exception handling

Run the test suite:

```bash
pytest tests/test_examples.py -v
```

## Anti-Patterns to Avoid

### ❌ Don't: Use bare except
```python
try:
    theme.apply(stdscr)
except:  # Catches KeyboardInterrupt!
    pass
```

### ❌ Don't: Use theme.colors directly with addstr
```python
stdscr.addstr(y, x, "Text", theme.colors.primary)  # Missing color_pair()!
```

### ❌ Don't: Ignore all errors silently
```python
try:
    theme = ThemeManager.load("nonexistent")
except Exception:
    pass  # User has no idea what went wrong
```

### ❌ Don't: Manual terminal cleanup
```python
if __name__ == "__main__":
    stdscr = curses.initscr()  # Manual initialization
    # ... code ...
    curses.endwin()  # Manual cleanup - use curses.wrapper() instead!
```

## Summary Checklist

When writing a new example:

- [ ] Use `curses.wrapper()` for main entry point
- [ ] Add comprehensive module docstring
- [ ] Wrap `ThemeManager.load()` in try/except
- [ ] Wrap `theme.apply()` in try/except
- [ ] Use `curses.color_pair()` with all theme.colors values
- [ ] Catch specific exception types (not bare `except:`)
- [ ] Add comments explaining exception handling
- [ ] Test on multiple terminal types
- [ ] Verify no syntax errors with `python -m py_compile`
- [ ] Run example test suite

## Getting Help

If you're unsure about a pattern:

1. Check existing examples in this directory
2. Review this best practices document
3. Look at the library's main documentation
4. Check the test suite for expected patterns

## References

- [curses-themes API Documentation](../README.md)
- [Python curses Documentation](https://docs.python.org/3/library/curses.html)
- [Example Test Suite](../tests/test_examples.py)
