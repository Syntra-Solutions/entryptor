"""Tests for resource utilities."""

from unittest.mock import patch

from src.utils.resources import (
    get_resource_path, get_app_data_directory, get_settings_file_path,
    get_icon_path, get_help_file_path, resource_exists
)


class TestResourceUtils:
    """Test resource utility functions."""
    
    def test_get_resource_path_basic(self):
        """Test basic resource path functionality."""
        path = get_resource_path("test_file.txt")
        assert isinstance(path, str)
        assert "test_file.txt" in path
    
    def test_get_app_data_directory_macos(self):
        """Test getting app data directory on macOS."""
        with patch("sys.platform", "darwin"):
            with patch("os.path.expanduser") as mock_expand:
                mock_expand.return_value = "/Users/test/Library/Application Support/Entryptor"
                with patch("os.makedirs") as mock_makedirs:
                    result = get_app_data_directory()
                    assert result == "/Users/test/Library/Application Support/Entryptor"
                    mock_makedirs.assert_called_once()
    
    def test_get_app_data_directory_windows(self):
        """Test getting app data directory on Windows."""
        with patch("sys.platform", "win32"):
            with patch("os.path.expanduser") as mock_expand:
                mock_expand.return_value = "C:\\Users\\test\\AppData\\Roaming\\Entryptor"
                with patch("os.makedirs") as mock_makedirs:
                    result = get_app_data_directory()
                    assert result == "C:\\Users\\test\\AppData\\Roaming\\Entryptor"
                    mock_makedirs.assert_called_once()
    
    def test_get_app_data_directory_linux(self):
        """Test getting app data directory on Linux."""
        with patch("sys.platform", "linux"):
            with patch("os.path.expanduser") as mock_expand:
                mock_expand.return_value = "/home/test/.config/entryptor"
                with patch("os.makedirs") as mock_makedirs:
                    result = get_app_data_directory()
                    assert result == "/home/test/.config/entryptor"
                    mock_makedirs.assert_called_once()
    
    def test_get_settings_file_path(self):
        """Test getting settings file path."""
        with patch("src.utils.resources.get_app_data_directory") as mock_get_app_data:
            mock_get_app_data.return_value = "/test/app/data"
            result = get_settings_file_path()
            assert result == "/test/app/data/settings.json"
    
    def test_get_icon_path_found(self):
        """Test getting icon path when icon exists."""
        with patch("src.utils.resources.get_resource_path") as mock_get_resource:
            mock_get_resource.return_value = "/test/path/icon.png"
            with patch("os.path.exists", return_value=True):
                result = get_icon_path("icon.png")
                assert result == "/test/path/icon.png"
    
    def test_get_icon_path_not_found(self):
        """Test getting icon path when icon doesn't exist."""
        with patch("src.utils.resources.get_resource_path") as mock_get_resource:
            mock_get_resource.return_value = "/test/path/icon.png"
            with patch("os.path.exists", return_value=False):
                result = get_icon_path("icon.png")
                assert result is None
    
    def test_get_help_file_path_found(self):
        """Test getting help file path when help file exists."""
        with patch("src.utils.resources.get_resource_path") as mock_get_resource:
            mock_get_resource.return_value = "/test/path/HELP.md"
            with patch("os.path.exists", return_value=True):
                result = get_help_file_path()
                assert result == "/test/path/HELP.md"
    
    def test_get_help_file_path_not_found(self):
        """Test getting help file path when help file doesn't exist."""
        with patch("src.utils.resources.get_resource_path") as mock_get_resource:
            mock_get_resource.return_value = "/test/path/HELP.md"
            with patch("os.path.exists", return_value=False):
                result = get_help_file_path()
                assert result is None
    
    def test_resource_exists_true(self):
        """Test resource_exists returns True when resource exists."""
        with patch("src.utils.resources.get_resource_path") as mock_get_resource:
            mock_get_resource.return_value = "/test/path/resource.txt"
            with patch("os.path.exists", return_value=True):
                result = resource_exists("resource.txt")
                assert result is True
    
    def test_resource_exists_false(self):
        """Test resource_exists returns False when resource doesn't exist."""
        with patch("src.utils.resources.get_resource_path") as mock_get_resource:
            mock_get_resource.return_value = "/test/path/resource.txt"
            with patch("os.path.exists", return_value=False):
                result = resource_exists("resource.txt")
                assert result is False
    
    def test_pyinstaller_bundle_mode(self):
        """Test resource path in PyInstaller bundle mode."""
        with patch("sys._MEIPASS", "/bundle/path", create=True):
            with patch("hasattr", return_value=True):
                result = get_resource_path("test_file.txt")
                assert result == "/bundle/path/test_file.txt"
