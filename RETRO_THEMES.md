# Retro Themes Port from curses-java

This document describes the 5 retro themes ported from the [curses-java](https://github.com/FlossWare/curses-java) project.

## Overview

All retro themes have been successfully ported with full historical context, authentic color schemes, and period-appropriate border styles. Each theme includes comprehensive documentation about its historical context and visual identity.

## Ported Themes

### 1. TI-99/4A Theme (`ti-99-4a`)

**Era:** 1981-1984  
**System:** Texas Instruments TI-99/4A home computer

**Historical Context:**  
The first 16-bit home computer, featuring the TMS9918A video display processor. Competed with the Commodore 64, Apple II, and Atari 8-bit computers.

**Color Scheme:**
- Background: Cyan on blue (signature TI-99/4A appearance)
- Buttons: White on blue (enhanced visibility)
- Focused: Blue on cyan (inverted)
- Text Input: Cyan on blue
- Borders: Cyan on blue
- Selection: Blue on white (high contrast)
- Disabled: Blue on blue (muted)
- Border Style: ASCII `+-+||+-+` (1981-era authenticity)

**Usage:**
```python
theme = ThemeManager.load('ti-99-4a')
theme.apply(stdscr)
```

---

### 2. TRS-80 Theme (`trs-80`)

**Era:** 1980-1983  
**System:** Tandy/Radio Shack TRS-80 Model III and Model 4

**Historical Context:**  
Part of the "1977 Trinity" of home computers (along with Apple II and Commodore PET). Featured monochrome displays praised for clarity and lack of color fringing. Popular for business applications and word processing.

**Color Scheme:**
- Background: White on black (pure monochrome)
- Buttons: White on black
- Focused: Black on white (high-contrast inversion)
- Text Input: White on black
- Borders: White on black
- Selection: Black on white (maximum contrast)
- Disabled: Black on black (completely hidden)
- Border Style: ASCII `+-+||+-+` (early 1980s authenticity)

**Usage:**
```python
theme = ThemeManager.load('trs-80')
theme.apply(stdscr)
```

---

### 3. DOS Theme (`dos`)

**Era:** 1981-1995  
**System:** MS-DOS and PC-DOS

**Historical Context:**  
The dominant operating system of the PC era. Text-mode interface running in 80×25 character mode with 16 colors became the de facto standard. Key applications like WordPerfect, Lotus 1-2-3, and dBASE all shared this visual language.

**Color Scheme:**
- Background: White on black (standard DOS palette)
- Buttons: Yellow on black (bright menu items)
- Focused: Black on yellow (inverted)
- Text Input: Cyan on black (distinguishes input fields)
- Borders: White on black
- Selection: Black on white (high-contrast)
- Disabled: Black on black (hidden)
- Border Style: ASCII `+-+||+-+` (compatible with all terminals)

**Usage:**
```python
theme = ThemeManager.load('dos')
theme.apply(stdscr)
```

---

### 4. dBASE III Theme (`dbase-iii`)

**Era:** 1984-1985  
**Software:** Ashton-Tate dBASE III and dBASE III Plus

**Historical Context:**  
Revolutionized database management on personal computers. The best-selling database software by 1985, powering thousands of custom business applications. Its programming language (xBase) spawned numerous clones including Clipper and FoxPro.

**Color Scheme:**
- Background: White on black (classic dot prompt)
- Buttons: Cyan on black (dBASE's signature menu color)
- Focused: Black on cyan (inverted)
- Text Input: Green on black (data entry fields)
- Borders: White on black
- Selection: Black on cyan (highlighted records)
- Disabled: Black on black (hidden)
- Border Style: ASCII `+-+||+-+` (mid-1980s authenticity)

**Usage:**
```python
theme = ThemeManager.load('dbase-iii')
theme.apply(stdscr)
```

---

### 5. dBASE IV Theme (`dbase-iv`)

**Era:** 1988-1993  
**Software:** Ashton-Tate/Borland dBASE IV

**Historical Context:**  
Introduced a revolutionary menu-driven interface (the Control Center) with multiple windows, pull-down menus, and mouse support. The shift from black to blue backgrounds was part of a broader trend in late-1980s software design toward GUI-inspired interfaces.

**Color Scheme:**
- Background: White on blue (Control Center interface)
- Buttons: Yellow on blue (menu bar)
- Focused: Blue on yellow (inverted)
- Text Input: Cyan on blue (data entry)
- Borders: White on blue (window frames)
- Selection: Blue on white (highlighted records)
- Disabled: Blue on blue (dimmed)
- Border Style: ASCII `+-+||+-+` (universal compatibility)

**Usage:**
```python
theme = ThemeManager.load('dbase-iv')
theme.apply(stdscr)
```

---

## Demo

Run the retro themes demo to see all themes in action:

```bash
python3 examples/retro_themes_demo.py
```

Press any key to cycle through themes, 'q' to quit.

## Implementation Notes

### Color Mapping

Each theme provides both:
1. **Component-based colors** (matching curses-java API):
   - `get_background()`, `get_button()`, `get_button_focused()`
   - `get_text_input()`, `get_border()`, `get_selection()`, `get_disabled()`

2. **Semantic colors** (Python extension):
   - `primary`, `success`, `error`, `warning`, `info`, `accent`

### Border Characters

All retro themes use ASCII borders (`+-+||+-+`) for period authenticity and maximum terminal compatibility. The original systems predated Unicode box-drawing characters.

### Terminal Compatibility

The `ColorManager` automatically adapts colors to terminal capabilities:
- 256-color terminals: Full RGB palette mapping
- 16-color terminals: Maps to closest ANSI colors
- 8-color terminals: Maps to basic 8-color palette

### Windows Support

These themes work on Windows with the `windows-curses` package:
```bash
pip install windows-curses
```

## Theme Comparison

| Theme | Background | Interactive Color | Era | Best For |
|-------|------------|-------------------|-----|----------|
| TI-99/4A | Cyan on blue | White | 1981-1984 | Warm retro aesthetic |
| TRS-80 | White on black | White inverted | 1980-1983 | Maximum text clarity |
| DOS | White on black | Yellow | 1981-1995 | Command-line utilities |
| dBASE III | White on black | Cyan | 1984-1985 | Database applications |
| dBASE IV | White on blue | Yellow | 1988-1993 | Windowed interfaces |

## Credits

Themes ported from [FlossWare curses-java](https://github.com/FlossWare/curses-java) with full attribution to the original historical research and design.

Original Java implementation: FlossWare  
Python port: FlossWare (2024)

## License

GPL-3.0 - Same as the main curses-themes library.
