"""
Status Message Components

Provides consistent status message formatting:
- success(), error(), warning(), info(), debug()
- Tags: [OK], [ERROR], [WARNING], [INFO], [DEBUG]
"""

from typing import Optional
from ..core.capabilities import get_capabilities
from ..tokens.colors import Colors, RESET
from ..tokens.symbols import Symbols


def _format_status(
    symbol: Symbols,
    label: str,
    message: str,
    color: Colors,
    indent: int = 0,
    prefix: str = "",
) -> str:
    """Format a status message with consistent styling"""
    caps = get_capabilities()

    # Build components
    indent_str = " " * indent
    symbol_str = symbol.render()

    if caps.color_support.value > 0:
        tag = f"{color.code()}{symbol_str}{RESET}"
        msg = message
    else:
        tag = symbol_str
        msg = message

    return f"{prefix}{indent_str}{tag} {msg}"


def success(message: str, *, indent: int = 0, prefix: str = "") -> str:
    """Format success message with green checkmark"""
    return _format_status(
        Symbols.SUCCESS, "[OK]", message, Colors.SUCCESS, indent=indent, prefix=prefix
    )


def error(message: str, *, indent: int = 0, prefix: str = "") -> str:
    """Format error message with red X"""
    return _format_status(
        Symbols.ERROR, "[ERROR]", message, Colors.ERROR, indent=indent, prefix=prefix
    )


def warning(message: str, *, indent: int = 0, prefix: str = "") -> str:
    """Format warning message with yellow warning sign"""
    return _format_status(
        Symbols.WARNING,
        "[WARNING]",
        message,
        Colors.WARNING,
        indent=indent,
        prefix=prefix,
    )


def info(message: str, *, indent: int = 0, prefix: str = "") -> str:
    """Format info message with cyan info symbol"""
    return _format_status(
        Symbols.INFO, "[INFO]", message, Colors.INFO, indent=indent, prefix=prefix
    )


def debug(message: str, *, indent: int = 0, prefix: str = "") -> str:
    """Format debug message with gray debug symbol"""
    return _format_status(
        Symbols.DEBUG, "[DEBUG]", message, Colors.DEBUG, indent=indent, prefix=prefix
    )


# Print variants that output directly
def print_success(message: str, **kwargs) -> None:
    """Print success message"""
    print(success(message, **kwargs))


def print_error(message: str, **kwargs) -> None:
    """Print error message"""
    print(error(message, **kwargs))


def print_warning(message: str, **kwargs) -> None:
    """Print warning message"""
    print(warning(message, **kwargs))


def print_info(message: str, **kwargs) -> None:
    """Print info message"""
    print(info(message, **kwargs))


def print_debug(message: str, **kwargs) -> None:
    """Print debug message"""
    print(debug(message, **kwargs))
