# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

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
