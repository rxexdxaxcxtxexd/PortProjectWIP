#!/usr/bin/env python3
"""
Test script for table formatting components.

Demonstrates all table formatting functions with various options.
"""

from claude_terminal_ui.components.tables import (
    key_value,
    table,
    stats_panel,
    print_key_value,
    print_table,
    print_stats_panel,
)
from claude_terminal_ui.tokens.colors import Colors
from claude_terminal_ui.tokens.spacing import DEFAULT_WIDTH, WIDE_WIDTH


def test_key_value():
    """Test key-value pair formatting"""
    print("\n" + "=" * 70)
    print("TEST: key_value() - Basic formatting")
    print("=" * 70)

    items = {
        "Session": "5150ba34",
        "Started": "2025-12-29 12:49",
        "Tokens": "1,234 / 200,000",
        "Status": "Active",
    }

    print("\nBasic aligned key-value pairs:")
    print(key_value(items, indent=2))

    print("\nWith value coloring:")
    print(key_value(items, indent=2, value_color=Colors.INFO))

    print("\nWithout alignment:")
    print(key_value(items, indent=2, align_colon=False))


def test_table_basic():
    """Test basic table formatting"""
    print("\n" + "=" * 70)
    print("TEST: table() - Basic table")
    print("=" * 70)

    headers = ["Key", "Status", "Count"]
    data = [
        ["BOPS-123", "Done", "5"],
        ["BOPS-124", "Active", "12"],
        ["BOPS-125", "Pending", "3"],
    ]

    print("\nBasic table with borders:")
    print(table(data, headers))

    print("\nTable without borders:")
    print(table(data, headers, show_borders=False))

    print("\nCompact table:")
    print(table(data, headers, compact=True))


def test_table_alignment():
    """Test table column alignment"""
    print("\n" + "=" * 70)
    print("TEST: table() - Column alignment")
    print("=" * 70)

    headers = ["Name", "Amount", "Status"]
    data = [
        ["Invoice #1", "1,234.56", "Paid"],
        ["Invoice #2", "567.89", "Pending"],
        ["Invoice #3", "12,345.00", "Paid"],
    ]

    print("\nRight-aligned amounts:")
    print(table(data, headers, align=["left", "right", "left"]))

    print("\nCentered status:")
    print(table(data, headers, align=["left", "right", "center"]))


def test_table_wide():
    """Test wide table with WIDE_WIDTH"""
    print("\n" + "=" * 100)
    print("TEST: table() - Wide table (WIDE_WIDTH)")
    print("=" * 100)

    headers = ["Ticket Key", "Summary", "Status", "Account"]
    data = [
        ["BOPS-3597", "Missing license-dependent filters", "Groomed", "None"],
        ["BOPS-3665", "Crews - Boat Detail Show Manning", "IN CSG QA/UVT", "BargeOps Maintenance"],
        ["BOPS-3614", "Licensing screen missing", "In Code Review", "None"],
    ]

    print(table(data, headers, width=WIDE_WIDTH))


def test_table_colored():
    """Test table with colored headers"""
    print("\n" + "=" * 70)
    print("TEST: table() - Colored headers")
    print("=" * 70)

    headers = ["Project", "Status", "Progress"]
    data = [
        ["API Agent", "Active", "85%"],
        ["Terminal UI", "Active", "92%"],
        ["Session Tracker", "Complete", "100%"],
    ]

    print(table(data, headers, header_color=Colors.ACCENT))


def test_stats_panel_list():
    """Test stats panel in list layout"""
    print("\n" + "=" * 70)
    print("TEST: stats_panel() - List layout")
    print("=" * 70)

    stats = {
        "Total Tickets": 50,
        "With Account": 35,
        "Without Account": 15,
        "Completion Rate": "92.3%",
    }

    print("\nList layout with borders:")
    print(stats_panel(stats, title="STATISTICS SUMMARY", layout="list"))

    print("\nList layout without borders:")
    print(stats_panel(stats, title="Summary", layout="list", show_borders=False))


