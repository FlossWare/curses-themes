#!/usr/bin/env python3
"""
System Monitor Dashboard - Real-time system monitoring with themed UI

A comprehensive real-time system monitoring dashboard demonstrating advanced
curses-themes features including:
- Animated ASCII graphs for CPU and memory usage
- Color-coded status indicators (success/warning/error zones)
- Live process list with themed selection
- Network traffic monitoring
- System uptime and load average displays
- Alert notifications with themed modal windows
- Multiple bordered panels using draw_box
- Runtime theme cycling
- Time-based color transitions for thresholds

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.

Usage:
    python3 system_monitor_demo.py

Controls:
    t - Cycle through available themes
    p - Toggle process sort (CPU/Memory/Name)
    a - Trigger test alert
    q - Quit

Features Demonstrated:
    - Real-time data visualization with ASCII graphs
    - Semantic color usage for status indicators
    - Dynamic UI updates with theme support
    - Multiple panel layouts with borders
    - Interactive controls and modal dialogs
    - Process management and sorting
    - Network and system statistics
"""

import curses
import time
from datetime import timedelta
from typing import List, Tuple

import psutil

from curses_tui import ThemeManager


class SystemMonitor:
    """
    Real-time system monitoring dashboard with themed UI.

    Manages multiple panels showing CPU, memory, processes, network,
    and system information with live updates and theme support.
    """

    def __init__(self, stdscr):
        """
        Initialize the system monitor.

        Args:
            stdscr: Main curses window
        """
        self.stdscr = stdscr
        self.running = True

        height, width = stdscr.getmaxyx()
        if height < 24 or width < 80:
            raise RuntimeError(
                f"Terminal too small ({width}x{height}). Minimum 80x24 required."
            )

        # Available themes
        self.themes = [
            "default",
            "dark",
            "light",
            "ti-99-4a",
            "trs-80",
            "dos",
            "dbase-iii",
            "dbase-iv",
        ]
        self.current_theme_idx = 0
        self.theme = None

        # Process sorting mode
        self.sort_modes = ["cpu", "memory", "name"]
        self.current_sort_idx = 0

        # History for graphs (last 60 samples)
        self.cpu_history = []
        self.mem_history = []
        self.max_history = 60

        # Alert state
        self.show_alert = False
        self.alert_message = ""

        # Network tracking
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()
        self.net_upload_rate = 0
        self.net_download_rate = 0

        # Initialize curses
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(1)  # Non-blocking input
        self.stdscr.timeout(100)  # 100ms timeout for getch

        # Load initial theme
        self._load_theme()

    def _load_theme(self):
        """Load and apply the current theme."""
        theme_name = self.themes[self.current_theme_idx]
        self.theme = ThemeManager.load(theme_name)
        self.theme.apply(self.stdscr)

    def _cycle_theme(self):
        """Cycle to the next theme."""
        self.current_theme_idx = (self.current_theme_idx + 1) % len(self.themes)
        self._load_theme()

    def _cycle_sort(self):
        """Cycle to the next process sort mode."""
        self.current_sort_idx = (self.current_sort_idx + 1) % len(self.sort_modes)

    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        return psutil.cpu_percent(interval=0.1)

    def _get_memory_usage(self) -> Tuple[float, int, int]:
        """
        Get memory usage information.

        Returns:
            Tuple of (percentage, used_gb, total_gb)
        """
        mem = psutil.virtual_memory()
        used_gb = mem.used / (1024**3)
        total_gb = mem.total / (1024**3)
        return mem.percent, used_gb, total_gb

    def _get_processes(self) -> List[dict]:
        """
        Get list of top processes sorted by current mode.

        Returns:
            List of process dictionaries with name, cpu, and memory
        """
        processes = []
        for proc in psutil.process_iter(
            ["pid", "name", "cpu_percent", "memory_percent"]
        ):
            try:
                pinfo = proc.info
                processes.append(
                    {
                        "pid": pinfo["pid"],
                        "name": pinfo["name"][:20],  # Truncate long names
                        "cpu": pinfo["cpu_percent"] or 0.0,
                        "memory": pinfo["memory_percent"] or 0.0,
                    }
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort by current mode
        sort_key = self.sort_modes[self.current_sort_idx]
        if sort_key == "cpu":
            processes.sort(key=lambda p: p["cpu"], reverse=True)
        elif sort_key == "memory":
            processes.sort(key=lambda p: p["memory"], reverse=True)
        else:  # name
            processes.sort(key=lambda p: p["name"])

        return processes[:15]  # Top 15 processes

    def _update_network_stats(self):
        """Update network upload/download rates."""
        current_io = psutil.net_io_counters()
        current_time = time.time()

        # Calculate rates in KB/s
        time_delta = current_time - self.last_net_time
        if time_delta > 0:
            bytes_sent = current_io.bytes_sent - self.last_net_io.bytes_sent
            bytes_recv = current_io.bytes_recv - self.last_net_io.bytes_recv

            self.net_upload_rate = (bytes_sent / time_delta) / 1024
            self.net_download_rate = (bytes_recv / time_delta) / 1024

        self.last_net_io = current_io
        self.last_net_time = current_time

    def _get_threshold_color(self, value: float, low: float, high: float) -> int:
        """
        Get color based on threshold zones.

        Args:
            value: Current value
            low: Low threshold (success zone)
            high: High threshold (error zone)

        Returns:
            Color pair number (success/warning/error)
        """
        if value < low:
            return self.theme.colors.success
        elif value < high:
            return self.theme.colors.warning
        else:
            return self.theme.colors.error

    def _draw_progress_bar(
        self, window, y: int, x: int, width: int, percentage: float, label: str = ""
    ):
        """
        Draw a progress bar with percentage.

        Args:
            window: Curses window to draw on
            y: Y coordinate
            x: X coordinate
            width: Width of progress bar
            percentage: Percentage (0-100)
            label: Optional label text
        """
        # Get color based on threshold
        color = self._get_threshold_color(percentage, 50, 80)

        # Draw label if provided
        if label:
            window.addstr(y, x, label, curses.color_pair(self.theme.colors.foreground))
            y += 1

        # Calculate filled width
        filled = int((percentage / 100.0) * width)

        # Draw bar
        bar = "█" * filled + "░" * (width - filled)
        window.addstr(y, x, bar, curses.color_pair(color))

        # Draw percentage
        pct_text = f" {percentage:.1f}%"
        window.addstr(
            y, x + width + 1, pct_text, curses.color_pair(self.theme.colors.foreground)
        )

    def _draw_graph(
        self,
        window,
        y: int,
        x: int,
        width: int,
        height: int,
        data: List[float],
        max_value: float = 100.0,
        title: str = "",
    ):
        """
        Draw an ASCII graph with historical data.

        Args:
            window: Curses window to draw on
            y: Top Y coordinate
            x: Left X coordinate
            width: Graph width
            height: Graph height
            data: List of data points
            max_value: Maximum value for scaling
            title: Graph title
        """
        if not data:
            return

        # Draw title
        if title:
            window.addstr(
                y,
                x,
                title,
                curses.color_pair(self.theme.colors.primary) | curses.A_BOLD,
            )
            y += 1
            height -= 1

        # Scale data to fit height
        visible_data = data[-width:]
        scaled_data = [
            min(int((val / max_value) * height), height - 1) for val in visible_data
        ]

        # Draw graph from bottom to top
        for row in range(height):
            row_y = y + (height - 1 - row)
            for col, val_height in enumerate(scaled_data):
                if val_height >= row:
                    # Get color based on value
                    orig_val = visible_data[col]
                    color = self._get_threshold_color(orig_val, 50, 80)
                    try:
                        window.addstr(row_y, x + col, "▀", curses.color_pair(color))
                    except curses.error:
                        pass

    def _draw_header(self):
        """Draw the main header with title and theme info."""
        height, width = self.stdscr.getmaxyx()

        # Title
        title = "System Monitor Dashboard"
        title_x = (width - len(title)) // 2
        self.stdscr.addstr(
            0,
            title_x,
            title,
            curses.color_pair(self.theme.colors.primary) | curses.A_BOLD,
        )

        # Theme name
        theme_name = f"Theme: {self.themes[self.current_theme_idx]}"
        self.stdscr.addstr(
            0, 2, theme_name, curses.color_pair(self.theme.colors.accent)
        )

        # Timestamp
        timestamp = time.strftime("%H:%M:%S")
        self.stdscr.addstr(
            0,
            width - len(timestamp) - 2,
            timestamp,
            curses.color_pair(self.theme.colors.info),
        )

    def _draw_cpu_panel(self, y: int, x: int, width: int, height: int):
        """Draw CPU usage panel with gauge and graph."""
        # Draw panel border
        self.theme.draw_box(self.stdscr, y, x, height, width, title="CPU Usage")

        # Get CPU usage
        cpu_usage = self._get_cpu_usage()
        self.cpu_history.append(cpu_usage)
        if len(self.cpu_history) > self.max_history:
            self.cpu_history.pop(0)

        # Draw gauge
        self._draw_progress_bar(
            self.stdscr, y + 2, x + 2, width - 4, cpu_usage, "Current:"
        )

        # Draw graph
        if height > 10:
            self._draw_graph(
                self.stdscr,
                y + 5,
                x + 2,
                width - 4,
                height - 7,
                self.cpu_history,
                100.0,
                "History:",
            )

    def _draw_memory_panel(self, y: int, x: int, width: int, height: int):
        """Draw memory usage panel with gauge and info."""
        # Draw panel border
        self.theme.draw_box(self.stdscr, y, x, height, width, title="Memory Usage")

        # Get memory info
        mem_percent, used_gb, total_gb = self._get_memory_usage()
        self.mem_history.append(mem_percent)
        if len(self.mem_history) > self.max_history:
            self.mem_history.pop(0)

        # Draw gauge
        self._draw_progress_bar(
            self.stdscr, y + 2, x + 2, width - 4, mem_percent, "Current:"
        )

        # Draw memory info
        mem_info = f"{used_gb:.1f} GB / {total_gb:.1f} GB"
        self.stdscr.addstr(
            y + 4, x + 2, mem_info, curses.color_pair(self.theme.colors.foreground)
        )

        # Draw graph
        if height > 10:
            self._draw_graph(
                self.stdscr,
                y + 6,
                x + 2,
                width - 4,
                height - 8,
                self.mem_history,
                100.0,
                "History:",
            )

    def _draw_process_panel(self, y: int, x: int, width: int, height: int):
        """Draw process list panel."""
        # Draw panel border
        sort_mode = self.sort_modes[self.current_sort_idx].upper()
        title = f"Processes (Sort: {sort_mode})"
        self.theme.draw_box(self.stdscr, y, x, height, width, title=title)

        # Draw column headers
        header = f"{'PID':<8} {'NAME':<20} {'CPU%':<8} {'MEM%':<8}"
        self.stdscr.addstr(
            y + 2,
            x + 2,
            header,
            curses.color_pair(self.theme.colors.accent) | curses.A_BOLD,
        )

        # Draw separator
        self.stdscr.addstr(
            y + 3,
            x + 2,
            "-" * (width - 4),
            curses.color_pair(self.theme.colors.foreground),
        )

        # Get and draw processes
        processes = self._get_processes()
        for idx, proc in enumerate(processes):
            if idx >= height - 5:
                break

            row_y = y + 4 + idx
            row = f"{proc['pid']:<8} {proc['name']:<20} {proc['cpu']:<8.1f} {proc['memory']:<8.1f}"

            # Highlight high CPU/memory processes
            if proc["cpu"] > 50 or proc["memory"] > 50:
                color = self.theme.colors.error
            elif proc["cpu"] > 20 or proc["memory"] > 20:
                color = self.theme.colors.warning
            else:
                color = self.theme.colors.foreground

            try:
                self.stdscr.addstr(row_y, x + 2, row, curses.color_pair(color))
            except curses.error:
                pass

    def _draw_network_panel(self, y: int, x: int, width: int, height: int):
        """Draw network traffic panel."""
        # Draw panel border
        self.theme.draw_box(self.stdscr, y, x, height, width, title="Network Traffic")

        # Update network stats
        self._update_network_stats()

        # Draw upload/download with arrows
        upload_text = f"↑ Upload:   {self.net_upload_rate:>8.1f} KB/s"
        download_text = f"↓ Download: {self.net_download_rate:>8.1f} KB/s"

        # Color based on traffic intensity
        upload_color = self._get_threshold_color(self.net_upload_rate, 100, 1000)
        download_color = self._get_threshold_color(self.net_download_rate, 100, 1000)

        self.stdscr.addstr(y + 2, x + 2, upload_text, curses.color_pair(upload_color))
        self.stdscr.addstr(
            y + 3, x + 2, download_text, curses.color_pair(download_color)
        )

        # Draw total bytes
        total_sent = self.last_net_io.bytes_sent / (1024**3)
        total_recv = self.last_net_io.bytes_recv / (1024**3)

        self.stdscr.addstr(
            y + 5,
            x + 2,
            f"Total Sent: {total_sent:.2f} GB",
            curses.color_pair(self.theme.colors.info),
        )
        self.stdscr.addstr(
            y + 6,
            x + 2,
            f"Total Recv: {total_recv:.2f} GB",
            curses.color_pair(self.theme.colors.info),
        )

    def _draw_system_panel(self, y: int, x: int, width: int, height: int):
        """Draw system information panel."""
        # Draw panel border
        self.theme.draw_box(self.stdscr, y, x, height, width, title="System Info")

        # Get system info
        boot_time = psutil.boot_time()
        uptime = timedelta(seconds=int(time.time() - boot_time))
        load_avg = psutil.getloadavg()
        cpu_count = psutil.cpu_count()

        # Draw info
        info_y = y + 2
        self.stdscr.addstr(
            info_y,
            x + 2,
            f"Uptime: {uptime}",
            curses.color_pair(self.theme.colors.success),
        )

        info_y += 1
        load_text = f"Load Avg: {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"

        # Color load average based on CPU count
        load_color = self._get_threshold_color(load_avg[0], cpu_count * 0.7, cpu_count)
        self.stdscr.addstr(info_y, x + 2, load_text, curses.color_pair(load_color))

        info_y += 1
        self.stdscr.addstr(
            info_y,
            x + 2,
            f"CPU Cores: {cpu_count}",
            curses.color_pair(self.theme.colors.info),
        )

    def _draw_controls(self):
        """Draw control instructions at bottom."""
        height, width = self.stdscr.getmaxyx()
        controls = "Controls: [T]heme | [P]rocess Sort | [A]lert | [Q]uit"

        try:
            self.stdscr.addstr(
                height - 1,
                (width - len(controls)) // 2,
                controls,
                curses.color_pair(self.theme.colors.info) | curses.A_DIM,
            )
        except curses.error:
            pass

    def _draw_alert(self):
        """Draw modal alert dialog."""
        if not self.show_alert:
            return

        height, width = self.stdscr.getmaxyx()

        # Calculate alert box dimensions
        alert_width = min(60, width - 10)
        alert_height = 8
        alert_y = (height - alert_height) // 2
        alert_x = (width - alert_width) // 2

        # Draw shadow effect
        for i in range(alert_height):
            try:
                self.stdscr.addstr(
                    alert_y + i + 1,
                    alert_x + 2,
                    " " * alert_width,
                    curses.color_pair(self.theme.colors.foreground) | curses.A_DIM,
                )
            except curses.error:
                pass

        # Draw alert box
        self.theme.draw_box(
            self.stdscr, alert_y, alert_x, alert_height, alert_width, title="ALERT"
        )

        # Draw alert icon
        icon = "⚠"
        self.stdscr.addstr(
            alert_y + 2,
            alert_x + (alert_width // 2) - 1,
            icon,
            curses.color_pair(self.theme.colors.warning) | curses.A_BOLD,
        )

        # Draw message
        msg_lines = [self.alert_message, "", "Press any key to dismiss"]

        for idx, line in enumerate(msg_lines):
            line_x = alert_x + (alert_width - len(line)) // 2
            self.stdscr.addstr(
                alert_y + 3 + idx,
                line_x,
                line,
                curses.color_pair(self.theme.colors.foreground),
            )

    def _draw_all_panels(self):
        """Draw all monitoring panels."""
        height, width = self.stdscr.getmaxyx()

        # Calculate panel layout (3 columns)
        col_width = width // 3
        panel_height = (height - 4) // 2

        # Top row: CPU, Memory, Processes
        self._draw_cpu_panel(2, 0, col_width, panel_height)
        self._draw_memory_panel(2, col_width, col_width, panel_height)
        self._draw_process_panel(2, col_width * 2, width - col_width * 2, height - 3)

        # Bottom row: Network, System
        bottom_y = 2 + panel_height
        bottom_height = height - bottom_y - 2
        self._draw_network_panel(bottom_y, 0, col_width, bottom_height)
        self._draw_system_panel(bottom_y, col_width, col_width, bottom_height)

    def _handle_input(self):
        """Handle keyboard input."""
        try:
            key = self.stdscr.getch()

            if key == ord("q") or key == ord("Q"):
                self.running = False
            elif key == ord("t") or key == ord("T"):
                self._cycle_theme()
            elif key == ord("p") or key == ord("P"):
                self._cycle_sort()
            elif key == ord("a") or key == ord("A"):
                self.show_alert = True
                self.alert_message = "Test Alert: System monitoring active!"
            elif self.show_alert:
                # Any key dismisses alert
                self.show_alert = False
        except curses.error:
            pass

    def run(self):
        """Main monitoring loop."""
        last_update = time.time()
        update_interval = 1.0  # Update every second

        while self.running:
            try:
                # Clear screen
                self.stdscr.erase()

                # Draw all components
                self._draw_header()
                self._draw_all_panels()
                self._draw_controls()

                # Draw alert on top if active
                if self.show_alert:
                    self._draw_alert()

                # Refresh screen
                self.stdscr.refresh()

                # Handle input
                self._handle_input()

                # Throttle updates
                current_time = time.time()
                if current_time - last_update < update_interval:
                    time.sleep(0.1)
                else:
                    last_update = current_time

            except KeyboardInterrupt:
                self.running = False
            except curses.error:
                # Ignore curses errors from drawing at boundaries
                pass


def main(stdscr):
    """
    Main entry point for the system monitor dashboard.

    Args:
        stdscr: Main curses window from curses.wrapper
    """
    monitor = SystemMonitor(stdscr)
    monitor.run()


if __name__ == "__main__":
    # Verify psutil is available
    try:
        import psutil
    except ImportError:
        print("Error: psutil is required for system monitoring")
        print("Install with: pip install psutil")
        exit(1)

    # Run the monitor
    curses.wrapper(main)
