#!/usr/bin/env python3
"""
Portfolio Status Display - Beautiful CLI for Context-Aware Memory System

Displays session analytics, lifetime statistics, and project breakdowns
with beautiful terminal formatting using claude-terminal-ui components.

Usage:
    python status.py                    # Show all sections
    python status.py --current          # Current session only
    python status.py --lifetime         # Lifetime stats only
    python status.py --days 30          # Last 30 days
    python status.py --export json      # Export to JSON
"""

import sys
import os
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add claude-terminal-ui to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'claude-terminal-ui' / 'src'))

from claude_terminal_ui.components.headers import header, divider
from claude_terminal_ui.components.panels import panel, compact_panel, info_panel
from claude_terminal_ui.components.tables import key_value, table, stats_panel
from claude_terminal_ui.tokens.colors import Colors
from claude_terminal_ui.tokens.symbols import Symbols

# Import analytics DB
from analytics_db import AnalyticsDB

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_current_session_info() -> Dict[str, Any]:
    """
    Get current session information from the most recent checkpoint.

    Returns:
        Dictionary with current session data
    """
    # Look for current session file (implementation depends on session tracking)
    session_dir = Path.home() / '.claude-sessions'

    if not session_dir.exists():
        return {
            'session_id': 'No active session',
            'status': 'Not tracking',
            'duration': 'N/A',
            'files_changed': 0
        }

    # Find most recent session
    try:
        checkpoint_files = sorted(session_dir.glob('*.checkpoint.json'), reverse=True)
        if not checkpoint_files:
            return {
                'session_id': 'No sessions found',
                'status': 'No checkpoints',
                'duration': 'N/A',
                'files_changed': 0
            }

        # Read most recent checkpoint
        with open(checkpoint_files[0], 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)

        session_id = checkpoint.get('session_id', 'Unknown')[:8]
        timestamp = checkpoint.get('timestamp')
        started_at = checkpoint.get('started_at')
        files_changed = len(checkpoint.get('file_changes', []))

        # Calculate duration if available
        duration = 'N/A'
        if started_at and timestamp:
            try:
                start = datetime.fromisoformat(started_at)
                end = datetime.fromisoformat(timestamp)
                delta = end - start
                hours = delta.total_seconds() / 3600
                duration = f"{hours:.1f} hours"
            except Exception:
                pass

        return {
            'session_id': session_id,
            'status': 'Active' if (datetime.now() - datetime.fromisoformat(timestamp)).total_seconds() < 3600 else 'Inactive',
            'duration': duration,
            'files_changed': files_changed,
            'timestamp': timestamp
        }

    except Exception as e:
        logger.warning(f"Error reading current session: {e}")
        return {
            'session_id': 'Error',
            'status': 'Unknown',
            'duration': 'N/A',
            'files_changed': 0
        }


def display_current_session(db: AnalyticsDB) -> None:
    """
    Display current session information.

    Args:
        db: AnalyticsDB instance
    """
    session_info = get_current_session_info()

    # Header
    print("\n")
    print(divider(char="━", label="CURRENT SESSION", width=70))
    print()

    # Session details
    status_symbol = Symbols.SUCCESS.render() if session_info['status'] == 'Active' else Symbols.INFO.render()

    data = {
        'Session ID': session_info['session_id'],
        'Duration': session_info['duration'],
        'Files Changed': session_info['files_changed'],
        'Status': f"{status_symbol} {session_info['status']}"
    }

    print(key_value(data, indent=2))
    print()


def display_lifetime_stats(db: AnalyticsDB, days: Optional[int] = None) -> None:
    """
    Display lifetime statistics with visual polish.

    Args:
        db: AnalyticsDB instance
        days: Number of days for stats (None for all-time)
    """
    # Get stats
    if days:
        stats = db.get_session_stats(days=days)
        period_label = f"LIFETIME STATISTICS (Last {days} Days)"
    else:
        stats = db.get_aggregate_stats()
        period_label = "LIFETIME STATISTICS (All Time)"

    # Header
    print(divider(char="━", label=period_label, width=70))
    print()

    # Extract stats
    total_sessions = stats.get('total_sessions', 0)
    time_saved_hours = stats.get('time_saved_hours', 0)
    work_days_saved = time_saved_hours / 8
    success_rate = stats.get('success_rate', 0)
    successful_sessions = stats.get('successful_sessions', 0)
    total_decisions = stats.get('total_decisions', 0)
    total_resume_points = stats.get('total_resume_points', 0)

    # Calculate token efficiency estimate
    total_tokens = stats.get('total_tokens_saved', 0)
    if total_tokens > 0 and total_sessions > 0:
        baseline_tokens = total_sessions * 200000
        token_efficiency = (total_tokens / baseline_tokens) * 100
    else:
        token_efficiency = 0.0

    # Format data
    data = {
        'Total Sessions': f"{total_sessions:,}",
        'Time Saved': f"{time_saved_hours:.1f} hours ({work_days_saved:.1f} work days)",
        'Success Rate': f"{success_rate:.1f}% ({successful_sessions}/{total_sessions} successful)",
        'Decisions Preserved': f"{total_decisions:,}",
        'Resume Points': f"{total_resume_points:,}"
    }

    if token_efficiency > 0:
        data['Token Efficiency'] = f"{token_efficiency:.1f}% reduction"

    print(key_value(data, indent=2))
    print()


