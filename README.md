# Easy-Venv

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**A simple, cross-platform script to quickly create a Python virtual environment, upgrade pip, install dependencies from multiple file formats, and automatically launch an activated shell - all from anywhere on your system!**

---

## Why Easy-Venv?

Setting up a Python project often involves the same repetitive steps:

1. Create a virtual environment (`python -m venv .venv`).
2. Activate it.
3. Upgrade pip (`pip install --upgrade pip`).
4. Install dependencies from various file formats (`pyproject.toml`, `requirements.txt`, `Pipfile`, etc.).
5. Navigate to your project directory.

**Easy-Venv** automates ALL these steps into a single command and automatically launches you into an activated shell session, ready to start coding immediately!

---

## Features

-   ✅ **One-Command Setup**: Creates venv, upgrades pip, installs dependencies, AND launches activated shell
-   🚀 **Auto-Activation**: Automatically opens a new shell with your environment activated
-   🖥️ **Cross-Platform**: Works reliably on Windows (PowerShell), macOS, and Linux
-   📁 **Remote Project Setup**: Work on any project directory from anywhere on your system
-   📦 **Multi-Format Support**: Detects and installs from `pyproject.toml`, `requirements.txt`, `Pipfile`, and more
-   📝 **Optional Template Generation**: Create `requirements.txt` template with flag when needed
-   🛠️ **Customizable**: All options have convenient short flags (`-p`, `-n`, `-r`, `-s`)
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
3. Launch a new shell with everything activated!

```bash
# Creates venv and launches activated shell
easy-venv

# Work on any project from anywhere
easy-venv -p /path/to/my/project
```

### Advanced Usage with Short Flags

```bash
# All the power with convenient short options
easy-venv -p ~/projects/web-app -n dev

# Create requirements.txt template when needed
easy-venv -p ~/my-project -r

# Create custom requirements file
easy-venv -p ~/my-project -r dev-requirements.txt

# Skip auto-features when needed
easy-venv -p ~/my-project -s  # no auto-shell

# Mix and match
easy-venv -p "C:\Users\Me\Desktop\my-project" -n production
```

---

## Command-Line Options

| Option                  | Short | Default                 | Description                                                                 |
| ----------------------- | ----- | ----------------------- | --------------------------------------------------------------------------- |
| `--path`                | `-p`  | `.` (current directory) | Target directory containing your project                                    |
| `--name`                | `-n`  | `.venv`                 | Name of the virtual environment folder                                      |
| `--create-requirements` | `-r`  | None                    | Create requirements file (default: requirements.txt) or specify custom name |
| `--no-auto-shell`       | `-s`  | False                   | Skip automatically launching an activated shell session                     |
| `--help`                | `-h`  | -                       | Show help message and exit                                                  |

---

## Real-World Examples

### Scenario 1: New Project Setup

```bash
# Start a new project
mkdir my-new-project
easy-venv -p my-new-project
# → Creates venv, detects existing dependency files, launches activated shell

# Create with requirements.txt template
easy-venv -p my-new-project -r
# → Also generates requirements.txt template for manual editing

# Create with custom requirements file name
easy-venv -p my-new-project -r dev-requirements.txt
# → Creates dev-requirements.txt template
```

### Scenario 2: Existing Project

```bash
# Setup existing project with dependencies
easy-venv -p ~/projects/existing-app
# → Auto-detects pyproject.toml, requirements.txt, Pipfile, etc.
# → Installs dependencies, launches activated shell
```

### Scenario 3: Multiple Environments

```bash
# Different environments for the same project
easy-venv -p ~/my-project -n dev-env -r requirements-dev.txt
easy-venv -p ~/my-project -n test-env -r requirements-test.txt
easy-venv -p ~/my-project -n prod-env -r requirements-prod.txt
```

### Scenario 4: CI/CD or Automated Scripts

```bash
# Skip auto-shell for automation
easy-venv -p /path/to/project -s
```

---

## What Easy-Venv Does

