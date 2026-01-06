#!/usr/bin/env python3
"""
Backfill Analytics Database

Parses existing checkpoint JSON files from .claude-sessions and populates
the analytics database with historical session data.

Usage:
    python backfill_analytics.py              # Backfill last 90 days
    python backfill_analytics.py --days 30    # Backfill last 30 days
    python backfill_analytics.py --all        # Backfill all checkpoints
    python backfill_analytics.py --dry-run    # Preview without inserting
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Import analytics database
from analytics_db import AnalyticsDB

# Import terminal UI
try:
    import claude_terminal_ui as ui
    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False
    # Fallback
    class ui:
        @staticmethod
        def header(title, **kwargs):
            print("=" * 70)
            print(" " * ((70 - len(title)) // 2) + title)
            print("=" * 70)

        @staticmethod
        def divider(**kwargs):
            print("-" * 70)

        @staticmethod
        def print_success(message, **kwargs):
            print(f"[OK] {message}")

        @staticmethod
        def print_error(message, **kwargs):
            print(f"[ERROR] {message}")

        @staticmethod
        def print_warning(message, **kwargs):
            print(f"[WARNING] {message}")

        @staticmethod
        def print_info(message, **kwargs):
            print(f"[INFO] {message}")


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CheckpointBackfiller:
    """Backfill analytics database from checkpoint files"""

    def __init__(self, db: AnalyticsDB, checkpoints_dir: Optional[Path] = None):
        """Initialize backfiller

        Args:
            db: AnalyticsDB instance
            checkpoints_dir: Path to checkpoints directory (default: ~/.claude-sessions/checkpoints)
        """
        self.db = db

        if checkpoints_dir is None:
            home = Path.home()
            checkpoints_dir = home / '.claude-sessions' / 'checkpoints'

        self.checkpoints_dir = checkpoints_dir

        if not self.checkpoints_dir.exists():
            raise ValueError(f"Checkpoints directory not found: {checkpoints_dir}")

    def find_checkpoint_files(self, days: Optional[int] = None) -> List[Path]:
        """Find checkpoint JSON files

        Args:
            days: Only include files from last N days (None for all)

        Returns:
            List of checkpoint file paths, sorted by date
        """
        logger.info(f"Scanning for checkpoint files in {self.checkpoints_dir}")

        # Find all checkpoint JSON files
        checkpoint_files = list(self.checkpoints_dir.glob('checkpoint-*.json'))

        if days:
            # Filter by date
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_files = []

            for file_path in checkpoint_files:
                # Parse timestamp from filename: checkpoint-20251215-205523.json
                try:
                    filename = file_path.stem  # Remove .json
                    date_str = filename.replace('checkpoint-', '')  # Remove prefix
                    # Parse: 20251215-205523 -> 2025-12-15 20:55:23
                    file_date = datetime.strptime(date_str, '%Y%m%d-%H%M%S')

                    if file_date >= cutoff_date:
                        filtered_files.append(file_path)
                except ValueError:
                    logger.warning(f"Could not parse date from filename: {file_path.name}")
                    continue

            checkpoint_files = filtered_files

        # Sort by filename (which sorts by date due to timestamp format)
        checkpoint_files.sort()

        logger.info(f"Found {len(checkpoint_files)} checkpoint files")
        return checkpoint_files

    def parse_checkpoint(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse a checkpoint JSON file

        Args:
            file_path: Path to checkpoint file

        Returns:
            Checkpoint data dictionary, or None if parsing fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path.name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to read {file_path.name}: {e}")
            return None

    def backfill(
        self,
        days: Optional[int] = None,
        dry_run: bool = False,
        verbose: bool = False
    ) -> Dict[str, Any]:
        """Backfill database from checkpoint files

        Args:
            days: Only include files from last N days (None for all)
            dry_run: If True, don't insert into database
            verbose: If True, show detailed progress

        Returns:
            Dictionary with backfill statistics
        """
        # Find checkpoint files
        checkpoint_files = self.find_checkpoint_files(days)

        if not checkpoint_files:
            logger.warning("No checkpoint files found")
            return {
                'total_files': 0,
                'processed': 0,
                'inserted': 0,
                'skipped': 0,
                'errors': 0
            }

        stats = {
            'total_files': len(checkpoint_files),
            'processed': 0,
            'inserted': 0,
            'skipped': 0,
            'errors': 0,
            'success_rate': 0.0,
            'time_saved_hours': 0.0
        }

        # Process files with progress display
        total = len(checkpoint_files)
        show_progress = not verbose and total > 10

        if show_progress:
            print(f"\nProcessing {total} checkpoint files...")

        for i, file_path in enumerate(checkpoint_files, 1):
            # Parse checkpoint
            checkpoint_data = self.parse_checkpoint(file_path)

            if checkpoint_data is None:
                stats['errors'] += 1
                if verbose:
                    print(f"[{i}/{total}] ERROR: Failed to parse {file_path.name}")
                continue

            stats['processed'] += 1

            # Insert into database (unless dry run)
            if not dry_run:
                success = self.db.insert_session(checkpoint_data)
                if success:
                    stats['inserted'] += 1
                else:
                    stats['skipped'] += 1
            else:
                stats['inserted'] += 1  # Count as inserted for dry run

            # Show progress
            if verbose:
                print(f"[{i}/{total}] Processed {file_path.name}")
            elif show_progress and (i % 100 == 0 or i == total):
                percentage = (i / total) * 100
                bar_length = 40
                filled = int(bar_length * i / total)
                bar = '#' * filled + '-' * (bar_length - filled)
                print(f"\r[{bar}] {i}/{total} ({percentage:.1f}%)", end='', flush=True)

        if show_progress:
            print()  # New line after progress bar

        # Calculate final statistics from database
        if not dry_run:
            aggregate = self.db.get_aggregate_stats()
            stats['success_rate'] = aggregate.get('success_rate', 0.0)
            stats['time_saved_hours'] = aggregate.get('time_saved_hours', 0.0)

        return stats


def format_duration(hours: float) -> str:
    """Format hours into human-readable duration

    Args:
        hours: Number of hours

    Returns:
        Formatted string (e.g., "127.3 hours" or "2.1 days")
    """
    if hours < 24:
        return f"{hours:.1f} hours"
    else:
        days = hours / 24
        return f"{days:.1f} days ({hours:.1f} hours)"


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Backfill analytics database from checkpoint files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python backfill_analytics.py
      Backfill last 90 days (default)

  python backfill_analytics.py --days 30
      Backfill last 30 days

  python backfill_analytics.py --all
      Backfill all checkpoint files

  python backfill_analytics.py --dry-run
      Preview without inserting into database
        """
    )

    parser.add_argument(
        '--days',
        type=int,
        default=90,
        help='Backfill checkpoints from last N days (default: 90)'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Backfill all checkpoint files (overrides --days)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview without inserting into database'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed progress'
    )

    parser.add_argument(
        '--db-path',
        type=str,
        help='Custom database path (default: .analytics/stats.db)'
    )

    parser.add_argument(
        '--checkpoints-dir',
        type=str,
        help='Custom checkpoints directory (default: ~/.claude-sessions/checkpoints)'
    )

    args = parser.parse_args()

    # Print header
    print()
    print(ui.header("BACKFILLING ANALYTICS DATABASE"))
    print()

    if args.dry_run:
        ui.print_info("DRY RUN MODE - No data will be inserted")
        print()

    # Initialize database
    try:
        db = AnalyticsDB(db_path=args.db_path)
        ui.print_success(f"Database initialized: {db.db_path}")
    except Exception as e:
        ui.print_error(f"Failed to initialize database: {e}")
        return 1

    print()

    # Initialize backfiller
    try:
        checkpoints_dir = Path(args.checkpoints_dir) if args.checkpoints_dir else None
        backfiller = CheckpointBackfiller(db, checkpoints_dir=checkpoints_dir)
        ui.print_success(f"Checkpoint directory: {backfiller.checkpoints_dir}")
    except Exception as e:
        ui.print_error(f"Failed to initialize backfiller: {e}")
        db.close()
        return 1

    print()
    print(ui.divider())

    # Determine days to backfill
    days = None if args.all else args.days
    if days:
        ui.print_info(f"Processing checkpoints from last {days} days")
    else:
        ui.print_info("Processing all checkpoint files")

    print()

    # Backfill
    try:
        stats = backfiller.backfill(
            days=days,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
    except Exception as e:
        ui.print_error(f"Backfill failed: {e}")
        logger.exception("Backfill error details:")
        db.close()
        return 1

    # Print results
    print()
    print(ui.header("BACKFILL COMPLETE"))
    print()

    ui.print_success(f"Sessions processed: {stats['processed']}")
    ui.print_success(f"Sessions inserted: {stats['inserted']}")

    if stats['skipped'] > 0:
        ui.print_warning(f"Sessions skipped (duplicates): {stats['skipped']}")

    if stats['errors'] > 0:
        ui.print_error(f"Errors encountered: {stats['errors']}")

    if not args.dry_run:
        print()
        print(ui.divider())
        print()
        ui.print_info("Database Statistics:")
        print(f"  Success rate: {stats['success_rate']:.1f}%")
        print(f"  Time saved: {format_duration(stats['time_saved_hours'])}")

    print()
    print(ui.divider())

    # Clean up
    db.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
