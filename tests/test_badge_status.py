#!/usr/bin/env python3
"""
Tests for Badge Generator and Status Display

Tests badge URL generation, markdown formatting, status display functions,
and export functionality.
"""

import unittest
import json
import csv
import tempfile
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from badge_generator import (
    generate_badge_url,
    generate_stats_badges,
    generate_badge_markdown,
    generate_readme_section
)

from status import (
    export_stats_json,
    export_stats_csv,
    export_stats_markdown
)

from analytics_db import AnalyticsDB


class TestBadgeGeneration(unittest.TestCase):
    """Test badge URL and markdown generation"""

    def test_generate_badge_url_basic(self):
        """Test basic badge URL generation"""
        url = generate_badge_url("sessions", "87", "blue")
        self.assertIn("https://img.shields.io/badge/", url)
        self.assertIn("sessions", url)
        self.assertIn("87", url)
        self.assertIn("blue", url)

    def test_generate_badge_url_special_chars(self):
        """Test badge URL with special characters"""
        url = generate_badge_url("time saved", "127.3 hours", "green")
        self.assertIn("https://img.shields.io/badge/", url)
        # Spaces should be encoded
        self.assertIn("time%20saved", url)
        self.assertIn("127.3%20hours", url)

    def test_generate_badge_url_dashes(self):
        """Test badge URL handles dashes correctly"""
        url = generate_badge_url("test-label", "test-value", "blue")
        # Single dashes should become double dashes for shields.io
        self.assertIn("test--label", url)
        self.assertIn("test--value", url)

    def test_generate_stats_badges_structure(self):
        """Test that generate_stats_badges returns expected structure"""
        # Create mock database
        db = Mock(spec=AnalyticsDB)
        db.get_aggregate_stats.return_value = {
            'total_sessions': 87,
            'time_saved_hours': 127.3,
            'success_rate': 95.8,
            'successful_sessions': 83,
            'total_decisions': 847,
            'total_resume_points': 1204,
            'total_files_changed': 523,
            'total_tokens_saved': 15000000
        }

        badges = generate_stats_badges(db)

        # Check expected badges exist
        self.assertIn('sessions', badges)
        self.assertIn('time_saved', badges)
        self.assertIn('success_rate', badges)
        self.assertIn('decisions', badges)
        self.assertIn('resume_points', badges)
        self.assertIn('files_changed', badges)

        # Check structure of each badge
        for badge_name, badge_data in badges.items():
            self.assertIn('url', badge_data)
            self.assertIn('alt_text', badge_data)
            self.assertIn('description', badge_data)
            self.assertTrue(badge_data['url'].startswith('https://img.shields.io/badge/'))

    def test_generate_stats_badges_success_rate_colors(self):
        """Test success rate badge uses appropriate colors"""
        db = Mock(spec=AnalyticsDB)

        # Test high success rate (>= 95%) -> brightgreen
        db.get_aggregate_stats.return_value = {
            'total_sessions': 100,
            'success_rate': 96.0,
            'successful_sessions': 96,
            'time_saved_hours': 100.0,
            'total_decisions': 100,
            'total_resume_points': 100,
            'total_files_changed': 100
        }
        badges = generate_stats_badges(db)
        self.assertIn('brightgreen', badges['success_rate']['url'])

        # Test medium success rate (>= 90%) -> green
        db.get_aggregate_stats.return_value['success_rate'] = 92.0
        badges = generate_stats_badges(db)
        self.assertIn('green', badges['success_rate']['url'])

        # Test lower success rate (>= 80%) -> yellowgreen
        db.get_aggregate_stats.return_value['success_rate'] = 85.0
        badges = generate_stats_badges(db)
        self.assertIn('yellowgreen', badges['success_rate']['url'])

    def test_generate_badge_markdown_inline(self):
        """Test inline markdown layout"""
        badges = {
            'sessions': {
                'url': 'https://img.shields.io/badge/sessions-87-blue',
                'alt_text': 'Total Sessions',
                'description': 'Number of sessions'
            },
            'time_saved': {
                'url': 'https://img.shields.io/badge/time%20saved-127.3%20hours-green',
                'alt_text': 'Time Saved',
                'description': 'Time saved'
            }
        }

        markdown = generate_badge_markdown(badges, layout='inline')

        # Should be on one line
        self.assertNotIn('\n\n', markdown.strip())

        # Should contain both badges
        self.assertIn('![Total Sessions]', markdown)
        self.assertIn('![Time Saved]', markdown)
        self.assertIn('https://img.shields.io/badge/sessions-87-blue', markdown)

    def test_generate_badge_markdown_grid(self):
        """Test grid markdown layout"""
        badges = {
            'badge1': {'url': 'url1', 'alt_text': 'Badge 1', 'description': 'Desc 1'},
            'badge2': {'url': 'url2', 'alt_text': 'Badge 2', 'description': 'Desc 2'},
            'badge3': {'url': 'url3', 'alt_text': 'Badge 3', 'description': 'Desc 3'},
        }

        markdown = generate_badge_markdown(badges, layout='grid')

        # Should have multiple lines (2 per line)
        lines = markdown.strip().split('\n')
        self.assertGreater(len(lines), 1)

        # Should contain all badges
        for badge_data in badges.values():
            self.assertIn(badge_data['alt_text'], markdown)

    def test_generate_badge_markdown_detailed(self):
        """Test detailed markdown layout with descriptions"""
        badges = {
            'sessions': {
                'url': 'https://img.shields.io/badge/sessions-87-blue',
                'alt_text': 'Total Sessions',
                'description': 'Number of session checkpoints'
            }
        }

        markdown = generate_badge_markdown(badges, layout='detailed')

        # Should include header
        self.assertIn('## Portfolio Metrics', markdown)

        # Should include badge
        self.assertIn('![Total Sessions]', markdown)

        # Should include description
        self.assertIn('Number of session checkpoints', markdown)

    def test_generate_badge_markdown_empty(self):
        """Test markdown generation with no badges"""
        markdown = generate_badge_markdown({})
        self.assertIn('No badges available', markdown)

    def test_generate_readme_section(self):
        """Test complete README section generation"""
        db = Mock(spec=AnalyticsDB)
        db.get_aggregate_stats.return_value = {
            'total_sessions': 87,
            'time_saved_hours': 127.3,
            'success_rate': 95.8,
            'successful_sessions': 83,
            'total_decisions': 847,
            'total_resume_points': 1204,
            'total_files_changed': 523,
            'total_tokens_saved': 0
        }

        section = generate_readme_section(db)

        # Should include header
        self.assertIn('## Context-Aware Memory System', section)
        self.assertIn('Lifetime Impact', section)

        # Should include badges
        self.assertIn('![', section)
        self.assertIn('https://img.shields.io/badge/', section)

        # Should include summary text
        self.assertIn('87 sessions', section)
        self.assertIn('127.3 hours', section)
        self.assertIn('95.8% success rate', section)


