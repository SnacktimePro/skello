#!/usr/bin/env python3
"""
Easy-Venv CLI Entry Point

Create a Python virtual environment, upgrade pip, install dependencies,
and optionally launch an activated shell.
"""

import argparse
import textwrap
from pathlib import Path
from typing import List

from .file_manager import FileManager
from .venv_manager import VirtualEnvironmentManager
from .dependency_handler import DependencyHandler
from .shell_launcher import ShellLauncher

# Your mapping of all possible inputs to a standardized name
OPTION_MAP = {
    # requirements.txt
    'r': 'requirements', 'req': 'requirements', 'requirements': 'requirements',
    # pyproject.toml
    'p': 'pyproject', 'toml': 'pyproject', 'pyproject': 'pyproject',
    # .gitignore
    'g': 'gitignore', 'git': 'gitignore', 'gitignore': 'gitignore',
    # README.md
    'md': 'readme', 'read': 'readme', 'readme': 'readme',
    # CHANGELOG.md
    'c': 'changelog', 'log': 'changelog', 'changelog': 'changelog', 
    # LICENSE
    'l': 'license', 'lic': 'license', 'license': 'license',
    # MAIN STRUCTURE
    'm': 'main', 'main': 'main', 'structure': 'structure',
    # All files
    '*': 'all', 'all': 'all',
}

# Define what 'all' expands to. We get the unique values from the map, excluding 'all' itself.
ALL_FILES = sorted(list(set(v for v in OPTION_MAP.values() if v != 'all')))


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
            %(prog)s -c all                           # Create all project files
            %(prog)s -c r g readme                    # Create requirements, gitignore, readme
            %(prog)s -p /path/to/project -c all -s    # Full setup but skip auto shell
            
            Create flags (can be combined with commas):
            r/req/requirements    →  requirements.txt
            p/toml/pyproject      →  pyproject.toml  
            g/git/gitignore       →  .gitignore
            md/read/readme        →  README.md
            c/log/changelog       →  CHANGELOG.md
            l/mit/license         →  LICENSE
            */all                 →  All project files
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
        nargs='*',  # 👈 Accept 0 or more space-separated values
        choices=OPTION_MAP.keys(),  # 👈 Validate against the allowed keys
        metavar="FILE_TYPE", # 👈 A clean name for the help message
        help=f"Create project files. Options: {' '.join(ALL_FILES)}. Use 'all' for all files."
    )
    
    parser.add_argument(
        "-s", "--no-auto-shell",
        action="store_true",
        help="Skip automatically launching an activated shell session"
    )

    return parser.parse_args()

def get_files_to_create(create_args: List[str]) -> List[str]:
    """
    Takes the list of file aliases from argparse and returns a clean list
    of standardized file type names.
    """
    if not create_args:
        return []

    # Use a set for efficiency and to automatically handle duplicates
    # (e.g., if user types "-c r requirements")
    standardized_choices = {OPTION_MAP[arg] for arg in create_args}

    # If 'all' is in the set, immediately return the full list
    if 'all' in standardized_choices:
        return ALL_FILES

    return sorted(list(standardized_choices))


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
    dependency_handler.detect_and_install()
     # Parse create options if provided
    if args.create:
        files = get_files_to_create(args.create)
        # Create project files if requested
        if files:
            file_manager.create_project_files(files)
    
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