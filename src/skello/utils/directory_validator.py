import os
from pathlib import Path
from typing import List


class DirectoryValidationError(Exception):
    """Raised when directory validation fails."""
    pass


class DirectoryValidator:
    def __init__(self, target_dir: Path):
        self.target_dir = target_dir
        self.validation_errors: List[str] = []

    def validate_target_directory(self) -> bool:
        """
        Validates the target directory for project setup.
        
        Returns:
            bool: True if directory is valid, False otherwise
            
        Side effects:
            Populates self.validation_errors with any issues found
        """
        self.validation_errors.clear()
        
        try:
            # Check if directory exists
            if self.target_dir.exists():
                return self._validate_existing_directory()
            
        except (OSError, PermissionError) as e:
            self.validation_errors.append(f"System error accessing directory: {e}")
            return False
        
    
    def _validate_existing_directory(self) -> bool:
        """Validate an existing directory."""
        is_valid = True
        
        # Check if it's actually a directory
        if not self.target_dir.is_dir():
            self.validation_errors.append(f"Path exists but is not a directory: {self.target_dir}")
            return False
        
        # Check read permissions
        if not os.access(self.target_dir, os.R_OK):
            self.validation_errors.append(f"No read permission for directory: {self.target_dir}")
            is_valid = False
        
        # Check write permissions
        if not os.access(self.target_dir, os.W_OK):
            self.validation_errors.append(f"No write permission for directory: {self.target_dir}")
            is_valid = False
        
        # Check execute permissions (needed to traverse directory)
        if not os.access(self.target_dir, os.X_OK):
            self.validation_errors.append(f"No execute permission for directory: {self.target_dir}")
            is_valid = False
        
        # Check available disk space (at least 100MB recommended)
        if not self._check_disk_space():
            is_valid = False
        
        return is_valid

    def _validate_parent_directory(self) -> bool:
        """Validate parent directory when creating new directory."""
        parent_dir = self.target_dir.parent
        
        # Check if parent exists
        if not parent_dir.exists():
            self.validation_errors.append(f"Parent directory does not exist: {parent_dir}")
            return False
        
        # Check parent permissions
        if not os.access(parent_dir, os.W_OK):
            self.validation_errors.append(f"No write permission in parent directory: {parent_dir}")
            return False
        
        # Check if target name would conflict
        if self.target_dir.exists():
            self.validation_errors.append(f"Target already exists: {self.target_dir}")
            return False
        
        # Check available disk space
        if not self._check_disk_space(check_parent=True):
            return False
        
        return True
    
    def _check_disk_space(self, min_space_mb: int = 100, check_parent: bool = False) -> bool:
        """Check if there's sufficient disk space."""
        try:
            check_path = self.target_dir.parent if check_parent else self.target_dir
            stat_result = os.statvfs(check_path)
            
            # Calculate free space in MB
            free_space_bytes = stat_result.f_bavail * stat_result.f_frsize
            free_space_mb = free_space_bytes / (1024 * 1024)
            
            if free_space_mb < min_space_mb:
                self.validation_errors.append(
                    f"Insufficient disk space: {free_space_mb:.1f}MB available, "
                    f"{min_space_mb}MB required"
                )
                return False
            
            return True
            
        except (OSError, AttributeError):
            # os.statvfs not available on Windows, or other OS error
            # Skip disk space check rather than failing
            return True

    def get_validation_summary(self) -> str:
        """Get a formatted summary of validation results."""
        if not self.validation_errors:
            return "✅ Directory validation passed"
        
        summary = "❌ Directory validation failed:\n"
        for i, error in enumerate(self.validation_errors, 1):
            summary += f"   {i}. {error}\n"
        
        return summary.rstrip()