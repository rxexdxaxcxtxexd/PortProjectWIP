"""
Header Components

Consistent section headers with configurable width:
- header(), subheader(), divider()
- Standardized 70-character default width
"""

from typing import Optional
from ..core.capabilities import get_capabilities
from ..tokens.colors import Colors, RESET, Styles, Color
from ..tokens.spacing import DEFAULT_WIDTH


def header(
    title: str,
    *,
    width: int = DEFAULT_WIDTH,
    char: str = "=",
    centered: bool = True,
    color: Optional[Color] = None,
) -> str:
    """
    Create a major section header.

    Example output:
    ======================================================================
                            UNIFIED CHECKPOINT
    ======================================================================
    """
    caps = get_capabilities()

    # Render header character
    line_char = char if caps.unicode_support else "="

    # Build lines
    border = line_char * width

    if centered:
        padding = (width - len(title)) // 2
        title_line = " " * padding + title
    else:
        title_line = title

    # Apply color if supported
    if color and caps.color_support.value > 0:
        border = f"{color.code()}{border}{RESET}"
        title_line = f"{Styles.BOLD}{title_line}{RESET}"

    return f"{border}\n{title_line}\n{border}"


def subheader(
    title: str, *, width: int = DEFAULT_WIDTH, char: str = "-", prefix: str = ""
) -> str:
    """
    Create a subsection header.

    Example output:
    ----------------------------------------------------------------------
    PROJECT CONTEXT
    ----------------------------------------------------------------------
    """
    caps = get_capabilities()
    line_char = char if caps.unicode_support else "-"
    border = line_char * width

    return f"{prefix}{border}\n{prefix}{title}\n{prefix}{border}"


def divider(
    *, width: int = DEFAULT_WIDTH, char: str = "-", label: str = "", prefix: str = ""
) -> str:
    """
    Create a dividing line, optionally with a label.

    Example outputs:
    ----------------------------------------------------------------------
    --- Step 1 -----------------------------------------------------------
    """
    caps = get_capabilities()
    line_char = char if caps.unicode_support else "-"

    if label:
        label_section = f" {label} "
        remaining = width - len(label_section) - len(prefix)
        left_pad = 3
        right_pad = remaining - left_pad
        return f"{prefix}{line_char * left_pad}{label_section}{line_char * right_pad}"
    else:
        return f"{prefix}{line_char * width}"


def step_header(step: int, total: int, description: str, *, width: int = DEFAULT_WIDTH) -> str:
    """
    Create a step indicator header.

    Example output:
    [1/3] Collecting and saving session data...
    """
    caps = get_capabilities()

    step_tag = f"[{step}/{total}]"

    if caps.color_support.value > 0:
        step_tag = f"{Colors.INFO.code()}{step_tag}{RESET}"

    return f"{step_tag} {description}"
