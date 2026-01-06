#!/usr/bin/env python3
"""
Comprehensive Test Suite for Analytics Database

Tests all functionality of analytics_db.py and backfill_analytics.py
with >90% code coverage.

Usage:
    python -m pytest test_analytics.py -v
    python -m pytest test_analytics.py --cov=analytics_db --cov=backfill_analytics
"""

import sys
import unittest
import tempfile
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analytics_db import AnalyticsDB
from backfill_analytics import CheckpointBackfiller, format_duration


class TestAnalyticsDB(unittest.TestCase):
    """Test cases for AnalyticsDB class"""

    def setUp(self):
        """Set up test database"""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name

        # Initialize database
        self.db = AnalyticsDB(db_path=self.db_path)

    def tearDown(self):
        """Clean up test database"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    def test_database_initialization(self):
        """Test database and schema creation"""
        # Check that database file exists
        self.assertTrue(Path(self.db_path).exists())

        # Check that tables were created
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row['name'] for row in cursor.fetchall()]

        expected_tables = ['sessions', 'file_changes', 'decisions', 'aggregate_stats']
        for table in expected_tables:
            self.assertIn(table, tables)

    def test_insert_session_success(self):
        """Test successful session insertion"""
        checkpoint_data = {
            'session_id': 'test-session-001',
            'timestamp': datetime.now().isoformat(),
            'started_at': (datetime.now() - timedelta(minutes=30)).isoformat(),
            'file_changes': [
                {'path': 'test.py', 'type': 'modified'},
                {'path': 'test2.py', 'type': 'added'}
            ],
            'decisions': [
                'Decision 1: Use pytest for testing',
                'Decision 2: Add comprehensive coverage'
            ],
            'resume_points': ['Continue testing', 'Add more coverage'],
            'problems_encountered': [],
            'project': {
                'name': 'TestProject'
            },
            'git_commit_hash': 'abc123',
            'git_branch': 'main',
            'context': {
                'tool': 'manual'
            }
        }

        # Insert session
        success = self.db.insert_session(checkpoint_data)
        self.assertTrue(success)

        # Verify session was inserted
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", ('test-session-001',))
        row = cursor.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row['session_id'], 'test-session-001')
        self.assertEqual(row['files_changed'], 2)
        self.assertEqual(row['decisions_logged'], 2)
        self.assertEqual(row['resume_points_generated'], 2)
        self.assertEqual(row['project_name'], 'TestProject')

        # Verify file changes were inserted
        cursor.execute("SELECT COUNT(*) as count FROM file_changes WHERE session_id = ?",
                      ('test-session-001',))
        count = cursor.fetchone()['count']
        self.assertEqual(count, 2)

        # Verify decisions were inserted
        cursor.execute("SELECT COUNT(*) as count FROM decisions WHERE session_id = ?",
                      ('test-session-001',))
        count = cursor.fetchone()['count']
        self.assertEqual(count, 2)

    def test_insert_duplicate_session(self):
        """Test duplicate session insertion is prevented"""
        checkpoint_data = {
            'session_id': 'duplicate-session',
            'timestamp': datetime.now().isoformat(),
            'project': {'name': 'TestProject'}
        }

        # Insert first time
        success1 = self.db.insert_session(checkpoint_data)
        self.assertTrue(success1)

        # Try to insert duplicate
        success2 = self.db.insert_session(checkpoint_data)
        self.assertFalse(success2)

    def test_session_stats(self):
        """Test session statistics calculation"""
        # Insert multiple sessions
        for i in range(5):
            checkpoint_data = {
                'session_id': f'session-{i}',
                'timestamp': (datetime.now() - timedelta(days=i)).isoformat(),
                'started_at': (datetime.now() - timedelta(days=i, minutes=30)).isoformat(),
                'file_changes': [f'file{j}.py' for j in range(i + 1)],
                'decisions': [f'Decision {j}' for j in range(i)],
                'resume_points': ['Resume point'],
                'problems_encountered': [],
                'project': {'name': 'TestProject'}
            }
            self.db.insert_session(checkpoint_data)

        # Get stats for last 7 days
        stats = self.db.get_session_stats(days=7)

        self.assertEqual(stats['total_sessions'], 5)
        self.assertEqual(stats['successful_sessions'], 5)
        self.assertGreater(stats['total_files_changed'], 0)
        self.assertGreater(stats['total_decisions'], 0)
        self.assertEqual(stats['success_rate'], 100.0)

    def test_aggregate_stats(self):
        """Test aggregate statistics"""
        # Insert sessions
        for i in range(3):
            checkpoint_data = {
                'session_id': f'agg-session-{i}',
                'timestamp': datetime.now().isoformat(),
                'file_changes': [f'file{i}.py'],
                'decisions': [f'Decision {i}'],
                'resume_points': [],
                'problems_encountered': [],
                'project': {'name': f'Project{i % 2}'}  # 2 different projects
            }
            self.db.insert_session(checkpoint_data)

        # Get aggregate stats
        stats = self.db.get_aggregate_stats()

        self.assertEqual(stats['total_sessions'], 3)
        self.assertEqual(stats['successful_sessions'], 3)
        self.assertEqual(stats['total_projects'], 2)
        self.assertEqual(stats['success_rate'], 100.0)
        self.assertGreater(stats['time_saved_hours'], 0)

    def test_calculate_time_saved(self):
        """Test time saved calculation"""
        # Insert sessions with known counts
        checkpoint_data = {
            'session_id': 'time-test',
            'timestamp': datetime.now().isoformat(),
            'file_changes': ['file1.py', 'file2.py'],  # 2 files
            'decisions': ['Decision 1'],  # 1 decision
            'resume_points': [],
            'problems_encountered': [],
            'project': {'name': 'TestProject'}
        }
        self.db.insert_session(checkpoint_data)

        # Calculate time saved
        time_saved = self.db.calculate_time_saved()

        # Expected: (1 session * 15) + (1 decision * 5) + (2 files * 2) = 24 minutes = 0.4 hours
        expected = (1 * 15 + 1 * 5 + 2 * 2) / 60
        self.assertAlmostEqual(time_saved, expected, places=2)

    def test_success_rate(self):
        """Test success rate calculation"""
        # Insert successful sessions
        for i in range(8):
            checkpoint_data = {
                'session_id': f'success-{i}',
                'timestamp': datetime.now().isoformat(),
                'project': {'name': 'TestProject'}
            }
            self.db.insert_session(checkpoint_data)

        # Get success rate (all should be successful)
        rate = self.db.get_success_rate()
        self.assertEqual(rate, 100.0)

        # Test with specific days
        rate_7days = self.db.get_success_rate(days=7)
        self.assertEqual(rate_7days, 100.0)

    def test_project_breakdown(self):
        """Test project breakdown statistics"""
        # Insert sessions for different projects
        projects = ['ProjectA', 'ProjectB', 'ProjectC']
        for project in projects:
            for i in range(2):  # 2 sessions per project
                checkpoint_data = {
                    'session_id': f'{project}-session-{i}',
                    'timestamp': datetime.now().isoformat(),
                    'file_changes': [f'file{i}.py'],
                    'decisions': [f'Decision {i}'],
                    'project': {'name': project}
                }
                self.db.insert_session(checkpoint_data)

        # Get project breakdown
        breakdown = self.db.get_project_breakdown()

        self.assertEqual(len(breakdown), 3)

        # Check each project has correct stats
        for project_stats in breakdown:
            self.assertEqual(project_stats['total_sessions'], 2)
            self.assertEqual(project_stats['successful_sessions'], 2)
            self.assertEqual(project_stats['success_rate'], 100.0)

    def test_tokens_estimation(self):
        """Test token estimation calculation"""
        # Create session with known counts
        tokens = self.db._estimate_tokens_saved(
            files=5,
            decisions=3,
            resume_points=2
        )

        # Expected: (5 * 200) + (3 * 150) + (2 * 100) = 1650
        expected = (5 * 200) + (3 * 150) + (2 * 100)
        self.assertEqual(tokens, expected)

    def test_context_manager(self):
        """Test database context manager"""
        with AnalyticsDB(db_path=self.db_path) as db:
            self.assertIsNotNone(db.conn)

        # Connection should be closed after context
        # Note: We can't easily test this without implementation details

    def test_missing_fields(self):
        """Test handling of checkpoint data with missing fields"""
        # Minimal checkpoint data
        minimal_data = {
            'session_id': 'minimal-session'
        }

        success = self.db.insert_session(minimal_data)
        self.assertTrue(success)

        # Verify defaults were used
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", ('minimal-session',))
        row = cursor.fetchone()

        self.assertEqual(row['files_changed'], 0)
        self.assertEqual(row['decisions_logged'], 0)
        self.assertEqual(row['resume_points_generated'], 0)


class TestCheckpointBackfiller(unittest.TestCase):
    """Test cases for CheckpointBackfiller class"""

    def setUp(self):
        """Set up test environment"""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.db = AnalyticsDB(db_path=self.db_path)

        # Create temporary checkpoints directory
        self.temp_checkpoints = tempfile.mkdtemp()
        self.checkpoints_dir = Path(self.temp_checkpoints)

    def tearDown(self):
        """Clean up test environment"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

        # Clean up checkpoint files
        import shutil
        shutil.rmtree(self.temp_checkpoints, ignore_errors=True)

    def create_test_checkpoint(self, session_id: str, days_ago: int = 0) -> Path:
        """Create a test checkpoint file

        Args:
            session_id: Session ID
            days_ago: Number of days in the past

        Returns:
            Path to created checkpoint file
        """
        timestamp = datetime.now() - timedelta(days=days_ago)
        filename = f"checkpoint-{timestamp.strftime('%Y%m%d-%H%M%S')}.json"
        file_path = self.checkpoints_dir / filename

        checkpoint_data = {
            'session_id': session_id,
            'timestamp': timestamp.isoformat(),
            'started_at': (timestamp - timedelta(minutes=30)).isoformat(),
            'file_changes': ['test.py'],
            'decisions': ['Test decision'],
            'resume_points': ['Test resume'],
            'problems_encountered': [],
            'project': {'name': 'TestProject'},
            'git_commit_hash': 'abc123',
            'git_branch': 'main',
            'context': {'tool': 'test'}
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f)

        return file_path

    def test_find_checkpoint_files(self):
        """Test finding checkpoint files"""
        # Create test checkpoints
        self.create_test_checkpoint('session-1', days_ago=5)
        self.create_test_checkpoint('session-2', days_ago=10)
        self.create_test_checkpoint('session-3', days_ago=50)

        backfiller = CheckpointBackfiller(self.db, self.checkpoints_dir)

        # Find all files
        all_files = backfiller.find_checkpoint_files(days=None)
        self.assertEqual(len(all_files), 3)

        # Find files from last 30 days
        recent_files = backfiller.find_checkpoint_files(days=30)
        self.assertEqual(len(recent_files), 2)

    def test_parse_checkpoint(self):
        """Test parsing checkpoint files"""
        # Create test checkpoint
        file_path = self.create_test_checkpoint('parse-test')

        backfiller = CheckpointBackfiller(self.db, self.checkpoints_dir)
        data = backfiller.parse_checkpoint(file_path)

        self.assertIsNotNone(data)
        self.assertEqual(data['session_id'], 'parse-test')

    def test_parse_invalid_checkpoint(self):
        """Test parsing invalid checkpoint file"""
        # Create invalid JSON file
        invalid_file = self.checkpoints_dir / 'checkpoint-invalid.json'
        with open(invalid_file, 'w') as f:
            f.write('{ invalid json }')

        backfiller = CheckpointBackfiller(self.db, self.checkpoints_dir)
        data = backfiller.parse_checkpoint(invalid_file)

        self.assertIsNone(data)

    def test_backfill_dry_run(self):
        """Test backfill in dry run mode"""
        # Create test checkpoints
        for i in range(3):
            self.create_test_checkpoint(f'dry-run-{i}', days_ago=i)

        backfiller = CheckpointBackfiller(self.db, self.checkpoints_dir)
        stats = backfiller.backfill(days=None, dry_run=True)

        # Check stats
        self.assertEqual(stats['total_files'], 3)
        self.assertEqual(stats['processed'], 3)
        self.assertEqual(stats['inserted'], 3)

        # Verify nothing was actually inserted
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM sessions")
        count = cursor.fetchone()['count']
        self.assertEqual(count, 0)

    def test_backfill_actual(self):
        """Test actual backfill"""
        # Create test checkpoints
        for i in range(5):
            self.create_test_checkpoint(f'backfill-{i}', days_ago=i)

        backfiller = CheckpointBackfiller(self.db, self.checkpoints_dir)
        stats = backfiller.backfill(days=None, dry_run=False)

        # Check stats
        self.assertEqual(stats['total_files'], 5)
        self.assertEqual(stats['processed'], 5)
        self.assertEqual(stats['inserted'], 5)

        # Verify sessions were inserted
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM sessions")
        count = cursor.fetchone()['count']
        self.assertEqual(count, 5)

    def test_backfill_with_date_filter(self):
        """Test backfill with date filtering"""
        # Create checkpoints at different dates
        self.create_test_checkpoint('recent-1', days_ago=5)
        self.create_test_checkpoint('recent-2', days_ago=10)
        self.create_test_checkpoint('old-1', days_ago=100)

        backfiller = CheckpointBackfiller(self.db, self.checkpoints_dir)
        stats = backfiller.backfill(days=30, dry_run=False)

        # Should only process recent files
        self.assertEqual(stats['processed'], 2)
        self.assertEqual(stats['inserted'], 2)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""

    def test_format_duration(self):
        """Test duration formatting"""
        # Test hours
        self.assertEqual(format_duration(5.5), "5.5 hours")

        # Test days
        result = format_duration(48.0)
        self.assertIn("2.0 days", result)
        self.assertIn("48.0 hours", result)


def run_tests_with_coverage():
    """Run tests with coverage reporting"""
    try:
        import pytest
        import sys

        # Run pytest with coverage
        args = [
            __file__,
            '-v',
            '--cov=analytics_db',
            '--cov=backfill_analytics',
            '--cov-report=term-missing',
            '--cov-report=html'
        ]
        return pytest.main(args)
    except ImportError:
        print("pytest not installed, running basic tests")
        unittest.main()


if __name__ == '__main__':
    # Try to run with coverage, fall back to basic unittest
    try:
        import pytest
        run_tests_with_coverage()
    except ImportError:
        unittest.main()
