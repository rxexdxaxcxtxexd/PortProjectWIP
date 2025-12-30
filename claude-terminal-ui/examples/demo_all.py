"""
Interactive demo showcasing all components.

Run: python -m claude_terminal_ui.examples.demo_all
Or from package root: python examples/demo_all.py
"""

import sys
import time
from pathlib import Path

# Add src to path if running from examples directory
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import claude_terminal_ui as ui


def demo_status_messages():
    """Demonstrate status message components"""
    print(ui.header("Status Messages", width=60))
    print()
    ui.print_success("Operation completed successfully")
    ui.print_error("Failed to connect to database")
    ui.print_warning("Disk space running low")
    ui.print_info("Processing 1,234 files...")
    ui.print_debug("Cache hit ratio: 85%")
    print()


def demo_headers():
    """Demonstrate header components"""
    print(ui.header("Major Section Header"))
    print()
    print(ui.subheader("Subsection Header"))
    print()
    print(ui.divider(label="Step 1"))
    print()


def demo_progress():
    """Demonstrate progress indicators"""
    print(ui.header("Progress Indicators", width=60))
    print()

    # Static progress bars
    print("Static bars:")
    for pct in [0, 25, 50, 75, 100]:
        bar = ui.progress_bar(pct, 100, width=30)
        print(f"  {bar}")

    print()
    print("Step indicators:")
    for i in range(1, 6):
        print(ui.step_indicator(i, 5, f"Processing item {i}"))

    # Animated spinner (if interactive)
    print()
    print("Spinner demo (2 seconds):")
    with ui.spinner("Loading data"):
        time.sleep(2)
    ui.print_success("Data loaded!")
    print()


def demo_terminal_info():
    """Show detected terminal capabilities"""
    from claude_terminal_ui.core.capabilities import get_capabilities

    caps = get_capabilities()

    print(ui.header("Terminal Capabilities", width=60))
    print()
    print(f"Terminal Name:      {caps.terminal_name}")
    print(f"Color Support:      {caps.color_support.name} ({caps.color_support.value} colors)")
    print(f"Unicode Support:    {'Yes' if caps.unicode_support else 'No (ASCII fallback)'}")
    print(f"Terminal Size:      {caps.width}x{caps.height}")
    print(f"Interactive:        {'Yes' if caps.is_interactive else 'No'}")
    print(f"Platform:           {'Windows' if caps.is_windows else 'Unix/Linux/macOS'}")
    print(f"Hyperlink Support:  {'Yes' if caps.supports_hyperlinks else 'No'}")
    print()


def main():
    """Run all demos"""
    print()
    print(ui.header("Claude Terminal UI - Component Showcase", width=70))
    print()

    demo_terminal_info()
    input("\nPress Enter to continue...")

    demo_status_messages()
    input("\nPress Enter to continue...")

    demo_headers()
    input("\nPress Enter to continue...")

    demo_progress()

    print()
    print(ui.header("Demo Complete", width=70))
    print()
    ui.print_success("All components demonstrated!")


if __name__ == "__main__":
    main()
