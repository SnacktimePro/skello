"""File management utilities for easy-venv."""

import sys
from pathlib import Path
from typing import Dict, Optional


class FileManager:
    """Handles file operations and validation for virtual environment setup."""
    
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
    
    def create_requirements_file(self, filename: str = "requirements.txt") -> bool:
        """
        Creates a basic requirements file with placeholder content.
        
        Args:
            filename: Name of the requirements file to create
            
        Returns:
            True if file was created successfully, False otherwise
        """
        req_file = self.target_dir / filename
        
        if req_file.exists():
            print(f"✅ {filename} already exists - skipping creation")
            return False
        
        content = [
            "# TODO: Add your project dependencies here",
            f"# This file was auto-created by Easy-Venv because it was missing",
            "# Example: requests>=2.28.0",
            ""
        ]
        
        self._write_file(req_file, content, filename)
        
    def _write_file(self, file_path: Path, content: str, filename: str) -> bool:
        """Helper method to write content to a file with error handling."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created {filename}")
            return True
        except Exception as e:
            print(f"❌ Error creating {filename}: {e}")
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