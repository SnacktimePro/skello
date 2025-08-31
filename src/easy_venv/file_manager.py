"""File management utilities for easy-venv with project scaffolding features."""

import string
import sys
import textwrap
from pathlib import Path
from typing import Dict, Optional, List
from importlib import resources


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
        self.templates_dir = resources.files('easy_venv').joinpath('templates')
    
    def _validate_target_directory(self) -> None:
        """Validates that target directory exists and is a directory."""
        if not self.target_dir.exists():
            print(f"❌ Error: Target directory '{self.target_dir}' does not exist.")
            sys.exit(1)
        
        if not self.target_dir.is_dir():
            print(f"❌ Error: '{self.target_dir}' is not a directory.")
            sys.exit(1)

    def _get_template_content(self, filename: str, **kwargs) -> str:
        """
        Reads a template file, substitutes variables, and returns the content.
        """
        template_path = self.templates_dir / filename
        template_content = template_path.read_text(encoding='utf-8')
        template = string.Template(template_content)
        return template.safe_substitute(**kwargs)
    
    def create_project_files(self, file_types: List[str]) -> None:
        """
        Creates multiple project files based on the specified types.
        
        Args:
            file_types: List of file types to create. Options: 
                    'requirements', 'pyproject', 'gitignore', 'readme', 'changelog', 'license', 'structure', 'all'
        """
        if 'all' in file_types:
            file_types = ['pyproject', 'gitignore', 'readme', 'changelog', 'license', 'structure']
        
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
        
        # Build context for what will be created (for pyproject.toml)
        will_create = {
            'readme': 'readme' in file_types,
            'license': 'license' in file_types, 
            'structure': 'structure' in file_types or 'main' in file_types,
            'tests': 'structure' in file_types
        }
        
        for file_type in file_types:
            if file_type == 'requirements':
                if self.create_requirements_file():
                    created_files.append('requirements.txt')
                else:
                    skipped_files.append('requirements.txt')
            elif file_type == 'pyproject':
                if self.create_pyproject_toml(will_create):
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
                if self.create_changelog(will_create):
                    created_files.append('CHANGELOG.md')
                else:
                    skipped_files.append('CHANGELOG.md')
            elif file_type == 'license':
                if self.create_license():
                    created_files.append('LICENSE')
                else:
                    skipped_files.append('LICENSE')
            elif file_type == 'main':
                if self.create_main_structure():
                    created_files.append('src/main.py structure')
                else:
                    skipped_files.append('src/main.py structure')
            elif file_type == 'structure':
                if self.create_project_structure():
                    created_files.append('full project structure')
                else:
                    skipped_files.append('full project structure')
        
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
        
        content = textwrap.dedent(f'''
        # TODO: Add your project dependencies here
        # This file was auto-created by Easy-Venv
        # Example: requests>=2.28.0
        ''').strip()
        
        return self._write_file(req_file, content)
    
    def create_pyproject_toml(self, will_create: dict = None) -> bool:
        """
        Creates a pyproject.toml file that's aware of what other files will be created.
        
        Args:
            will_create: Dict indicating what files will be created in this session
            
        Returns:
            True if file was created successfully, False if already exists
        """
        toml_file = self.target_dir / "pyproject.toml"
        
        if toml_file.exists():
            return False
        
        project_name = self.target_dir.name
        project_package = project_name.replace('-', '_')
        
        # Generate the actual section content
        sections = self._build_pyproject_sections(project_name, project_package, will_create or {})
        content = self._get_template_content('pyproject.toml.tmpl', **sections)

        return self._write_file(toml_file, content)
            
    def _build_pyproject_sections(self, project_name: str, project_package: str, will_create: dict) -> dict:
        """
        Builds all sections and variables for pyproject.toml 
        based on existing + will-be-created files.
        """
        # --- Context building ---
        context = {
            'project_name': project_name,
            'project_package': project_package,
            'has_readme': (self.target_dir / "README.md").exists() or will_create.get('readme', False),
            'has_license': (self.target_dir / "LICENSE").exists() or will_create.get('license', False),
            'has_src_structure': (self.target_dir / "src").exists() or will_create.get('structure', False),
            'has_tests': (self.target_dir / "tests").exists() or will_create.get('tests', False),
            'readme_file': 'README.md'
        }
        
        # Pick the README filename
        for readme_name in ['README.md', 'README.txt', 'README.rst']:
            if (self.target_dir / readme_name).exists():
                context['readme_file'] = readme_name
                break

        # --- Section generation ---
        project_name = context.get('project_name', self.target_dir.name)
        project_package = context.get('project_package', project_name.replace('-', '_'))

        sections = {
            'project_name': project_name,
            'project_package': project_package,
            'license_type': self._detect_license_type(),
        }

        # README section
        if context['has_readme']:
            sections['readme_section'] = f'readme = "{context["readme_file"]}"'
        else:
            sections['readme_section'] = '# readme = "README.md"  # Uncomment when you add a README'

        # LICENSE section
        if context['has_license']:
            sections['license_section'] = 'license = {file = "LICENSE"}'
        else:
            sections['license_section'] = '# license = {file = "LICENSE"}  # Uncomment when you add a LICENSE'

        # pytest section
        if context['has_tests']:
            sections['pytest_section'] = textwrap.dedent('''
            [tool.pytest.ini_options]
            testpaths = ["tests"]
            python_files = ["test_*.py", "*_test.py"]
            ''').strip()
        else:
            sections['pytest_section'] = textwrap.dedent('''
            # [tool.pytest.ini_options]
            # testpaths = ["tests"]
            # python_files = ["test_*.py", "*_test.py"]
            ''').strip()

        # Build section
        if context['has_src_structure']:
            sections['build_section'] = textwrap.dedent(f'''
            [tool.hatch.build.targets.wheel]
            packages = ["src/{project_package}"]
            ''').strip()
        else:
            sections['build_section'] = textwrap.dedent(f'''
            # [tool.hatch.build.targets.wheel]
            # packages = ["src/{project_package}"]  # Uncomment if using src/ layout
            ''').strip()

        return sections


    def _detect_license_type(self) -> str:
        """
        Detects license type from existing LICENSE file or returns default.
        
        Returns:
            License classifier string for pyproject.toml
        """
        # License type mappings for pyproject.toml classifiers
        license_mappings = {
            'MIT': 'MIT License',
            'APACHE': 'Apache Software License',
            'BSD': 'BSD License', 
            'GPL': 'GNU General Public License v3 (GPLv3)',
            'LGPL': 'GNU Lesser General Public License v3 (LGPLv3)',
            'MPL': 'Mozilla Public License 2.0 (MPL 2.0)',
            'UNLICENSE': 'The Unlicense (Unlicense)',
        }
        
        # Check for existing LICENSE file
        for license_name in ['LICENSE', 'LICENSE.txt', 'LICENSE.md', 'COPYING']:
            license_file = self.target_dir / license_name
            if license_file.exists():
                try:
                    license_content = license_file.read_text().upper()
                    
                    # Simple keyword detection
                    for keyword, classifier in license_mappings.items():
                        if keyword in license_content:
                            return classifier
                            
                except Exception:
                    pass  # If we can't read the file, fall back to default
        
        # Default to MIT License
        return 'MIT License'


    def _get_supported_licenses(self) -> dict:
        """
        Returns mapping of supported license types for future CLI options.
        
        This makes it easy to add license selection later:
        easy-venv -c license:apache
        """
        return {
            'mit': 'MIT License',
            'apache': 'Apache Software License', 
            'bsd': 'BSD License',
            'gpl': 'GNU General Public License v3 (GPLv3)',
            'lgpl': 'GNU Lesser General Public License v3 (LGPLv3)',
            'mpl': 'Mozilla Public License 2.0 (MPL 2.0)',
            'unlicense': 'The Unlicense (Unlicense)',
        }
            
    def create_gitignore(self) -> bool:
        """
        Creates a comprehensive .gitignore file for Python projects.
        
        Returns:
            True if file was created successfully, False if already exists
        """
        gitignore_file = self.target_dir / ".gitignore"
        
        if gitignore_file.exists():
            return False
        
        # Get content from the template
        content = self._get_template_content(
            "gitignore.tmpl", 
        )
        
        return self._write_file(gitignore_file, content)
    
    def create_readme(self) -> bool:
        """
        Creates a basic README.md file from template.
        
        Returns:
            True if file was created successfully, False if already exists
        """
        readme_file = self.target_dir / "README.md"
        
        if readme_file.exists():
            return False
        
        project_name = self.target_dir.name
        project_title = project_name.replace('-', ' ').replace('_', ' ').title()
        project_package = project_name.replace('-', '_')
        
        content = self._get_template_content(
            'README.md.tmpl',
            project_name=project_name,
            project_title=project_title,
            project_package=project_package
        )
        
        return self._write_file(readme_file, content)
            
    def create_license(self) -> bool:
        """
        Creates an MIT License file with current year and placeholder for name.

        TODO:  Use _get_supported_licenses() mapping
               easy-venv -c license:apache
        
        Returns:
            True if file was created successfully, False if already exists
        """
        license_file = self.target_dir / "LICENSE"
        
        if license_file.exists():
            return False
        
        from datetime import datetime
        current_year = datetime.now().year
        
        content = self._get_template_content(
            "LICENSE_MIT.tmpl", 
            current_year=current_year
        )
        
        return self._write_file(license_file, content)
    
    def create_changelog(self, will_create: dict = None) -> bool:
        """
        Creates a CHANGELOG.md file from template with initial project setup entry.
        
        Args:
            will_create: Dict indicating what files will be created in this session
            
        Returns:
            True if file was created successfully, False if already exists
        """
        changelog_file = self.target_dir / "CHANGELOG.md"
        
        if changelog_file.exists():
            return False
        
        from datetime import date
        
        project_name = self.target_dir.name
        will_create = will_create or {}
        
        # Build list of features being added in initial setup
        features = []
        
        if will_create.get('readme', False):
            features.append("-  Added README.md documentation")
        
        if will_create.get('license', False):
            features.append("-  Added LICENSE file")
        
        if will_create.get('structure', False):
            features.append("-  Added src/ package structure")
            features.append("-  Added main.py entry point")
        
        if will_create.get('tests', False):
            features.append("-  Added tests/ directory with basic test structure")
        
        # Check for pyproject.toml (likely being created if this is called)
        if (self.target_dir / "pyproject.toml").exists() or 'pyproject' in str(will_create):
            features.append("-  Added pyproject.toml configuration")
        
        # Check for other common files that might exist
        if (self.target_dir / ".gitignore").exists():
            features.append("-  Added .gitignore file")
        
        # Format features for template
        if features:
            changelog_features = "\n" + "\n".join(features)
        else:
            changelog_features = ""
        
        content = self._get_template_content(
            'CHANGELOG.md.tmpl',
            project_name=project_name,
            current_date=date.today().strftime("%Y-%m-%d"),
            changelog_features=changelog_features
        )
        
        return self._write_file(changelog_file, content)
    
    def create_main_structure(self) -> bool:
        """
        Creates a src/project_name/main.py structure with proper Python package layout.
        
        Creates:
        - src/ directory
        - src/project_name/ directory (based on target directory name)
        - src/project_name/__init__.py
        - src/project_name/main.py
        
        Returns:
            True if structure was created successfully, False if already exists
        """
        project_name = self.target_dir.name.lower().replace('-', '_').replace(' ', '_')
        project_title = project_name.replace('_', ' ').title()
        
        # Define paths
        package_dir = self.target_dir / "src" / project_name
        init_file = package_dir / "__init__.py"
        main_file = package_dir / "main.py"
        
        if main_file.exists():
            return False
        
        package_dir.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py from template
        if not init_file.exists():
            init_content = self._get_template_content(
                '__init__.py.tmpl',
                project_title=project_title
            )
            self._write_file(init_file, init_content)
        
        # Create main.py from template
        main_content = self._get_template_content(
            'main.py.tmpl', 
            project_name=project_name,
            project_title=project_title
        )
        return self._write_file(main_file, main_content)
      
    def create_project_structure(self) -> bool:
        """
        Creates a complete modern Python project structure.
        
        Creates:
        - src/project_name/ package structure
        - src/project_name/__init__.py
        - src/project_name/main.py
        - tests/ directory
        - tests/__init__.py
        - tests/test_main.py
        
        Returns:
            True if structure was created successfully, False if partially exists
        """
        project_name = self.target_dir.name.lower().replace('-', '_').replace(' ', '_')
        
        # Define paths
        src_dir = self.target_dir / "src"
        package_dir = src_dir / project_name
        tests_dir = self.target_dir / "tests"
        
        main_file = package_dir / "main.py"
        tests_init = tests_dir / "__init__.py"
        test_main = tests_dir / "test_main.py"
        
        created_items = []
    
        # Create src structure
        if not main_file.exists():
            if self.create_main_structure():
                created_items.append("src package structure")
        
        # Create tests directory
        tests_dir.mkdir(exist_ok=True)
        
        # Create tests/__init__.py
        if not tests_init.exists():
            tests_init_content = '"""Tests for the project."""\n'
            self._write_file(tests_init, tests_init_content)
            created_items.append("tests/__init__.py")
        
        # Create test_main.py
        if not test_main.exists():
            # Create test_main.py from template
            test_content = self._get_template_content(
                'test_main.py.tmpl', 
                project_name=project_name,
            )
            
            self._write_file(test_main, test_content)
            created_items.append("tests/test_main.py")
        
        return len(created_items) > 0
    
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