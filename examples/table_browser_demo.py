#!/usr/bin/env python3
"""
Database Table Browser - Advanced Interactive Demo

An interactive database-style table viewer with pagination, sorting, filtering,
and column resizing. Demonstrates how to build data-rich interfaces with themed
tables, headers, and navigation. Perfect for showcasing dBASE retro themes with
authentic database UI patterns.

Features:
    - Paginated table view with alternating row colors
    - Column headers with sort indicators (themed arrows/symbols)
    - Status bar showing record count, page numbers, filter status
    - Column highlighting on hover/selection
    - Search/filter bar with themed input fields
    - Navigation controls (Page Up/Down, Home/End, Arrow keys)
    - Detail view panel showing selected record in themed box
    - Support for multiple tables/views with tab switching
    - Live theme switching to compare retro (dBASE, DOS) vs modern themes
    - SQL-style command input area with syntax hints

Controls:
    Arrow Keys      - Navigate cells
    Page Up/Down    - Navigate pages
    Home/End        - Jump to first/last record
    Tab/Shift+Tab   - Switch between tables
    Enter           - Toggle detail view
    /               - Enter filter/search mode
    :               - Enter SQL command mode
    s               - Cycle sort column
    r               - Reverse sort order
    t               - Switch theme
    q               - Quit
    Esc             - Cancel input/close detail view

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
from curses import panel
from curses_themes import ThemeManager
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import random


# Sample database tables for demonstration
def generate_employees_table(count: int = 100) -> List[Dict[str, Any]]:
    """Generate sample employee data."""
    first_names = [
        "John",
        "Jane",
        "Bob",
        "Alice",
        "Charlie",
        "Diana",
        "Eve",
        "Frank",
        "Grace",
        "Henry",
        "Iris",
        "Jack",
        "Karen",
        "Leo",
        "Mary",
        "Nancy",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Rodriguez",
        "Martinez",
        "Hernandez",
        "Lopez",
        "Wilson",
    ]
    departments = [
        "Engineering",
        "Sales",
        "Marketing",
        "HR",
        "Finance",
        "Operations",
        "IT",
    ]
    titles = [
        "Manager",
        "Senior",
        "Junior",
        "Lead",
        "Specialist",
        "Analyst",
        "Director",
    ]

    employees = []
    base_date = datetime(2010, 1, 1)

    for i in range(count):
        emp_id = 1000 + i
        first = random.choice(first_names)
        last = random.choice(last_names)
        dept = random.choice(departments)
        title = random.choice(titles)
        hire_date = base_date + timedelta(days=random.randint(0, 5000))
        salary = random.randint(40000, 150000)
        active = random.choice([True, True, True, False])  # 75% active

        employees.append(
            {
                "ID": emp_id,
                "First Name": first,
                "Last Name": last,
                "Department": dept,
                "Title": title,
                "Hire Date": hire_date.strftime("%Y-%m-%d"),
                "Salary": f"${salary:,}",
                "Active": "Yes" if active else "No",
            }
        )

    return employees


def generate_customers_table(count: int = 80) -> List[Dict[str, Any]]:
    """Generate sample customer data."""
    companies = [
        "Acme Corp",
        "TechStart Inc",
        "Global Solutions",
        "DataFlow LLC",
        "Innovate Systems",
        "Future Tech",
        "Digital Dynamics",
        "Smart Analytics",
    ]
    cities = [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego",
        "Dallas",
        "San Jose",
    ]
    states = ["NY", "CA", "IL", "TX", "AZ", "PA", "FL", "OH"]

    customers = []

    for i in range(count):
        cust_id = 5000 + i
        company = f"{random.choice(companies)} #{i + 1}"
        city = random.choice(cities)
        state = random.choice(states)
        balance = random.randint(-5000, 50000)
        status = random.choice(["Active", "Inactive", "Pending", "Suspended"])

        customers.append(
            {
                "ID": cust_id,
                "Company": company,
                "City": city,
                "State": state,
                "Balance": f"${balance:,}",
                "Status": status,
                "Records": random.randint(0, 500),
            }
        )

    return customers


def generate_products_table(count: int = 60) -> List[Dict[str, Any]]:
    """Generate sample product inventory data."""
    categories = ["Electronics", "Furniture", "Office Supplies", "Software", "Hardware"]
    products = [
        "Monitor",
        "Keyboard",
        "Mouse",
        "Desk",
        "Chair",
        "Laptop",
        "Tablet",
        "Printer",
        "Scanner",
        "Headset",
        "Webcam",
        "Router",
    ]

    inventory = []

    for i in range(count):
        prod_id = f"P{1000 + i}"
        product = f"{random.choice(products)} Model {chr(65 + random.randint(0, 25))}"
        category = random.choice(categories)
        stock = random.randint(0, 1000)
        price = random.randint(10, 5000)
        reorder = stock < 100

        inventory.append(
            {
                "SKU": prod_id,
                "Product": product,
                "Category": category,
                "In Stock": stock,
                "Unit Price": f"${price:.2f}",
                "Reorder": "YES" if reorder else "NO",
            }
        )

    return inventory


class TableBrowser:
    """Advanced database table browser with full features."""

    def __init__(self, stdscr):
        """Initialize the table browser."""
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()

        # Initialize curses settings
        curses.curs_set(0)  # Hide cursor
        stdscr.keypad(True)  # Enable keypad for special keys
        stdscr.timeout(100)  # Non-blocking input with 100ms timeout

        # Theme management
        self.themes = ["dbase-iii", "dbase-iv", "dos", "dark", "light"]
        self.current_theme_idx = 0
        self.theme = None
        self.load_theme()

        # Table data
        self.tables = {
            "EMPLOYEES": {
                "data": generate_employees_table(),
                "columns": [
                    "ID",
                    "First Name",
                    "Last Name",
                    "Department",
                    "Title",
                    "Hire Date",
                    "Salary",
                    "Active",
                ],
            },
            "CUSTOMERS": {
                "data": generate_customers_table(),
                "columns": [
                    "ID",
                    "Company",
                    "City",
                    "State",
                    "Balance",
                    "Status",
                    "Records",
                ],
            },
            "PRODUCTS": {
                "data": generate_products_table(),
                "columns": [
                    "SKU",
                    "Product",
                    "Category",
                    "In Stock",
                    "Unit Price",
                    "Reorder",
                ],
            },
        }
        self.table_names = list(self.tables.keys())
        self.current_table_idx = 0

        # View state
        self.current_row = 0  # Selected row in current view
        self.current_col = 0  # Selected column
        self.top_row = 0  # First visible row (for scrolling)
        self.rows_per_page = 10  # Will be adjusted based on screen size

        # Sorting
        self.sort_column = None
        self.sort_reverse = False

        # Filtering
        self.filter_text = ""
        self.filtered_data = None

        # UI state
        self.show_detail = False
        self.input_mode = None  # None, 'filter', or 'command'
        self.input_buffer = ""
        self.status_message = "Ready"

        # Windows and panels for advanced UI
        self.create_windows()

    def create_windows(self):
        """Create curses windows and panels for complex UI."""
        # Main table window (most of screen)
        table_height = self.height - 6  # Leave room for header, status, input
        self.table_win = curses.newwin(table_height, self.width, 3, 0)
        self.table_panel = panel.new_panel(self.table_win)

        # Header window (top 3 lines)
        self.header_win = curses.newwin(3, self.width, 0, 0)
        self.header_panel = panel.new_panel(self.header_win)

        # Status bar window (bottom area)
        self.status_win = curses.newwin(2, self.width, self.height - 3, 0)
        self.status_panel = panel.new_panel(self.status_win)

        # Input window (bottom line)
        self.input_win = curses.newwin(1, self.width, self.height - 1, 0)
        self.input_panel = panel.new_panel(self.input_win)

        # Detail view window (popup, created when needed)
        self.detail_win = None
        self.detail_panel = None

        # Update rows per page based on table window height
        self.rows_per_page = table_height - 3  # Subtract header rows

    def load_theme(self):
        """Load and apply the current theme."""
        try:
            theme_name = self.themes[self.current_theme_idx]
            self.theme = ThemeManager.load(theme_name)
            self.theme.apply(self.stdscr)

            # Apply theme to all windows
            if hasattr(self, "table_win"):
                self.theme.apply(self.table_win)
            if hasattr(self, "header_win"):
                self.theme.apply(self.header_win)
            if hasattr(self, "status_win"):
                self.theme.apply(self.status_win)
            if hasattr(self, "input_win"):
                self.theme.apply(self.input_win)

        except Exception as e:
            self.status_message = f"Error loading theme: {e}"

    def get_current_table(self) -> Dict[str, Any]:
        """Get the currently active table."""
        table_name = self.table_names[self.current_table_idx]
        return self.tables[table_name]

    def get_visible_data(self) -> List[Dict[str, Any]]:
        """Get the data to display (filtered and sorted)."""
        table = self.get_current_table()
        data = table["data"]

        # Apply filter if active
        if self.filter_text:
            data = [
                row
                for row in data
                if any(
                    self.filter_text.lower() in str(val).lower() for val in row.values()
                )
            ]
            self.filtered_data = data
        else:
            self.filtered_data = None

        # Apply sorting
        if self.sort_column is not None:
            columns = table["columns"]
            if 0 <= self.sort_column < len(columns):
                col_name = columns[self.sort_column]
                try:
                    data = sorted(
                        data,
                        key=lambda x: str(x.get(col_name, "")),
                        reverse=self.sort_reverse,
                    )
                except Exception:
                    pass  # If sorting fails, keep original order

        return data

    def draw_header(self):
        """Draw the header with title, tabs, and theme info."""
        self.header_win.clear()

        # Title bar (line 0)
        title = "DATABASE TABLE BROWSER"
        theme_info = f"Theme: {self.theme.name}"

        try:
            self.header_win.addstr(
                0,
                2,
                title,
                curses.color_pair(self.theme.components.button_focused) | curses.A_BOLD,
            )
            self.header_win.addstr(
                0,
                self.width - len(theme_info) - 2,
                theme_info,
                curses.color_pair(self.theme.components.foreground),
            )
        except curses.error:
            pass

        # Table tabs (line 1)
        x = 2
        for i, table_name in enumerate(self.table_names):
            if i == self.current_table_idx:
                attr = (
                    curses.color_pair(self.theme.components.selection) | curses.A_BOLD
                )
                tab = f"[{table_name}]"
            else:
                attr = curses.color_pair(self.theme.components.button)
                tab = f" {table_name} "

            try:
                self.header_win.addstr(1, x, tab, attr)
            except curses.error:
                pass
            x += len(tab) + 1

        # Separator line (line 2)
        try:
            self.header_win.addstr(
                2,
                0,
                "=" * (self.width - 1),
                curses.color_pair(self.theme.components.border),
            )
        except curses.error:
            pass

        self.header_win.refresh()

    def draw_table(self):
        """Draw the main table with data."""
        self.table_win.clear()

        table = self.get_current_table()
        columns = table["columns"]
        data = self.get_visible_data()

        # Calculate column widths dynamically
        col_widths = []
        available_width = self.width - 2
        num_cols = len(columns)

        for col in columns:
            # Base width on column name and sample data
            max_width = len(col)
            if data:
                sample_width = max(len(str(row.get(col, ""))) for row in data[:10])
                max_width = max(max_width, min(sample_width, 20))
            col_widths.append(min(max_width + 2, available_width // num_cols))

        # Draw column headers (row 0)
        x = 1
        for i, col in enumerate(columns):
            width = col_widths[i]
            col_text = col[: width - 1].ljust(width - 1)

            # Add sort indicator
            if i == self.sort_column:
                indicator = " v" if self.sort_reverse else " ^"
                col_text = col_text[:-2] + indicator

            # Highlight selected column
            if i == self.current_col:
                attr = (
                    curses.color_pair(self.theme.components.button_focused)
                    | curses.A_BOLD
                )
            else:
                attr = curses.color_pair(self.theme.components.button) | curses.A_BOLD

            try:
                self.table_win.addstr(0, x, col_text, attr)
            except curses.error:
                pass
            x += width

        # Draw separator
        try:
            self.table_win.addstr(
                1,
                0,
                "-" * (self.width - 1),
                curses.color_pair(self.theme.components.border),
            )
        except curses.error:
            pass

        # Draw data rows
        start_idx = self.top_row
        end_idx = min(start_idx + self.rows_per_page, len(data))

        for row_idx in range(start_idx, end_idx):
            row = data[row_idx]
            display_row = row_idx - start_idx + 2  # +2 for header and separator

            # Determine row colors (alternating)
            is_selected = row_idx == self.current_row
            is_even = row_idx % 2 == 0

            if is_selected:
                attr = (
                    curses.color_pair(self.theme.components.selection) | curses.A_BOLD
                )
            elif is_even:
                attr = curses.color_pair(self.theme.components.foreground)
            else:
                # Use text_input color for alternating rows
                attr = curses.color_pair(self.theme.components.text_input)

            # Draw each cell
            x = 1
            for col_idx, col in enumerate(columns):
                width = col_widths[col_idx]
                value = str(row.get(col, ""))[: width - 1].ljust(width - 1)

                # Highlight selected column
                cell_attr = attr
                if col_idx == self.current_col and is_selected:
                    cell_attr = attr | curses.A_REVERSE

                try:
                    self.table_win.addstr(display_row, x, value, cell_attr)
                except curses.error:
                    pass
                x += width

        self.table_win.refresh()

    def draw_status_bar(self):
        """Draw the status bar with record count, page info, and messages."""
        self.status_win.clear()

        data = self.get_visible_data()
        total_records = len(data)
        current_page = (self.top_row // self.rows_per_page) + 1
        total_pages = (total_records + self.rows_per_page - 1) // self.rows_per_page

        # Status line 1: Record info
        record_info = f"Record {self.current_row + 1}/{total_records}"
        page_info = f"Page {current_page}/{total_pages}"

        if self.filter_text:
            original_count = len(self.get_current_table()["data"])
            filter_info = f"Filtered: {total_records}/{original_count}"
        else:
            filter_info = ""

        try:
            self.status_win.addstr(
                0, 2, record_info, curses.color_pair(self.theme.colors.info)
            )
            self.status_win.addstr(
                0, 25, page_info, curses.color_pair(self.theme.colors.info)
            )
            if filter_info:
                self.status_win.addstr(
                    0, 40, filter_info, curses.color_pair(self.theme.colors.warning)
                )
        except curses.error:
            pass

        # Status line 2: Messages and help
        help_text = "t:Theme q:Quit /:Filter s:Sort Enter:Detail"

        try:
            self.status_win.addstr(
                1,
                2,
                self.status_message,
                curses.color_pair(self.theme.components.foreground),
            )
            self.status_win.addstr(
                1,
                self.width - len(help_text) - 2,
                help_text,
                curses.color_pair(self.theme.colors.accent),
            )
        except curses.error:
            pass

        self.status_win.refresh()

    def draw_input_line(self):
        """Draw the input line (filter or command mode)."""
        self.input_win.clear()

        if self.input_mode == "filter":
            prompt = "Filter: "
            text = prompt + self.input_buffer
            try:
                self.input_win.addstr(
                    0, 0, text, curses.color_pair(self.theme.components.text_input)
                )
            except curses.error:
                pass
        elif self.input_mode == "command":
            prompt = "SQL> "
            text = prompt + self.input_buffer
            try:
                self.input_win.addstr(
                    0, 0, text, curses.color_pair(self.theme.colors.success)
                )
            except curses.error:
                pass

        self.input_win.refresh()

    def draw_detail_view(self):
        """Draw a popup detail view for the selected record."""
        if not self.show_detail:
            return

        data = self.get_visible_data()
        if not data or self.current_row >= len(data):
            return

        record = data[self.current_row]
        table = self.get_current_table()

        # Calculate window size
        detail_height = min(len(record) + 4, self.height - 6)
        detail_width = min(60, self.width - 10)
        detail_y = (self.height - detail_height) // 2
        detail_x = (self.width - detail_width) // 2

        # Create detail window if needed
        if self.detail_win is None:
            self.detail_win = curses.newwin(
                detail_height, detail_width, detail_y, detail_x
            )
            self.detail_panel = panel.new_panel(self.detail_win)

        self.detail_win.clear()
        self.theme.apply(self.detail_win)

        # Draw border
        try:
            self.theme.draw_box(
                self.detail_win,
                0,
                0,
                detail_height,
                detail_width,
                title=f"Record Details",
            )
        except Exception:
            # Fallback if draw_box not available
            self.detail_win.border()
            title = "Record Details"
            self.detail_win.addstr(0, (detail_width - len(title)) // 2, title)

        # Draw field data
        y = 2
        for col in table["columns"]:
            if y >= detail_height - 2:
                break

            value = str(record.get(col, ""))
            field_text = f"{col}: {value}"

            if len(field_text) > detail_width - 4:
                field_text = field_text[: detail_width - 7] + "..."

            try:
                self.detail_win.addstr(
                    y,
                    2,
                    col + ":",
                    curses.color_pair(self.theme.components.button) | curses.A_BOLD,
                )
                self.detail_win.addstr(
                    y,
                    2 + len(col) + 2,
                    value,
                    curses.color_pair(self.theme.components.foreground),
                )
            except curses.error:
                pass
            y += 1

        # Instructions
        try:
            self.detail_win.addstr(
                detail_height - 1,
                2,
                "Press Esc or Enter to close",
                curses.color_pair(self.theme.colors.accent),
            )
        except curses.error:
            pass

        panel.update_panels()
        self.detail_win.refresh()

    def handle_input(self, key):
        """Handle keyboard input based on current mode."""
        if self.show_detail:
            # Detail view mode
            if key in [27, ord("\n"), ord("q")]:  # Esc, Enter, q
                self.show_detail = False
                if self.detail_panel:
                    self.detail_panel.hide()
            return

        if self.input_mode:
            # Input mode (filter or command)
            if key == 27:  # Esc
                self.input_mode = None
                self.input_buffer = ""
            elif key in [ord("\n"), curses.KEY_ENTER]:
                if self.input_mode == "filter":
                    self.filter_text = self.input_buffer
                    self.current_row = 0
                    self.top_row = 0
                    self.status_message = f"Filter applied: '{self.filter_text}'"
                elif self.input_mode == "command":
                    self.status_message = f"SQL: {self.input_buffer} (demo mode)"
                self.input_mode = None
                self.input_buffer = ""
            elif key in [curses.KEY_BACKSPACE, 127, 8]:
                self.input_buffer = self.input_buffer[:-1]
            elif 32 <= key <= 126:  # Printable characters
                self.input_buffer += chr(key)
            return

        # Normal navigation mode
        data = self.get_visible_data()
        table = self.get_current_table()

        if key == ord("q"):
            return False  # Signal to quit

        elif key == ord("t"):
            # Switch theme
            self.current_theme_idx = (self.current_theme_idx + 1) % len(self.themes)
            self.load_theme()
            self.status_message = f"Theme: {self.theme.name}"

        elif key == ord("/"):
            # Enter filter mode
            self.input_mode = "filter"
            self.input_buffer = self.filter_text

        elif key == ord(":"):
            # Enter command mode
            self.input_mode = "command"
            self.input_buffer = ""

        elif key == ord("s"):
            # Cycle sort column
            num_cols = len(table["columns"])
            if self.sort_column is None:
                self.sort_column = 0
            else:
                self.sort_column = (self.sort_column + 1) % num_cols
            self.status_message = f"Sort by: {table['columns'][self.sort_column]}"

        elif key == ord("r"):
            # Reverse sort order
            self.sort_reverse = not self.sort_reverse
            order = "DESC" if self.sort_reverse else "ASC"
            self.status_message = f"Sort order: {order}"

        elif key in [ord("\n"), curses.KEY_ENTER]:
            # Toggle detail view
            self.show_detail = True

        elif key == ord("\t"):
            # Next table
            self.current_table_idx = (self.current_table_idx + 1) % len(
                self.table_names
            )
            self.current_row = 0
            self.top_row = 0
            self.current_col = 0
            self.filter_text = ""
            self.sort_column = None
            self.status_message = f"Table: {self.table_names[self.current_table_idx]}"

        elif key == curses.KEY_BTAB:  # Shift+Tab
            # Previous table
            self.current_table_idx = (self.current_table_idx - 1) % len(
                self.table_names
            )
            self.current_row = 0
            self.top_row = 0
            self.current_col = 0
            self.filter_text = ""
            self.sort_column = None
            self.status_message = f"Table: {self.table_names[self.current_table_idx]}"

        # Navigation keys
        elif key == curses.KEY_UP:
            if self.current_row > 0:
                self.current_row -= 1
                if self.current_row < self.top_row:
                    self.top_row = self.current_row

        elif key == curses.KEY_DOWN:
            if self.current_row < len(data) - 1:
                self.current_row += 1
                if self.current_row >= self.top_row + self.rows_per_page:
                    self.top_row = self.current_row - self.rows_per_page + 1

        elif key == curses.KEY_LEFT:
            if self.current_col > 0:
                self.current_col -= 1

        elif key == curses.KEY_RIGHT:
            if self.current_col < len(table["columns"]) - 1:
                self.current_col += 1

        elif key == curses.KEY_PPAGE:  # Page Up
            self.current_row = max(0, self.current_row - self.rows_per_page)
            self.top_row = max(0, self.top_row - self.rows_per_page)

        elif key == curses.KEY_NPAGE:  # Page Down
            self.current_row = min(len(data) - 1, self.current_row + self.rows_per_page)
            self.top_row = min(
                max(0, len(data) - self.rows_per_page),
                self.top_row + self.rows_per_page,
            )

        elif key == curses.KEY_HOME:
            self.current_row = 0
            self.top_row = 0

        elif key == curses.KEY_END:
            self.current_row = len(data) - 1
            self.top_row = max(0, len(data) - self.rows_per_page)

        return True  # Continue running

    def run(self):
        """Main event loop."""
        running = True

        while running:
            try:
                # Draw all components
                self.draw_header()
                self.draw_table()
                self.draw_status_bar()
                self.draw_input_line()

                if self.show_detail:
                    self.draw_detail_view()

                # Update panels
                panel.update_panels()
                curses.doupdate()

                # Get input
                key = self.stdscr.getch()

                if key != -1:  # Key was pressed
                    result = self.handle_input(key)
                    if result is False:
                        running = False

            except KeyboardInterrupt:
                running = False
            except Exception as e:
                self.status_message = f"Error: {str(e)[:50]}"


def main(stdscr):
    """Main entry point."""
    try:
        browser = TableBrowser(stdscr)
        browser.run()
    except Exception as e:
        # Clean error display
        stdscr.clear()
        stdscr.addstr(0, 0, f"Fatal error: {e}")
        stdscr.addstr(2, 0, "Press any key to exit...")
        stdscr.refresh()
        stdscr.getch()
        raise


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nDatabase browser terminated by user")
    except Exception as e:
        print(f"\nError running database browser: {e}")
        import traceback

        traceback.print_exc()
