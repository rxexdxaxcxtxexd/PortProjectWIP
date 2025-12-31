"""
Interactive Component Showcase for Claude Terminal UI Design System

This demo provides:
- Interactive menu system to explore components
- Before/after comparisons showing raw print vs UI components
- All component variants with real-world examples
- Portfolio-ready presentation

Run: python -m claude_terminal_ui.examples.demo_showcase
Or: python examples/demo_showcase.py
"""

import sys
import time
from pathlib import Path
from typing import Callable, Dict, List

# Add src to path if running from examples directory
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import claude_terminal_ui as ui
from claude_terminal_ui.tokens.colors import Colors


class ShowcaseDemo:
    """Interactive showcase for the Terminal UI Design System"""

    def __init__(self):
        self.demos: Dict[str, Callable] = {
            "1": ("Status Messages", self.demo_status_messages),
            "2": ("Headers & Dividers", self.demo_headers),
            "3": ("Progress Indicators", self.demo_progress),
            "4": ("Tables", self.demo_tables),
            "5": ("Trees & Lists", self.demo_trees),
            "6": ("Panels & Boxes", self.demo_panels),
            "7": ("Real-World Examples", self.demo_real_world),
            "8": ("Before/After Comparison", self.demo_before_after),
            "9": ("Terminal Capabilities", self.demo_capabilities),
        }

    def clear_screen(self):
        """Clear the screen (cross-platform)"""
        print("\n" * 3)  # Simple scroll clear for better portability

    def show_menu(self):
        """Display main menu"""
        self.clear_screen()
        print(ui.header("CLAUDE TERMINAL UI - INTERACTIVE SHOWCASE", width=70))
        print()

        print(ui.panel(
            "Portfolio-Ready Component Library\n"
            "Professional terminal UIs for Python CLI applications",
            title="Design System v0.1.0",
            color=Colors.INFO,
            width=70
        ))
        print()

        print(ui.subheader("Component Categories", width=70))
        print()

        # Create menu with tree structure
        menu_items = [
            ui.TreeNode("1. Status Messages", [
                ui.TreeNode("Success, Error, Warning, Info, Debug")
            ]),
            ui.TreeNode("2. Headers & Dividers", [
                ui.TreeNode("Major headers, Subheaders, Dividers, Steps")
            ]),
            ui.TreeNode("3. Progress Indicators", [
                ui.TreeNode("Progress bars, Spinners, Step indicators")
            ]),
            ui.TreeNode("4. Tables", [
                ui.TreeNode("Key-value pairs, Data tables, Stats panels")
            ]),
            ui.TreeNode("5. Trees & Lists", [
                ui.TreeNode("Tree structures, Nested lists")
            ]),
            ui.TreeNode("6. Panels & Boxes", [
                ui.TreeNode("Bordered panels, Info boxes, Titled boxes")
            ]),
            ui.TreeNode("7. Real-World Examples", [
                ui.TreeNode("Complete application scenarios")
            ]),
            ui.TreeNode("8. Before/After Comparison", [
                ui.TreeNode("Raw print vs UI components")
            ]),
            ui.TreeNode("9. Terminal Capabilities", [
                ui.TreeNode("Auto-detection and fallbacks")
            ]),
        ]

        for item in menu_items:
            print(ui.tree(item, indent=2))
            print()

        print(ui.divider(width=70))
        print()
        print("  0. Run All Demos")
        print("  q. Quit")
        print()

    def demo_status_messages(self):
        """Demonstrate status message components"""
        print(ui.header("1. STATUS MESSAGES", width=70))
        print()

        print(ui.compact_panel(
            {
                "Component": "Status Messages",
                "Functions": "5 variants",
                "Use Case": "Operation feedback, logging, alerts"
            },
            title="Component Info",
            width=70,
            color=Colors.INFO
        ))
        print()

        print(ui.subheader("All Status Types", width=70))
        print()

        # Basic usage
        print("  Basic Usage:")
        print()
        ui.print_success("Database connection established successfully")
        ui.print_error("Failed to authenticate user credentials")
        ui.print_warning("Cache size exceeding recommended limit (85%)")
        ui.print_info("Processing batch 3 of 12 (1,234 records)")
        ui.print_debug("Query execution time: 145ms (cache hit)")
        print()

        # With indentation
        print("  With Indentation:")
        print()
        print(ui.success("Build completed", indent=4))
        print(ui.success("Tests passed (127/127)", indent=8))
        print(ui.warning("2 deprecation warnings", indent=8))
        print(ui.info("Generated documentation", indent=4))
        print()

        # Nested workflow example
        print("  Real Workflow Example:")
        print()
        ui.print_info("Starting deployment pipeline...")
        print(ui.success("Code linting passed", indent=4))
        print(ui.success("Unit tests passed (156/156)", indent=4))
        print(ui.success("Integration tests passed (23/23)", indent=4))
        print(ui.warning("Coverage: 87% (target: 90%)", indent=4))
        print(ui.success("Build artifacts created", indent=4))
        ui.print_success("Deployment complete!")
        print()

    def demo_headers(self):
        """Demonstrate header components"""
        print(ui.header("2. HEADERS & DIVIDERS", width=70))
        print()

        print(ui.info_panel(
            "Headers provide visual hierarchy and structure to terminal output",
            title="Component Info",
            panel_type="info"
        ))
        print()

        print("  Major Section Header:")
        print()
        print(ui.header("SYSTEM CONFIGURATION", width=70))
        print()

        print("  Subsection Header:")
        print()
        print(ui.subheader("Database Settings", width=70))
        print()

        print("  Simple Divider:")
        print()
        print(ui.divider(width=70))
        print()

        print("  Labeled Divider:")
        print()
        print(ui.divider(width=70, label="Section Break"))
        print()

        print("  Step Headers (for multi-step processes):")
        print()
        print(ui.step_header(1, 4, "Initialize configuration"))
        print(ui.step_header(2, 4, "Connect to services"))
        print(ui.step_header(3, 4, "Validate settings"))
        print(ui.step_header(4, 4, "Apply changes"))
        print()

    def demo_progress(self):
        """Demonstrate progress indicators"""
        print(ui.header("3. PROGRESS INDICATORS", width=70))
        print()

        print(ui.titled_box(
            [
                "Progress bars for batch operations",
                "Spinners for indeterminate tasks",
                "Step indicators for multi-stage processes"
            ],
            title="Use Cases",
            width=70,
            color=Colors.SUCCESS
        ))
        print()

        print("  Progress Bars (various states):")
        print()
        print(f"    Empty:     {ui.progress_bar(0, 100, width=40)}")
        print(f"    Starting:  {ui.progress_bar(15, 100, width=40)}")
        print(f"    Progress:  {ui.progress_bar(45, 100, width=40)}")
        print(f"    Almost:    {ui.progress_bar(85, 100, width=40)}")
        print(f"    Complete:  {ui.progress_bar(100, 100, width=40)}")
        print()

        print("  With Custom Labels:")
        print()
        print(f"    {ui.progress_bar(67, 100, width=35, prefix='Files: ', suffix=' (234/350)')}")
        print(f"    {ui.progress_bar(92, 100, width=35, prefix='Upload: ', suffix=' (4.6/5.0 GB)')}")
        print()

        print("  Step Indicators:")
        print()
        for i in range(1, 6):
            status = ui.success("Complete") if i < 4 else ui.info("In progress") if i == 4 else ""
            print(f"    {ui.step_indicator(i, 5, f'Processing batch {i}...')} {status}")
        print()

        print("  Spinner Demo (animated, 2 seconds):")
        print()
        with ui.spinner("  Loading configuration data"):
            time.sleep(2)
        ui.print_success("  Configuration loaded!", indent=2)
        print()

    def demo_tables(self):
        """Demonstrate table components"""
        print(ui.header("4. TABLES", width=70))
        print()

        print("  Key-Value Pairs (aligned colons):")
        print()
        session_info = {
            "Session ID": "5150ba34",
            "Started": "2025-12-29 14:30:15",
            "User": "admin@example.com",
            "Tokens Used": "12,450 / 200,000",
            "Status": "Active",
        }
        print(ui.key_value(session_info, indent=4, value_color=Colors.SUCCESS))
        print()

        print("  Data Table (with borders):")
        print()
        headers = ["Task ID", "Status", "Duration", "Progress"]
        data = [
            ["TASK-001", "Complete", "2.3s", "100%"],
            ["TASK-002", "Running", "5.1s", "67%"],
            ["TASK-003", "Pending", "-", "0%"],
            ["TASK-004", "Failed", "1.2s", "45%"],
        ]
        print(ui.table(data, headers=headers, align=['left', 'left', 'right', 'right']))
        print()

        print("  Stats Panel (grid layout):")
        print()
        stats = {
            "Total Tasks": "156",
            "Completed": "142",
            "Failed": "8",
            "Pending": "6",
            "Success Rate": "91.0%",
            "Avg Duration": "3.2s",
        }
        print(ui.stats_panel(stats, title="PIPELINE STATISTICS", width=70, columns=3))
        print()

        print("  Stats Panel (list layout):")
        print()
        db_stats = {
            "Connections": "45 active",
            "Query Rate": "1,234 qps",
            "Cache Hit": "87.5%",
            "Avg Latency": "12ms",
        }
        print(ui.stats_panel(db_stats, title="Database Metrics", layout="list", width=50))
        print()

    def demo_trees(self):
        """Demonstrate tree and list components"""
        print(ui.header("5. TREES & LISTS", width=70))
        print()

        print("  Simple Tree (flat list with title):")
        print()
        tasks = ["Initialize database", "Load configuration", "Start services", "Run health checks"]
        print(ui.simple_tree(tasks, title="Startup Tasks", indent=4, color=Colors.SUCCESS))
        print()

        print("  Complex Tree (nested structure):")
        print()
        project_tree = ui.TreeNode("Project Structure", [
            ui.TreeNode("src/", [
                ui.TreeNode("components/", [
                    ui.TreeNode("status.py"),
                    ui.TreeNode("headers.py"),
                    ui.TreeNode("progress.py"),
                ]),
                ui.TreeNode("core/", [
                    ui.TreeNode("capabilities.py"),
                ]),
            ]),
            ui.TreeNode("tests/", [
                ui.TreeNode("test_status.py"),
                ui.TreeNode("test_headers.py"),
            ]),
            ui.TreeNode("examples/", [
                ui.TreeNode("demo_showcase.py"),
            ]),
        ])
        print(ui.tree(project_tree, indent=4))
        print()

        print("  Nested List (with bullet points):")
        print()
        items = [
            "Phase 1: Planning",
            ("Requirements", [
                "Gather stakeholder input",
                "Define success criteria",
            ]),
            ("Design", [
                "Create mockups",
                "Review with team",
            ]),
            "Phase 2: Implementation",
        ]
        print(ui.nested_list(items, indent=4, color=Colors.INFO))
        print()

    def demo_panels(self):
        """Demonstrate panel and box components"""
        print(ui.header("6. PANELS & BOXES", width=70))
        print()

        print("  Basic Panel (with title):")
        print()
        print(ui.panel(
            "This is a simple panel with a title.\nIt can contain multiple lines of text.",
            title="Sample Panel",
            width=60,
            color=Colors.INFO
        ))
        print()

        print("  Simple Box (no title):")
        print()
        print(ui.box(
            "Important notice: System maintenance tonight at 10 PM",
            width=60,
            color=Colors.WARNING
        ))
        print()

        print("  Info Panels (typed with icons):")
        print()
        print(ui.info_panel("Configuration loaded successfully", panel_type="success"))
        print()
        print(ui.info_panel("API rate limit approaching (80% used)", panel_type="warning"))
        print()
        print(ui.info_panel("Connection timeout after 3 retries", panel_type="error"))
        print()
        print(ui.info_panel("Processing 1,234 records...", panel_type="info"))
        print()

        print("  Titled Box (with list items):")
        print()
        tasks = [
            "Review pull requests",
            "Update documentation",
            "Run integration tests",
            "Deploy to staging"
        ]
        print(ui.titled_box(tasks, title="Today's Tasks", width=50, color=Colors.SUCCESS))
        print()

        print("  Compact Panel (key-value pairs):")
        print()
        system_info = {
            "Hostname": "prod-server-01",
            "OS": "Ubuntu 22.04 LTS",
            "Uptime": "45 days, 3 hours",
            "Load": "2.34, 2.12, 1.98"
        }
        print(ui.compact_panel(system_info, title="System Info", width=50, color=Colors.INFO))
        print()

    def demo_real_world(self):
        """Demonstrate real-world application scenarios"""
        print(ui.header("7. REAL-WORLD EXAMPLES", width=70))
        print()

        print(ui.subheader("Example 1: Deployment Pipeline", width=70))
        print()

        ui.print_info("Starting deployment to production...")
        print()

        # Pre-deployment checks
        print(ui.step_header(1, 4, "Running pre-deployment checks"))
        time.sleep(0.3)
        print(ui.success("Git repository is clean", indent=4))
        print(ui.success("All tests passing", indent=4))
        print(ui.success("Security scan complete", indent=4))
        print()

        # Build stage
        print(ui.step_header(2, 4, "Building application"))
        time.sleep(0.3)
        print(f"    {ui.progress_bar(100, 100, width=40, prefix='Build: ')}")
        print(ui.success("Build artifacts generated", indent=4))
        print()

        # Deploy stage
        print(ui.step_header(3, 4, "Deploying to production"))
        time.sleep(0.3)
        print(f"    {ui.progress_bar(100, 100, width=40, prefix='Deploy: ')}")
        print(ui.success("3 instances updated", indent=4))
        print()

        # Verification
        print(ui.step_header(4, 4, "Running smoke tests"))
        time.sleep(0.3)
        print(ui.success("Health check: OK", indent=4))
        print(ui.success("API endpoints responding", indent=4))
        print()

        ui.print_success("Deployment completed successfully!")
        print()

        print(ui.divider(width=70, label="Results"))
        print()

        deployment_stats = {
            "Duration": "2m 34s",
            "Instances": "3/3 healthy",
            "Version": "v2.1.5",
            "Status": "Active"
        }
        print(ui.compact_panel(deployment_stats, title="Deployment Summary", width=50, color=Colors.SUCCESS))
        print()

        print(ui.divider(width=70))
        print()

        print(ui.subheader("Example 2: Data Processing Job", width=70))
        print()

        ui.print_info("Processing customer data export...")
        print()

        job_config = {
            "Job ID": "export-2025-12-29-001",
            "Dataset": "customers_2025",
            "Records": "45,678",
            "Format": "CSV"
        }
        print(ui.key_value(job_config, indent=4))
        print()

        # Processing stages
        stages = [
            ("Extract", 100),
            ("Transform", 100),
            ("Validate", 67),
            ("Load", 0),
        ]

        for stage_name, progress in stages:
            bar = ui.progress_bar(progress, 100, width=35, prefix=f"{stage_name}: ")
            status = ui.success("Complete") if progress == 100 else ui.info("In progress") if progress > 0 else ""
            print(f"    {bar} {status}")
        print()

        processing_stats = {
            "Processed": "30,502",
            "Valid": "30,450",
            "Errors": "52",
            "Success Rate": "99.8%"
        }
        print(ui.stats_panel(
            processing_stats,
            title="PROCESSING STATISTICS",
            width=60,
            columns=2,
            title_color=Colors.INFO
        ))
        print()

    def demo_before_after(self):
        """Show before/after comparison of raw print vs UI components"""
        print(ui.header("8. BEFORE/AFTER COMPARISON", width=70))
        print()

        print(ui.info_panel(
            "See how the UI components improve readability and professionalism",
            title="Comparison Demo",
            panel_type="info"
        ))
        print()

        # Example 1: Status messages
        print(ui.subheader("Status Messages", width=70))
        print()

        print(ui.box("  BEFORE (raw print):", width=68, color=Colors.ERROR))
        print()
        print("  [OK] Task completed")
        print("  [ERROR] Connection failed")
        print("  [WARNING] Low memory")
        print()

        print(ui.box("  AFTER (UI components):", width=68, color=Colors.SUCCESS))
        print()
        ui.print_success("  Task completed", indent=0)
        ui.print_error("  Connection failed", indent=0)
        ui.print_warning("  Low memory", indent=0)
        print()

        # Example 2: Data display
        print(ui.subheader("Data Display", width=70))
        print()

        print(ui.box("  BEFORE (raw print):", width=68, color=Colors.ERROR))
        print()
        print("  Server: prod-01")
        print("  Status: Running")
        print("  Uptime: 45 days")
        print("  Load: 2.34")
        print()

        print(ui.box("  AFTER (UI components):", width=68, color=Colors.SUCCESS))
        print()
        server_data = {
            "Server": "prod-01",
            "Status": "Running",
            "Uptime": "45 days",
            "Load": "2.34"
        }
        print(ui.compact_panel(server_data, title="Server Status", width=40, color=Colors.INFO))
        print()

        # Example 3: Progress
        print(ui.subheader("Progress Indication", width=70))
        print()

        print(ui.box("  BEFORE (raw print):", width=68, color=Colors.ERROR))
        print()
        print("  Processing... 67% complete")
        print()

        print(ui.box("  AFTER (UI components):", width=68, color=Colors.SUCCESS))
        print()
        print(f"    {ui.progress_bar(67, 100, width=40, prefix='Processing: ')}")
        print()

    def demo_capabilities(self):
        """Show detected terminal capabilities"""
        from claude_terminal_ui.core.capabilities import get_capabilities

        print(ui.header("9. TERMINAL CAPABILITIES", width=70))
        print()

        print(ui.info_panel(
            "The design system automatically detects terminal capabilities\n"
            "and gracefully degrades features when needed",
            title="Auto-Detection",
            panel_type="info"
        ))
        print()

        caps = get_capabilities()

        print(ui.subheader("Detected Capabilities", width=70))
        print()

        capabilities = {
            "Terminal": caps.terminal_name or "Unknown",
            "Color Support": f"{caps.color_support.name} ({caps.color_support.value} colors)",
            "Unicode": "Enabled" if caps.unicode_support else "Disabled (ASCII fallback)",
            "Terminal Size": f"{caps.width}x{caps.height} characters",
            "Interactive": "Yes" if caps.is_interactive else "No",
            "Platform": "Windows" if caps.is_windows else "Unix/Linux/macOS",
            "Hyperlinks": "Supported" if caps.supports_hyperlinks else "Not supported",
        }
        print(ui.key_value(capabilities, indent=4, value_color=Colors.SUCCESS))
        print()

        print(ui.subheader("Fallback Behavior", width=70))
        print()

        fallbacks = ui.TreeNode("Graceful Degradation", [
            ui.TreeNode("Unicode → ASCII", [
                ui.TreeNode("Box drawing: ┌─┐ → +-+"),
                ui.TreeNode("Bullets: • → *"),
                ui.TreeNode("Arrows: → → ->"),
            ]),
            ui.TreeNode("Colors → Monochrome", [
                ui.TreeNode("Status colors removed"),
                ui.TreeNode("Formatting preserved"),
            ]),
            ui.TreeNode("Interactive → Static", [
                ui.TreeNode("Spinners → Simple text"),
                ui.TreeNode("Animations disabled"),
            ]),
        ])
        print(ui.tree(fallbacks, indent=4))
        print()

        print(ui.subheader("Cross-Platform Compatibility", width=70))
        print()

        platforms = [
            "Windows Terminal (full support)",
            "PowerShell (full support)",
            "Windows CMD (ASCII fallback)",
            "macOS Terminal (full support)",
            "Linux terminals (full support)",
            "VS Code integrated terminal (full support)",
            "SSH sessions (adaptive)",
            "CI/CD pipelines (graceful degradation)",
        ]
        print(ui.simple_tree(platforms, title="Tested Platforms", indent=4, color=Colors.SUCCESS))
        print()

    def run_all_demos(self):
        """Run all demos in sequence"""
        all_demos = [
            self.demo_status_messages,
            self.demo_headers,
            self.demo_progress,
            self.demo_tables,
            self.demo_trees,
            self.demo_panels,
            self.demo_real_world,
            self.demo_before_after,
            self.demo_capabilities,
        ]

        for i, demo in enumerate(all_demos, 1):
            self.clear_screen()
            demo()

            if i < len(all_demos):
                print(ui.divider(width=70))
                print()
                input("  Press Enter to continue to next demo...")
                print()

        print(ui.divider(width=70))
        print()
        ui.print_success("All demos completed!")
        print()
        input("  Press Enter to return to menu...")

    def run(self):
        """Main showcase loop"""
        while True:
            self.show_menu()

            choice = input("  Select option (0-9, q): ").strip().lower()
            print()

            if choice == 'q':
                self.clear_screen()
                print(ui.header("THANK YOU!", width=70))
                print()
                print(ui.panel(
                    "Claude Terminal UI Design System\n"
                    "Professional terminal UIs for Python CLI applications\n\n"
                    "Visit: github.com/yourusername/claude-terminal-ui",
                    title="Portfolio Project",
                    color=Colors.SUCCESS,
                    width=70
                ))
                print()
                break

            elif choice == '0':
                self.run_all_demos()

            elif choice in self.demos:
                self.clear_screen()
                _, demo_func = self.demos[choice]
                demo_func()
                print(ui.divider(width=70))
                print()
                input("  Press Enter to return to menu...")

            else:
                print(ui.error(f"Invalid choice: {choice}"))
                time.sleep(1)


def main():
    """Entry point for the showcase demo"""
    try:
        showcase = ShowcaseDemo()
        showcase.run()
    except KeyboardInterrupt:
        print()
        print()
        ui.print_info("Showcase interrupted by user")
        print()
    except Exception as e:
        print()
        ui.print_error(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        print()


if __name__ == "__main__":
    main()
