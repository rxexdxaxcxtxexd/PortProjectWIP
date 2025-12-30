"""Design tokens for terminal UI."""

from .colors import Color, Colors, BgColors, Styles, RESET, colorize
from .symbols import Symbol, Symbols
from .spacing import (
    DEFAULT_WIDTH,
    WIDE_WIDTH,
    NARROW_WIDTH,
    CELL_PADDING,
    INDENT_UNIT,
    LIST_INDENT,
    PROGRESS_BAR_WIDTH,
    PROGRESS_BAR_WIDTH_NARROW,
)

__all__ = [
    # Colors
    "Color",
    "Colors",
    "BgColors",
    "Styles",
    "RESET",
    "colorize",
    # Symbols
    "Symbol",
    "Symbols",
    # Spacing
    "DEFAULT_WIDTH",
    "WIDE_WIDTH",
    "NARROW_WIDTH",
    "CELL_PADDING",
    "INDENT_UNIT",
    "LIST_INDENT",
    "PROGRESS_BAR_WIDTH",
    "PROGRESS_BAR_WIDTH_NARROW",
]