class TestExportFunctions(unittest.TestCase):
    """Test export functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.db = Mock(spec=AnalyticsDB)
        self.db.get_aggregate_stats.return_value = {
            'total_sessions': 87,
            'time_saved_hours': 127.3,
            'success_rate': 95.8,
            'successful_sessions': 83,
            'total_decisions': 847,
            'total_resume_points': 1204,
            'total_files_changed': 523
        }
        self.db.get_project_breakdown.return_value = [
            {
                'project_name': 'Project A',
                'total_sessions': 50,
                'successful_sessions': 48,
                'success_rate': 96.0,
                'total_files_changed': 300,
                'total_decisions': 400,
                'first_session': '2025-01-01T00:00:00',
                'last_session': '2025-01-05T00:00:00'
            },
            {
                'project_name': 'Project B',
                'total_sessions': 37,
                'successful_sessions': 35,
                'success_rate': 94.6,
                'total_files_changed': 223,
                'total_decisions': 447,
                'first_session': '2025-01-02T00:00:00',
                'last_session': '2025-01-05T00:00:00'
            }
        ]

    def test_export_stats_json_structure(self):
        """Test JSON export creates valid JSON with correct structure"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            output_path = f.name

        try:
            export_stats_json(self.db, output_path)

            # Read and parse JSON
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check structure
            self.assertIn('generated_at', data)
            self.assertIn('period_days', data)
            self.assertIn('summary', data)
            self.assertIn('projects', data)

            # Check summary data
            self.assertEqual(data['summary']['total_sessions'], 87)
            self.assertEqual(data['summary']['success_rate'], 95.8)

            # Check projects data
            self.assertEqual(len(data['projects']), 2)
            self.assertEqual(data['projects'][0]['project_name'], 'Project A')

        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_export_stats_csv_structure(self):
        """Test CSV export creates valid CSV with correct headers"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            output_path = f.name

        try:
            export_stats_csv(self.db, output_path)

            # Read and parse CSV
            with open(output_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)

            # Check header
            self.assertGreater(len(rows), 0)
            header = rows[0]
            self.assertIn('Project', header)
            self.assertIn('Total Sessions', header)
            self.assertIn('Success Rate %', header)

            # Check data rows
            self.assertEqual(len(rows), 3)  # Header + 2 projects
            self.assertEqual(rows[1][0], 'Project A')
            self.assertEqual(rows[1][1], '50')

        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_export_stats_markdown_structure(self):
        """Test Markdown export creates valid markdown"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            output_path = f.name

        try:
            export_stats_markdown(self.db, output_path)

            # Read markdown
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check structure
            self.assertIn('# Context-Aware Memory System', content)
            self.assertIn('## Summary Statistics', content)
            self.assertIn('## Project Breakdown', content)

            # Check data
            self.assertIn('87', content)  # Total sessions
            self.assertIn('127.3 hours', content)  # Time saved
            self.assertIn('95.8%', content)  # Success rate

            # Check markdown table
            self.assertIn('| Project | Sessions |', content)
            self.assertIn('| Project A |', content)

        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_export_json_with_days_filter(self):
        """Test JSON export with days filter"""
        self.db.get_session_stats.return_value = {
            'total_sessions': 20,
            'time_saved_hours': 30.0,
            'success_rate': 100.0,
            'successful_sessions': 20,
            'total_decisions': 150,
            'total_resume_points': 200,
            'total_files_changed': 100
        }

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            output_path = f.name

        try:
            export_stats_json(self.db, output_path, days=30)

            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check period is set correctly
            self.assertEqual(data['period_days'], 30)
            self.assertEqual(data['summary']['total_sessions'], 20)

        finally:
            Path(output_path).unlink(missing_ok=True)


