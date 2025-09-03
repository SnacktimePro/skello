# Easy-Venv

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**A complete Python project initialization tool - create virtual environments, install dependencies, and scaffold modern project structure in seconds!**

---

## Why Easy-Venv?

Setting up a Python project often involves the same repetitive steps:

1. Create a virtual environment (`python -m venv .venv`).
2. Activate it.
3. Upgrade pip (`pip install --upgrade pip`).
4. Install dependencies from various file formats (`pyproject.toml`, `requirements.txt`, `Pipfile`, etc.).
5. Create project files (README, .gitignore, LICENSE, etc.).
6. Navigate to your project directory.

**Easy-Venv** automates ALL these steps into a single command and automatically launches you into an activated shell session, ready to start coding immediately!

---

## Features

-   ✅ **One-Command Setup**: Creates venv, upgrades pip, installs dependencies, AND launches activated shell
-   🏗️ **Modern Project Scaffolding**: Optionally generate complete project structure with `--create`
-   🚀 **Auto-Activation**: Automatically opens a new shell with your environment activated
-   🖥️ **Cross-Platform**: Works reliably on Windows (PowerShell), macOS, and Linux
-   📁 **Remote Project Setup**: Work on any project directory from anywhere on your system
-   📦 **Multi-Format Support**: Detects and installs from `pyproject.toml`, `requirements.txt`, `Pipfile`, and more
-   🔧 **Modern Standards**: Prefers `pyproject.toml` over legacy `requirements.txt`
-   📝 **Smart File Creation**: Only creates files that don't already exist - never overwrites
-   🛠️ **Fully Optional**: Every feature is optional - use what you need, skip what you don't
-   🧘 **Safe**: Validates directories and handles existing environments gracefully
-   📖 **Beginner-Friendly**: Clear progress indicators and helpful error messages

---

## Installation

### Option 1: Global Installation (Recommended)

Install once and use from anywhere:

```bash
git clone https://github.com/snacktimepro/easy-venv.git
cd easy-venv
pip install -e .
```

After installation, use `easy-venv` command from anywhere on your system!

### Option 2: Direct Usage

Download and run directly:

```bash
git clone https://github.com/snacktimepro/easy-venv.git
cd easy-venv
python -m easy_venv -p /path/to/project
```

---

## Usage

### Basic Usage - The Magic! ✨

Simply run in any directory and Easy-Venv will:

1. Create `.venv` and upgrade pip
2. Detect and install dependencies from existing files (`pyproject.toml`, `requirements.txt`, `Pipfile`, etc.)
3. (Optional)Scaffold modern project structure if requested
4. Launch a new shell with everything activated!

```bash
# Creates venv and launches activated shell
easy-venv

# Work on any project from anywhere
easy-venv -p /path/to/my/project
```

### Project Scaffolding - The Real Power! 🏗️

Create complete, modern Python projects instantly:

```bash
# Create a complete modern Python project (power user style)
easy-venv -c *
# → Creates: pyproject.toml, .gitignore, README.md, CHANGELOG.md, LICENSE, and venv!

# Ultra-short power user combinations
easy-venv -c p g l          # pyproject, gitignore, license
easy-venv -c l g c          # license, gitignore, changelog
easy-venv -c p md c         # pyproject, readme, changelog

# Medium-length for readability
easy-venv -c toml git lic   # same as above but clearer
easy-venv -c lic git log    # license, gitignore, changelog

# Full names for ultimate clarity
easy-venv -c pyproject gitignore license

# Mix and match styles as you prefer
easy-venv -p ~/my-project -n dev -c *
```

### Advanced Usage

```bash
# Legacy requirements.txt support
easy-venv -c r g            # requirements, gitignore (short)
easy-venv -c req git        # requirements, gitignore (medium)

# Custom project path with specific files
easy-venv -p ~/projects/web-app -c p md l    # pyproject, readme, license

# Skip auto-shell launch for automation
easy-venv -c * -s           # all files, no shell

# Just create venv without any files
easy-venv -p ~/existing-project
```

---

## Command-Line Options

| Option            | Short | Default                 | Description                                             |
| ----------------- | ----- | ----------------------- | ------------------------------------------------------- |
| `--path`          | `-p`  | `.` (current directory) | Target directory for the virtual environment and files  |
| `--name`          | `-n`  | `.venv`                 | Name of the virtual environment folder                  |
| `--create`        | `-c`  | None                    | Create project files (see options below)                |
| `--no-auto-shell` | `-s`  | False                   | Skip automatically launching an activated shell session |
| `--help`          | `-h`  | -                       | Show help message and exit                              |

### Project File Creation Options

