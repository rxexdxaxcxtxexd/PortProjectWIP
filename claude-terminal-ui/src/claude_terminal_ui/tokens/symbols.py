"""
Symbol Token Definitions

Unicode symbols with ASCII fallbacks for cross-platform support.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Symbol:
    """Symbol with Unicode and ASCII variants"""

    name: str
    unicode: str
    ascii: str

    def render(self, force_ascii: Optional[bool] = None) -> str:
        """Render appropriate symbol based on terminal capability"""
        if force_ascii is not None:
            return self.ascii if force_ascii else self.unicode

        from ..core.capabilities import get_capabilities

        caps = get_capabilities()
        return self.unicode if caps.unicode_support else self.ascii


class Symbols:
    """Standard symbol library"""

    # Status indicators
    SUCCESS = Symbol("success", "\u2714", "[OK]")  # Heavy check mark
    ERROR = Symbol("error", "\u2718", "[X]")  # Heavy ballot X
    WARNING = Symbol("warning", "\u26a0", "[!]")  # Warning sign
    INFO = Symbol("info", "\u2139", "[i]")  # Information source
    DEBUG = Symbol("debug", "\u2699", "[D]")  # Gear

    # Progress indicators
    BULLET = Symbol("bullet", "\u2022", "*")  # Bullet point
    ARROW_RIGHT = Symbol("arrow_right", "\u2192", "->")  # Right arrow
    ARROW_LEFT = Symbol("arrow_left", "\u2190", "<-")  # Left arrow
    ARROW_UP = Symbol("arrow_up", "\u2191", "^")  # Up arrow
    ARROW_DOWN = Symbol("arrow_down", "\u2193", "v")  # Down arrow

    # Task status
    TASK_DONE = Symbol("task_done", "\u2713", "[x]")  # Check mark
    TASK_TODO = Symbol("task_todo", "\u2610", "[ ]")  # Ballot box
    TASK_PROGRESS = Symbol("task_progress", "\u25cb", "[~]")  # Circle

    # File operations
    FILE_ADD = Symbol("file_add", "\u2795", "+")  # Heavy plus sign
    FILE_REMOVE = Symbol("file_remove", "\u2796", "-")  # Heavy minus sign
    FILE_MODIFY = Symbol("file_modify", "\u270e", "*")  # Pencil

    # Tree structure
    TREE_BRANCH = Symbol("tree_branch", "\u251c\u2500\u2500", "|--")  # Branch
    TREE_LAST = Symbol("tree_last", "\u2514\u2500\u2500", "`--")  # Last branch
    TREE_PIPE = Symbol("tree_pipe", "\u2502", "|")  # Vertical line
    TREE_SPACE = Symbol("tree_space", "   ", "   ")  # Space indent

    # Boxes
    BOX_TOP_LEFT = Symbol("box_tl", "\u250c", "+")
    BOX_TOP_RIGHT = Symbol("box_tr", "\u2510", "+")
    BOX_BOTTOM_LEFT = Symbol("box_bl", "\u2514", "+")
    BOX_BOTTOM_RIGHT = Symbol("box_br", "\u2518", "+")
    BOX_HORIZONTAL = Symbol("box_h", "\u2500", "-")
    BOX_VERTICAL = Symbol("box_v", "\u2502", "|")
    BOX_CROSS = Symbol("box_cross", "\u253c", "+")

    # Progress bar
    PROGRESS_FULL = Symbol("progress_full", "\u2588", "#")  # Full block
    PROGRESS_PARTIAL = Symbol("progress_partial", "\u2592", "=")  # Medium shade
    PROGRESS_EMPTY = Symbol("progress_empty", "\u2591", "-")  # Light shade

    # Spinner frames (for animation)
    SPINNER_FRAMES = [
        Symbol(f"spin_{i}", char, "|/-\\"[i % 4])
        for i, char in enumerate(
            [
                "\u280b",
                "\u2819",
                "\u2838",
                "\u2834",
                "\u2826",
                "\u2807",
                "\u280f",
                "\u281f",
            ]
        )
    ]

    # Misc
    STAR = Symbol("star", "\u2605", "*")  # Black star
    HEART = Symbol("heart", "\u2665", "<3")  # Heart
    LIGHTNING = Symbol("lightning", "\u26a1", "!")  # Lightning
    CLOCK = Symbol("clock", "\u23f0", "@")  # Alarm clock
    FOLDER = Symbol("folder", "\U0001f4c1", "[D]")  # Folder
    FILE = Symbol("file", "\U0001f4c4", "[F]")  # File
