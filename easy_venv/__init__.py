"""
Easy-Venv: A simple, cross-platform script to quickly create Python virtual environments.

A tool to automate the creation of Python virtual environments, pip upgrades,
dependency installation, and automatic activation - all in one command.
"""

__version__ = "1.0.0"
__author__ = "SnacktimePro"
__email__ = "No-reply@example.com"
__description__ = "A simple, cross-platform script to quickly create Python virtual environments with automatic activation"

from .main import main

__all__ = ["main"]