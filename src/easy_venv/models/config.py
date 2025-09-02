from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional


class FileType(Enum):
    """File types that can be created."""
    LICENSE = "license"
    REQUIREMENTS = "requirements"
    PYPROJECT = "pyproject"
    GITIGNORE = "gitignore"
    README = "readme"
    CHANGELOG = "changelog"


class StructureTemplate(Enum):
    """Project structure templates."""
    MAIN = "main"        # Creates src/package/main.py structure
    FULL = "full"        # Creates complete project structure
    ALL = "all"          # Creates all files + full structure


@dataclass
class FileSpec:
    """A parsed file creation request - merged specification and config."""
    file_type: FileType
    options: Dict[str, str] = field(default_factory=dict)
    
    # Config data embedded directly
    _CONFIGS = {
        FileType.LICENSE: {
            "aliases": ["l", "lic"],
            "option_keys": ["type", "author", "filename"]
        },
        FileType.REQUIREMENTS: {
            "aliases": ["r", "req"], 
            "option_keys": ["filename"]
        },
        FileType.PYPROJECT: {
            "aliases": ["p", "toml"],
            "option_keys": []
        },
        FileType.GITIGNORE: {
            "aliases": ["g", "git"],
            "option_keys": []
        },
        FileType.README: {
            "aliases": ["md", "read"],
            "option_keys": []
        },
        FileType.CHANGELOG: {
            "aliases": ["ch", "log"],
            "option_keys": []
        },
    }
    
    _STRUCTURE_ALIASES = {
        "m": StructureTemplate.MAIN, "main": StructureTemplate.MAIN,
        "f": StructureTemplate.FULL, "full": StructureTemplate.FULL,
        "*": StructureTemplate.ALL, "all": StructureTemplate.ALL,
    }
    
    @classmethod
    def parse(cls, arg_str: str) -> tuple[Optional['FileSpec'], Optional[StructureTemplate]]:
        """Parse into FileSpec or StructureTemplate."""
        parts = arg_str.split(':', 1)
        alias = parts[0]
        option_string = parts[1] if len(parts) > 1 else None
        
        # Check structure templates first
        if alias in cls._STRUCTURE_ALIASES:
            return None, cls._STRUCTURE_ALIASES[alias]
        
        # Check file types
        for file_type, config in cls._CONFIGS.items():
            if alias in config["aliases"]:
                options = {}
                if option_string and config["option_keys"]:
                    option_values = option_string.split(':')
                    options = {
                        key: value for key, value in 
                        zip(config["option_keys"], option_values) if value
                    }
                return cls(file_type=file_type, options=options), None
        
        return None, None
    
    def get(self, key: str, default: str = None) -> str:
        """Get option value."""
        return self.options.get(key, default)