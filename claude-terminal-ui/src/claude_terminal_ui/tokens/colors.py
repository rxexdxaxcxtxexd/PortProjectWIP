"""
Color Token Definitions

Provides semantic color names with ANSI code mappings.
Supports graceful degradation based on terminal capabilities.
"""

from dataclasses import dataclass
from typing import Optional

# Avoid circular import by using TYPE_CHECKING
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.capabilities import ColorSupport


@dataclass
class Color:
    """Color definition with fallbacks"""

    name: str
    ansi_16: str  # Basic ANSI code
    ansi_256: int  # 256-color palette index
    rgb: tuple  # (r, g, b) for truecolor

    def code(self, support: Optional["ColorSupport"] = None) -> str:
        """Get appropriate escape code for terminal capability"""
        if support is None:
            from ..core.capabilities import get_capabilities

            support = get_capabilities().color_support

        # Import ColorSupport enum
        from ..core.capabilities import ColorSupport

        if support == ColorSupport.NONE:
            return ""
        elif support == ColorSupport.BASIC:
            return self.ansi_16
        elif support == ColorSupport.EXTENDED:
            return f"\033[38;5;{self.ansi_256}m"
        else:  # TRUECOLOR
            r, g, b = self.rgb
            return f"\033[38;2;{r};{g};{b}m"


# Reset code
RESET = "\033[0m"


class Colors:
    """Semantic color definitions"""

    # Status colors
    SUCCESS = Color("success", "\033[32m", 34, (46, 204, 113))  # Green
    ERROR = Color("error", "\033[31m", 196, (231, 76, 60))  # Red
    WARNING = Color("warning", "\033[33m", 214, (241, 196, 15))  # Yellow
    INFO = Color("info", "\033[36m", 39, (52, 152, 219))  # Cyan
    DEBUG = Color("debug", "\033[90m", 242, (127, 140, 141))  # Gray

    # Text colors
    PRIMARY = Color("primary", "\033[97m", 255, (255, 255, 255))  # White
    SECONDARY = Color("secondary", "\033[37m", 250, (189, 195, 199))  # Light gray
    MUTED = Color("muted", "\033[90m", 245, (149, 165, 166))  # Dark gray

    # Accent colors
    ACCENT = Color("accent", "\033[35m", 141, (155, 89, 182))  # Purple
    HIGHLIGHT = Color("highlight", "\033[93m", 227, (243, 156, 18))  # Bright yellow
    LINK = Color("link", "\033[94m", 75, (41, 128, 185))  # Blue

    # Semantic colors
    ADD = Color("add", "\033[32m", 34, (46, 204, 113))  # Green (added)
    REMOVE = Color("remove", "\033[31m", 196, (231, 76, 60))  # Red (removed)
    CHANGE = Color("change", "\033[33m", 214, (241, 196, 15))  # Yellow (modified)


class BgColors:
    """Background color definitions"""

    SUCCESS = Color("bg_success", "\033[42m", 34, (46, 204, 113))
    ERROR = Color("bg_error", "\033[41m", 196, (231, 76, 60))
    WARNING = Color("bg_warning", "\033[43m", 214, (241, 196, 15))
    INFO = Color("bg_info", "\033[46m", 39, (52, 152, 219))


class Styles:
    """Text style codes"""

    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    STRIKETHROUGH = "\033[9m"


def colorize(text: str, color: Color, bold: bool = False) -> str:
    """Apply color to text with automatic capability detection"""
    from ..core.capabilities import ColorSupport, get_capabilities

    caps = get_capabilities()
    if caps.color_support == ColorSupport.NONE:
        return text

    prefix = color.code()
    if bold:
        prefix = Styles.BOLD + prefix

    return f"{prefix}{text}{RESET}"