| Short | Medium | Creates              | Description                        |
| ----- | ------ | -------------------- | ---------------------------------- |
| `p`   | `toml` | `pyproject.toml`     | Modern Python package config       |
| `r`   | `req`  | `requirements.txt`   | Legacy pip requirements            |
| `g`   | `git`  | `.gitignore`         | Git ignore rules for Python        |
| `md`  | `read` | `README.md`          | Project documentation              |
| `ch`  | `log`  | `CHANGELOG.md`       | Keep a Changelog format            |
| `l`   | `lic`  | `LICENSE`            | MIT license with current year      |
| `m`   | `main` | `main.py`            | Creates Python package layout      |
| `f`   | `full` | `main.py + tests.py` | Creates Full Python package layout |
| `*`   | `all`  | All modern files     | Everything except requirements     |

---

## Real-World Examples

### Scenario 1: Brand New Project - Full Setup

```bash
# Create everything for a new Python project (power user)
mkdir my-awesome-app
easy-venv -p my-awesome-app -c *

# Same thing with readable medium style
easy-venv -p my-awesome-app -c toml git read log lic

# Result: Complete project with:
# ✅ Virtual environment (.venv)
# ✅ Modern packaging (pyproject.toml)
# ✅ Git ignore (.gitignore)
# ✅ Documentation (README.md)
# ✅ Changelog (CHANGELOG.md)
# ✅ License (LICENSE)
# ✅ Activated shell ready to go!
```

### Scenario 2: Existing Project - Just Environment

```bash
# Setup venv for existing project with dependencies
easy-venv -p ~/projects/existing-app
# → Detects pyproject.toml/requirements.txt, installs deps, activates
```

### Scenario 3: Selective File Creation

```bash
# Just add missing essentials to existing project (power user)
easy-venv -p ~/my-project -c l g          # license, gitignore

# Add modern packaging to legacy project (medium style)
easy-venv -p ~/old-project -c toml        # pyproject.toml

# Create documentation files only (mixed styles)
easy-venv -p ~/my-lib -c md log           # readme, changelog
```

### Scenario 4: Multiple Environments

```bash
# Different environments for same project
easy-venv -p ~/my-project -n dev -c p     # pyproject only
easy-venv -p ~/my-project -n test -c r    # requirements only
easy-venv -p ~/my-project -n prod         # just venv
```

### Scenario 5: CI/CD and Automation

```bash
# Automated setup without shell launch
easy-venv -p /path/to/project -c * -s     # all files, no shell

# Just environment setup for containers
easy-venv -s                              # venv only, no shell
```

---

## What Easy-Venv Does

