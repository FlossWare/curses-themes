# Screenshot Generation System

This directory contains screenshots of all curses-themes color schemes and documentation for generating them.

## Overview

The screenshot generation system creates visual documentation for all themes in the curses-themes library. Screenshots show each theme's color palette, semantic colors, border styles, and special effects (3D themes) in a standardized layout.

## Prerequisites

### Required Dependencies

- **Python 3.9+** - Core runtime
- **PIL/Pillow** - Image generation library
- **curses-themes library** - The theme library (from this project)
- **Monospace font** - One of the following (auto-detected):
  - DejaVu Sans Mono (most common)
  - Liberation Mono (Fedora/RHEL default)
  - Noto Sans Mono (Google fonts)
  - Courier New (fallback)
  - Any system monospace font

### Install Pillow

```bash
# Using pip
pip install Pillow

# Using system package manager (Fedora/RHEL)
sudo dnf install python3-pillow

# Using system package manager (Debian/Ubuntu)
sudo apt install python3-pil
```

### Install Fonts (if needed)

```bash
# Fedora/RHEL
sudo dnf install dejavu-sans-mono-fonts liberation-mono-fonts

# Debian/Ubuntu
sudo apt install fonts-dejavu fonts-liberation

# Arch Linux
sudo pacman -S ttf-dejavu ttf-liberation
```

## Generating Screenshots

### Basic Usage

Generate all theme screenshots with default settings:

```bash
cd /home/sfloess/Development/github/FlossWare/curses-themes
python3 tools/screenshot_capture.py
```

This creates PNG images in `screenshots/` directory (created automatically).

### Advanced Options

```bash
# Custom output directory
python3 tools/screenshot_capture.py --output-dir ./images

# Larger font size (default: 14pt)
python3 tools/screenshot_capture.py --font-size 16

# Custom terminal dimensions (default: 80x24)
python3 tools/screenshot_capture.py --width 100 --height 30

# Generate specific theme only
python3 tools/screenshot_capture.py --theme borland-3d

# Create comparison grid image
python3 tools/screenshot_capture.py --create-grid

# Combine multiple options
python3 tools/screenshot_capture.py --output-dir ./docs/images --font-size 16 --create-grid
```

### Command-Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--output-dir` | `screenshots/` | Output directory for PNG files |
| `--width` | `80` | Terminal width in characters |
| `--height` | `24` | Terminal height in characters |
| `--font-size` | `14` | Font size in points |
| `--theme` | (all) | Generate specific theme only |
| `--create-grid` | false | Generate multi-theme comparison image |

## Generated Screenshots

### Individual Theme Screenshots

Each theme generates a PNG image (~800x600px at default settings) showing:

**Modern Themes:**
- `screenshots/default.png` - Classic white-on-black terminal
- `screenshots/dark.png` - Professional dark mode with blues
- `screenshots/light.png` - High contrast light mode

**Retro Computer Themes:**
- `screenshots/ti-99-4a.png` - Texas Instruments TI-99/4A (1981-1984)
- `screenshots/trs-80.png` - Tandy/Radio Shack TRS-80 (1980-1983)

**Business Software Themes:**
- `screenshots/dos.png` - MS-DOS text mode (1981-1995)
- `screenshots/dbase-iii.png` - dBASE III database software (1984-1985)
- `screenshots/dbase-iv.png` - dBASE IV Control Center (1988-1993)

**3D Effect Themes:**
- `screenshots/borland-3d.png` - Borland Turbo Vision 3D interface
- `screenshots/dbase-iv-3d.png` - dBASE IV with 3D shadow effects

### Comparison Grid

When `--create-grid` is specified:
- `screenshots/comparison.png` - Multi-theme grid showing all themes side-by-side

## Screenshot Specifications

### Layout (80x24 characters, ~800x600px)

```
Row 0:    Theme name header (centered, bold, focused button colors)
Row 1:    Theme description
Row 3-17: Demo panel with sample UI elements
          - Buttons (normal and focused)
          - Text input fields
          - Selection highlighting
          - Semantic colors (success, error, warning, info)
Row 13-15: Border style indicator
Row 19-22: 3D effects panel (Theme3D subclasses only)
Row 23:   Footer with theme metadata
```

### Image Dimensions

