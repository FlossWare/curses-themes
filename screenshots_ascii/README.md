# ASCII Theme Screenshots

This directory contains ASCII text-based screenshots of all 10 curses-themes themes.
These are pure text representations of how each theme appears in a terminal.

## Generated Themes

All 10 themes are documented with sample UI layouts showing:

1. **Theme Header** - Name and description
2. **Sample Panel** - Bordered container with buttons and text
3. **UI Elements** - Demonstrates:
   - Normal and focused buttons
   - Text input fields  
   - Selection indicators
   - Semantic color indicators (Success, Error, Warning, Info)
4. **Border Style** - Shows the specific border characters used by each theme
5. **Color Palette** - Lists foreground and background color assignments

## Themes Included

### Modern Themes
- **default** - Classic terminal (white on black)
- **dark** - Modern dark mode aesthetic
- **light** - Bright background with dark text

### Retro/Vintage Themes
- **ti-99-4a** - TI-99/4A home computer (cyan on blue)
- **trs-80** - Tandy/Radio Shack TRS-80 (white on black, monochrome)
- **dos** - MS-DOS / PC-DOS era (white on black)
- **dbase-iii** - Ashton-Tate dBASE III (cyan on black)
- **dbase-iv** - Ashton-Tate/Borland dBASE IV (blue interface)

### 3D Themes  
- **borland-3d** - Borland Turbo Vision 3D (beveled, drop shadows)
- **dbase-iv-3d** - dBASE IV 3D (windowed Control Center)

## File Format

Each file is a fixed-width ASCII text file (80 chars x 25 lines) that can be:
- Viewed directly in any text editor
- Displayed in terminals for documentation
- Captured and converted to images using terminal screenshot tools
- Included in markdown/documentation as code blocks

## Viewing

To view a theme screenshot:

```bash
cat borland-3d.txt
```

Or pipe to your pager:

```bash
less default.txt
```

## Generation

These screenshots were generated using the `generate_screenshots_headless.py`
script in the `examples/` directory. To regenerate:

```bash
python3 examples/generate_screenshots_headless.py --output-dir screenshots_ascii/
```

## Displaying in Documentation

For Markdown documentation, use code blocks:

\`\`\`
[Include content of theme screenshot]
\`\`\`

## Future Enhancements

Potential improvements:
- Add color ANSI codes to demonstrate actual terminal colors
- Generate side-by-side theme comparison
- Create HTML/CSS versions from ASCII art
- Add screenshot metadata files (JSON with color values, border chars, etc.)

## License

These screenshots are generated from the curses-themes library and inherit
the same license as the parent project.
