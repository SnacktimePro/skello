"""File management utilities for easy-venv with project scaffolding features."""

import sys
from pathlib import Path
from typing import Dict, Optional, List


class FileManager:
    """Handles file operations and validation for virtual environment setup and project scaffolding."""
    
    def __init__(self, target_dir: Path):
        """
        Initialize FileManager with target directory.
        
        Args:
            target_dir: Directory where virtual environment and files will be managed
        """
        self.target_dir = target_dir.resolve()
        self._validate_target_directory()
    
    def _validate_target_directory(self) -> None:
        """Validates that target directory exists and is a directory."""
        if not self.target_dir.exists():
            print(f"❌ Error: Target directory '{self.target_dir}' does not exist.")
            sys.exit(1)
        
        if not self.target_dir.is_dir():
            print(f"❌ Error: '{self.target_dir}' is not a directory.")
            sys.exit(1)
    
    def create_project_files(self, file_types: List[str]) -> None:
        """
        Creates multiple project files based on the specified types.
        
        Args:
            file_types: List of file types to create. Options: 
                       'requirements', 'pyproject', 'gitignore', 'readme', 'changelog', 'license', 'all'
        """
        if 'all' in file_types:
            file_types = ['pyproject', 'gitignore', 'readme', 'changelog', 'license']
        
        # Smart dependency file creation - prefer pyproject.toml over requirements.txt
        if 'requirements' in file_types and 'pyproject' in file_types:
            print("📝 Note: Creating pyproject.toml instead of requirements.txt (modern standard)")
            file_types = [ft for ft in file_types if ft != 'requirements']
        elif 'requirements' in file_types:
            # Check if pyproject.toml already exists
            if (self.target_dir / "pyproject.toml").exists():
                print("📝 Note: pyproject.toml already exists, skipping requirements.txt creation")
                file_types = [ft for ft in file_types if ft != 'requirements']
        
        created_files = []
        skipped_files = []
        
        for file_type in file_types:
            if file_type == 'requirements':
                if self.create_requirements_file():
                    created_files.append('requirements.txt')
                else:
                    skipped_files.append('requirements.txt')
            elif file_type == 'pyproject':
                if self.create_pyproject_toml():
                    created_files.append('pyproject.toml')
                else:
                    skipped_files.append('pyproject.toml')
            elif file_type == 'gitignore':
                if self.create_gitignore():
                    created_files.append('.gitignore')
                else:
                    skipped_files.append('.gitignore')
            elif file_type == 'readme':
                if self.create_readme():
                    created_files.append('README.md')
                else:
                    skipped_files.append('README.md')
            elif file_type == 'changelog':
                if self.create_changelog():
                    created_files.append('CHANGELOG.md')
                else:
                    skipped_files.append('CHANGELOG.md')
            elif file_type == 'license':
                if self.create_license():
                    created_files.append('LICENSE')
                else:
                    skipped_files.append('LICENSE')
        
        # Summary output
        if created_files:
            print(f"📝 Created project files: {', '.join(created_files)}")
        if skipped_files:
            print(f"⏭️  Skipped existing files: {', '.join(skipped_files)}")
    
    def create_requirements_file(self, filename: str = "requirements.txt") -> bool:
        """
        Creates a basic requirements file with placeholder content.
        
        Args:
            filename: Name of the requirements file to create
            
        Returns:
            True if file was created successfully, False if already exists
        """
        req_file = self.target_dir / filename
        
        if req_file.exists():
            return False
        
        content = """# TODO: Add your project dependencies here
# This file was auto-created by Easy-Venv
# Example: requests>=2.28.0

"""
        
        return self._write_file(req_file, content)
    
    def create_pyproject_toml(self) -> bool:
        """
        Creates a basic pyproject.toml file with modern Python packaging structure.
        
        Returns:
            True if file was created successfully, False if already exists
        """
        toml_file = self.target_dir / "pyproject.toml"
        
        if toml_file.exists():
            return False
        
        project_name = self.target_dir.name
        content = f"""[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{project_name}"
version = "0.1.0"
description = "TODO: Add project description"
readme = "README.md"
authors = [
    {{name = "TODO: Add your name", email = "your.email@example.com"}},
]

license = {{file = "LICENSE"}}
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
requires-python = ">=3.8"
dependencies = [
    # TODO: Add your project dependencies here
    # "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=22.0",
    "isort>=5.0",
    "flake8>=4.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/{project_name}"
Repository = "https://github.com/yourusername/{project_name}"
Issues = "https://github.com/yourusername/{project_name}/issues"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]

[tool.hatch.build.targets.wheel]
# This tells Hatch to look for the package code inside a 'src' directory.
# This satisfies the build tool's check, even if the directory doesn't exist yet.
packages = ["src/{project_name}"]
"""
        
        return self._write_file(toml_file, content)
    
    def create_gitignore(self) -> bool:
        """
        Creates a comprehensive .gitignore file for Python projects.
        
        Returns:
            True if file was created successfully, False if already exists
        """
        gitignore_file = self.target_dir / ".gitignore"
        
        if gitignore_file.exists():
            return False
        
        content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
