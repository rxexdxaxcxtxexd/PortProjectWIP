#!/usr/bin/env python3
"""
Badge Generator for Context-Aware Memory System Portfolio

Generates shields.io badges to display portfolio metrics beautifully
in README files and documentation.

Usage:
    from badge_generator import generate_stats_badges, generate_badge_markdown

    db = AnalyticsDB()
    badges = generate_stats_badges(db)
    markdown = generate_badge_markdown(badges)
    print(markdown)
"""

from typing import Dict, List, Optional
from urllib.parse import quote
import logging
from analytics_db import AnalyticsDB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_badge_url(label: str, message: str, color: str) -> str:
    """
    Generate a shields.io badge URL.

    Args:
        label: Badge label (left side)
        message: Badge message (right side)
        color: Badge color (blue, green, brightgreen, orange, red, etc.)

    Returns:
        Full shields.io URL

    Example:
        >>> generate_badge_url("sessions", "87", "blue")
        'https://img.shields.io/badge/sessions-87-blue'
    """
    # URL-encode special characters
    label_encoded = quote(label.replace('-', '--').replace('_', '__'))
    message_encoded = quote(message.replace('-', '--').replace('_', '__'))

    return f"https://img.shields.io/badge/{label_encoded}-{message_encoded}-{color}"


def generate_stats_badges(db: AnalyticsDB, days: Optional[int] = None) -> Dict[str, Dict[str, str]]:
    """
    Generate all portfolio badges from analytics database.

    Args:
        db: AnalyticsDB instance
        days: Number of days for stats (None for all-time)

    Returns:
        Dictionary mapping badge names to badge data (url, alt_text, description)

    Example:
        {
            'sessions': {
                'url': 'https://img.shields.io/badge/...',
                'alt_text': 'Total Sessions',
                'description': 'Number of session continuity checkpoints'
            },
            ...
        }
    """
    badges = {}

    try:
        # Get statistics
        if days:
            stats = db.get_session_stats(days=days)
            period_label = f"{days} Days"
        else:
            stats = db.get_aggregate_stats()
            period_label = "All Time"

        # Sessions badge
        total_sessions = stats.get('total_sessions', 0)
        badges['sessions'] = {
            'url': generate_badge_url('sessions', str(total_sessions), 'blue'),
            'alt_text': f'Total Sessions ({period_label})',
            'description': 'Number of session continuity checkpoints'
        }

        # Time Saved badge
        time_saved = stats.get('time_saved_hours', 0)
        time_display = f"{time_saved:.1f} hours"
        badges['time_saved'] = {
            'url': generate_badge_url('time saved', time_display, 'green'),
            'alt_text': f'Time Saved ({period_label})',
            'description': 'Estimated developer time saved through context preservation'
        }

        # Success Rate badge
        success_rate = stats.get('success_rate', 0)
        success_display = f"{success_rate:.1f}%"

        # Color based on success rate
        if success_rate >= 95:
            success_color = 'brightgreen'
        elif success_rate >= 90:
            success_color = 'green'
        elif success_rate >= 80:
            success_color = 'yellowgreen'
        elif success_rate >= 70:
            success_color = 'yellow'
        else:
            success_color = 'orange'

        badges['success_rate'] = {
            'url': generate_badge_url('success rate', success_display, success_color),
            'alt_text': f'Success Rate ({period_label})',
            'description': 'Percentage of successful session checkpoints'
        }

        # Decisions badge
        total_decisions = stats.get('total_decisions', 0)
        badges['decisions'] = {
            'url': generate_badge_url('decisions', str(total_decisions), 'blue'),
            'alt_text': f'Decisions Logged ({period_label})',
            'description': 'Total architectural and implementation decisions preserved'
        }

        # Resume Points badge
        total_resume_points = stats.get('total_resume_points', 0)
        badges['resume_points'] = {
            'url': generate_badge_url('resume points', str(total_resume_points), 'blue'),
            'alt_text': f'Resume Points ({period_label})',
            'description': 'Total resume points generated for session continuity'
        }

        # Token Efficiency badge (if available)
        total_tokens = stats.get('total_tokens_saved', 0)
        if total_tokens > 0:
            # Assume baseline of 200,000 tokens per session without tracking
            baseline_tokens = total_sessions * 200000
            if baseline_tokens > 0:
                efficiency = (total_tokens / baseline_tokens) * 100
                efficiency_display = f"{efficiency:.1f}%"

                # Color based on efficiency
                if efficiency >= 85:
                    efficiency_color = 'brightgreen'
                elif efficiency >= 70:
                    efficiency_color = 'green'
                elif efficiency >= 50:
                    efficiency_color = 'yellow'
                else:
                    efficiency_color = 'orange'

                badges['token_efficiency'] = {
                    'url': generate_badge_url('token efficiency', efficiency_display, efficiency_color),
                    'alt_text': f'Token Efficiency ({period_label})',
                    'description': 'Percentage of context window tokens saved through intelligent tracking'
                }

        # Files Changed badge
        total_files = stats.get('total_files_changed', 0)
        badges['files_changed'] = {
            'url': generate_badge_url('files tracked', str(total_files), 'blue'),
            'alt_text': f'Files Tracked ({period_label})',
            'description': 'Total file changes tracked across sessions'
        }

        logger.info(f"Generated {len(badges)} badges successfully")
        return badges

    except Exception as e:
        logger.error(f"Failed to generate badges: {e}")
        return {}


