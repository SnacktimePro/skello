"""Easy-Venv: Simplified Python virtual environment management."""

from .dependency_handler import DependencyHandler
from .file_manager import FileManager
from .shell_launcher import ShellLauncher
from .utils import CommandRunner
from .venv_manager import VirtualEnvironmentManager

__version__ = "1.0.0"
__all__ = [
    "VirtualEnvironmentManager",
    "DependencyHandler",
    "FileManager", 
    "ShellLauncher",
    "CommandRunner"
]