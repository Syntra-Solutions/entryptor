"""Tests for key derivation functionality."""

import os
import tempfile
import pytest
from unittest.mock import patch

from src.crypto.key_derivation import (
    derive_key_from_password, derive_key_from_keyfile, generate_salt
)
from src.crypto.secure_memory import SecurePassword


class TestKeyDerivation:
    """Test key derivation functions."""
    
    def test_derive_key_from_password_basic(self):
        """Test basic key derivation from password."""
        password = SecurePassword("test_password")
        salt = b"test_salt_16bytes"
        
        key, returned_salt = derive_key_from_password(password, salt)
        
        assert isinstance(key, bytes)
        assert len(key) == 44  # base64 encoded 32 bytes
        assert returned_salt == salt
    
    def test_derive_key_from_password_consistency(self):
        """Test that same password/salt produces same key."""
        password = SecurePassword("test_password")
        salt = b"test_salt_16bytes"
        
        key1, _ = derive_key_from_password(password, salt)
        key2, _ = derive_key_from_password(password, salt)
        
        assert key1 == key2
    
    def test_derive_key_from_password_different_salts(self):
        """Test that different salts produce different keys."""
        password = SecurePassword("test_password")
        salt1 = b"test_salt_16byte1"
        salt2 = b"test_salt_16byte2"
        
        key1, _ = derive_key_from_password(password, salt1)
        key2, _ = derive_key_from_password(password, salt2)
        
        assert key1 != key2
    
    def test_derive_key_from_password_different_passwords(self):
        """Test that different passwords produce different keys."""
        password1 = SecurePassword("test_password1")
        password2 = SecurePassword("test_password2")
        salt = b"test_salt_16bytes"
        
        key1, _ = derive_key_from_password(password1, salt)
        key2, _ = derive_key_from_password(password2, salt)
        
        assert key1 != key2
    
    def test_derive_key_from_password_empty_password(self):
        """Test key derivation with empty password."""
        password = SecurePassword("")
        salt = b"test_salt_16bytes"
        
        with pytest.raises(ValueError, match="Password cannot be empty"):
            derive_key_from_password(password, salt)
    
    def test_derive_key_from_password_unicode_password(self):
        """Test key derivation with unicode password."""
        password = SecurePassword("tëst_pässwörd_🔒")
        salt = b"test_salt_16bytes"
        
        key, _ = derive_key_from_password(password, salt)
        
        assert isinstance(key, bytes)
        assert len(key) == 44  # base64 encoded 32 bytes
    
    def test_derive_key_from_keyfile_basic(self):
        """Test basic key derivation from keyfile."""
        keyfile_data = b"test_keyfile_data_must_be_at_least_32_bytes_long"
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(keyfile_data)
            temp_file_path = temp_file.name
        
        try:
            key = derive_key_from_keyfile(temp_file_path)
            
            assert isinstance(key, bytes)
            assert len(key) == 44  # base64 encoded 32 bytes
        finally:
            os.unlink(temp_file_path)
    
    def test_derive_key_from_keyfile_consistency(self):
        """Test that same keyfile data produces same key."""
        keyfile_data = b"test_keyfile_data_must_be_at_least_32_bytes_long"
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(keyfile_data)
            temp_file_path = temp_file.name
        
        try:
            key1 = derive_key_from_keyfile(temp_file_path)
            key2 = derive_key_from_keyfile(temp_file_path)
            
            assert key1 == key2
        finally:
            os.unlink(temp_file_path)
    
    def test_derive_key_from_keyfile_different_data(self):
        """Test that different keyfile data produces different keys."""
        keyfile_data1 = b"test_keyfile_data1_must_be_at_least_32_bytes_long"
        keyfile_data2 = b"test_keyfile_data2_must_be_at_least_32_bytes_long"
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file1:
            temp_file1.write(keyfile_data1)
            temp_file1_path = temp_file1.name
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file2:
            temp_file2.write(keyfile_data2)
            temp_file2_path = temp_file2.name
        
        try:
            key1 = derive_key_from_keyfile(temp_file1_path)
            key2 = derive_key_from_keyfile(temp_file2_path)
            
            assert key1 != key2
        finally:
            os.unlink(temp_file1_path)
            os.unlink(temp_file2_path)
    
    def test_derive_key_from_keyfile_empty_data(self):
        """Test key derivation with empty keyfile data."""
        keyfile_data = b""
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(keyfile_data)
            temp_file_path = temp_file.name
        
        try:
            with pytest.raises(ValueError, match="Keyfile is empty"):
                derive_key_from_keyfile(temp_file_path)
        finally:
            os.unlink(temp_file_path)
    
    def test_derive_key_from_keyfile_large_data(self):
        """Test key derivation with large keyfile data."""
        keyfile_data = b"x" * 10000  # 10KB of data
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(keyfile_data)
            temp_file_path = temp_file.name
        
        try:
            key = derive_key_from_keyfile(temp_file_path)
            
            assert isinstance(key, bytes)
            assert len(key) == 44  # base64 encoded 32 bytes
        finally:
            os.unlink(temp_file_path)
    
    def test_derive_key_from_keyfile_nonexistent_file(self):
        """Test key derivation with non-existent keyfile."""
        nonexistent_path = "/nonexistent/keyfile.key"
        
        with pytest.raises(FileNotFoundError, match="Keyfile not found"):
            derive_key_from_keyfile(nonexistent_path)
    
    def test_derive_key_from_keyfile_too_small(self):
        """Test key derivation with keyfile that is too small."""
        keyfile_data = b"small"  # Less than 32 bytes
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(keyfile_data)
            temp_file_path = temp_file.name
        
        try:
            with pytest.raises(ValueError, match="Keyfile must be at least 32 bytes"):
                derive_key_from_keyfile(temp_file_path)
        finally:
            os.unlink(temp_file_path)
    
    def test_generate_salt_basic(self):
        """Test basic salt generation."""
        salt = generate_salt()
        
        assert isinstance(salt, bytes)
        assert len(salt) == 16  # Default SALT_SIZE
    
    def test_generate_salt_uniqueness(self):
        """Test that generated salts are unique."""
        salt1 = generate_salt()
        salt2 = generate_salt()
        
        assert salt1 != salt2
    
    def test_generate_salt_custom_length(self):
        """Test salt generation with custom length."""
        salt = generate_salt(32)
        
        assert isinstance(salt, bytes)
        assert len(salt) == 32
    
    def test_generate_salt_zero_length(self):
        """Test salt generation with zero length."""
        salt = generate_salt(0)
        
        assert isinstance(salt, bytes)
        assert len(salt) == 0
    
    @patch('src.crypto.key_derivation.os.urandom')
    def test_generate_salt_uses_urandom(self, mock_urandom):
        """Test that salt generation uses os.urandom."""
        mock_urandom.return_value = b"test_random_data"
        
        salt = generate_salt(16)
        
        mock_urandom.assert_called_once_with(16)
        assert salt == b"test_random_data"
    
    def test_derive_key_from_password_with_cleared_password(self):
        """Test key derivation with cleared password raises error."""
        password = SecurePassword("test_password")
        salt = b"test_salt_16bytes"
        
        password.clear()
        
        with pytest.raises(RuntimeError, match="Password has been cleared"):
            derive_key_from_password(password, salt)