| Setting | Width | Height | File Size |
|---------|-------|--------|-----------|
| Default (80x24) | ~800px | ~600px | 20-40 KB |
| Large (100x30) | ~1000px | ~750px | 30-60 KB |
| Font size 16pt | ~900px | ~680px | 25-50 KB |

### Color Accuracy

- Screenshots use **direct RGB mapping** from theme definitions
- No color approximation or terminal palette conversion
- Exact rendering of theme.get_color_map() RGB values
- True color output (24-bit RGB PNG files)

## Using Screenshots in Documentation

### In THEMES.md

Add screenshots to each theme section:

```markdown
### 1. Default Theme

**Classic terminal white-on-black**

![Default Theme Screenshot](screenshots/default.png)

The Default theme provides a timeless terminal aesthetic with high contrast and excellent readability.
```

**Recommended placement:** After theme title and tagline, before color palette description.

### In README.md

Add theme showcase section:

```markdown
## Built-in Themes

### Modern Themes

| Theme | Screenshot | Description |
|-------|------------|-------------|
| Default | ![Default](screenshots/default.png) | Classic white-on-black terminal |
| Dark | ![Dark](screenshots/dark.png) | Professional dark mode with blues |
| Light | ![Light](screenshots/light.png) | High contrast light mode |
```

Or create a visual gallery:

```markdown
## Theme Gallery

### Modern Themes

<table>
  <tr>
    <td><img src="screenshots/default.png" width="300"/><br/><b>Default</b></td>
    <td><img src="screenshots/dark.png" width="300"/><br/><b>Dark</b></td>
    <td><img src="screenshots/light.png" width="300"/><br/><b>Light</b></td>
  </tr>
</table>
```

**Recommended placement:** After "Quick Start" section, before "Installation" or in dedicated "Gallery" section.

## GitHub Social Preview

Create a 1280x640px social preview image for GitHub repository:

### Method 1: Comparison Grid

```bash
# Generate comparison grid (creates all themes in one image)
python3 tools/screenshot_capture.py --create-grid --output-dir ./

# Resize to 1280x640 using ImageMagick
convert comparison.png -resize 1280x640 -gravity center -extent 1280x640 social-preview.png
```

### Method 2: Custom Layout

```bash
# Generate larger individual screenshots
python3 tools/screenshot_capture.py --width 100 --height 30 --font-size 16

# Use ImageMagick to create montage
montage screenshots/default.png screenshots/dark.png screenshots/borland-3d.png \
  -geometry 400x300+10+10 -tile 3x1 -background black social-preview-temp.png

# Resize to exact GitHub dimensions
convert social-preview-temp.png -resize 1280x640 -gravity center -extent 1280x640 social-preview.png
```

### Method 3: Manual Composite

Create a custom layout highlighting key themes:

```bash
# Generate high-quality screenshots
python3 tools/screenshot_capture.py --font-size 18

# Use image editor (GIMP, Photoshop, etc.) to create 1280x640 layout
# - Add project title/logo
# - Show 3-4 representative themes
# - Include tagline: "Professional theme support for Python curses applications"
```

### Upload to GitHub

1. Go to repository Settings on GitHub
2. Scroll to "Social Preview" section
3. Click "Edit" and upload `social-preview.png`
4. Preview will appear in GitHub search results and link previews

## Troubleshooting

### Font Not Found

**Error:** `OSError: cannot open resource`

**Solution:**
```bash
# Install monospace fonts
sudo dnf install dejavu-sans-mono-fonts  # Fedora/RHEL
sudo apt install fonts-dejavu            # Debian/Ubuntu

# Or specify custom font in screenshot_capture.py
# Edit line with ImageFont.truetype() to use your font path
```

### Pillow Not Installed

**Error:** `ModuleNotFoundError: No module named 'PIL'`

**Solution:**
```bash
pip install Pillow
# or
sudo dnf install python3-pillow
```

### Unicode Characters Not Rendering

**Symptom:** Box-drawing characters appear as squares or missing

**Solution:**
- Use a font with full Unicode support (DejaVu Sans Mono recommended)
- Or install Noto Sans Mono: `sudo dnf install google-noto-sans-mono-fonts`

### Image Too Small/Large

**Solution:**
```bash
# Adjust font size
python3 tools/screenshot_capture.py --font-size 12  # smaller
python3 tools/screenshot_capture.py --font-size 18  # larger

# Adjust terminal dimensions
python3 tools/screenshot_capture.py --width 100 --height 30
```

