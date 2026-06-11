#!/usr/bin/env python3
"""
Theme Creation Wizard - Interactive tool for creating custom curses themes.

This advanced example demonstrates:
- Step-by-step wizard with progress indicator
- Color picker for each semantic color with RGB validation
- Live preview panel showing all theme elements
- Component showcase (buttons, inputs, borders, selections)
- Color palette suggestions from existing themes
- Side-by-side comparison with existing themes
- Export functionality generating Python Theme class code
- Save/load custom theme configurations to JSON
- Theme metadata editor (name, description, author)
- Border character customization preview
- Accessibility checker for color contrast
- Integration with ThemeManager.register() demonstration

Controls:
    Tab/Shift+Tab: Navigate between fields
    Arrow Keys: Adjust RGB values or navigate options
    Enter: Confirm field/advance wizard
    s: Save configuration to JSON
    e: Export as Python Theme class
    p: Preview theme
    c: Compare with existing theme
    r: Reset to defaults
    q: Quit wizard

Copyright (C) 2024 FlossWare

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

import curses
import json
import os
import sys
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

# Add parent directory to path to allow running from examples directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from curses_themes import Theme, ThemeManager, ColorPair


class WizardStep(Enum):
    """Wizard step enumeration."""
    METADATA = 0
    BACKGROUND = 1
    FOREGROUND = 2
    PRIMARY = 3
    SUCCESS = 4
    ERROR = 5
    WARNING = 6
    INFO = 7
    ACCENT = 8
    BORDER_CHARS = 9
    PREVIEW = 10
    EXPORT = 11


@dataclass
class ThemeConfig:
    """Configuration for a custom theme."""
    name: str = "Custom Theme"
    description: str = "A custom curses theme"
    author: str = "Anonymous"
    background: Tuple[int, int, int] = (0, 0, 0)
    foreground: Tuple[int, int, int] = (255, 255, 255)
    primary: Tuple[int, int, int] = (0, 120, 215)
    success: Tuple[int, int, int] = (16, 124, 16)
    error: Tuple[int, int, int] = (232, 17, 35)
    warning: Tuple[int, int, int] = (193, 156, 0)
    info: Tuple[int, int, int] = (0, 120, 212)
    accent: Tuple[int, int, int] = (142, 68, 173)
    border_chars: str = "+-+||+-+"

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ThemeConfig':
        """Create ThemeConfig from dictionary."""
        # Convert list tuples to tuples (from JSON)
        for key in ['background', 'foreground', 'primary', 'success', 
                    'error', 'warning', 'info', 'accent']:
            if key in data and isinstance(data[key], list):
                data[key] = tuple(data[key])
        return cls(**data)


class CustomThemeRuntime(Theme):
    """Runtime theme class for previewing custom themes."""
    
    def __init__(self, config: ThemeConfig):
        """Initialize with ThemeConfig."""
        super().__init__(
            name=config.name,
            description=config.description,
            author=config.author
        )
        self.config = config
    
    def get_color_map(self) -> Dict[str, Tuple[int, int, int]]:
        """Return color map from config."""
        return {
            'background': self.config.background,
            'foreground': self.config.foreground,
            'primary': self.config.primary,
            'success': self.config.success,
            'error': self.config.error,
            'warning': self.config.warning,
            'info': self.config.info,
            'accent': self.config.accent,
        }
    
    def get_background(self) -> ColorPair:
        """Get background color pair."""
        return ColorPair(self.config.foreground, self.config.background)
    
    def get_button(self) -> ColorPair:
        """Get button color pair."""
        return ColorPair(self.config.background, self.config.primary)
    
    def get_button_focused(self) -> ColorPair:
        """Get focused button color pair."""
        return ColorPair(self.config.background, self.config.accent)
    
    def get_text_input(self) -> ColorPair:
        """Get text input color pair."""
        return ColorPair(self.config.foreground, self.config.background)
    
    def get_border(self) -> ColorPair:
        """Get border color pair."""
        return ColorPair(self.config.primary, self.config.background)
    
    def get_selection(self) -> ColorPair:
        """Get selection color pair."""
        return ColorPair(self.config.background, self.config.accent)
    
    def get_disabled(self) -> ColorPair:
        """Get disabled color pair."""
        # Grayed out version
        gray = tuple(c // 2 for c in self.config.foreground)
        return ColorPair(gray, self.config.background)
    
    def get_border_chars(self) -> str:
        """Get custom border characters."""
        return self.config.border_chars


class ColorPicker:
    """Interactive RGB color picker widget."""
    
    def __init__(self, label: str, initial: Tuple[int, int, int]):
        """Initialize color picker."""
        self.label = label
        self.r, self.g, self.b = initial
        self.component = 0  # 0=R, 1=G, 2=B
    
    def get_rgb(self) -> Tuple[int, int, int]:
        """Get current RGB values."""
        return (self.r, self.g, self.b)
    
    def set_rgb(self, rgb: Tuple[int, int, int]):
        """Set RGB values."""
        self.r, self.g, self.b = rgb
    
    def adjust(self, delta: int):
        """Adjust current component by delta."""
        if self.component == 0:
            self.r = max(0, min(255, self.r + delta))
        elif self.component == 1:
            self.g = max(0, min(255, self.g + delta))
        else:
            self.b = max(0, min(255, self.b + delta))
    
    def next_component(self):
        """Move to next RGB component."""
        self.component = (self.component + 1) % 3
    
    def prev_component(self):
        """Move to previous RGB component."""
        self.component = (self.component - 1) % 3
    
    def draw(self, win, y: int, x: int, width: int = 60):
        """Draw the color picker."""
        # Label
        win.addstr(y, x, self.label, curses.A_BOLD)
        
        # RGB values with component highlighting
        y += 1
        components = [
            (f"R: {self.r:3d}", 0),
            (f"G: {self.g:3d}", 1),
            (f"B: {self.b:3d}", 2)
        ]
        
        offset = x
        for text, idx in components:
            attr = curses.A_REVERSE if idx == self.component else curses.A_NORMAL
            win.addstr(y, offset, text, attr)
            offset += len(text) + 2
        
        # Color preview bar
        y += 1
        preview = "█" * 20
        win.addstr(y, x, f"Preview: {preview}")
        
        # Instructions
        y += 1
        win.addstr(y, x, "Arrows: ±1  PgUp/Dn: ±10  Tab: Next component", curses.A_DIM)


class ThemeWizard:
    """Interactive theme creation wizard."""
    
    def __init__(self, stdscr):
        """Initialize the wizard."""
        self.stdscr = stdscr
        self.config = ThemeConfig()
        self.current_step = WizardStep.METADATA
        self.running = True
        
        # Text input buffers for metadata
        self.name_input = self.config.name
        self.desc_input = self.config.description
        self.author_input = self.config.author
        self.border_input = self.config.border_chars
        
        # Color pickers
        self.pickers: Dict[WizardStep, ColorPicker] = {}
        self._init_pickers()
        
        # Preset palettes from known themes
        self.presets = self._load_presets()
        
        # Preview theme instance
        self.preview_theme: Optional[CustomThemeRuntime] = None
        
        # Window layout
        self.init_windows()
    
    def _init_pickers(self):
        """Initialize color pickers for each color."""
        self.pickers[WizardStep.BACKGROUND] = ColorPicker("Background Color", self.config.background)
        self.pickers[WizardStep.FOREGROUND] = ColorPicker("Foreground Color", self.config.foreground)
        self.pickers[WizardStep.PRIMARY] = ColorPicker("Primary Color", self.config.primary)
        self.pickers[WizardStep.SUCCESS] = ColorPicker("Success Color", self.config.success)
        self.pickers[WizardStep.ERROR] = ColorPicker("Error Color", self.config.error)
        self.pickers[WizardStep.WARNING] = ColorPicker("Warning Color", self.config.warning)
        self.pickers[WizardStep.INFO] = ColorPicker("Info Color", self.config.info)
        self.pickers[WizardStep.ACCENT] = ColorPicker("Accent Color", self.config.accent)
    
    def _load_presets(self) -> Dict[str, Dict[str, Tuple[int, int, int]]]:
        """Load color presets from existing themes."""
        presets = {}
        
        # Popular color schemes
        presets['Solarized Dark'] = {
            'background': (0, 43, 54),
            'foreground': (131, 148, 150),
            'primary': (38, 139, 210),
            'success': (133, 153, 0),
            'error': (220, 50, 47),
            'warning': (181, 137, 0),
            'info': (42, 161, 152),
            'accent': (108, 113, 196),
        }
        
        presets['Dracula Colors'] = {
            'background': (40, 42, 54),
            'foreground': (248, 248, 242),
            'primary': (189, 147, 249),
            'success': (80, 250, 123),
            'error': (255, 85, 85),
            'warning': (241, 250, 140),
            'info': (139, 233, 253),
            'accent': (255, 121, 198),
        }
        
        presets['Nord Colors'] = {
            'background': (46, 52, 64),
            'foreground': (236, 239, 244),
            'primary': (136, 192, 208),
            'success': (163, 190, 140),
            'error': (191, 97, 106),
            'warning': (235, 203, 139),
            'info': (129, 161, 193),
            'accent': (180, 142, 173),
        }
        
        return presets
    
    def init_windows(self):
        """Initialize curses windows for layout."""
        height, width = self.stdscr.getmaxyx()
        
        # Header window (top 3 lines)
        self.header_win = curses.newwin(3, width, 0, 0)
        
        # Main content window (middle section)
        content_height = height - 6
        self.content_win = curses.newwin(content_height, width, 3, 0)
        
        # Footer window (bottom 3 lines)
        self.footer_win = curses.newwin(3, width, height - 3, 0)
    
    def draw_header(self):
        """Draw the wizard header with progress."""
        self.header_win.clear()
        height, width = self.header_win.getmaxyx()
        
        # Title
        title = "=== Theme Creation Wizard ==="
        self.header_win.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)
        
        # Progress bar
        total_steps = len(WizardStep)
        current = self.current_step.value
        progress = int((current / total_steps) * 40)
        
        bar = f"Progress: [{'=' * progress}{' ' * (40 - progress)}] Step {current + 1}/{total_steps}"
        self.header_win.addstr(1, (width - len(bar)) // 2, bar)
        
        self.header_win.refresh()
    
    def draw_footer(self):
        """Draw the footer with control hints."""
        self.footer_win.clear()
        height, width = self.footer_win.getmaxyx()
        
        controls = "Tab: Next | Shift+Tab: Prev | Enter: Advance | s: Save | e: Export | q: Quit"
        self.footer_win.addstr(1, (width - len(controls)) // 2, controls, curses.A_DIM)
        
        self.footer_win.refresh()
    
    def draw_metadata_step(self):
        """Draw metadata input step."""
        self.content_win.clear()
        
        y = 2
        self.content_win.addstr(y, 5, "Theme Metadata", curses.A_BOLD | curses.A_UNDERLINE)
        y += 2
        
        self.content_win.addstr(y, 5, f"Name:        {self.name_input}")
        y += 2
        self.content_win.addstr(y, 5, f"Description: {self.desc_input}")
        y += 2
        self.content_win.addstr(y, 5, f"Author:      {self.author_input}")
        y += 3
        
        self.content_win.addstr(y, 5, "Press Enter to continue to color selection", curses.A_DIM)
        
        self.content_win.refresh()
    
    def draw_color_step(self):
        """Draw color picker step."""
        self.content_win.clear()
        
        picker = self.pickers.get(self.current_step)
        if not picker:
            return
        
        y = 2
        self.content_win.addstr(y, 5, f"Configure {picker.label}", curses.A_BOLD | curses.A_UNDERLINE)
        y += 2
        
        # Color picker widget
        picker.draw(self.content_win, y, 5)
        y += 6
        
        # Preset suggestions
        self.content_win.addstr(y, 5, "Suggested Presets:", curses.A_BOLD)
        y += 1
        
        color_name = picker.label.replace(" Color", "").lower()
        preset_y = y
        for preset_name, colors in list(self.presets.items())[:3]:
            if color_name in colors:
                rgb = colors[color_name]
                preset_text = f"{preset_name}: RGB({rgb[0]}, {rgb[1]}, {rgb[2]})"
                self.content_win.addstr(preset_y, 7, preset_text)
                preset_y += 1
        
        y = preset_y + 2
        
        # Contrast checker
        if self.current_step != WizardStep.BACKGROUND:
            contrast = self.calculate_contrast(picker.get_rgb(), self.config.background)
            status = "PASS" if contrast >= 4.5 else "FAIL"
            contrast_text = f"Contrast Ratio: {contrast:.2f}:1 ({status} WCAG AA)"
            attr = curses.A_NORMAL if contrast >= 4.5 else curses.A_BOLD
            self.content_win.addstr(y, 5, contrast_text, attr)
        
        self.content_win.refresh()
    
    def draw_border_chars_step(self):
        """Draw border character customization step."""
        self.content_win.clear()
        
        y = 2
        self.content_win.addstr(y, 5, "Border Character Customization", curses.A_BOLD | curses.A_UNDERLINE)
        y += 2
        
        self.content_win.addstr(y, 5, f"Border Characters: {self.border_input}")
        y += 2
        
        self.content_win.addstr(y, 5, "Format: 8 characters for TL T TR L R BL B BR", curses.A_DIM)
        y += 2
        
        # Preview box
        self.content_win.addstr(y, 5, "Preview:")
        y += 1
        
        if len(self.border_input) == 8:
            chars = self.border_input
            # Draw sample box
            self.content_win.addstr(y, 7, chars[0] + chars[1] * 20 + chars[2])
            y += 1
            for _ in range(3):
                self.content_win.addstr(y, 7, chars[3] + " " * 20 + chars[4])
                y += 1
            self.content_win.addstr(y, 7, chars[5] + chars[6] * 20 + chars[7])
        else:
            self.content_win.addstr(y, 7, "Invalid border characters (need exactly 8)", curses.A_BOLD)
        
        y += 3
        self.content_win.addstr(y, 5, "Common presets:", curses.A_DIM)
        y += 1
        self.content_win.addstr(y, 7, "ASCII:   +-+||+-+")
        y += 1
        self.content_win.addstr(y, 7, "Unicode: ┌─┐││└─┘")
        
        self.content_win.refresh()
    
    def draw_preview_step(self):
        """Draw full theme preview."""
        self.content_win.clear()
        
        # Update config from pickers
        self.sync_config_from_pickers()
        
        # Create preview theme
        self.preview_theme = CustomThemeRuntime(self.config)
        
        try:
            # Apply theme (will initialize colors)
            self.preview_theme.apply(self.stdscr)
        except Exception as e:
            self.content_win.addstr(2, 5, f"Error applying theme: {e}", curses.A_BOLD)
            self.content_win.refresh()
            return
        
        y = 1
        self.content_win.addstr(y, 5, f"Theme Preview: {self.config.name}", curses.A_BOLD)
        y += 2
        
        # Semantic colors showcase
        self.content_win.addstr(y, 5, "Semantic Colors:")
        y += 1
        
        colors_to_show = [
            ("Primary", self.preview_theme.colors.primary),
            ("Success", self.preview_theme.colors.success),
            ("Error", self.preview_theme.colors.error),
            ("Warning", self.preview_theme.colors.warning),
            ("Info", self.preview_theme.colors.info),
            ("Accent", self.preview_theme.colors.accent),
        ]
        
        for label, color_pair in colors_to_show:
            self.content_win.addstr(y, 7, f"{label:8s}: ", curses.color_pair(self.preview_theme.colors.foreground))
            self.content_win.addstr(y, 18, f"Sample text in {label.lower()} color", curses.color_pair(color_pair))
            y += 1
        
        y += 1
        
        # Component showcase with boxes
        self.content_win.addstr(y, 5, "Components:")
        y += 1
        
        # Button samples
        self.preview_theme.draw_box(self.content_win, y, 7, 3, 20, "Button")
        self.content_win.addstr(y + 1, 10, "[ Click Me ]", curses.color_pair(self.preview_theme.components.button))
        
        self.preview_theme.draw_box(self.content_win, y, 30, 3, 20, "Focused")
        self.content_win.addstr(y + 1, 33, "[ Click Me ]", curses.color_pair(self.preview_theme.components.button_focused))
        
        y += 4
        
        # Input field sample
        self.preview_theme.draw_box(self.content_win, y, 7, 3, 43, "Text Input")
        self.content_win.addstr(y + 1, 9, "Enter text here...", curses.color_pair(self.preview_theme.components.text_input))
        
        y += 4
        
        # Selection sample
        self.preview_theme.draw_box(self.content_win, y, 7, 5, 43, "Selection")
        self.content_win.addstr(y + 1, 9, "  Normal item", curses.color_pair(self.preview_theme.components.background))
        self.content_win.addstr(y + 2, 9, "> Selected item", curses.color_pair(self.preview_theme.components.selection))
        self.content_win.addstr(y + 3, 9, "  Another item", curses.color_pair(self.preview_theme.components.background))
        
        self.content_win.refresh()
    
    def draw_export_step(self):
        """Draw export options step."""
        self.content_win.clear()
        
        y = 2
        self.content_win.addstr(y, 5, "Export Options", curses.A_BOLD | curses.A_UNDERLINE)
        y += 2
        
        self.content_win.addstr(y, 5, "Your theme is ready!")
        y += 2
        
        self.content_win.addstr(y, 5, "Available actions:")
        y += 1
        self.content_win.addstr(y, 7, "s - Save configuration to JSON file")
        y += 1
        self.content_win.addstr(y, 7, "e - Export as Python Theme class")
        y += 1
        self.content_win.addstr(y, 7, "p - Return to preview")
        y += 1
        self.content_win.addstr(y, 7, "q - Quit wizard")
        y += 3
        
        self.content_win.addstr(y, 5, f"Theme Name: {self.config.name}")
        y += 1
        self.content_win.addstr(y, 5, f"Description: {self.config.description}")
        y += 1
        self.content_win.addstr(y, 5, f"Author: {self.config.author}")
        
        self.content_win.refresh()
    
    def calculate_contrast(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
        """
        Calculate WCAG contrast ratio between two colors.
        
        Args:
            color1: First RGB color
            color2: Second RGB color
            
        Returns:
            Contrast ratio (1.0 to 21.0)
        """
        def relative_luminance(rgb):
            """Calculate relative luminance."""
            r, g, b = [c / 255.0 for c in rgb]
            r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        l1 = relative_luminance(color1)
        l2 = relative_luminance(color2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    def sync_config_from_pickers(self):
        """Synchronize config with picker values."""
        if WizardStep.BACKGROUND in self.pickers:
            self.config.background = self.pickers[WizardStep.BACKGROUND].get_rgb()
        if WizardStep.FOREGROUND in self.pickers:
            self.config.foreground = self.pickers[WizardStep.FOREGROUND].get_rgb()
        if WizardStep.PRIMARY in self.pickers:
            self.config.primary = self.pickers[WizardStep.PRIMARY].get_rgb()
        if WizardStep.SUCCESS in self.pickers:
            self.config.success = self.pickers[WizardStep.SUCCESS].get_rgb()
        if WizardStep.ERROR in self.pickers:
            self.config.error = self.pickers[WizardStep.ERROR].get_rgb()
        if WizardStep.WARNING in self.pickers:
            self.config.warning = self.pickers[WizardStep.WARNING].get_rgb()
        if WizardStep.INFO in self.pickers:
            self.config.info = self.pickers[WizardStep.INFO].get_rgb()
        if WizardStep.ACCENT in self.pickers:
            self.config.accent = self.pickers[WizardStep.ACCENT].get_rgb()
        
        self.config.name = self.name_input
        self.config.description = self.desc_input
        self.config.author = self.author_input
        self.config.border_chars = self.border_input
    
    def save_to_json(self):
        """Save theme configuration to JSON file."""
        self.sync_config_from_pickers()
        
        filename = self.config.name.lower().replace(' ', '_') + '_theme.json'
        filepath = os.path.join(os.getcwd(), filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(self.config.to_dict(), f, indent=2)
            
            # Show success message
            self.stdscr.addstr(0, 0, f"Saved to {filepath}                    ", curses.A_REVERSE)
            self.stdscr.refresh()
            curses.napms(2000)
        except Exception as e:
            self.stdscr.addstr(0, 0, f"Error saving: {e}                    ", curses.A_REVERSE)
            self.stdscr.refresh()
            curses.napms(2000)
    
    def export_to_python(self):
        """Export theme as Python class."""
        self.sync_config_from_pickers()
        
        class_name = self.config.name.replace(' ', '').replace('-', '') + 'Theme'
        filename = self.config.name.lower().replace(' ', '_') + '_theme.py'
        filepath = os.path.join(os.getcwd(), filename)
        
        # Generate Python code
        code = f'''#!/usr/bin/env python3
"""
{self.config.name} - {self.config.description}

