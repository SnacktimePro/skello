import argparse
import subprocess
import sys
import venv
from pathlib import Path
from typing import List

def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="A script to create a Python virtual environment, upgrade pip, and install dependencies from a requirements file.",
        epilog="Example: python setup_venv.py -p /path/to/project -n myenv -r dev-requirements.txt"
    )
    parser.add_argument(
        "-p", "--path",
        type=str,
        default=".",
        help="The target directory path where the venv and requirements file are located (default: current directory)"
    )
    parser.add_argument(
        "-n", "--name",
        type=str,
        default=".venv",
        help="The name of the virtual environment folder (default: .venv)"
    )
    parser.add_argument(
        "-r", "--requirements",
        type=str,
        default="requirements.txt",
        help="The name of the requirements file (default: requirements.txt)"
    )
    parser.add_argument(
        "--no-create-requirements",
        action="store_true",
        help="Skip creating requirements.txt if it doesn't exist"
    )
    return parser.parse_args()

def get_python_executable(venv_dir: Path) -> Path:
    """Gets the path to the Python executable in the virtual environment."""
    if sys.platform == "win32":
        return venv_dir / "Scripts" / "python.exe"
    else:
        return venv_dir / "bin" / "python"

def run_command(python_executable: Path, command: List[str], venv_dir: Path):
    """Runs a command using the virtual environment's Python interpreter."""
    try:
        subprocess.check_call([python_executable] + command)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {' '.join(command)}")
        print(f"   Venv: {venv_dir}")
        print(f"   Error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ Error: Could not find Python executable at '{python_executable}'")
        sys.exit(1)

def create_requirements_file(req_file: Path):
    """Creates a basic requirements.txt file."""
    content = [
        "# TODO: Add your project dependencies here",
        "# This file was auto-created by Easy-Venv because it was missing",
        "# Example: requests>=2.28.0",
        ""
    ]
    
    try:
        with open(req_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        print(f"📝 Created requirements.txt (auto-generated because it was missing)")
        return True
    except Exception as e:
        print(f"❌ Error creating requirements file: {e}")
        return False

def main():
    """Main script execution."""
    args = parse_args()
    
    # Resolve the target directory
    target_dir = Path(args.path).resolve()
    
    # Validate target directory exists
    if not target_dir.exists():
        print(f"❌ Error: Target directory '{target_dir}' does not exist.")
        sys.exit(1)
    
    if not target_dir.is_dir():
        print(f"❌ Error: '{target_dir}' is not a directory.")
        sys.exit(1)
    
    # Set up paths relative to target directory
    venv_dir = target_dir / args.name
    req_file = target_dir / args.requirements
    
    print(f"🎯 Target directory: {target_dir}")
    
    # 1. Create the virtual environment
    if not venv_dir.exists():
        print(f"🌱 Creating virtual environment in '{venv_dir}'...")
        venv.create(venv_dir, with_pip=True)
    else:
        print(f"✅ Virtual environment '{venv_dir}' already exists. Skipping creation.")

    python_executable = get_python_executable(venv_dir)

    # 2. Upgrade pip
    print("🔧 Upgrading pip...")
    run_command(python_executable, ["-m", "pip", "install", "--upgrade", "pip"], venv_dir)

    # 3. Handle requirements file
    if not req_file.is_file():
        if not args.no_create_requirements:
            create_requirements_file(req_file)
        else:
            print(f"⚠️  Warning: Requirements file not found at '{req_file}'. Skipping dependency installation.")
    elif req_file.stat().st_size == 0:
        print(f"🤔 Requirements file '{req_file}' is empty. Nothing to install.")
    else:
        print(f"📦 Installing dependencies from '{req_file}'...")
        run_command(python_executable, ["-m", "pip", "install", "-r", str(req_file)], venv_dir)

    print("\n🎉 Setup complete!")
    
    # 4. Provide activation instructions
    if sys.platform == "win32":
        activate_script = venv_dir / "Scripts" / "Activate.ps1"
        print(f"   To activate, run: {activate_script}")
    else:
        activate_script = venv_dir / "bin" / "activate"
        print(f"   To activate, run: source {activate_script}")
    
    print(f"   Virtual environment location: {venv_dir}")
    print(f"   Project directory: {target_dir}")

if __name__ == "__main__":
    main()