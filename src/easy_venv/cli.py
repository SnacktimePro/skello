#!/usr/bin/env python3
"""
Easy-Venv CLI Entry Point

Create a Python virtual environment, upgrade pip, install dependencies,
and optionally launch an activated shell.
"""

import argparse
import textwrap
from pathlib import Path

from .file_manager import FileManager
from .venv_manager import VirtualEnvironmentManager
from .dependency_handler import DependencyHandler
from .shell_launcher import ShellLauncher


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="easy-venv",
        description=(
            "Create a Python virtual environment, upgrade pip, install dependencies, "
            "and optionally launch an activated shell."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
            %(prog)s                                  # All defaults (current directory, .venv)
            %(prog)s -p /path/to/project              # Specify project path only
            %(prog)s -p /path/to/project -n myenv     # Custom env name
            %(prog)s -p /path/to/project -r           # Create requirements.txt if no dependencies found
            %(prog)s -p /path/to/project -s           # Skip auto shell launch
            """)
    )

    parser.add_argument(
        "-p", "--path",
        type=str,
        default=".",
        help="Target directory for the virtual environment and requirements file (default: current directory)"
    )
    parser.add_argument(
        "-n", "--name",
        type=str,
        default=".venv",
        help="Name of the virtual environment folder (default: .venv)"
    )
    parser.add_argument(
        "-r", "--create-requirements",
        nargs="?",
        const="requirements.txt",   # default if they don't pass a filename
        help="Create a basic requirements file (default: requirements.txt). "
            "Optionally pass a filename, e.g. --create-requirements dev-requirements.txt"
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
    
    # Initialize managers
    file_manager = FileManager(Path(args.path))
    venv_manager = VirtualEnvironmentManager(file_manager.target_dir, args.name)
    dependency_handler = DependencyHandler(venv_manager, file_manager)
    shell_launcher = ShellLauncher(venv_manager)
    
    print(f"🎯 Target directory: {file_manager.target_dir}")
    
    # Execute workflow
    venv_manager.create_environment()
    venv_manager.upgrade_pip()
    dependency_handler.detect_and_install(args.create_requirements)
    
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