"""
        
        return self._write_file(gitignore_file, content)
    
    def create_readme(self) -> bool:
        """
        Creates a basic README.md file with project template.
        
        Returns:
            True if file was created successfully, False if already exists
        """
        readme_file = self.target_dir / "README.md"
        
        if readme_file.exists():
            return False
        
        project_name = self.target_dir.name
        content = f"""# {project_name.replace('-', ' ').replace('_', ' ').title()}

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**TODO: Add a brief description of your project**

## Installation

### Using pip

```bash
pip install {project_name}
```

### Development Installation

```bash
git clone https://github.com/yourusername/{project_name}.git
cd {project_name}
pip install -e .[dev]
```

## Usage

```python
# TODO: Add usage examples
import {project_name.replace('-', '_')}

# Example usage here
```

## Features

- TODO: List your project features
- Feature 2
- Feature 3

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
"""
        
        return self._write_file(readme_file, content)
    
    def create_license(self) -> bool:
        """
        Creates an MIT License file with current year and placeholder for name.
        
        Returns:
            True if file was created successfully, False if already exists
        """
        license_file = self.target_dir / "LICENSE"
        
        if license_file.exists():
            return False
        
        from datetime import datetime
        current_year = datetime.now().year
        
        content = f"""MIT License

Copyright (c) {current_year} [Your Name Here]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        
        return self._write_file(license_file, content)
    
    def create_changelog(self) -> bool:
        """
        Creates a basic CHANGELOG.md file following Keep a Changelog format.
        
        Returns:
            True if file was created successfully, False if already exists
        """
        changelog_file = self.target_dir / "CHANGELOG.md"
        
        if changelog_file.exists():
            return False
        
        content = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
- TODO: Add new features here

### Changed
- TODO: Add changes here

### Deprecated
- TODO: Add deprecations here

### Removed
- TODO: Add removals here

### Fixed
- TODO: Add bug fixes here

### Security
- TODO: Add security improvements here

## [0.1.0] - $(date +%Y-%m-%d)

### Added
- Initial release
- Basic project structure
"""
        
        return self._write_file(changelog_file, content)
    
    def _write_file(self, file_path: Path, content: str) -> bool:
        """Helper method to write content to a file with error handling."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"❌ Error creating {file_path.name}: {e}")
            return False
    
    def find_dependency_files(self) -> Dict[str, Optional[Path]]:
        """
        Searches for common dependency files in the target directory.
        
        Returns:
            Dictionary mapping file types to their paths (or None if not found)
        """
        dependency_files = {
            'pyproject.toml': self.target_dir / "pyproject.toml",
            'requirements.txt': self.target_dir / "requirements.txt", 
            'Pipfile': self.target_dir / "Pipfile",
            'environment.yml': self.target_dir / "environment.yml"
        }
        
        # Return only existing files, others as None
        return {
            name: path if path.exists() else None 
            for name, path in dependency_files.items()
        }
    
    def get_file_size(self, file_path: Path) -> int:
        """
        Gets the size of a file in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes, or 0 if file doesn't exist
        """
        try:
            return file_path.stat().st_size if file_path.exists() else 0
        except OSError:
            return 0
    
    def is_file_empty(self, file_path: Path) -> bool:
        """
        Checks if a file is empty (0 bytes).
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file is empty or doesn't exist, False otherwise
        """
        return self.get_file_size(file_path) == 0