1. **🎯 Validates** the target directory exists and is accessible
2. **🌱 Creates** a virtual environment (skips if already exists)
3. **🔧 Upgrades** pip to the latest version
4. **📦 Detects** dependency files (`pyproject.toml`, `requirements.txt`, `Pipfile`, etc.)
5. **⬇️ Installs** dependencies from detected files (if present and not empty)
6. **📝 Optionally creates** requirements file template (with `-r` flag)
7. **🚀 Launches** a new shell session with the environment activated and correct directory!

---

## Dependency File Detection

Easy-Venv automatically detects and installs from these dependency files in order of preference:

1. **`pyproject.toml`** - Modern Python packaging standard
2. **`requirements.txt`** - Traditional pip requirements
3. **`Pipfile`** - Pipenv format
4. **Other formats** - Additional formats as supported

You can override auto-detection by specifying a file with the `-r` flag.

---

## Example Session

```bash
$ easy-venv -p ~/my-awesome-project

🎯 Target directory: /home/user/my-awesome-project
🌱 Creating virtual environment in '/home/user/my-awesome-project/.venv'...
🔧 Upgrading pip...
📦 Found pyproject.toml - installing dependencies...
📦 Installing dependencies from pyproject.toml...

🎉 Setup complete!
🚀 Automatically launching activated shell session...
🎉 Virtual environment activated in new shell!
📁 Current directory: /home/user/my-awesome-project
🐍 Virtual environment: /home/user/my-awesome-project/.venv
✨ You can now work in your activated environment. Type 'exit' to return.

(.venv) user@computer:~/my-awesome-project$ pip install requests
(.venv) user@computer:~/my-awesome-project$ python my_script.py
# You're ready to code! 🎉
```

---

## Requirements Template Generation

When you need a requirements file template, use the `-r` flag:

```bash
# Create default requirements.txt
easy-venv -p my-project -r

# Create custom requirements file
easy-venv -p my-project -r dev-requirements.txt
```

This creates a template like:

```txt
# TODO: Add your project dependencies here
# This file was auto-created by Easy-Venv
# Example: requests>=2.28.0

```

Clean, simple, and ready for you to add your dependencies!

---

## Error Handling & Safety

Easy-Venv handles edge cases gracefully:

-   **Missing target directory**: Clear error message with path validation
-   **No dependency files found**: Informative message, skips installation
-   **Empty dependency files**: Informative message, skips installation
-   **Existing virtual environment**: Skips creation, proceeds with upgrades and installation
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

-   **One command setup**: Just run `easy-venv` in any project directory
-   **Remote management**: Keep Easy-Venv installed globally, work on projects anywhere
-   **Multiple environments**: Use descriptive names (`-n dev`, `-n testing`, `-n prod`)

### 📁 **Organization Tips**

-   **Modern dependency files**: Use `pyproject.toml` for new projects
-   **Separate requirements**: `-r requirements-dev.txt`, `-r requirements-prod.txt`, etc.
-   **Consistent naming**: Use the same venv names across similar projects

### 🚀 **Power User Tips**

-   **Automation friendly**: Use `-s` flag in scripts and CI/CD
-   **Quick setup**: `easy-venv && code .` for instant VSCode setup
-   **Batch processing**: Set up multiple projects with shell loops

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
| **Direct Run**     | `python easy_venv/main.py`   | One-time use         |

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
pip install -e .[dev]  # Installs development dependencies
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

### v1.1.0

-   📦 **Multi-format dependency detection**: Auto-detects `pyproject.toml`, `requirements.txt`, `Pipfile`, and more
-   📝 **Optional template generation**: Requirements.txt template now requires `--create-requirements` flag
-   🔍 **Smart dependency handling**: No longer auto-creates files by default
-   🚀 **Improved workflow**: Focus on existing projects with better file detection

### v1.0.0

-   ✨ **Auto-shell activation**: Automatically launches activated shell
-   📝 **Smart requirements**: Auto-creates requirements.txt with helpful template
-   🚀 **Short flags**: All options have convenient short versions (`-p`, `-n`, `-r`, `-s`)
-   🖥️ **Better cross-platform**: Improved Windows PowerShell and Unix shell support
-   📦 **Installable package**: Available via `pip install -e .` with `pyproject.toml`

---

_Made with ❤️ to make Python development setup effortless_

**Ready to code in seconds, not minutes! 🚀**
