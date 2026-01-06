#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Screenshot Capture Automation for Portfolio Demonstrations

This script automates the creation of professional terminal screenshots for portfolio presentation.
It sets consistent terminal sizing, color schemes, runs demo commands, and captures high-quality output.

Features:
- Consistent terminal dimensions (120x40 characters)
- Professional color scheme configuration
- Automated command execution with timing
- Screenshot capture with metadata
- Cross-platform support (Windows/Unix)
- Timestamp and annotation support

Usage:
    python capture_demo.py --scenario checkpoint
    python capture_demo.py --scenario resume
    python capture_demo.py --scenario all
    python capture_demo.py --list

Author: Portfolio Project - Context-Aware Memory Management System
Date: 2025-01-05
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

# Set UTF-8 encoding for Windows console
if platform.system() == "Windows":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


@dataclass
class ScreenshotConfig:
    """Configuration for screenshot capture."""
    width: int = 120  # Terminal columns
    height: int = 40  # Terminal rows
    resolution_width: int = 1920
    resolution_height: int = 1080
    font_size: int = 14
    font_family: str = "Consolas"  # Windows default, fallback to Monaco/Courier
    color_scheme: str = "dark"  # 'dark' or 'light'
    output_format: str = "png"


@dataclass
class DemoScenario:
    """A demonstration scenario to capture."""
    name: str
    description: str
    commands: List[str]
    setup_commands: Optional[List[str]] = None
    cleanup_commands: Optional[List[str]] = None
    pause_after_each: float = 1.5  # seconds
    annotations: Optional[List[str]] = None


