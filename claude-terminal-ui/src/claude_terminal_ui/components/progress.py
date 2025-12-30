"""
Progress Indicator Components

- progress_bar(): ASCII/Unicode progress bars
- spinner(): Animated spinners
- step_indicator(): [1/N] step counters
"""

import sys
import time
import threading
from typing import Optional
from contextlib import contextmanager
from ..core.capabilities import get_capabilities
from ..tokens.colors import Colors, RESET
from ..tokens.symbols import Symbols
from ..tokens.spacing import PROGRESS_BAR_WIDTH


def progress_bar(
    current: int,
    total: int,
    *,
    width: int = PROGRESS_BAR_WIDTH,
    filled_char: Optional[str] = None,
    empty_char: Optional[str] = None,
    show_percentage: bool = True,
    prefix: str = "",
    suffix: str = "",
) -> str:
    """
    Create a text-based progress bar.

    Example output:
    [==========================----------------] 65%
    """
    caps = get_capabilities()

    # Select characters based on capability
    if filled_char is None:
        filled_char = Symbols.PROGRESS_FULL.render()
    if empty_char is None:
        empty_char = Symbols.PROGRESS_EMPTY.render()

    # Calculate fill
    if total <= 0:
        percentage = 0
        filled_width = 0
    else:
        percentage = min(100, (current / total) * 100)
        filled_width = int((current / total) * width)

    # Build bar
    bar = filled_char * filled_width + empty_char * (width - filled_width)

    # Format output
    pct_str = f" {percentage:.0f}%" if show_percentage else ""

    if caps.color_support.value > 0:
        # Color the filled portion
        colored_bar = (
            f"{Colors.SUCCESS.code()}{filled_char * filled_width}{RESET}"
            f"{empty_char * (width - filled_width)}"
        )
        return f"{prefix}[{colored_bar}]{pct_str}{suffix}"
    else:
        return f"{prefix}[{bar}]{pct_str}{suffix}"


class Spinner:
    """
    Animated spinner for long-running operations.

    Usage:
        with Spinner("Loading"):
            long_operation()

    Or:
        spinner = Spinner("Processing")
        spinner.start()
        # ... work ...
        spinner.stop()
    """

    def __init__(
        self, message: str = "Working", *, frames: Optional[list] = None, interval: float = 0.1
    ):
        self.message = message
        self.interval = interval
        self._running = False
        self._thread: Optional[threading.Thread] = None

        caps = get_capabilities()
        if frames is None:
            if caps.unicode_support:
                self.frames = [s.unicode for s in Symbols.SPINNER_FRAMES]
            else:
                self.frames = ["|", "/", "-", "\\"]
        else:
            self.frames = frames

        self._frame_index = 0

    def start(self) -> None:
        """Start the spinner animation"""
        caps = get_capabilities()
        if not caps.is_interactive:
            # Non-interactive: just print message
            print(f"{self.message}...")
            return

        self._running = True
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def stop(self, final_message: Optional[str] = None) -> None:
        """Stop the spinner and optionally display final message"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.5)

        # Clear the spinner line
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()

        if final_message:
            print(final_message)

    def _animate(self) -> None:
        """Animation loop (runs in background thread)"""
        while self._running:
            frame = self.frames[self._frame_index % len(self.frames)]
            sys.stdout.write(f"\r{frame} {self.message}")
            sys.stdout.flush()
            self._frame_index += 1
            time.sleep(self.interval)

    def __enter__(self) -> "Spinner":
        self.start()
        return self

    def __exit__(self, *args) -> None:
        self.stop()


@contextmanager
def spinner(message: str = "Working", **kwargs):
    """Context manager for spinner"""
    s = Spinner(message, **kwargs)
    try:
        s.start()
        yield s
    finally:
        s.stop()


def step_indicator(current: int, total: int, message: str = "") -> str:
    """
    Format step indicator.

    Example: [2/5] Processing files...
    """
    caps = get_capabilities()
    indicator = f"[{current}/{total}]"

    if caps.color_support.value > 0:
        indicator = f"{Colors.INFO.code()}{indicator}{RESET}"

    if message:
        return f"{indicator} {message}"
    return indicator
