"""Quick non-interactive test of all components."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import claude_terminal_ui as ui

print("\n" + "=" * 70)
print("Quick Component Test")
print("=" * 70 + "\n")

# Test status messages
ui.print_success("Success message test")
ui.print_error("Error message test")
ui.print_warning("Warning message test")
ui.print_info("Info message test")
ui.print_debug("Debug message test")

print()

# Test headers
print(ui.header("MAIN HEADER"))
print()
print(ui.subheader("Subheader Test"))
print()

# Test progress
print(ui.step_indicator(1, 3, "Step one"))
print(ui.step_indicator(2, 3, "Step two"))
print(ui.step_indicator(3, 3, "Step three"))
print()

# Test progress bars
print("Progress bars:")
for i in [0, 25, 50, 75, 100]:
    print(ui.progress_bar(i, 100, width=40))

print()

# Show capabilities
from claude_terminal_ui.core.capabilities import get_capabilities

caps = get_capabilities()
print(f"Terminal: {caps.terminal_name}")
print(f"Colors: {caps.color_support.name}")
print(f"Unicode: {'Yes' if caps.unicode_support else 'No'}")

print("\n[OK] All tests passed!\n")