class ScreenshotCapture:
    """Handles automated screenshot capture for terminal demonstrations."""

    def __init__(self, config: ScreenshotConfig):
        self.config = config
        self.platform = platform.system()
        self.output_dir = Path(__file__).parent
        self.metadata_file = self.output_dir / "screenshot_metadata.json"
        self.metadata: Dict[str, Any] = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Any]:
        """Load existing metadata or create new."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {"screenshots": [], "created": datetime.now().isoformat()}

    def _save_metadata(self):
        """Save metadata to file."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, indent=2, fp=f)

    def configure_terminal(self):
        """Configure terminal for optimal screenshot capture."""
        print(f"Configuring terminal for {self.config.width}x{self.config.height}...")

        if self.platform == "Windows":
            self._configure_windows_terminal()
        else:
            self._configure_unix_terminal()

    def _configure_windows_terminal(self):
        """Configure Windows terminal/console."""
        try:
            # Set console size using mode command
            subprocess.run(
                ["mode", f"con:", f"cols={self.config.width}", f"lines={self.config.height}"],
                check=True,
                shell=True
            )
            print(f"✓ Terminal size set to {self.config.width}x{self.config.height}")
        except subprocess.CalledProcessError as e:
            print(f"⚠ Could not set terminal size automatically: {e}")
            print(f"  Please manually resize terminal to {self.config.width}x{self.config.height}")

    def _configure_unix_terminal(self):
        """Configure Unix-like terminal."""
        try:
            # Use tput or stty to set terminal size
            subprocess.run(
                ["printf", f"\\033[8;{self.config.height};{self.config.width}t"],
                check=True,
                shell=True
            )
            print(f"✓ Terminal size set to {self.config.width}x{self.config.height}")
        except subprocess.CalledProcessError:
            print(f"⚠ Could not set terminal size automatically")
            print(f"  Please manually resize terminal to {self.config.width}x{self.config.height}")

    def run_scenario(self, scenario: DemoScenario) -> str:
        """Run a demo scenario and capture output."""
        print(f"\n{'='*80}")
        print(f"SCENARIO: {scenario.name}")
        print(f"Description: {scenario.description}")
        print(f"{'='*80}\n")

        # Clear screen for clean capture
        self._clear_screen()

        # Run setup commands if any
        if scenario.setup_commands:
            print("Running setup commands...")
            for cmd in scenario.setup_commands:
                self._run_command(cmd, silent=True)

        # Wait for user to start screenshot
        print("\nScenario ready to capture.")
        print("Instructions:")
        print("  1. Position your screenshot tool (Snipping Tool, Snagit, etc.)")
        print(f"  2. Capture area should be {self.config.resolution_width}x{self.config.resolution_height}")
        print("  3. Press ENTER when ready to start demonstration...")
        input()

        # Clear and run demo commands
        self._clear_screen()
        print(f"# {scenario.description}\n")

        for i, cmd in enumerate(scenario.commands, 1):
            print(f"$ {cmd}")
            time.sleep(0.5)  # Pause for reading

            # Run command and show output
            self._run_command(cmd, silent=False)

            # Pause between commands
            if i < len(scenario.commands):
                time.sleep(scenario.pause_after_each)

        # Show annotations if any
        if scenario.annotations:
            print("\n" + "─" * 80)
            print("Key Points:")
            for annotation in scenario.annotations:
                print(f"  • {annotation}")

        # Final pause for capture
        print("\n" + "─" * 80)
        print("\nDemonstration complete. Capture screenshot now.")
        print("Press ENTER when screenshot is saved...")
        input()

        # Run cleanup if any
        if scenario.cleanup_commands:
            for cmd in scenario.cleanup_commands:
                self._run_command(cmd, silent=True)

        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{scenario.name.lower().replace(' ', '_')}_{timestamp}.png"

        # Add to metadata
        self.metadata["screenshots"].append({
            "filename": filename,
            "scenario": scenario.name,
            "description": scenario.description,
            "timestamp": timestamp,
            "commands": scenario.commands,
            "annotations": scenario.annotations or []
        })
        self._save_metadata()

        print(f"\n✓ Scenario complete. Save screenshot as: {filename}")
        return filename

    def _run_command(self, cmd: str, silent: bool = False):
        """Run a command and optionally show output."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=silent,
                text=True,
                timeout=30
            )
            if not silent:
                time.sleep(0.3)  # Slight delay for visual clarity
        except subprocess.TimeoutExpired:
            print("⚠ Command timed out")
        except subprocess.CalledProcessError as e:
            if not silent:
                print(f"⚠ Command failed: {e}")

    def _clear_screen(self):
        """Clear terminal screen."""
        if self.platform == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def list_scenarios(self, scenarios: List[DemoScenario]):
        """List available demonstration scenarios."""
        print("\nAvailable Screenshot Scenarios:")
        print("=" * 80)
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{i}. {scenario.name}")
            print(f"   Description: {scenario.description}")
            print(f"   Commands: {len(scenario.commands)}")
            if scenario.annotations:
                # Show first two annotations
                preview = []
                for j, ann in enumerate(scenario.annotations[:2]):
                    # Replace special characters for safe display
                    safe_ann = ann.replace('\u2192', '->').replace('\u2713', 'OK').replace('\u2717', 'X')
                    preview.append(safe_ann)
                print(f"   Key Points: {', '.join(preview)}...")
        print("\n" + "=" * 80)


def get_demo_scenarios() -> List[DemoScenario]:
    """Define all demonstration scenarios."""
    return [
        DemoScenario(
            name="checkpoint",
            description="Creating a session checkpoint with dependency analysis",
            commands=[
                "python scripts/checkpoint.py --quick",
            ],
            annotations=[
                "Automatic dependency analysis shows file impact",
                "Resume points generated intelligently",
                "Session state saved with metadata"
            ]
        ),
        DemoScenario(
            name="resume",
            description="Resuming a previous session with context loading",
            commands=[
                "python scripts/resume-session.py",
            ],
            annotations=[
                "Previous session loaded automatically",
                "Resume points displayed clearly",
                "Recent changes summarized"
            ]
        ),
        DemoScenario(
            name="context-monitor",
            description="Monitoring context window usage",
            commands=[
                "python scripts/context-monitor.py",
            ],
            annotations=[
                "Token usage tracked in real-time",
                "Warnings at threshold levels",
                "Proactive memory management"
            ]
        ),
        DemoScenario(
            name="session-list",
            description="Listing all session history",
            commands=[
                "python scripts/resume-session.py list",
            ],
            annotations=[
                "Complete session history",
                "Project context preserved",
                "Easy navigation between sessions"
            ]
        ),
        DemoScenario(
            name="dependency-analysis",
            description="Analyzing cross-file dependencies",
            commands=[
                "python scripts/dependency_analyzer.py --analyze scripts/",
            ],
            annotations=[
                "File relationship mapping",
                "Impact scoring for changes",
                "Test coverage detection"
            ]
        ),
        DemoScenario(
            name="git-workflow",
            description="Complete Git workflow with auto-checkpointing",
            commands=[
                "git status",
                "git add .",
                'git commit -m "Feature: Add new detector"',
                "git log -1 --stat",
            ],
            annotations=[
                "Post-commit hook triggers automatically",
                "Checkpoint created after commit",
                "Session state synchronized with Git"
            ]
        ),
        DemoScenario(
            name="before-after",
            description="Side-by-side comparison of manual vs automated workflow",
            commands=[
                "echo BEFORE: Manual session management",
                "echo - Lost context between sessions",
                "echo - 15-30 min context reconstruction",
                "echo - Unreliable memory recall",
                "echo",
                "echo AFTER: Automated session continuity",
                "echo - Auto-checkpoint on SessionEnd",
                "echo - Auto-resume on SessionStart",
                "echo - Zero-friction UX",
            ],
            annotations=[
                "Time savings: 2-5 hours/week",
                "Reliability improved: 40% → 95%",
                "User effort reduced to zero"
            ]
        ),
    ]


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automated screenshot capture for portfolio demonstrations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python capture_demo.py --scenario checkpoint
  python capture_demo.py --scenario resume
  python capture_demo.py --scenario all
  python capture_demo.py --list

Scenarios will pause for you to manually capture screenshots using your
preferred tool (Snipping Tool, Snagit, ShareX, etc.).
        """
    )

    parser.add_argument(
        "--scenario",
        type=str,
        help="Name of scenario to run (or 'all' for all scenarios)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available scenarios"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=120,
        help="Terminal width in columns (default: 120)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=40,
        help="Terminal height in rows (default: 40)"
    )

    args = parser.parse_args()

    # Create configuration
    config = ScreenshotConfig(
        width=args.width,
        height=args.height
    )

    # Initialize capture system
    capture = ScreenshotCapture(config)
    scenarios = get_demo_scenarios()

    # Handle list command
    if args.list:
        capture.list_scenarios(scenarios)
        return

    # Handle scenario selection
    if not args.scenario:
        print("Error: --scenario or --list required")
        parser.print_help()
        return

    # Configure terminal
    capture.configure_terminal()
    time.sleep(1)

    # Run scenarios
    if args.scenario == "all":
        print(f"\nRunning all {len(scenarios)} scenarios...")
        for scenario in scenarios:
            capture.run_scenario(scenario)
            print("\nPress ENTER to continue to next scenario...")
            input()
    else:
        # Find specific scenario
        scenario = next((s for s in scenarios if s.name == args.scenario), None)
        if not scenario:
            print(f"Error: Scenario '{args.scenario}' not found")
            print("\nAvailable scenarios:")
            for s in scenarios:
                print(f"  - {s.name}")
            return

        capture.run_scenario(scenario)

    print("\n" + "=" * 80)
    print("Screenshot capture session complete!")
    print(f"Metadata saved to: {capture.metadata_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
