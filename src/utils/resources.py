"""Resource path utilities."""

import os
import sys
from pathlib import Path
from typing import Optional


def get_resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and PyInstaller bundle.

    Args:
        relative_path: Relative path to resource

    Returns:
        Absolute path to resource
    """
    if hasattr(sys, "_MEIPASS"):
        # Running as PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)

    # Running as script - look relative to this file
    current_dir = Path(__file__).parent.parent.parent
    return os.path.join(current_dir, relative_path)


def get_app_data_directory() -> str:
    """
    Get application data directory for storing settings.

    Returns:
        Path to application data directory
    """
    if sys.platform == "darwin":  # macOS
        app_data = os.path.expanduser("~/Library/Application Support/Entryptor")
    elif sys.platform == "win32":  # Windows
        app_data = os.path.expanduser("~/AppData/Roaming/Entryptor")
    else:  # Linux and others
        app_data = os.path.expanduser("~/.config/entryptor")

    # Create directory if it doesn't exist
    os.makedirs(app_data, exist_ok=True)
    return app_data


def get_settings_file_path() -> str:
    """
    Get path to settings file.

    Returns:
        Path to settings file
    """
    return os.path.join(get_app_data_directory(), "settings.json")


def get_icon_path(icon_name: str) -> Optional[str]:
    """
    Get path to application icon.

    Args:
        icon_name: Name of icon file

    Returns:
        Path to icon file or None if not found
    """
    # Look for icon in resources
    icon_path = get_resource_path(f"resources/icons/{icon_name}")
    if os.path.exists(icon_path):
        return icon_path

    # Look in examples directory for backwards compatibility
    examples_path = get_resource_path(f"examples/Entryptor/{icon_name}")
    if os.path.exists(examples_path):
        return examples_path

    return None


def get_help_file_path() -> Optional[str]:
    """
    Get path to help file.

    Returns:
        Path to help file or None if not found
    """
    # Look for help file in root directory first (new HELP.md)
    root_help_path = get_resource_path("HELP.md")
    if os.path.exists(root_help_path):
        return root_help_path

    # Look for help file in resources
    help_path = get_resource_path("resources/HELP.md")
    if os.path.exists(help_path):
        return help_path

    # Look in examples directory for backwards compatibility (avoid this)
    examples_help_path = get_resource_path("examples/Entryptor/HELP.md")
    if os.path.exists(examples_help_path):
        return examples_help_path

    return None


def resource_exists(relative_path: str) -> bool:
    """
    Check if resource exists.

    Args:
        relative_path: Relative path to resource

    Returns:
        True if resource exists, False otherwise
    """
    return os.path.exists(get_resource_path(relative_path))