class TestStatusDisplayFunctions(unittest.TestCase):
    """Test status display helper functions"""

    def setUp(self):
        """Set up test database"""
        self.db = Mock(spec=AnalyticsDB)
        self.db.conn = Mock()
        self.db.conn.cursor = Mock()

    def test_get_current_session_info_no_sessions(self):
        """Test current session info when no sessions exist"""
        from status import get_current_session_info

        with patch('status.Path.home') as mock_home:
            mock_session_dir = Mock()
            mock_session_dir.exists.return_value = False
            # Mock the __truediv__ (/) operator to return our mock directory
            mock_home.return_value.__truediv__.return_value = mock_session_dir

            info = get_current_session_info()

            self.assertIn('session_id', info)
            self.assertIn('status', info)
            self.assertEqual(info['status'], 'Not tracking')

    def test_display_functions_no_crash(self):
        """Test that display functions don't crash with valid data"""
        from status import (
            display_current_session,
            display_lifetime_stats,
            display_project_breakdown
        )

        self.db.get_aggregate_stats.return_value = {
            'total_sessions': 87,
            'time_saved_hours': 127.3,
            'success_rate': 95.8,
            'successful_sessions': 83,
            'total_decisions': 847,
            'total_resume_points': 1204,
            'total_tokens_saved': 0
        }

        self.db.get_project_breakdown.return_value = [
            {
                'project_name': 'Test Project',
                'total_sessions': 87,
                'successful_sessions': 83,
                'success_rate': 95.8,
                'total_files_changed': 523,
                'total_decisions': 847
            }
        ]

        # These should not raise exceptions
        try:
            display_current_session(self.db)
            display_lifetime_stats(self.db)
            display_project_breakdown(self.db)
        except Exception as e:
            self.fail(f"Display function raised exception: {e}")


class TestCLIArgumentParsing(unittest.TestCase):
    """Test CLI argument parsing (without executing main)"""

    def test_badge_generator_imports(self):
        """Test that badge_generator module imports successfully"""
        try:
            import badge_generator
            self.assertTrue(hasattr(badge_generator, 'generate_badge_url'))
            self.assertTrue(hasattr(badge_generator, 'generate_stats_badges'))
            self.assertTrue(hasattr(badge_generator, 'generate_badge_markdown'))
        except ImportError as e:
            self.fail(f"Failed to import badge_generator: {e}")

    def test_status_imports(self):
        """Test that status module imports successfully"""
        try:
            import status
            self.assertTrue(hasattr(status, 'export_stats_json'))
            self.assertTrue(hasattr(status, 'export_stats_csv'))
            self.assertTrue(hasattr(status, 'export_stats_markdown'))
        except ImportError as e:
            self.fail(f"Failed to import status: {e}")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""

    def test_badge_generation_with_zero_stats(self):
        """Test badge generation with zero values"""
        db = Mock(spec=AnalyticsDB)
        db.get_aggregate_stats.return_value = {
            'total_sessions': 0,
            'time_saved_hours': 0.0,
            'success_rate': 0.0,
            'successful_sessions': 0,
            'total_decisions': 0,
            'total_resume_points': 0,
            'total_files_changed': 0,
            'total_tokens_saved': 0
        }

        badges = generate_stats_badges(db)

        # Should still generate badges with "0" values
        self.assertIn('sessions', badges)
        self.assertIn('0', badges['sessions']['url'])

    def test_badge_generation_handles_exception(self):
        """Test badge generation handles database errors gracefully"""
        db = Mock(spec=AnalyticsDB)
        db.get_aggregate_stats.side_effect = Exception("Database error")

        badges = generate_stats_badges(db)

        # Should return empty dict on error
        self.assertEqual(badges, {})

    def test_export_functions_with_none_days(self):
        """Test export functions work with days=None"""
        db = Mock(spec=AnalyticsDB)
        db.get_aggregate_stats.return_value = {
            'total_sessions': 50,
            'time_saved_hours': 75.0,
            'success_rate': 100.0,
            'successful_sessions': 50,
            'total_decisions': 300,
            'total_resume_points': 400,
            'total_files_changed': 200
        }
        db.get_project_breakdown.return_value = []

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            output_path = f.name

        try:
            # Should not raise exception
            export_stats_json(db, output_path, days=None)

            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.assertEqual(data['period_days'], 'all_time')

        finally:
            Path(output_path).unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
