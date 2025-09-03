#!/usr/bin/env python3
"""
Easy-Venv CLI Entry Point

Create a Python virtual environment, upgrade pip, install dependencies, 
scaffold project files and optionally launch an activated shell.
"""

import argparse
import textwrap
from pathlib import Path

from .models.cli_handler import CLIHandler
from .scaffold_manger import ScaffoldManager
from .venv_manager import VirtualEnvironmentManager
from .dependency_handler import DependencyHandler
from .shell_launcher import ShellLauncher


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="easy-venv",
        description=(
            "Create a Python virtual environment, upgrade pip, install dependencies, "
            "and optionally scaffold project files - all in one command."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
            %(prog)s                                  # Basic venv setup (current directory, .venv)
            %(prog)s -p /path/to/project              # Specify project path only
            %(prog)s -p /path/to/project -n myenv     # Custom env name
            %(prog)s -c all                           # Create all project files + full structure
            %(prog)s -c r g read main                 # Create requirements, gitignore, readme + main structure
            %(prog)s -c l:apache:Your Name            # Create an Apache license with your name
            %(prog)s -c r:dev-requirements.txt        # Create a requirements file named dev-requirements.txt
            %(prog)s -p /path/to/project -c full -s   # Full structure but skip auto shell
            
            File types:
            r/req       →  requirements.txt
            p/toml      →  pyproject.toml  
            g/git       →  .gitignore
            md/read     →  README.md
            ch/log      →  CHANGELOG.md
            l/lic       →  LICENSE
            
            Structure templates:
            m/main                →  Creates src/package/main.py structure
            f/full                →  Creates complete project with tests
            */all                 →  All files + full structure
            """)
    )

    parser.add_argument(
        "-p", "--path",
        type=str,
        default=".",
        help="Target directory for the virtual environment and project files (default: current directory)"
    )
    
    parser.add_argument(
        "-n", "--name",
        type=str,
        default=".venv",
        help="Name of the virtual environment folder (default: .venv)"
    )
    
    parser.add_argument(
        "-c", "--create",
        nargs='*',
        metavar="SPEC",
        help="Create files and structures using 'TYPE' or 'TYPE:ARG1:ARG2' syntax."
    )
    
    parser.add_argument(
        "-s", "--no-auto-shell",
        action="store_true",
        help="Skip automatically launching an activated shell session"
    )

    return parser.parse_args()


def main():
    """Main CLI entry point."""
    args = parse_args()
    
    # Create project context from CLI args
    target_path = Path(args.path).resolve()
    cli_handler = CLIHandler.from_cli(target_path, args.create)
    
    # Initialize managers
    venv_manager = VirtualEnvironmentManager(cli_handler.target_dir, args.name)
    dependency_handler = DependencyHandler(cli_handler.target_dir, venv_manager)
    shell_launcher = ShellLauncher(venv_manager)
    
    print(f"🎯 Target directory: {cli_handler.target_dir}")

    # Execute workflow
    venv_manager.create_environment()
    venv_manager.upgrade_pip()
    dependency_handler.detect_and_install()
    
    # Scaffold project if specifications provided
    if args.create:
        scaffold_context = cli_handler.build_context()
        print("\n📋 Project Configuration:")
        print(scaffold_context.project_summary())
        scaffold_manager = ScaffoldManager()
        scaffold_manager.execute_plan(scaffold_context)
    
    print("\n🎉 Setup complete!")
    
    # Launch shell or show manual instructions
    if not args.no_auto_shell:
        print(f"🚀 Automatically launching activated shell session...")
        shell_launcher.launch_activated_shell()
    else:
        print(shell_launcher.get_manual_activation_instructions())
    
    # Show summary information
    info = venv_manager.get_info()
    print(f"\n📁 Paths:")
    print(f"   Virtual environment: {info['venv_dir']}")
    print(f"   Project directory: {info['target_dir']}")


if __name__ == "__main__":
    main()