# Easy-Venv

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**A simple, cross-platform script to quickly create a Python virtual environment, upgrade pip, and install dependencies from a requirements file - from anywhere on your system.**

---

## Why Easy-Venv?

Setting up a Python project often involves the same repetitive steps:
1. Create a virtual environment (`python -m venv .venv`).
2. Activate it.
3. Upgrade pip (`pip install --upgrade pip`).
4. Install dependencies (`pip install -r requirements.txt`).

**Easy-Venv** automates these steps into a single, hassle-free command, ensuring a consistent setup experience on Windows, macOS, and Linux. Now with the ability to work on any project directory from anywhere on your system!

---

## Features

- ✅ **One-Command Setup**: Creates a venv, upgrades pip, and installs dependencies.
- 🖥️ **Cross-Platform**: Works reliably on Windows, macOS, and Linux.
- 📁 **Remote Project Setup**: Work on any project directory from anywhere on your system.
- 🛠️ **Customizable**: Easily specify custom venv names, requirements files, and target directories.
- 🧘 **Safe**: Checks for existing environments and validates directories to avoid conflicts.
- 📖 **Beginner-Friendly**: Simple CLI with clear, helpful output and progress indicators.

---

## Installation

### Option 1: Standalone Script (Recommended)
No installation needed! Just clone the repository or download the `setup_venv.py` file.

```bash
git clone https://github.com/your-username/easy-venv.git
cd easy-venv
```

### Option 2: System-wide Installation
Install it globally to use from anywhere:

```bash
git clone https://github.com/your-username/easy-venv.git
cd easy-venv
pip install -e .
```

After installation, you can use `easy-venv` command from anywhere.

---

## Usage

### Basic Usage (Current Directory)
Run in your project's root directory to create `.venv` and install from `requirements.txt`:

```bash
python setup_venv.py
```

### Working with Different Project Directories
Point Easy-Venv to any project directory on your system:

```bash
# Setup a project in a different directory
python setup_venv.py -p /path/to/my/project

# Example: Setup a project on your Desktop (Windows)
python setup_venv.py -p "C:\Users\YourName\Desktop\my-python-project"

# Example: Setup a project in your home directory (macOS/Linux)
python setup_venv.py -p ~/projects/my-awesome-app
```

### Advanced Usage
Combine all options for full customization:

```bash
# Custom everything
python setup_venv.py -p /path/to/project -n myenv -r dev-requirements.txt
```

### If Installed System-wide
```bash
# From anywhere on your system
easy-venv -p /path/to/your/project
easy-venv -p ~/projects/web-app -n production -r prod-requirements.txt
```

---

## Command-Line Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--path` | `-p` | `.` (current directory) | Target directory containing your project |
| `--name` | `-n` | `.venv` | Name of the virtual environment folder |
| `--requirements` | `-r` | `requirements.txt` | Name of the requirements file to install from |
| `--help` | `-h` | - | Show help message and exit |

---

## Examples

### Real-World Scenarios

**Scenario 1: Quick local setup**
```bash
cd my-project
python /path/to/setup_venv.py
```

**Scenario 2: Setup multiple projects from a central location**
```bash
# Keep easy-venv in ~/tools/ and use it for different projects
python ~/tools/easy-venv/setup_venv.py -p ~/projects/web-app
python ~/tools/easy-venv/setup_venv.py -p ~/projects/data-analysis -r requirements-dev.txt
python ~/tools/easy-venv/setup_venv.py -p ~/projects/ml-model -n ml-env
```

**Scenario 3: Different environments for the same project**
```bash
# Development environment
python setup_venv.py -p ~/my-project -n dev-env -r requirements-dev.txt

# Production environment  
python setup_venv.py -p ~/my-project -n prod-env -r requirements-prod.txt
```

---

## What Easy-Venv Does

1. **🎯 Validates** the target directory exists and is accessible
2. **🌱 Creates** a virtual environment (skips if already exists)
3. **🔧 Upgrades** pip to the latest version
4. **📦 Installs** dependencies from requirements file (if present)
5. **📋 Provides** activation instructions for your platform

---

## Output Example

```
🎯 Target directory: /home/user/projects/my-app
🌱 Creating virtual environment in '/home/user/projects/my-app/.venv'...
🔧 Upgrading pip...
📦 Installing dependencies from '/home/user/projects/my-app/requirements.txt'...

🎉 Setup complete!
   To activate, run: source /home/user/projects/my-app/.venv/bin/activate
   Virtual environment location: /home/user/projects/my-app/.venv
   Project directory: /home/user/projects/my-app
```

---

## Error Handling

Easy-Venv handles common issues gracefully:

- **Missing target directory**: Clear error message with path validation
- **Missing requirements file**: Warning message, continues with venv creation
- **Empty requirements file**: Informative message, skips installation
- **Existing virtual environment**: Skips creation, proceeds with pip upgrade and installation
- **Permission issues**: Clear error messages with suggested solutions

---

## Platform-Specific Notes

### Windows
- Supports both Command Prompt and PowerShell
- Handles Windows path formatting automatically
- Provides PowerShell activation instructions

### macOS/Linux
- Full bash/zsh compatibility
- Handles symbolic links and permissions properly
- Provides source activation instructions

---

## Tips & Best Practices

- **Keep Easy-Venv centralized**: Place it in a tools directory and use the `-p` option
- **Use descriptive venv names**: For projects with multiple environments, use names like `dev-env`, `test-env`
- **Organize requirements files**: Use different requirements files for different purposes (`requirements-dev.txt`, `requirements-prod.txt`)
- **Check the output**: Easy-Venv provides detailed feedback about what it's doing

---

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Support

If you encounter any issues or have questions:
1. Check the examples above for common usage patterns
2. Run with `-h` flag to see all available options
3. Open an issue on GitHub with details about your setup and the error

---

*Made with ❤️ to simplify Python development workflow*
