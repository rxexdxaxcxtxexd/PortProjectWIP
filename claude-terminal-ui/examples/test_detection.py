"""Test capability detection."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from claude_terminal_ui.core.capabilities import get_capabilities, reset_capabilities

# Reset to force fresh detection
reset_capabilities()

caps = get_capabilities()

print(f"stdout.encoding: {sys.stdout.encoding}")
print(f"'utf' in encoding.lower(): {'utf' in (sys.stdout.encoding or '').lower()}")
print(f"Unicode support detected: {caps.unicode_support}")
print(f"Color support: {caps.color_support.name}")
print(f"Terminal: {caps.terminal_name}")

# Test symbol rendering
from claude_terminal_ui.tokens.symbols import Symbols

print(f"\nSuccess symbol: '{Symbols.SUCCESS.render()}'")
print(f"Error symbol: '{Symbols.ERROR.render()}'")