1. **🎯 Validates** the target directory exists and is accessible
2. **🌱 Creates** a virtual environment (skips if already exists)
3. **🔧 Upgrades** pip to the latest version
4. **📝 Creates** project files (only if specified and don't exist)
5. **📦 Detects** dependency files (`pyproject.toml`, `requirements.txt`, `Pipfile`, etc.)
6. **⬇️ Installs** dependencies from detected files (if present and not empty)
7. **🚀 Launches** a new shell session with the environment activated and correct directory!

---

## Smart Project File Logic

Easy-Venv makes intelligent decisions about file creation:

### Dependency File Priority

1. **`pyproject.toml`** - Modern Python packaging standard (preferred)
2. **`requirements.txt`** - Legacy pip requirements (for compatibility)
3. **`Pipfile`** - Pipenv format
4. **Other formats** - Additional formats as detected

### Smart Behaviors

-   **Prevents conflicts**: Won't create `requirements.txt` if creating `pyproject.toml`
-   **Respects existing**: Never overwrites existing files
-   **Modern by default**: `*` and `all` create `pyproject.toml`, not `requirements.txt`
-   **Clear messaging**: Explains why files are created or skipped

---

## Example Sessions

### Complete New Project Setup

```bash
$ easy-venv -p ~/my-new-api -c all

🎯 Target directory: /home/user/my-new-api
🌱 Creating virtual environment in '/home/user/my-new-api/.venv'...
🔧 Upgrading pip...
📝 Created project files: pyproject.toml, .gitignore, README.md, CHANGELOG.md, LICENSE

🎉 Setup complete!
🚀 Automatically launching activated shell session...
🎉 Virtual environment activated in new shell!
📁 Current directory: /home/user/my-new-api
🐍 Virtual environment: /home/user/my-new-api/.venv
✨ You can now work in your activated environment. Type 'exit' to return.

(.venv) user@computer:~/my-new-api$ # Ready to code!
```

### Existing Project with Dependencies

```bash
$ easy-venv -p ~/existing-project

🎯 Target directory: /home/user/existing-project
🌱 Creating virtual environment in '/home/user/existing-project/.venv'...
🔧 Upgrading pip...
📦 Found pyproject.toml - installing dependencies...
📦 Installing dependencies from pyproject.toml...

🎉 Setup complete!
🚀 Automatically launching activated shell session...
(.venv) user@computer:~/existing-project$ # Dependencies installed and ready!
```

---

## Generated File Templates

### pyproject.toml (Modern Standard)

-   Complete modern Python packaging configuration
-   Build system setup with hatchling
-   Development dependencies included
-   Tool configurations (black, isort, pytest)
-   Ready for `pip install -e .`

### .gitignore (Comprehensive)

-   Python-specific ignore patterns
-   Virtual environment exclusions
-   IDE and OS file exclusions
-   Build and distribution ignores

### README.md (Professional)

-   Project title with badges
-   Installation instructions
-   Usage examples
-   Contributing guidelines

### CHANGELOG.md (Keep a Changelog Format)

-   Semantic versioning ready
-   Organized by release sections
-   Standard change categories

### LICENSE (MIT with Current Year)

-   MIT license text
-   Current year automatically inserted
-   Placeholder for author name

---

## Error Handling & Safety

Easy-Venv handles edge cases gracefully:

-   **Missing target directory**: Clear error message with path validation
-   **File conflicts**: Never overwrites existing files, shows what was skipped
-   **Invalid file options**: Validates create options and shows available choices
-   **Empty dependency files**: Informative message, skips installation
-   **Existing virtual environment**: Skips creation, proceeds with other steps
-   **Permission issues**: Clear error messages with suggested solutions
-   **Shell launch failures**: Falls back to manual activation instructions

---

## Platform Support

### Windows

-   **PowerShell**: Full support with colored output and proper activation
-   **Command Prompt**: Alternative batch scripts when needed
-   **Path Handling**: Automatic Windows path formatting

### macOS/Linux

-   **Bash/Zsh**: Native shell integration with `exec` for seamless experience
-   **Permissions**: Proper executable permissions on scripts
-   **Symbolic Links**: Full support for linked directories

---

## Tips & Best Practices

### 🎯 **Workflow Tips**

-   **Complete setup**: Use `easy-venv -c all` for new projects
-   **Selective creation**: Add missing files to existing projects with specific flags
-   **Modern standards**: Prefer `pyproject` over `requirements` for new projects
-   **Remote management**: Keep Easy-Venv installed globally, work on projects anywhere

### 📁 **Organization Tips**

-   **Consistent structure**: Use `all` for uniform project layouts
-   **Documentation first**: Always include `readme` and `license`
-   **Version control ready**: Include `gitignore` from the start
-   **Professional setup**: Add `changelog` for release tracking

### 🚀 **Power User Tips**

-   **Automation friendly**: Use `-s` flag in scripts and CI/CD
-   **Quick iterations**: `easy-venv -c pyproject && code .` for instant development
-   **Batch processing**: Set up multiple projects with shell loops
-   **Template projects**: Create template directories and scaffold them with Easy-Venv

---

## Why This Approach Rocks

### Traditional Way (Multiple Commands)

```bash
mkdir my-project && cd my-project
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install --upgrade pip
# Create pyproject.toml manually...
# Create .gitignore manually...
# Create README.md manually...
# Create LICENSE manually...
# ...5-10 minutes later you can start coding
```

### Easy-Venv Way (One Command)

```bash
easy-venv -p my-project -c *
# 🎉 Done! Activated shell, all files created, ready to code in 10 seconds
```

### The Best Part: It's All Optional!

-   **Just need a venv?** → `easy-venv`
-   **Need project files?** → `easy-venv -c *`
-   **Existing project?** → `easy-venv -p existing-project`
-   **Specific files only?** → `easy-venv -c l g` (license, gitignore)
-   **Automation script?** → `easy-venv -c * -s`

---

## Requirements

-   **Python 3.7+** (no external dependencies!)
-   **PowerShell** (Windows) or **Bash** (macOS/Linux)
-   **Pip** (included with Python)

---

## Installation Methods Summary

| Method             | Command                      | Use Case             |
| ------------------ | ---------------------------- | -------------------- |
| **Global Install** | `pip install -e .`           | Best for daily use   |
| **User Install**   | `pip install -e . --user`    | No admin permissions |
| **Virtual Env**    | `pip install -e .` (in venv) | Development/testing  |
| **Direct Run**     | `python -m easy_venv`        | One-time use         |

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
git clone https://github.com/snacktimepro/easy-venv.git
cd easy-venv
easy-venv -c all  # Use Easy-Venv to set up Easy-Venv! 🎉
```

---

## Support

If you encounter any issues:

1. **Check the help**: `easy-venv -h`
2. **Review examples**: Common patterns above
3. **Check permissions**: Run as administrator on Windows if needed
4. **Open an issue**: Include your OS, Python version, and error message

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for a full list of changes.

---

_Made with ❤️ to make Python development setup effortless_

**From zero to fully-configured Python project in seconds! 🚀**