def display_project_breakdown(db: AnalyticsDB) -> None:
    """
    Display statistics broken down by project.

    Args:
        db: AnalyticsDB instance
    """
    projects = db.get_project_breakdown()

    if not projects:
        print(info_panel("No project data available", panel_type="info"))
        return

    # Header
    print(divider(char="━", label="PROJECT BREAKDOWN", width=70))
    print()

    # Build table data
    headers = ['Project', 'Sessions', 'Success %', 'Files', 'Decisions']
    rows = []

    total_sessions = sum(p['total_sessions'] for p in projects)

    for project in projects:
        project_name = project['project_name']
        sessions = project['total_sessions']
        success_rate = project['success_rate']
        files = project['total_files_changed']
        decisions = project['total_decisions']

        # Calculate percentage
        percentage = (sessions / total_sessions * 100) if total_sessions > 0 else 0

        # Format row
        row = [
            project_name[:30],  # Truncate long names
            f"{sessions} ({percentage:.1f}%)",
            f"{success_rate:.1f}%",
            str(files),
            str(decisions)
        ]
        rows.append(row)

    # Display table
    print(table(rows, headers=headers, align=['left', 'right', 'right', 'right', 'right']))
    print()


def display_recent_activity(db: AnalyticsDB, limit: int = 5) -> None:
    """
    Display recent session activity.

    Args:
        db: AnalyticsDB instance
        limit: Number of recent sessions to show
    """
    cursor = db.conn.cursor()

    try:
        cursor.execute("""
            SELECT
                session_id,
                timestamp,
                project_name,
                files_changed,
                decisions_logged,
                checkpoint_success
            FROM sessions
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))

        sessions = cursor.fetchall()

        if not sessions:
            print(info_panel("No recent activity", panel_type="info"))
            return

        # Header
        print(divider(char="━", label=f"RECENT ACTIVITY (Last {limit} Sessions)", width=70))
        print()

        # Build table
        headers = ['Session ID', 'Time', 'Project', 'Files', 'Decisions']
        rows = []

        for session in sessions:
            session_id = session['session_id'][:8]
            timestamp = datetime.fromisoformat(session['timestamp'])
            time_str = timestamp.strftime('%m/%d %H:%M')
            project = session['project_name'][:20]
            files = session['files_changed']
            decisions = session['decisions_logged']
            success = session['checkpoint_success']

            # Add status indicator
            status = Symbols.SUCCESS.render() if success else Symbols.ERROR.render()

            rows.append([
                f"{status} {session_id}",
                time_str,
                project,
                str(files),
                str(decisions)
            ])

        print(table(rows, headers=headers, align=['left', 'left', 'left', 'right', 'right']))
        print()

    except Exception as e:
        logger.error(f"Failed to fetch recent activity: {e}")


def export_stats_json(db: AnalyticsDB, output_path: str, days: Optional[int] = None) -> None:
    """
    Export statistics to JSON format.

    Args:
        db: AnalyticsDB instance
        output_path: Output file path
        days: Number of days for stats (None for all-time)
    """
    # Gather all data
    if days:
        stats = db.get_session_stats(days=days)
    else:
        stats = db.get_aggregate_stats()

    projects = db.get_project_breakdown()

    # Build export data
    export_data = {
        'generated_at': datetime.now().isoformat(),
        'period_days': days if days else 'all_time',
        'summary': stats,
        'projects': projects
    }

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, default=str)

    logger.info(f"Exported JSON to {output_path}")
    print(info_panel(f"Exported to {output_path}", panel_type="success"))


def export_stats_csv(db: AnalyticsDB, output_path: str, days: Optional[int] = None) -> None:
    """
    Export project statistics to CSV format.

    Args:
        db: AnalyticsDB instance
        output_path: Output file path
        days: Number of days for stats (None for all-time)
    """
    projects = db.get_project_breakdown()

    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'Project',
            'Total Sessions',
            'Successful Sessions',
            'Success Rate %',
            'Files Changed',
            'Decisions Logged',
            'First Session',
            'Last Session'
        ])

        # Data rows
        for project in projects:
            writer.writerow([
                project['project_name'],
                project['total_sessions'],
                project['successful_sessions'],
                f"{project['success_rate']:.1f}",
                project['total_files_changed'],
                project['total_decisions'],
                project['first_session'],
                project['last_session']
            ])

    logger.info(f"Exported CSV to {output_path}")
    print(info_panel(f"Exported to {output_path}", panel_type="success"))


def export_stats_markdown(db: AnalyticsDB, output_path: str, days: Optional[int] = None) -> None:
    """
    Export statistics to Markdown format.

    Args:
        db: AnalyticsDB instance
        output_path: Output file path
        days: Number of days for stats (None for all-time)
    """
    # Get stats
    if days:
        stats = db.get_session_stats(days=days)
        period_label = f"Last {days} Days"
    else:
        stats = db.get_aggregate_stats()
        period_label = "All Time"

    projects = db.get_project_breakdown()

    # Build markdown
    lines = []

    # Header
    lines.append(f"# Context-Aware Memory System - Portfolio Statistics")
    lines.append(f"")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Period:** {period_label}")
    lines.append(f"")

    # Summary statistics
    lines.append("## Summary Statistics")
    lines.append("")

    total_sessions = stats.get('total_sessions', 0)
    time_saved = stats.get('time_saved_hours', 0)
    work_days = time_saved / 8
    success_rate = stats.get('success_rate', 0)
    successful = stats.get('successful_sessions', 0)
    decisions = stats.get('total_decisions', 0)
    resume_points = stats.get('total_resume_points', 0)

    lines.append(f"- **Total Sessions:** {total_sessions:,}")
    lines.append(f"- **Time Saved:** {time_saved:.1f} hours ({work_days:.1f} work days)")
    lines.append(f"- **Success Rate:** {success_rate:.1f}% ({successful}/{total_sessions} successful)")
    lines.append(f"- **Decisions Preserved:** {decisions:,}")
    lines.append(f"- **Resume Points Generated:** {resume_points:,}")
    lines.append("")

    # Project breakdown
    if projects:
        lines.append("## Project Breakdown")
        lines.append("")
        lines.append("| Project | Sessions | Success Rate | Files Changed | Decisions |")
        lines.append("|---------|----------|--------------|---------------|-----------|")

        for project in projects:
            name = project['project_name']
            sessions = project['total_sessions']
            rate = project['success_rate']
            files = project['total_files_changed']
            decs = project['total_decisions']

            lines.append(f"| {name} | {sessions} | {rate:.1f}% | {files} | {decs} |")

        lines.append("")

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    logger.info(f"Exported Markdown to {output_path}")
    print(info_panel(f"Exported to {output_path}", panel_type="success"))


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Display beautiful portfolio status and statistics"
    )

    # Display options
    parser.add_argument(
        '--current',
        action='store_true',
        help='Show current session only'
    )
    parser.add_argument(
        '--lifetime',
        action='store_true',
        help='Show lifetime statistics only'
    )
    parser.add_argument(
        '--projects',
        action='store_true',
        help='Show project breakdown only'
    )
    parser.add_argument(
        '--recent',
        type=int,
        metavar='N',
        help='Show N recent sessions'
    )
    parser.add_argument(
        '--days',
        type=int,
        help='Number of days for statistics (default: all-time)'
    )

    # Export options
    parser.add_argument(
        '--export',
        choices=['json', 'csv', 'markdown'],
        help='Export format'
    )
    parser.add_argument(
        '--output',
        help='Output file path for export'
    )

    # Database option
    parser.add_argument(
        '--db-path',
        help='Path to analytics database',
        default=None
    )

    args = parser.parse_args()

    # Initialize database
    try:
        db = AnalyticsDB(db_path=args.db_path)
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        print(info_panel(f"Database error: {e}", panel_type="error"))
        return 1

    try:
        # Handle export
        if args.export:
            if not args.output:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                args.output = f"portfolio_stats_{timestamp}.{args.export}"

            if args.export == 'json':
                export_stats_json(db, args.output, days=args.days)
            elif args.export == 'csv':
                export_stats_csv(db, args.output, days=args.days)
            elif args.export == 'markdown':
                export_stats_markdown(db, args.output, days=args.days)

            return 0

        # Display sections based on arguments
        show_all = not any([args.current, args.lifetime, args.projects, args.recent])

        # Main header
        if show_all or args.lifetime:
            print()
            title = "CONTEXT-AWARE MEMORY SYSTEM - PORTFOLIO STATUS"
            print(header(title, width=70, char="═", color=Colors.INFO))

        # Current session
        if show_all or args.current:
            display_current_session(db)

        # Lifetime stats
        if show_all or args.lifetime:
            display_lifetime_stats(db, days=args.days)

        # Project breakdown
        if show_all or args.projects:
            display_project_breakdown(db)

        # Recent activity
        if args.recent or show_all:
            limit = args.recent if args.recent else 5
            display_recent_activity(db, limit=limit)

        print()
        return 0

    except Exception as e:
        logger.error(f"Error displaying status: {e}")
        print(info_panel(f"Error: {e}", panel_type="error"))
        return 1

    finally:
        db.close()


if __name__ == '__main__':
    sys.exit(main())
