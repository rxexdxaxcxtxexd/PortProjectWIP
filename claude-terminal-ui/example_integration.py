#!/usr/bin/env python3
"""
Integration Example: Using table components in real scripts

Shows how to refactor existing scripts (context-monitor.py, bops_complete_audit.py)
to use the new table formatting components.
"""

import claude_terminal_ui as ui
from claude_terminal_ui.tokens.spacing import DEFAULT_WIDTH, WIDE_WIDTH
from claude_terminal_ui.tokens.colors import Colors


def example_context_monitor_refactored():
    """
    Example: Refactored context-monitor.py output using table components

    BEFORE: Manual string formatting
    AFTER: Clean component-based output
    """
    print(ui.header("CONTEXT WINDOW MONITOR", width=DEFAULT_WIDTH))
    print()

    # Session metadata as key-value pairs
    session_info = {
        "Session ID": "5150ba34",
        "History Entries": "42",
        "Time Range": "2025-12-29 12:49:35 -> 2025-12-29 14:32:10",
    }

    ui.print_key_value(session_info, indent=0)
    print()

    # Context usage statistics
    print(ui.subheader("Context Usage (APPROXIMATION)", width=DEFAULT_WIDTH))

    context_stats = {
        "Estimated Tokens": "~45,000 / 200,000",
        "Usage": "~22.5%",
        "Remaining": "~155,000 tokens (~77.5%)",
    }

    ui.print_key_value(context_stats, indent=2)
    print()

    print("  Note: Estimates based on user input only. Actual usage includes")
    print("        Claude's responses, tool calls, and system context.")
    print()

    # Visual progress bar
    bar_width = 50
    filled = int(0.225 * bar_width)
    bar = '=' * filled + '-' * (bar_width - filled)
    print(f"  [{bar}]")
    print()

    # Recommendation
    ui.print_info("Context usage is getting high.", indent=2)
    print("   SUGGESTED: Plan to checkpoint at next milestone.")
    print("   -> python scripts/checkpoint.py --quick")
    print()

    print("=" * DEFAULT_WIDTH)


def example_bops_audit_refactored():
    """
    Example: Refactored BOPS audit report using table components

    BEFORE: Manual table drawing with print statements
    AFTER: Clean table() calls with proper formatting
    """
    print(ui.header("BOPS BOARD 38 AUDIT REPORT", width=WIDE_WIDTH))
    print()

    metadata = {
        "Generated": "2025-12-29 14:32:10",
        "Time Range": "Last 30 days (updated >= -30d)",
        "Account Field": "customfield_10300",
    }

    ui.print_key_value(metadata, indent=0)
    print()
    print("=" * WIDE_WIDTH)
    print()

    # Summary statistics
    print(ui.subheader("SUMMARY", width=WIDE_WIDTH))

    summary = {
        "Total Tickets": "50",
        "[+] With Account": "35 (70.0%)",
        "[-] Without Account": "15 (30.0%)",
    }

    ui.print_key_value(summary, indent=2)
    print()

    # Account breakdown table
    print(ui.subheader("ACCOUNT BREAKDOWN", width=WIDE_WIDTH))

    headers = ["Account", "Tickets", "Percentage"]
    accounts = [
        ["BargeOps Maintenance", "18", "36%"],
        ["BargeOps R&D", "6", "12%"],
        ["PTC BargeOps Support - T&M", "4", "8%"],
        ["Other Accounts", "7", "14%"],
    ]

    ui.print_table(
        accounts,
        headers,
        align=["left", "right", "right"],
        width=WIDE_WIDTH
    )
    print()

    # Detailed tickets table
    print(ui.divider(label="TICKETS WITH ACCOUNT FIELD (35 tickets)", width=WIDE_WIDTH))

    headers = ["Key", "Status", "Account", "Summary"]
    tickets = [
        ["BOPS-3665", "IN CSG QA/UVT", "BargeOps Maintenance", "Crews - Boat Detail Show Manning..."],
        ["BOPS-3663", "IN CSG QA/UVT", "BargeOps Maintenance", "Onboard: Night mode fuel value..."],
        ["BOPS-3656", "IN CSG QA/UVT", "BargeOps Maintenance", "New Trip Planner issues"],
        ["BOPS-3662", "IN CSG QA/UVT", "BargeOps Maintenance", "Requested Draft cleared when..."],
        ["BOPS-3659", "In Progress", "PTC BargeOps Support", "Update Cargo Storage Invoice..."],
    ]

    ui.print_table(
        tickets,
        headers,
        width=WIDE_WIDTH,
        header_color=Colors.ACCENT
    )
    print()

    ui.print_info("Showing first 5 tickets. 30 more available in full report.")
    print()

    # Tickets without account
    print(ui.divider(label="TICKETS WITHOUT ACCOUNT FIELD (15 tickets)", width=WIDE_WIDTH))

    headers = ["Key", "Status", "Summary"]
    no_account_tickets = [
        ["BOPS-3597", "Groomed", "Missing license-dependent filters (Assist Tugs Only)"],
        ["BOPS-3614", "In Code Review", "Licensing screen missing"],
        ["BOPS-3550", "New", "Create Test Project Cursor"],
    ]

    ui.print_table(no_account_tickets, headers, width=WIDE_WIDTH)
    print()

    ui.print_warning("These tickets should have an account field assigned!")
    print()

    print("=" * WIDE_WIDTH)
    ui.print_success("Report complete! Exported to: bops_audit_20251229.csv")
    print("=" * WIDE_WIDTH)
    print()


