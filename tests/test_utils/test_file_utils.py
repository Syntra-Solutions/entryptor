"""Tests for file utilities."""

import os
import tempfile

from src.utils.file_utils import (
    get_file_size, get_file_extension, get_unique_filename,
    is_valid_file_path, get_file_basename, safe_file_copy,
    safe_file_move, safe_file_delete, list_files_in_directory,
    ensure_directory_exists
)


class TestFileUtils:
    """Test file utility functions."""
    
    def test_get_file_size_existing_file(self):
        """Test getting size of existing file."""
        content = b"Test content"
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            size = get_file_size(temp_file_path)
            assert size == len(content)
        finally:
            os.unlink(temp_file_path)
    
    def test_get_file_size_nonexistent_file(self):
        """Test getting size of non-existent file."""
        size = get_file_size("/nonexistent/file.txt")
        assert size is None
    
    def test_get_file_size_empty_file(self):
        """Test getting size of empty file."""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
        
        try:
            size = get_file_size(temp_file_path)
            assert size == 0
        finally:
            os.unlink(temp_file_path)
    
    def test_get_file_extension_with_extension(self):
        """Test getting extension from file with extension."""
        assert get_file_extension("document.txt") == ".txt"
        assert get_file_extension("archive.tar.gz") == ".gz"
        assert get_file_extension("image.JPEG") == ".JPEG"
    
    def test_get_file_extension_without_extension(self):
        """Test getting extension from file without extension."""
        assert get_file_extension("document") == ""
        assert get_file_extension("README") == ""
    
    def test_get_file_extension_hidden_file(self):
        """Test getting extension from hidden file."""
        assert get_file_extension(".hidden") == ""
        assert get_file_extension(".hidden.txt") == ".txt"
    
    def test_get_file_extension_path_with_directories(self):
        """Test getting extension from full path."""
        assert get_file_extension("/Users/test/document.txt") == ".txt"
        assert get_file_extension("C:\\Users\\test\\document.docx") == ".docx"
    
    def test_get_file_extension_empty_path(self):
        """Test getting extension from empty path."""
        assert get_file_extension("") == ""
    
    def test_get_unique_filename_no_conflict(self):
        """Test ensuring unique filename when no conflict exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            desired_path = os.path.join(temp_dir, "test.txt")
            
            unique_path = get_unique_filename(desired_path)
            
            assert unique_path == desired_path
    
    def test_get_unique_filename_with_conflict(self):
        """Test ensuring unique filename when conflict exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create existing file
            existing_path = os.path.join(temp_dir, "test.txt")
            with open(existing_path, 'w') as f:
                f.write("existing content")
            
            unique_path = get_unique_filename(existing_path)
            
            assert unique_path != existing_path
            assert "test" in unique_path and ".txt" in unique_path
    
    def test_get_file_basename_basic(self):
        """Test getting basename from file path."""
        assert get_file_basename("/Users/test/document.txt") == "document"
        assert get_file_basename("document.txt") == "document"
        assert get_file_basename("/Users/test/") == ""
    
    def test_is_valid_file_path_valid_cases(self):
        """Test valid file path validation."""
        # Create a real file for testing
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"test content")
            temp_file_path = temp_file.name
        
        try:
            assert is_valid_file_path(temp_file_path) is True
        finally:
            os.unlink(temp_file_path)
    
    def test_is_valid_file_path_invalid_cases(self):
        """Test invalid file path validation."""
        assert is_valid_file_path("") is False
        assert is_valid_file_path("   ") is False
    
    def test_safe_file_copy_success(self):
        """Test safe file copying with successful copy."""
        content = b"Test content for safe copy"
        
        with tempfile.NamedTemporaryFile(delete=False) as source_file:
            source_file.write(content)
            source_path = source_file.name
        
        with tempfile.NamedTemporaryFile(delete=False) as dest_file:
            dest_path = dest_file.name
        
        try:
            os.unlink(dest_path)  # Remove the file created by NamedTemporaryFile
            
            result = safe_file_copy(source_path, dest_path)
            assert result is True
            
            # Verify content was copied
            with open(dest_path, 'rb') as f:
                copied_content = f.read()
            
            assert copied_content == content
        finally:
            for path in [source_path, dest_path]:
                if os.path.exists(path):
                    os.unlink(path)
    
    def test_safe_file_copy_nonexistent_source(self):
        """Test safe file copying with non-existent source."""
        result = safe_file_copy("/nonexistent/source.txt", "/tmp/dest.txt")
        assert result is False
    
    def test_safe_file_move_success(self):
        """Test safe file moving with successful move."""
        content = b"Test content for safe move"
        
        with tempfile.NamedTemporaryFile(delete=False) as source_file:
            source_file.write(content)
            source_path = source_file.name
        
        with tempfile.NamedTemporaryFile(delete=False) as dest_file:
            dest_path = dest_file.name
        
        try:
            os.unlink(dest_path)  # Remove the file created by NamedTemporaryFile
            
            result = safe_file_move(source_path, dest_path)
            assert result is True
            
            # Verify source no longer exists
            assert not os.path.exists(source_path)
            
            # Verify content was moved
            with open(dest_path, 'rb') as f:
                moved_content = f.read()
            
            assert moved_content == content
        finally:
            for path in [source_path, dest_path]:
                if os.path.exists(path):
                    os.unlink(path)
    
    def test_safe_file_delete_success(self):
        """Test safe file deletion with successful deletion."""
        content = b"Test content for safe delete"
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            result = safe_file_delete(temp_file_path)
            assert result is True
            
            # Verify file no longer exists
            assert not os.path.exists(temp_file_path)
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    def test_safe_file_delete_nonexistent_file(self):
        """Test safe file deletion with non-existent file."""
        result = safe_file_delete("/nonexistent/file.txt")
        assert result is True  # Returns True because file doesn't exist after operation
    
    def test_list_files_in_directory_success(self):
        """Test listing files in directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some test files
            test_files = ["file1.txt", "file2.pdf", "file3.jpg"]
            for filename in test_files:
                file_path = os.path.join(temp_dir, filename)
                with open(file_path, 'w') as f:
                    f.write("test content")
            
            files = list_files_in_directory(temp_dir)
            
            assert isinstance(files, list)
            assert len(files) == len(test_files)
            
            # Check that all test files are in the result
            file_basenames = [os.path.basename(f) for f in files]
            for test_file in test_files:
                assert test_file in file_basenames
    
    def test_list_files_in_directory_nonexistent(self):
        """Test listing files in non-existent directory."""
        files = list_files_in_directory("/nonexistent/directory")
        assert files == []
    
    def test_ensure_directory_exists_new_directory(self):
        """Test creating new directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir_path = os.path.join(temp_dir, "new_directory")
            
            result = ensure_directory_exists(new_dir_path)
            assert result is True
            assert os.path.exists(new_dir_path)
            assert os.path.isdir(new_dir_path)
    
    def test_ensure_directory_exists_existing_directory(self):
        """Test with existing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = ensure_directory_exists(temp_dir)
            assert result is True
            assert os.path.exists(temp_dir)
    
    def test_ensure_directory_exists_nested_directory(self):
        """Test creating nested directory structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir_path = os.path.join(temp_dir, "level1", "level2", "level3")
            
            result = ensure_directory_exists(nested_dir_path)
            assert result is True
            assert os.path.exists(nested_dir_path)
            assert os.path.isdir(nested_dir_path)