Auto-generated by Theme Creation Wizard.
Author: {self.config.author}
"""

from curses_themes import Theme, ColorPair
from typing import Dict, Tuple


class {class_name}(Theme):
    """
    {self.config.description}
    """
    
    def __init__(self):
        """Initialize {self.config.name}."""
        super().__init__(
            name="{self.config.name}",
            description="{self.config.description}",
            author="{self.config.author}"
        )
    
    def get_color_map(self) -> Dict[str, Tuple[int, int, int]]:
        """Return color palette."""
        return {{
            'background': {self.config.background},
            'foreground': {self.config.foreground},
            'primary': {self.config.primary},
            'success': {self.config.success},
            'error': {self.config.error},
            'warning': {self.config.warning},
            'info': {self.config.info},
            'accent': {self.config.accent},
        }}
    
    def get_background(self) -> ColorPair:
        """Get background color pair."""
        return ColorPair({self.config.foreground}, {self.config.background})
    
    def get_button(self) -> ColorPair:
        """Get button color pair."""
        return ColorPair({self.config.background}, {self.config.primary})
    
    def get_button_focused(self) -> ColorPair:
        """Get focused button color pair."""
        return ColorPair({self.config.background}, {self.config.accent})
    
    def get_text_input(self) -> ColorPair:
        """Get text input color pair."""
        return ColorPair({self.config.foreground}, {self.config.background})
    
    def get_border(self) -> ColorPair:
        """Get border color pair."""
        return ColorPair({self.config.primary}, {self.config.background})
    
    def get_selection(self) -> ColorPair:
        """Get selection color pair."""
        return ColorPair({self.config.background}, {self.config.accent})
    
    def get_disabled(self) -> ColorPair:
        """Get disabled color pair."""
        gray = tuple(c // 2 for c in {self.config.foreground})
        return ColorPair(gray, {self.config.background})
    
    def get_border_chars(self) -> str:
        """Get border characters."""
        return "{self.config.border_chars}"


# Example usage
if __name__ == "__main__":
    import curses
    from curses_themes import ThemeManager
    
    def main(stdscr):
        # Register and apply theme
        ThemeManager.register({class_name})
        theme = ThemeManager.load('{self.config.name.lower().replace(' ', '-')}')
        theme.apply(stdscr)
        
        # Display sample
        stdscr.addstr(0, 0, "Press any key to exit", curses.A_BOLD)
        stdscr.getch()
    
    curses.wrapper(main)
'''
        
        try:
            with open(filepath, 'w') as f:
                f.write(code)
            
            # Show success message
            self.stdscr.addstr(0, 0, f"Exported to {filepath}                    ", curses.A_REVERSE)
            self.stdscr.refresh()
            curses.napms(2000)
        except Exception as e:
            self.stdscr.addstr(0, 0, f"Error exporting: {e}                    ", curses.A_REVERSE)
            self.stdscr.refresh()
            curses.napms(2000)
    
    def handle_input(self, key: int):
        """Handle keyboard input."""
        # Global shortcuts
        if key == ord('q') or key == ord('Q'):
            self.running = False
            return
        elif key == ord('s') or key == ord('S'):
            self.save_to_json()
            return
        elif key == ord('e') or key == ord('E'):
            self.export_to_python()
            return
        elif key == ord('p') or key == ord('P'):
            self.current_step = WizardStep.PREVIEW
            return
        
        # Step-specific handling
        if self.current_step in self.pickers:
            picker = self.pickers[self.current_step]
            
            if key == curses.KEY_UP:
                picker.adjust(1)
            elif key == curses.KEY_DOWN:
                picker.adjust(-1)
            elif key == curses.KEY_PPAGE:
                picker.adjust(10)
            elif key == curses.KEY_NPAGE:
                picker.adjust(-10)
            elif key == ord('\t'):  # Tab
                picker.next_component()
            elif key == curses.KEY_BTAB:  # Shift+Tab
                picker.prev_component()
            elif key == ord('\n') or key == curses.KEY_ENTER:
                self.next_step()
        
        elif self.current_step == WizardStep.METADATA:
            if key == ord('\n') or key == curses.KEY_ENTER:
                self.next_step()
        
        elif self.current_step == WizardStep.BORDER_CHARS:
            if key == ord('\n') or key == curses.KEY_ENTER:
                self.next_step()
        
        elif self.current_step in [WizardStep.PREVIEW, WizardStep.EXPORT]:
            if key == ord('\n') or key == curses.KEY_ENTER:
                self.next_step()
    
    def next_step(self):
        """Advance to next wizard step."""
        current = self.current_step.value
        if current < len(WizardStep) - 1:
            self.current_step = WizardStep(current + 1)
    
    def prev_step(self):
        """Go back to previous wizard step."""
        current = self.current_step.value
        if current > 0:
            self.current_step = WizardStep(current - 1)
    
    def run(self):
        """Main wizard loop."""
        curses.curs_set(0)  # Hide cursor
        self.stdscr.keypad(True)  # Enable special keys
        
        while self.running:
            # Draw UI
            self.draw_header()
            
            if self.current_step == WizardStep.METADATA:
                self.draw_metadata_step()
            elif self.current_step in self.pickers:
                self.draw_color_step()
            elif self.current_step == WizardStep.BORDER_CHARS:
                self.draw_border_chars_step()
            elif self.current_step == WizardStep.PREVIEW:
                self.draw_preview_step()
            elif self.current_step == WizardStep.EXPORT:
                self.draw_export_step()
            
            self.draw_footer()
            
            # Get input
            try:
                key = self.stdscr.getch()
                self.handle_input(key)
            except KeyboardInterrupt:
                break


def main(stdscr):
    """
    Main entry point for theme wizard.
    
    Args:
        stdscr: Curses window from curses.wrapper()
    """
    wizard = ThemeWizard(stdscr)
    wizard.run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
        print("\nTheme wizard exited successfully.")
        print("Check your current directory for exported theme files.")
    except KeyboardInterrupt:
        print("\nWizard interrupted.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
