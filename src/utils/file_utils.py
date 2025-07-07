"""File operation utilities."""

import os
import shutil
from pathlib import Path
from typing import Optional, List


def safe_file_copy(source: str, destination: str) -> bool:
    """
    Safely copy a file with error handling.

    Args:
        source: Source file path
        destination: Destination file path

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy2(source, destination)
        return True
    except Exception:
        return False


def safe_file_move(source: str, destination: str) -> bool:
    """
    Safely move a file with error handling.

    Args:
        source: Source file path
        destination: Destination file path

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.move(source, destination)
        return True
    except Exception:
        return False


def safe_file_delete(file_path: str) -> bool:
    """
    Safely delete a file with error handling.

    Args:
        file_path: Path to file to delete

    Returns:
        True if successful, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
    except Exception:
        return False


def get_unique_filename(file_path: str) -> str:
    """
    Get a unique filename by adding a counter if file exists.

    Args:
        file_path: Original file path

    Returns:
        Unique file path
    """
    if not os.path.exists(file_path):
        return file_path

    path = Path(file_path)
    counter = 1

    while True:
        if path.suffix:
            new_name = f"{path.stem}_{counter}{path.suffix}"
        else:
            new_name = f"{path.name}_{counter}"

        new_path = path.parent / new_name

        if not new_path.exists():
            return str(new_path)

        counter += 1


def is_valid_file_path(file_path: str) -> bool:
    """
    Check if a file path is valid and accessible.

    Args:
        file_path: Path to check

    Returns:
        True if valid and accessible, False otherwise
    """
    try:
        # Check if path exists and is a file
        if not os.path.exists(file_path):
            return False

        if not os.path.isfile(file_path):
            return False

        # Check if readable
        if not os.access(file_path, os.R_OK):
            return False

        return True
    except Exception:
        return False


def get_file_size(file_path: str) -> Optional[int]:
    """
    Get file size in bytes.

    Args:
        file_path: Path to file

    Returns:
        File size in bytes or None if error
    """
    try:
        return os.path.getsize(file_path)
    except Exception:
        return None


def get_file_extension(file_path: str) -> str:
    """
    Get file extension from path.

    Args:
        file_path: Path to file

    Returns:
        File extension (including dot) or empty string
    """
    return os.path.splitext(file_path)[1]


def get_file_basename(file_path: str) -> str:
    """
    Get file basename without extension.

    Args:
        file_path: Path to file

    Returns:
        File basename without extension
    """
    return os.path.splitext(os.path.basename(file_path))[0]


def list_files_in_directory(
    directory: str, extensions: Optional[List[str]] = None
) -> List[str]:
    """
    List files in directory with optional extension filtering.

    Args:
        directory: Directory path
        extensions: List of extensions to filter by (e.g., ['.txt', '.enc'])

    Returns:
        List of file paths
    """
    try:
        files = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                if extensions is None or get_file_extension(item_path) in extensions:
                    files.append(item_path)
        return sorted(files)
    except Exception:
        return []


def ensure_directory_exists(directory: str) -> bool:
    """
    Ensure directory exists, creating it if necessary.

    Args:
        directory: Directory path

    Returns:
        True if directory exists or was created, False otherwise
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception:
        return False