def example_sprint_report():
    """
    Example: Sprint velocity report with statistics panel
    """
    print(ui.header("ADMIN WEB APP V2 - SPRINT 12 REPORT"))
    print()

    # Sprint metadata
    sprint_info = {
        "Sprint": "Sprint 12",
        "Date Range": "2025-12-16 to 2025-12-29",
        "Team": "Admin Screens Team",
        "Focus": "Core admin screens development",
    }

    ui.print_key_value(sprint_info, indent=2, value_color=Colors.INFO)
    print()

    # Sprint statistics in grid
    sprint_stats = {
        "Total Stories": 24,
        "Completed": 20,
        "In Progress": 3,
        "Blocked": 1,
        "Story Points": 45,
        "Velocity": "37.5 pts",
    }

    ui.print_stats_panel(
        sprint_stats,
        title="SPRINT METRICS",
        layout="grid",
        columns=2,
        title_color=Colors.SUCCESS
    )
    print()

    # Completed stories table
    print(ui.subheader("COMPLETED STORIES (20)", width=DEFAULT_WIDTH))

    headers = ["Screen", "Points", "Status"]
    stories = [
        ["Boat Admin", "8", "Done"],
        ["Crew Management", "5", "Done"],
        ["Fuel Price Admin", "3", "Done"],
        ["Global Settings", "5", "Done"],
        ["Boat Status", "3", "Done"],
    ]

    ui.print_table(stories, headers, align=["left", "right", "left"])
    print()

    # Progress comparison
    print(ui.subheader("PROGRESS COMPARISON", width=DEFAULT_WIDTH))

    headers = ["Week", "Stories", "Points", "Velocity"]
    weeks = [
        ["Week 1", "5", "12", "12.0"],
        ["Week 2", "8", "18", "15.0"],
    ]

    ui.print_table(weeks, headers, align=["left", "right", "right", "right"])
    print()

    ui.print_success("Sprint 12 on track for completion!")
    print()


def example_dependency_analysis():
    """
    Example: Dependency analysis with impact scoring
    """
    print(ui.header("DEPENDENCY ANALYSIS REPORT"))
    print()

    # Analysis metadata
    analysis_info = {
        "Project": "api-documentation-agent",
        "Files Analyzed": "16 Python files",
        "Dependencies Found": "45 imports",
        "High Impact Files": "2 (score >= 70)",
    }

    ui.print_key_value(analysis_info, indent=2)
    print()

    # High-impact files
    print(ui.subheader("HIGH-IMPACT FILES", width=DEFAULT_WIDTH))

    headers = ["File", "Imported By", "Impact Score", "Tests"]
    files = [
        ["payment.py", "12 files", "85", "✓"],
        ["database.py", "8 files", "72", "✓"],
        ["api_client.py", "6 files", "58", "✗"],
    ]

    ui.print_table(
        files,
        headers,
        align=["left", "right", "right", "center"],
        header_color=Colors.WARNING
    )
    print()

    ui.print_warning("payment.py is used by 12 files - test thoroughly!")
    ui.print_error("api_client.py has no tests - create test_api_client.py", indent=0)
    print()


def main():
    """Run all integration examples"""
    print()
    print("=" * 70)
    print(" " * 15 + "TABLE INTEGRATION EXAMPLES")
    print("=" * 70)
    print()
    print("These examples show how to refactor existing scripts to use")
    print("the table formatting components for cleaner, more maintainable code.")
    print()
    print("=" * 70)
    print()

    example_context_monitor_refactored()
    print("\n\n")

    example_bops_audit_refactored()
    print("\n\n")

    example_sprint_report()
    print("\n\n")

    example_dependency_analysis()
    print("\n\n")

    print("=" * 70)
    print(" " * 20 + "EXAMPLES COMPLETE")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
