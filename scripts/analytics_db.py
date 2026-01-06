#!/usr/bin/env python3
"""
Analytics Database Layer for Context-Aware Memory System

Provides SQLite-based analytics tracking for session continuity metrics:
- Session checkpoints with metadata
- File change tracking
- Decision logging
- Aggregate statistics computation
- Time saved calculation

Usage:
    from analytics_db import AnalyticsDB

    db = AnalyticsDB()
    db.insert_session(checkpoint_data)
    stats = db.get_aggregate_stats()
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AnalyticsDB:
    """SQLite database layer for session analytics"""

    # Time saved estimates (in minutes)
    TIME_SAVED_PER_SESSION = 15  # Average time saved per successful session
    TIME_SAVED_PER_DECISION = 5   # Time saved by logging each decision
    TIME_SAVED_PER_FILE = 2       # Time saved by tracking file changes

    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection

        Args:
            db_path: Path to SQLite database file. If None, uses default location
        """
        if db_path is None:
            # Default to .analytics/stats.db relative to script location
            script_dir = Path(__file__).parent.parent
            analytics_dir = script_dir / '.analytics'
            analytics_dir.mkdir(exist_ok=True)
            db_path = str(analytics_dir / 'stats.db')

        self.db_path = db_path
        self.conn = None
        self._connect()
        self.initialize_schema()

    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def initialize_schema(self):
        """Create database tables and indexes"""
        cursor = self.conn.cursor()

        try:
            # Sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    timestamp DATETIME NOT NULL,
                    started_at DATETIME,
                    duration_seconds INTEGER,
                    checkpoint_success BOOLEAN DEFAULT 1,
                    files_changed INTEGER DEFAULT 0,
                    decisions_logged INTEGER DEFAULT 0,
                    resume_points_generated INTEGER DEFAULT 0,
                    problems_encountered INTEGER DEFAULT 0,
                    tokens_estimated INTEGER,
                    project_name TEXT,
                    git_commit_hash TEXT,
                    git_branch TEXT,
                    tool_triggered TEXT
                )
            """)

            # File changes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS file_changes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    change_type TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)

            # Decisions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    decision_text TEXT NOT NULL,
                    timestamp DATETIME,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)

            # Aggregate stats table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS aggregate_stats (
                    stat_key TEXT PRIMARY KEY,
                    stat_value REAL NOT NULL,
                    last_updated DATETIME NOT NULL
                )
            """)

            # Create indexes for better query performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_timestamp
                ON sessions(timestamp)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_project
                ON sessions(project_name)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_file_changes_session
                ON file_changes(session_id)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_decisions_session
                ON decisions(session_id)
            """)

            self.conn.commit()
            logger.info("Database schema initialized successfully")

        except sqlite3.Error as e:
            logger.error(f"Schema initialization failed: {e}")
            self.conn.rollback()
            raise

    def insert_session(self, checkpoint_data: Dict[str, Any]) -> bool:
        """Insert a session record from checkpoint data

        Args:
            checkpoint_data: Checkpoint JSON data

        Returns:
            True if successful, False otherwise
        """
        cursor = self.conn.cursor()

        try:
            session_id = checkpoint_data.get('session_id')

            # Check for duplicate
            cursor.execute(
                "SELECT session_id FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            if cursor.fetchone():
                logger.warning(f"Session {session_id} already exists, skipping")
                return False

            # Parse timestamps
            timestamp = datetime.fromisoformat(
                checkpoint_data.get('timestamp', datetime.now().isoformat())
            )

            started_at = None
            if checkpoint_data.get('started_at'):
                started_at = datetime.fromisoformat(checkpoint_data['started_at'])

            # Calculate duration
            duration_seconds = None
            if started_at and timestamp:
                duration_seconds = int((timestamp - started_at).total_seconds())

            # Extract metadata
            file_changes = checkpoint_data.get('file_changes', [])
            decisions = checkpoint_data.get('decisions', [])
            resume_points = checkpoint_data.get('resume_points', [])
            problems = checkpoint_data.get('problems_encountered', [])

            # Get project info
            project_info = checkpoint_data.get('project', {})
            project_name = project_info.get('name', 'Unknown')

            # Get git info
            git_commit_hash = checkpoint_data.get('git_commit_hash')
            git_branch = checkpoint_data.get('git_branch')

            # Get tool info
            context = checkpoint_data.get('context', {})
            tool_triggered = context.get('tool', 'manual')

            # Estimate tokens saved (rough calculation)
            tokens_estimated = self._estimate_tokens_saved(
                len(file_changes),
                len(decisions),
                len(resume_points)
            )

            # Insert session
            cursor.execute("""
                INSERT INTO sessions (
                    session_id, timestamp, started_at, duration_seconds,
                    checkpoint_success, files_changed, decisions_logged,
                    resume_points_generated, problems_encountered,
                    tokens_estimated, project_name, git_commit_hash,
                    git_branch, tool_triggered
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                timestamp,
                started_at,
                duration_seconds,
                True,  # If we got the checkpoint, it succeeded
                len(file_changes),
                len(decisions),
                len(resume_points),
                len(problems),
                tokens_estimated,
                project_name,
                git_commit_hash,
                git_branch,
                tool_triggered
            ))

            # Insert file changes
            for change in file_changes:
                if isinstance(change, dict):
                    file_path = change.get('path', '')
                    change_type = change.get('type', 'modified')
                else:
                    # Handle simple string format
                    file_path = str(change)
                    change_type = 'modified'

                cursor.execute("""
                    INSERT INTO file_changes (session_id, file_path, change_type)
                    VALUES (?, ?, ?)
                """, (session_id, file_path, change_type))

            # Insert decisions
            for decision in decisions:
                if isinstance(decision, dict):
                    decision_text = decision.get('text', str(decision))
                    decision_timestamp = decision.get('timestamp')
                    if decision_timestamp:
                        decision_timestamp = datetime.fromisoformat(decision_timestamp)
                else:
                    decision_text = str(decision)
                    decision_timestamp = timestamp

                cursor.execute("""
                    INSERT INTO decisions (session_id, decision_text, timestamp)
                    VALUES (?, ?, ?)
                """, (session_id, decision_text, decision_timestamp))

            self.conn.commit()
            logger.info(f"Session {session_id} inserted successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to insert session: {e}")
            self.conn.rollback()
            return False

    def _estimate_tokens_saved(self, files: int, decisions: int, resume_points: int) -> int:
        """Estimate tokens saved by session tracking

        Args:
            files: Number of files changed
            decisions: Number of decisions logged
            resume_points: Number of resume points generated

        Returns:
            Estimated tokens saved
        """
        # Rough estimates based on typical context usage
        tokens_per_file = 200       # Average tokens to describe a file change
        tokens_per_decision = 150   # Average tokens for a decision context
        tokens_per_resume = 100     # Average tokens for a resume point

        total = (
            files * tokens_per_file +
            decisions * tokens_per_decision +
            resume_points * tokens_per_resume
        )

        return total

    def get_session_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get session statistics for the last N days

        Args:
            days: Number of days to include

        Returns:
            Dictionary of statistics
        """
        cursor = self.conn.cursor()
        cutoff_date = datetime.now() - timedelta(days=days)

        try:
            # Get session counts
            cursor.execute("""
                SELECT
                    COUNT(*) as total_sessions,
                    SUM(CASE WHEN checkpoint_success = 1 THEN 1 ELSE 0 END) as successful_sessions,
                    SUM(files_changed) as total_files_changed,
                    SUM(decisions_logged) as total_decisions,
                    SUM(resume_points_generated) as total_resume_points,
                    SUM(problems_encountered) as total_problems,
                    AVG(duration_seconds) as avg_duration_seconds,
                    SUM(tokens_estimated) as total_tokens_saved
                FROM sessions
                WHERE timestamp >= ?
            """, (cutoff_date,))

            row = cursor.fetchone()

            stats = {
                'period_days': days,
                'total_sessions': row['total_sessions'] or 0,
                'successful_sessions': row['successful_sessions'] or 0,
                'total_files_changed': row['total_files_changed'] or 0,
                'total_decisions': row['total_decisions'] or 0,
                'total_resume_points': row['total_resume_points'] or 0,
                'total_problems': row['total_problems'] or 0,
                'avg_duration_seconds': row['avg_duration_seconds'] or 0,
                'total_tokens_saved': row['total_tokens_saved'] or 0
            }

            # Calculate success rate
            if stats['total_sessions'] > 0:
                stats['success_rate'] = (
                    stats['successful_sessions'] / stats['total_sessions']
                ) * 100
            else:
                stats['success_rate'] = 0.0

            # Calculate time saved
            stats['time_saved_minutes'] = self._calculate_time_saved_from_stats(stats)
            stats['time_saved_hours'] = stats['time_saved_minutes'] / 60

            return stats

        except sqlite3.Error as e:
            logger.error(f"Failed to get session stats: {e}")
            return {}

    def get_aggregate_stats(self) -> Dict[str, Any]:
        """Get lifetime aggregate statistics

        Returns:
            Dictionary of aggregate metrics
        """
        cursor = self.conn.cursor()

        try:
            # Get all-time stats
            cursor.execute("""
                SELECT
                    COUNT(*) as total_sessions,
                    SUM(CASE WHEN checkpoint_success = 1 THEN 1 ELSE 0 END) as successful_sessions,
                    SUM(files_changed) as total_files_changed,
                    SUM(decisions_logged) as total_decisions,
                    SUM(resume_points_generated) as total_resume_points,
                    MIN(timestamp) as first_session,
                    MAX(timestamp) as last_session,
                    COUNT(DISTINCT project_name) as total_projects
                FROM sessions
            """)

            row = cursor.fetchone()

            stats = {
                'total_sessions': row['total_sessions'] or 0,
                'successful_sessions': row['successful_sessions'] or 0,
                'total_files_changed': row['total_files_changed'] or 0,
                'total_decisions': row['total_decisions'] or 0,
                'total_resume_points': row['total_resume_points'] or 0,
                'first_session': row['first_session'],
                'last_session': row['last_session'],
                'total_projects': row['total_projects'] or 0
            }

            # Calculate success rate
            if stats['total_sessions'] > 0:
                stats['success_rate'] = (
                    stats['successful_sessions'] / stats['total_sessions']
                ) * 100
            else:
                stats['success_rate'] = 0.0

            # Calculate time saved
            stats['time_saved_hours'] = self.calculate_time_saved()

            return stats

        except sqlite3.Error as e:
            logger.error(f"Failed to get aggregate stats: {e}")
            return {}

    def _calculate_time_saved_from_stats(self, stats: Dict[str, Any]) -> float:
        """Calculate time saved in minutes from statistics

        Args:
            stats: Statistics dictionary

        Returns:
            Time saved in minutes
        """
        time_saved = (
            stats['successful_sessions'] * self.TIME_SAVED_PER_SESSION +
            stats['total_decisions'] * self.TIME_SAVED_PER_DECISION +
            stats['total_files_changed'] * self.TIME_SAVED_PER_FILE
        )
        return time_saved

    def calculate_time_saved(self) -> float:
        """Calculate total time saved in hours

        Returns:
            Total hours saved across all sessions
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    COUNT(*) as total_sessions,
                    SUM(decisions_logged) as total_decisions,
                    SUM(files_changed) as total_files
                FROM sessions
                WHERE checkpoint_success = 1
            """)

            row = cursor.fetchone()

            total_sessions = row['total_sessions'] or 0
            total_decisions = row['total_decisions'] or 0
            total_files = row['total_files'] or 0

            # Calculate time saved in minutes
            time_saved_minutes = (
                total_sessions * self.TIME_SAVED_PER_SESSION +
                total_decisions * self.TIME_SAVED_PER_DECISION +
                total_files * self.TIME_SAVED_PER_FILE
            )

            # Convert to hours
            time_saved_hours = time_saved_minutes / 60

            return time_saved_hours

        except sqlite3.Error as e:
            logger.error(f"Failed to calculate time saved: {e}")
            return 0.0

    def get_success_rate(self, days: Optional[int] = None) -> float:
        """Calculate checkpoint success percentage

        Args:
            days: Number of days to include (None for all-time)

        Returns:
            Success rate as percentage (0-100)
        """
        cursor = self.conn.cursor()

        try:
            if days:
                cutoff_date = datetime.now() - timedelta(days=days)
                cursor.execute("""
                    SELECT
                        COUNT(*) as total,
                        SUM(CASE WHEN checkpoint_success = 1 THEN 1 ELSE 0 END) as successful
                    FROM sessions
                    WHERE timestamp >= ?
                """, (cutoff_date,))
            else:
                cursor.execute("""
                    SELECT
                        COUNT(*) as total,
                        SUM(CASE WHEN checkpoint_success = 1 THEN 1 ELSE 0 END) as successful
                    FROM sessions
                """)

            row = cursor.fetchone()
            total = row['total'] or 0
            successful = row['successful'] or 0

            if total == 0:
                return 0.0

            return (successful / total) * 100

        except sqlite3.Error as e:
            logger.error(f"Failed to get success rate: {e}")
            return 0.0

    def get_project_breakdown(self) -> List[Dict[str, Any]]:
        """Get statistics broken down by project

        Returns:
            List of project statistics
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    project_name,
                    COUNT(*) as total_sessions,
                    SUM(CASE WHEN checkpoint_success = 1 THEN 1 ELSE 0 END) as successful_sessions,
                    SUM(files_changed) as total_files_changed,
                    SUM(decisions_logged) as total_decisions,
                    MIN(timestamp) as first_session,
                    MAX(timestamp) as last_session
                FROM sessions
                GROUP BY project_name
                ORDER BY total_sessions DESC
            """)

            projects = []
            for row in cursor.fetchall():
                project = {
                    'project_name': row['project_name'],
                    'total_sessions': row['total_sessions'],
                    'successful_sessions': row['successful_sessions'],
                    'total_files_changed': row['total_files_changed'],
                    'total_decisions': row['total_decisions'],
                    'first_session': row['first_session'],
                    'last_session': row['last_session']
                }

                # Calculate success rate
                if project['total_sessions'] > 0:
                    project['success_rate'] = (
                        project['successful_sessions'] / project['total_sessions']
                    ) * 100
                else:
                    project['success_rate'] = 0.0

                projects.append(project)

            return projects

        except sqlite3.Error as e:
            logger.error(f"Failed to get project breakdown: {e}")
            return []

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


if __name__ == "__main__":
    # Simple test
    db = AnalyticsDB()
    print("Database initialized successfully")
    print(f"Database location: {db.db_path}")

    # Display schema info
    cursor = db.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\nTables created: {[t['name'] for t in tables]}")

    db.close()