def generate_badge_markdown(badges: Dict[str, Dict[str, str]], layout: str = "inline") -> str:
    """
    Generate markdown for displaying badges.

    Args:
        badges: Dictionary of badge data from generate_stats_badges()
        layout: Display layout - "inline" (all on one line), "grid" (multi-line), or "detailed"

    Returns:
        Markdown string with badge images

    Example (inline layout):
        ![Total Sessions](https://img.shields.io/badge/...) ![Time Saved](...)

    Example (detailed layout):
        ## Portfolio Metrics

        ### Session Statistics
        ![Total Sessions](...)
        Number of session continuity checkpoints

        ...
    """
    if not badges:
        return "<!-- No badges available -->"

    lines = []

    if layout == "inline":
        # All badges on one line
        badge_images = []
        for badge_name, badge_data in badges.items():
            alt_text = badge_data['alt_text']
            url = badge_data['url']
            badge_images.append(f"![{alt_text}]({url})")

        lines.append(" ".join(badge_images))

    elif layout == "grid":
        # Badges in a grid pattern (2 per line)
        badge_list = list(badges.items())
        for i in range(0, len(badge_list), 2):
            row_badges = badge_list[i:i+2]
            row_images = []

            for badge_name, badge_data in row_badges:
                alt_text = badge_data['alt_text']
                url = badge_data['url']
                row_images.append(f"![{alt_text}]({url})")

            lines.append(" ".join(row_images))

    elif layout == "detailed":
        # Badges with descriptions
        lines.append("## Portfolio Metrics")
        lines.append("")

        for badge_name, badge_data in badges.items():
            alt_text = badge_data['alt_text']
            url = badge_data['url']
            description = badge_data['description']

            lines.append(f"![{alt_text}]({url})")
            lines.append(f"{description}")
            lines.append("")

    else:
        logger.warning(f"Unknown layout '{layout}', using inline")
        return generate_badge_markdown(badges, layout="inline")

    return "\n".join(lines)


def generate_readme_section(db: AnalyticsDB, days: Optional[int] = None) -> str:
    """
    Generate a complete README section with badges and summary.

    Args:
        db: AnalyticsDB instance
        days: Number of days for stats (None for all-time)

    Returns:
        Markdown section ready to insert into README

    Example output:
        ## Context-Aware Memory System - Impact Metrics

        ![Sessions](...)  ![Time Saved](...)  ![Success Rate](...)

        This project has successfully tracked 87 sessions, saving an estimated
        127.3 hours of developer time through intelligent context preservation.
    """
    lines = []

    # Get stats and badges
    if days:
        stats = db.get_session_stats(days=days)
        period_label = f"Last {days} Days"
    else:
        stats = db.get_aggregate_stats()
        period_label = "Lifetime Impact"

    badges = generate_stats_badges(db, days=days)

    # Header
    lines.append(f"## Context-Aware Memory System - {period_label}")
    lines.append("")

    # Badges (inline)
    badge_markdown = generate_badge_markdown(badges, layout="inline")
    lines.append(badge_markdown)
    lines.append("")

    # Summary text
    total_sessions = stats.get('total_sessions', 0)
    time_saved = stats.get('time_saved_hours', 0)
    success_rate = stats.get('success_rate', 0)
    total_decisions = stats.get('total_decisions', 0)

    work_days_saved = time_saved / 8  # Assuming 8-hour work days

    summary = (
        f"This project has successfully tracked **{total_sessions} sessions**, "
        f"saving an estimated **{time_saved:.1f} hours** ({work_days_saved:.1f} work days) "
        f"of developer time through intelligent context preservation. "
        f"With a **{success_rate:.1f}% success rate** and **{total_decisions} decisions** "
        f"logged, it demonstrates the power of automated session continuity."
    )

    lines.append(summary)

    return "\n".join(lines)


def main():
    """CLI entry point for badge generation"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate shields.io badges for portfolio metrics"
    )
    parser.add_argument(
        '--db-path',
        help='Path to analytics database',
        default=None
    )
    parser.add_argument(
        '--days',
        type=int,
        help='Number of days for stats (default: all-time)',
        default=None
    )
    parser.add_argument(
        '--layout',
        choices=['inline', 'grid', 'detailed'],
        help='Badge layout style',
        default='inline'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)',
        default=None
    )
    parser.add_argument(
        '--section',
        action='store_true',
        help='Generate complete README section'
    )

    args = parser.parse_args()

    # Initialize database
    try:
        db = AnalyticsDB(db_path=args.db_path)
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return 1

    # Generate output
    try:
        if args.section:
            output = generate_readme_section(db, days=args.days)
        else:
            badges = generate_stats_badges(db, days=args.days)
            output = generate_badge_markdown(badges, layout=args.layout)

        # Write or print output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            logger.info(f"Output written to {args.output}")
        else:
            print(output)

        return 0

    except Exception as e:
        logger.error(f"Failed to generate badges: {e}")
        return 1

    finally:
        db.close()


if __name__ == '__main__':
    import sys
    sys.exit(main())
