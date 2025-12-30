"""
Terminal Capability Detection System

Detects terminal capabilities for graceful degradation:
- Color support (none, 16, 256, truecolor)
- Unicode support
- Terminal dimensions
- Interactive capabilities
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import os
import sys
import platform


class ColorSupport(Enum):
    """Terminal color support levels"""

    NONE = 0
    BASIC = 16  # 16 ANSI colors
    EXTENDED = 256  # 256 colors
    TRUECOLOR = 16_777_216  # 24-bit RGB


@dataclass(frozen=True)
class TerminalCapabilities:
    """Immutable terminal capability snapshot"""

    color_support: ColorSupport
    unicode_support: bool
    width: int
    height: int
    is_interactive: bool
    is_windows: bool
    terminal_name: str
    supports_hyperlinks: bool


class CapabilityDetector:
    """
    Detects terminal capabilities via environment inspection.

    Detection hierarchy:
    1. Explicit environment variables (FORCE_COLOR, NO_COLOR, etc.)
    2. Terminal-specific detection (Windows Terminal, iTerm2, etc.)
    3. Generic TERM variable inspection
    4. Fallback defaults
    """

    @classmethod
    def detect(cls) -> TerminalCapabilities:
        """Perform full capability detection"""
        return TerminalCapabilities(
            color_support=cls._detect_color_support(),
            unicode_support=cls._detect_unicode_support(),
            width=cls._detect_width(),
            height=cls._detect_height(),
            is_interactive=cls._detect_interactive(),
            is_windows=platform.system() == "Windows",
            terminal_name=cls._detect_terminal_name(),
            supports_hyperlinks=cls._detect_hyperlinks(),
        )

    @classmethod
    def _detect_color_support(cls) -> ColorSupport:
        """
        Detect color support level.

        Checks (in order):
        1. NO_COLOR env var (forces none)
        2. FORCE_COLOR env var (forces basic+)
        3. WT_SESSION (Windows Terminal = truecolor)
        4. COLORTERM=truecolor/24bit
        5. TERM contains '256color'
        6. TERM is xterm/vt100/screen/etc.
        7. sys.stdout.isatty()
        """
        # NO_COLOR standard (https://no-color.org/)
        if os.environ.get("NO_COLOR"):
            return ColorSupport.NONE

        # FORCE_COLOR override
        force_color = os.environ.get("FORCE_COLOR", "")
        if force_color:
            if force_color in ("3", "true", "1"):
                return ColorSupport.TRUECOLOR
            return ColorSupport.BASIC

        # Windows Terminal detection (excellent support)
        if os.environ.get("WT_SESSION"):
            return ColorSupport.TRUECOLOR

        # COLORTERM for truecolor
        colorterm = os.environ.get("COLORTERM", "").lower()
        if colorterm in ("truecolor", "24bit"):
            return ColorSupport.TRUECOLOR

        # TERM variable inspection
        term = os.environ.get("TERM", "").lower()
        if "256color" in term:
            return ColorSupport.EXTENDED
        if term in ("xterm", "vt100", "screen", "linux", "cygwin"):
            return ColorSupport.BASIC

        # Fallback: check if stdout is a terminal
        if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
            return ColorSupport.BASIC

        return ColorSupport.NONE

    @classmethod
    def _detect_unicode_support(cls) -> bool:
        """
        Detect Unicode symbol support.

        The ONLY reliable check is Python's stdout encoding.
        Environment variables and terminal emulator detection can lie,
        especially when output is redirected.
        """
        # Check Python's stdout encoding - this is the ground truth
        encoding = getattr(sys.stdout, "encoding", "") or ""

        # Must have UTF-8 encoding to support Unicode symbols
        if "utf" in encoding.lower() or "utf-8" in encoding.lower():
            return True

        # All other checks are unreliable when encoding isn't UTF-8
        return False

    @classmethod
    def _detect_width(cls) -> int:
        """Detect terminal width, default 80"""
        try:
            size = os.get_terminal_size()
            return size.columns
        except (OSError, ValueError):
            return 80

    @classmethod
    def _detect_height(cls) -> int:
        """Detect terminal height, default 24"""
        try:
            size = os.get_terminal_size()
            return size.lines
        except (OSError, ValueError):
            return 24

    @classmethod
    def _detect_interactive(cls) -> bool:
        """Check if terminal supports interactive input"""
        return (
            hasattr(sys.stdin, "isatty")
            and sys.stdin.isatty()
            and hasattr(sys.stdout, "isatty")
            and sys.stdout.isatty()
        )

    @classmethod
    def _detect_terminal_name(cls) -> str:
        """Identify terminal emulator"""
        if os.environ.get("WT_SESSION"):
            return "Windows Terminal"
        if os.environ.get("TERM_PROGRAM") == "iTerm.app":
            return "iTerm2"
        if os.environ.get("TERM_PROGRAM") == "Apple_Terminal":
            return "Terminal.app"
        if os.environ.get("TERM_PROGRAM") == "vscode":
            return "VS Code"
        return os.environ.get("TERM", "unknown")

    @classmethod
    def _detect_hyperlinks(cls) -> bool:
        """Check for OSC 8 hyperlink support"""
        term_program = os.environ.get("TERM_PROGRAM", "")
        if term_program in ("iTerm.app", "WezTerm", "Hyper"):
            return True
        if os.environ.get("WT_SESSION"):  # Windows Terminal
            return True
        return False


# Global singleton for efficiency
_capabilities: Optional[TerminalCapabilities] = None


def get_capabilities() -> TerminalCapabilities:
    """Get cached terminal capabilities"""
    global _capabilities
    if _capabilities is None:
        _capabilities = CapabilityDetector.detect()
    return _capabilities


def reset_capabilities() -> None:
    """Reset cached capabilities (for testing)"""
    global _capabilities
    _capabilities = None
