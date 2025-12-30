"""Core functionality for terminal UI system."""

from .capabilities import (
    ColorSupport,
    TerminalCapabilities,
    CapabilityDetector,
    get_capabilities,
    reset_capabilities,
)

__all__ = [
    "ColorSupport",
    "TerminalCapabilities",
    "CapabilityDetector",
    "get_capabilities",
    "reset_capabilities",
]