### 3D Effects Not Showing

**Symptom:** Borland 3D and dBASE IV 3D themes look flat

**Solution:**
- 3D effects only appear for Theme3D subclasses
- Verify theme inherits from Theme3D (Borland3DTheme, DBase4_3DTheme)
- Check terminal height ≥ 24 for full 3D effect panel

### Permission Denied

**Error:** `PermissionError: [Errno 13] Permission denied: 'screenshots'`

**Solution:**
```bash
# Use custom output directory
python3 tools/screenshot_capture.py --output-dir ~/tmp/screenshots

# Or create directory manually
mkdir -p screenshots
```

## Advanced Usage

### Batch Generation Script

Create all screenshots with optimal settings:

```bash
#!/bin/bash
# generate_all.sh

OUTPUT="screenshots"
mkdir -p "$OUTPUT"

echo "Generating individual theme screenshots..."
python3 tools/screenshot_capture.py --output-dir "$OUTPUT" --font-size 14

echo "Generating comparison grid..."
python3 tools/screenshot_capture.py --create-grid --output-dir "$OUTPUT" --font-size 12

echo "Generating high-res for documentation..."
python3 tools/screenshot_capture.py --output-dir "${OUTPUT}/hires" --font-size 18 --width 100

echo "Done! Screenshots in $OUTPUT/"
```

### Custom Theme Screenshot

Generate screenshot for a custom theme:

```python
# custom_screenshot.py
from curses_themes import ThemeManager
from tools.screenshot_capture import render_theme_screenshot

# Register your custom theme
ThemeManager.register(MyCustomTheme, 'my-theme')

# Generate screenshot
render_theme_screenshot('my-theme', 'screenshots/my-theme.png')
```

### Automated CI/CD Integration

```yaml
# .github/workflows/screenshots.yml
name: Generate Screenshots

on:
  push:
    paths:
      - 'curses_themes/themes/**'

jobs:
  screenshots:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y python3-pil fonts-dejavu
      - name: Generate screenshots
        run: python3 tools/screenshot_capture.py
      - name: Commit screenshots
        run: |
          git config user.name "Screenshot Bot"
          git config user.email "bot@example.com"
          git add screenshots/*.png
          git commit -m "Update screenshots" || true
          git push
```

## Technical Details

### TerminalRenderer Class

The screenshot generator uses a custom PIL-based terminal emulator:

- **Grid rendering**: 80x24 character grid mapped to pixel coordinates
- **Font handling**: Automatic monospace font detection across distributions
- **Unicode support**: Full box-drawing character set (U+2500-U+257F)
- **Color mapping**: Direct RGB values from theme.get_color_map()
- **Text rendering**: Character-by-character with foreground/background colors
- **Bold simulation**: Font variant selection or synthetic bold rendering

### Output Format

- **Format**: PNG (Portable Network Graphics)
- **Color depth**: 24-bit RGB (true color)
- **Compression**: PNG default (lossless)
- **Transparency**: No alpha channel (opaque backgrounds)
- **Encoding**: UTF-8 metadata for theme names

### Performance

- **Generation time**: ~0.1-0.2 seconds per theme
- **Memory usage**: ~10-20 MB peak per screenshot
- **Disk space**: 20-40 KB per PNG file
- **Parallelization**: Not implemented (single-threaded)

## File Locations

- **Screenshot tool**: `/home/sfloess/Development/github/FlossWare/curses-themes/tools/screenshot_capture.py`
- **Output directory**: `/home/sfloess/Development/github/FlossWare/curses-themes/screenshots/`
- **This README**: `/home/sfloess/Development/github/FlossWare/curses-themes/screenshots/README.md`

## License

All screenshots are licensed under GPL-3.0, same as the curses-themes library.

Copyright (C) 2024 FlossWare

## Contributing

When adding new themes:

1. Add theme class to `curses_themes/themes/`
2. Register in `curses_themes/themes/__init__.py`
3. Run screenshot generator: `python3 tools/screenshot_capture.py`
4. Add screenshot to `THEMES.md` in appropriate section
5. Verify screenshot shows all theme features correctly

For screenshot generation improvements:

- See `tools/screenshot_capture.py` source code
- Test changes with all 10 themes
- Ensure Unicode box-drawing characters render correctly
- Verify 3D effects appear for Theme3D subclasses