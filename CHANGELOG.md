# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2025-09-01

### Added

-   **Template-based file generation system** - Complete rewrite of file creation using external template files
    -   All project files now generated from `.tmpl` files in `src/easy_venv/templates/`
    -   Clean separation of content from logic
    -   Easily maintainable and customizable templates
-   **Smart pyproject.toml generation** - Context-aware pyproject.toml creation
    -   Detects existing project structure (src/, tests/, README, LICENSE)
    -   Only includes sections for files that exist or will be created
    -   Prevents build errors from missing files
    -   Auto-detects license types from existing LICENSE files
-   **Project structure scaffolding** - New commands for modern Python project layout
    -   `create_main_structure()` - Creates `src/project_name/main.py` with proper package structure
    -   `create_project_structure()` - Full project scaffold with src/ layout and tests/
    -   Includes `__init__.py`, `main.py` with CLI entry points, and basic test files
-   **Enhanced license detection** - Smart license type identification
    -   Supports MIT, Apache, BSD, GPL, LGPL, MPL, and Unlicense
    -   Automatic detection from existing LICENSE file content
    -   Proper classifier mapping for pyproject.toml
    -   Defaults to MIT License for new projects
-   **Improved file creation logic** - Context-aware file generation
    -   Files are created based on what will be generated in the same session
    -   Prevents inconsistencies between pyproject.toml and actual project structure
    -   Better error handling and validation

### Changed

-   **File generation architecture** - Moved from inline string templates to external template files
-   **pyproject.toml generation** - Now adapts to actual project structure instead of using static template
-   **Template variable system** - Uses `string.Template` with `$variable` syntax for clean substitution

### Technical

-   Added `importlib.resources` support for template file access
-   Enhanced `FileManager` class with template handling capabilities
-   Improved project name sanitization for Python package names
-   Better separation of concerns between file detection and template generation

## [2.0.0] - 2025-08-31

### Added

-   🏗️ **Complete project scaffolding** with `--create` flag (`pyproject.toml`, `.gitignore`, `README.md`, `CHANGELOG.md`, `LICENSE`)
-   🔧 **Modern Python standards**: Prefer `pyproject.toml` over `requirements.txt`
-   🧠 **Smart file logic**: Never overwrites, conflict prevention, intelligent defaults
-   📝 **Professional templates** with current best practices
-   🎯 **Flexible options** with validation + aliases
-   ⚡ **Zero to production**: Setup in one command
-   🛡️ **Enhanced safety**: Comprehensive validation & error handling

---

## [1.1.0] - 2025-06-15

### Added

-   📦 Multi-format dependency detection (`pyproject.toml`, `requirements.txt`, `Pipfile`, etc.)

### Changed

-   📝 `requirements.txt` template now requires a flag
-   🔍 Smarter dependency handling (no auto-create by default)
-   🚀 Improved workflow: better file detection for existing projects

---

## [1.0.0] - 2025-04-10

### Added

-   ✨ Auto-shell activation
-   📝 Smart `requirements.txt` auto-template
-   🚀 Short flags for all options
-   🖥️ Cross-platform improvements (Windows + Unix shells)
-   📦 Installable package via `pip install -e .`
