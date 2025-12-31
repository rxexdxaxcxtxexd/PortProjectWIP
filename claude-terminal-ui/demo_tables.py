#!/usr/bin/env python3
"""
Interactive demo of table formatting components.

Run this in a terminal to see properly rendered output with colors.
"""

import claude_terminal_ui as ui


def demo_session_info():
    """Demo: Session information display"""
    print(ui.header("SESSION INFORMATION"))
    print()

    session_data = {
        "Session ID": "5150ba34",
        "Started": "2025-12-29 12:49:35",
        "Duration": "1h 42m",
        "Messages": "42",
    }

    ui.print_key_value(session_data, indent=2, value_color=ui.tokens.colors.Colors.INFO)
    print()


def demo_context_usage():
    """Demo: Context window usage"""
    print(ui.header("CONTEXT WINDOW STATUS"))
    print()

    context_info = {
        "Estimated Tokens": "~45,000 / 200,000",
        "Usage": "~22.5%",
        "Remaining": "~155,000 tokens",
    }

    ui.print_key_value(context_info, indent=2)
    print()


def demo_ticket_table():
    """Demo: Ticket tracking table"""
    print(ui.header("RECENT TICKETS"))
    print()

    headers = ["Ticket", "Status", "Priority", "Assignee"]
    tickets = [
        ["BOPS-3665", "In QA", "High", "Alice"],
        ["BOPS-3663", "In QA", "Medium", "Bob"],
        ["BOPS-3656", "In Progress", "High", "Charlie"],
        ["BOPS-3614", "Code Review", "Low", "Alice"],
    ]

    ui.print_table(tickets, headers, header_color=ui.tokens.colors.Colors.ACCENT)
    print()


def demo_statistics():
    """Demo: Statistics panel"""
    print(ui.header("PROJECT STATISTICS"))
    print()

    stats = {
        "Total": 100,
        "Complete": 85,
        "In Progress": 12,
        "Blocked": 3,
    }

    ui.print_stats_panel(
        stats,
        title="Sprint 12 Summary",
        layout="grid",
        columns=2,
        title_color=ui.tokens.colors.Colors.SUCCESS,
    )
    print()


def demo_audit_summary():
    """Demo: Audit report summary"""
    print(ui.header("BOPS AUDIT REPORT", width=ui.tokens.spacing.WIDE_WIDTH))
    print()

    print(ui.subheader("Summary Statistics"))
    summary = {
        "Total Tickets": 50,
        "With Account": "35 (70%)",
        "Without Account": "15 (30%)",
        "Last Updated": "2025-12-29",
    }
    ui.print_key_value(summary, indent=2)
    print()

    print(ui.subheader("Top Accounts"))
    headers = ["Account", "Tickets", "Percentage"]
    accounts = [
        ["BargeOps Maintenance", "18", "36%"],
        ["BargeOps R&D", "6", "12%"],
        ["PTC BargeOps Support", "4", "8%"],
        ["Other", "7", "14%"],
    ]
    ui.print_table(
        accounts,
        headers,
        align=["left", "right", "right"],
        width=ui.tokens.spacing.WIDE_WIDTH,
    )
    print()


def demo_comparison_table():
    """Demo: Before/after comparison"""
    print(ui.header("PERFORMANCE COMPARISON"))
    print()

    headers = ["Metric", "Before", "After", "Change"]
    data = [
        ["Load Time", "2.5s", "0.8s", "-68%"],
        ["Memory Usage", "450MB", "280MB", "-38%"],
        ["API Calls", "125", "45", "-64%"],
    ]

    ui.print_table(data, headers, align=["left", "right", "right", "right"])
    print()


def main():
    """Run all demos"""
    print()
    print("=" * 70)
    print(" " * 15 + "TABLE COMPONENTS DEMO")
    print("=" * 70)
    print()

    demo_session_info()
    demo_context_usage()
    demo_ticket_table()
    demo_statistics()
    demo_audit_summary()
    demo_comparison_table()

    print("=" * 70)
    print(" " * 20 + "DEMO COMPLETE")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
