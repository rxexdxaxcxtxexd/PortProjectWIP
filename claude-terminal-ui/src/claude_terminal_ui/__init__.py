"""
Claude Terminal UI Design System

A professional terminal UI design system for Python CLI applications.
Provides consistent, cross-platform terminal output with automatic capability detection.
"""

__version__ = "0.1.0"
__author__ = "Layden"

# Core imports
from . import core
from . import tokens
from . import components

# Convenience imports for common usage
from .components import (
    # Status messages
    print_success,
    print_error,
    print_warning,
    print_info,
    print_debug,
    success,
    error,
    warning,
    info,
    debug,
    # Headers
    header,
    subheader,
    divider,
    step_header,
    # Progress
    progress_bar,
    spinner,
    step_indicator,
    Spinner,
)

__all__ = [
    "__version__",
    "__author__",
    # Modules
    "core",
    "tokens",
    "components",
    # Status messages
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
    "print_debug",
    "success",
    "error",
    "warning",
    "info",
    "debug",
    # Headers
    "header",
    "subheader",
    "divider",
    "step_header",
    # Progress
    "progress_bar",
    "spinner",
    "step_indicator",
    "Spinner",
]