def test_stats_panel_grid():
    """Test stats panel in grid layout"""
    print("\n" + "=" * 70)
    print("TEST: stats_panel() - Grid layout")
    print("=" * 70)

    stats = {
        "Total": 100,
        "Active": 25,
        "Complete": 70,
        "Pending": 5,
        "Failed": 0,
        "Skipped": 0,
    }

    print("\nGrid layout (2 columns):")
    print(stats_panel(stats, title="TEST RESULTS", layout="grid", columns=2))

    print("\nGrid layout (3 columns):")
    print(stats_panel(stats, title="TEST RESULTS", layout="grid", columns=3))

    print("\nColored title:")
    print(stats_panel(stats, title="TEST RESULTS", layout="grid", columns=2, title_color=Colors.SUCCESS))


def test_context_monitor_example():
    """Test recreating context-monitor.py output"""
    print("\n" + "=" * 70)
    print("TEST: Recreate context-monitor.py output")
    print("=" * 70)

    session_info = {
        "Session ID": "5150ba34",
        "History Entries": 42,
        "Time Range": "2025-12-29 12:49:35 -> 2025-12-29 14:32:10",
    }

    print("\nSession Information:")
    print(key_value(session_info, indent=0))

    context_stats = {
        "Estimated Tokens": "~45,000 / 200,000",
        "Usage": "~22.5%",
        "Remaining": "~155,000 tokens (~77.5%)",
    }

    print("\nContext Usage (APPROXIMATION):")
    print(key_value(context_stats, indent=2))


def test_audit_report_example():
    """Test recreating BOPS audit report table"""
    print("\n" + "=" * 100)
    print("TEST: Recreate BOPS audit report")
    print("=" * 100)

    # Summary stats
    stats = {
        "Total Tickets": 50,
        "With Account": "35 (70.0%)",
        "Without Account": "15 (30.0%)",
    }

    print("\nSUMMARY")
    print(key_value(stats, indent=2))

    # Account breakdown
    print("\nACCOUNT BREAKDOWN")
    headers = ["Account", "Count"]
    data = [
        ["BargeOps Maintenance", "18"],
        ["BargeOps R&D", "6"],
        ["PTC BargeOps Support - T&M", "4"],
    ]
    print(table(data, headers, width=WIDE_WIDTH))

    # Tickets table
    print("\nTICKETS WITH ACCOUNT FIELD")
    headers = ["Key", "Status", "Account", "Summary"]
    data = [
        ["BOPS-3665", "IN CSG QA/UVT", "BargeOps Maintenance", "Crews - Boat Detail..."],
        ["BOPS-3663", "IN CSG QA/UVT", "BargeOps Maintenance", "Onboard: Night mode..."],
        ["BOPS-3656", "IN CSG QA/UVT", "BargeOps Maintenance", "New Trip Planner..."],
    ]
    print(table(data, headers, width=WIDE_WIDTH))


def test_print_functions():
    """Test print_* convenience functions"""
    print("\n" + "=" * 70)
    print("TEST: print_* convenience functions")
    print("=" * 70)

    print("\nUsing print_key_value():")
    print_key_value({"Name": "Test", "Value": 123}, indent=2)

    print("\nUsing print_table():")
    print_table([["A", "B"], ["C", "D"]], headers=["Col1", "Col2"])

    print("\nUsing print_stats_panel():")
    print_stats_panel({"Total": 10, "Active": 5}, title="Stats", layout="list")


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print(" " * 20 + "TABLE COMPONENTS TEST SUITE")
    print("=" * 70)

    test_key_value()
    test_table_basic()
    test_table_alignment()
    test_table_wide()
    test_table_colored()
    test_stats_panel_list()
    test_stats_panel_grid()
    test_context_monitor_example()
    test_audit_report_example()
    test_print_functions()

    print("\n" + "=" * 70)
    print(" " * 25 + "ALL TESTS COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
