from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

from .config import FileSpec, FileType, StructureTemplate
from ..directory_snapshot import DirectorySnapshot

@dataclass(frozen=True)
class ScaffoldContext:
    """Immutable scaffolding plan after parsing and conflict resolution."""
    target_dir: Path
    project_name: str
    project_package: str
    
    # What to create
    files_to_create: Dict[FileType, FileSpec]
    structures_to_create: Set[StructureTemplate]
    
    # Current state
    directory_snapshot: DirectorySnapshot
    
    @classmethod
    def build(cls, target_dir: Path, create_args: List[str] = None) -> 'ScaffoldContext':
        """Build complete scaffolding context with conflict resolution."""
        # 1. Scan directory first
        snapshot = DirectorySnapshot.scan(target_dir)
        
        # 2. Parse project info
        name = target_dir.name if target_dir.name != "." else target_dir.resolve().name
        package = name.replace("-", "_").replace(" ", "_").lower()
        
        # 3. Parse CLI arguments
        requested_files = {}
        requested_structures = set()
        
        if create_args:
            for arg in create_args:
                file_spec, structure = FileSpec.parse(arg)
                
                if structure == StructureTemplate.ALL:
                    # ALL = full structure + all files
                    requested_structures.add(StructureTemplate.FULL)
                    cls._add_all_file_types(requested_files)
                elif structure:
                    requested_structures.add(structure)
                elif file_spec:
                    requested_files[file_spec.file_type] = file_spec
                else:
                    print(f"⚠️ Unknown: {arg}")
        
        # 4. Apply prioritization rules
        final_files = cls._apply_prioritization(requested_files, snapshot)
        
        # 5. Remove files that already exist
        safe_files = {
            file_type: spec for file_type, spec in final_files.items()
            if not cls._file_would_conflict(file_type, spec, snapshot)
        }
        
        return cls(
            target_dir=target_dir,
            project_name=name,
            project_package=package,
            files_to_create=safe_files,
            structures_to_create=requested_structures,
            directory_snapshot=snapshot
        )
    
    @classmethod
    def _add_all_file_types(cls, files_dict: Dict[FileType, FileSpec]) -> None:
        """Add all file types to the dictionary."""
        for file_type in FileType:
            if file_type not in files_dict:
                files_dict[file_type] = FileSpec(file_type=file_type)
    
    @classmethod
    def _apply_prioritization(cls, files: Dict[FileType, FileSpec], snapshot: DirectorySnapshot) -> Dict[FileType, FileSpec]:
        """Apply prioritization rules (pyproject over requirements, etc)."""
        final_files = files.copy()
        
        # If pyproject.toml exists or is requested, remove requirements.txt
        has_pyproject_spec = FileType.PYPROJECT in final_files
        has_pyproject_file = snapshot.file_exists("pyproject.toml")
        
        if has_pyproject_spec or has_pyproject_file:
            if FileType.REQUIREMENTS in final_files:
                del final_files[FileType.REQUIREMENTS]
                print("📝 Note: Prioritizing pyproject.toml over requirements.txt.")
        
        return final_files
    
    @classmethod
    def _file_would_conflict(cls, file_type: FileType, spec: FileSpec, snapshot: DirectorySnapshot) -> bool:
        """Check if creating this file would conflict with existing files."""
        # Get the filename that would be created
        if file_type == FileType.LICENSE:
            filename = spec.get("filename", "LICENSE")
        elif file_type == FileType.REQUIREMENTS:
            filename = spec.get("filename", "requirements.txt")
        elif file_type == FileType.GITIGNORE:
            filename = spec.get("filename", ".gitignore")
        elif file_type == FileType.README:
            filename = spec.get("filename", "README.md")
        elif file_type == FileType.CHANGELOG:
            filename = spec.get("filename", "CHANGELOG.md")
        elif file_type == FileType.PYPROJECT:
            filename = "pyproject.toml"
        else:
            return False
        
        return snapshot.file_exists(filename)
    
    # Simple accessors
    def has_file_to_create(self, file_type: FileType) -> bool:
        """Check if file type will be created."""
        return file_type in self.files_to_create
    
    def has_structure_to_create(self, template: StructureTemplate) -> bool:
        """Check if structure template will be created."""
        return template in self.structures_to_create
    
    def get_file_spec(self, file_type: FileType) -> Optional[FileSpec]:
        """Get file spec for creation."""
        return self.files_to_create.get(file_type)
    
    def should_create_src(self) -> bool:
        """Check if src structure should be created."""
        return (StructureTemplate.MAIN in self.structures_to_create or 
                StructureTemplate.FULL in self.structures_to_create)
    
    def should_create_tests(self) -> bool:
        """Check if tests structure should be created."""
        return StructureTemplate.FULL in self.structures_to_create
    
    # Convenience getters for file options
    def license_type(self) -> str:
        """Get license type with fallback."""
        spec = self.get_file_spec(FileType.LICENSE)
        return spec.get("type", "mit") if spec else None
    
    def license_author(self) -> str:
        """Get license author with fallback."""
        spec = self.get_file_spec(FileType.LICENSE)
        return spec.get("author", "TODO: Add your name") if spec else "TODO: Add your name"
    
    def requirements_filename(self) -> str:
        """Get requirements filename with fallback."""
        spec = self.get_file_spec(FileType.REQUIREMENTS)
        return spec.get("filename", "requirements.txt") if spec else "requirements.txt"
    
    def project_summary(self) -> str:
        """Get a project summary of the context configuration."""
        lines = [
            f"   Project: {self.project_name} (package: {self.project_package})",
            f"   Target: {self.target_dir}",
            f"   Structure Templates: {[t.value for t in self.structures_to_create]}",
            f"   File Specifications: {[(key.value, spec.options) for key, spec in self.files_to_create.items()]}"
            "\n"
        ]
        return "\n".join(lines)