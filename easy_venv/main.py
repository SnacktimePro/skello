import argparse
import subprocess
import sys
import textwrap
import venv
from pathlib import Path
from typing import List


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
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
        const="requirements.txt",   # default if they don’t pass a filename
        help="Create a basic requirements file (default: requirements.txt). "
            "Optionally pass a filename, e.g. --create-requirements dev-requirements.txt"
    )
    parser.add_argument(
        "-s", "--no-auto-shell",
        action="store_true",
        help="Skip automatically launching an activated shell session"
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
    
def detect_and_install_dependencies(target_dir: Path, python_executable: Path, venv_dir: Path, create_requirements_filename: str = None):
    """Detects and installs dependencies based on available configuration files."""
    
    # Check for dependency files in order of preference
    pyproject_toml = target_dir / "pyproject.toml"
    requirements_txt = target_dir / "requirements.txt"
    pipfile = target_dir / "Pipfile"
    environment_yml = target_dir / "environment.yml"
    
    if pyproject_toml.exists():
        print(f"📦 Found pyproject.toml - installing project in editable mode...")
        try:
            # First install build dependencies
            run_command(python_executable, ["-m", "pip", "install", "build"], venv_dir)
            # Then install the project in editable mode
            run_command(python_executable, ["-m", "pip", "install", "-e", "."], venv_dir)
        except Exception as e:
            print(f"⚠️  Warning: Failed to install from pyproject.toml. Trying pip install anyway...")
            run_command(python_executable, ["-m", "pip", "install", "-e", str(target_dir)], venv_dir)
            
    elif requirements_txt.exists() and requirements_txt.stat().st_size > 0:
        print(f"📦 Installing dependencies from requirements.txt...")
        run_command(python_executable, ["-m", "pip", "install", "-r", str(requirements_txt)], venv_dir)
        
    elif requirements_txt.exists() and requirements_txt.stat().st_size == 0:
        print(f"🤔 Found empty requirements.txt - nothing to install")
        
    elif pipfile.exists():
        print(f"📦 Found Pipfile - attempting to extract requirements...")
        try:
            # Try to use pipenv to generate requirements, fallback to warning
            result = subprocess.run([
                "pipenv", "requirements"
            ], capture_output=True, text=True, cwd=target_dir)
            
            if result.returncode == 0:
                # Create temporary requirements file from pipenv output
                temp_req = target_dir / ".temp_requirements.txt"
                with open(temp_req, 'w') as f:
                    f.write(result.stdout)
                
                run_command(python_executable, ["-m", "pip", "install", "-r", str(temp_req)], venv_dir)
                temp_req.unlink()  # Clean up
                print(f"✅ Installed dependencies from Pipfile")
            else:
                print(f"⚠️  Found Pipfile but pipenv not available. Consider converting to requirements.txt or pyproject.toml")
                
        except FileNotFoundError:
            print(f"⚠️  Found Pipfile but pipenv not installed. Consider converting to requirements.txt or pyproject.toml")
            
    elif environment_yml.exists():
        print(f"⚠️  Found environment.yml (conda file) - this tool works with pip. Consider creating pyproject.toml or requirements.txt")
        
    elif create_requirements_filename:
        # Create requirements file with the specified name
        req_file = target_dir / create_requirements_filename
        if req_file.exists():
            print(f"✅ {create_requirements_filename} already exists - skipping creation")
        else:
            print(f"📝 Creating {create_requirements_filename}...")
            if create_requirements_file(req_file):
                print(f"✅ Created {create_requirements_filename} - you can now add your dependencies")
        
    else:
        print(f"📭 No dependency files found - skipping package installation")
        print(f"   Looked for: pyproject.toml, requirements.txt, Pipfile, environment.yml")
        print(f"   Use --create-requirements [filename] to generate a requirements file")

def launch_activated_shell(target_dir: Path, venv_dir: Path):
    """Launches a new shell with the virtual environment already activated."""
    try:
        if sys.platform == "win32":
            # Windows: Try PowerShell first, fallback to Command Prompt
            activate_ps1 = venv_dir / "Scripts" / "Activate.ps1"
            activate_bat = venv_dir / "Scripts" / "activate.bat"

            # Define the CMD command once to avoid repetition
            cmd_command = f'cd /d "{target_dir}" && "{activate_bat}" && echo 🎉 Virtual environment activated! && cmd /k'

            if activate_ps1.exists():
                # Use textwrap.dedent to remove leading whitespace from the multi-line string
                powershell_command = textwrap.dedent(f'''
                    Set-Location "{target_dir}"
                    try {{
                        & "{activate_ps1}"
                        Write-Host "🎉 Virtual environment activated in new shell!" -ForegroundColor Green
                        Write-Host "📁 Current directory: {target_dir}" -ForegroundColor Cyan
                    }} catch {{
                        Write-Host "⚠️ PowerShell activation failed." -ForegroundColor Yellow
                    }}
                    Write-Host "✨ You can now work in your activated environment. Type 'exit' to return." -ForegroundColor Yellow
                ''')

                print("🚀 Launching new PowerShell session...")
                try:
                    subprocess.run(
                        ["powershell.exe", "-ExecutionPolicy", "Bypass", "-NoExit", "-Command", powershell_command],
                        cwd=target_dir,
                        check=True
                    )
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("⚠️ PowerShell failed or not found, trying Command Prompt...")
                    subprocess.run(["cmd", "/c", cmd_command], cwd=target_dir)

            elif activate_bat.exists():
                print("🚀 Launching new Command Prompt session...")
                subprocess.run(["cmd", "/c", cmd_command], cwd=target_dir)
            else:
                raise FileNotFoundError("No Windows activation scripts (Activate.ps1, activate.bat) found.")

        else:
            # Unix-like systems: Launch bash with virtual environment activated
            activate_script = venv_dir / "bin" / "activate"
            if not activate_script.exists():
                raise FileNotFoundError(f"Activation script not found: {activate_script}")

            # Use shlex.quote() for security against command injection
            safe_target_dir = shlex.quote(str(target_dir))
            safe_activate_script = shlex.quote(str(activate_script))

            bash_command = textwrap.dedent(f'''
                cd {safe_target_dir}
                source {safe_activate_script}
                echo "🎉 Virtual environment activated in new shell!"
                echo "📁 Current directory: {target_dir}"
                echo "✨ You can now work in your activated environment. Type 'exit' to return."
                exec bash
            ''')

            print("🚀 Launching new shell session...")
            subprocess.run(["bash", "-c", bash_command], cwd=target_dir)

        print("👋 Returned from activated shell session.")

    except Exception as e:
        print(f"❌ Error launching activated shell: {e}")
        # Manual instructions are already great, no changes needed here.
        print("📋 Manual activation instructions:")
        if sys.platform == "win32":
            print(f"   In PowerShell: & '{venv_dir / 'Scripts' / 'Activate.ps1'}'")
            print(f"   In Cmd.exe:    \"{venv_dir / 'Scripts' / 'activate.bat'}\"")
        else:
            print(f"   In your shell: source '{venv_dir / 'bin' / 'activate'}'")
        print(f"   Then navigate to your directory: cd \"{target_dir}\"")

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

    # 3. Handle dependencies
    detect_and_install_dependencies(target_dir, python_executable, venv_dir, args.create_requirements)

    print("\n🎉 Setup complete!")
    
    # 4. Automatically launch activated shell (unless disabled)
    if not args.no_auto_shell:
        print(f"🚀 Automatically launching activated shell session...")
        launch_activated_shell(target_dir, venv_dir)
    else:
        print("\n📋 Manual activation instructions:")
        if sys.platform == "win32":
            activate_script = venv_dir / "Scripts" / "Activate.ps1"
            print(f"   PowerShell: {activate_script}")
            print(f"   Then run: cd \"{target_dir}\"")
        else:
            activate_script = venv_dir / "bin" / "activate"
            print(f"   Terminal: source {activate_script}")
            print(f"   Then run: cd \"{target_dir}\"")
    
    print(f"\n📁 Paths:")
    print(f"   Virtual environment: {venv_dir}")
    print(f"   Project directory: {target_dir}")

if __name__ == "__main__":
    main()