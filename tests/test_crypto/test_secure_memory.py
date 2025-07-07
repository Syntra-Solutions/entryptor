"""Tests for secure memory handling."""

import gc
import pytest

from src.crypto.secure_memory import SecurePassword, SecureBytes


class TestSecurePassword:
    """Test secure password handling."""
    
    def test_secure_password_creation(self):
        """Test secure password can be created and accessed."""
        password = SecurePassword("test_password")
        assert password.get_bytes() == b"test_password"
    
    def test_secure_password_context_manager(self):
        """Test secure password as context manager."""
        with SecurePassword("test_password") as password:
            assert password.get_bytes() == b"test_password"
        
        # After context manager exits, password should be cleared
        with pytest.raises(RuntimeError, match="Password has been cleared"):
            password.get_bytes()
    
    def test_secure_password_manual_clear(self):
        """Test manual password clearing."""
        password = SecurePassword("test_password")
        password.clear()
        
        with pytest.raises(RuntimeError, match="Password has been cleared"):
            password.get_bytes()
    
    def test_secure_password_cleanup_on_deletion(self):
        """Test password cleanup on object deletion."""
        password = SecurePassword("test_password")
        password_bytes = password.get_bytes()
        
        # Delete the object
        del password
        gc.collect()
        
        # Original password bytes should be unchanged (this is a reference)
        assert password_bytes == b"test_password"


class TestSecureBytes:
    """Test secure bytes handling."""
    
    def test_secure_bytes_creation(self):
        """Test secure bytes can be created and accessed."""
        data = b"test_data"
        secure_data = SecureBytes(data)
        assert secure_data.get_bytes() == data
    
    def test_secure_bytes_context_manager(self):
        """Test secure bytes as context manager."""
        data = b"test_data"
        with SecureBytes(data) as secure_data:
            assert secure_data.get_bytes() == data
        
        # After context manager exits, data should be cleared
        with pytest.raises(RuntimeError, match="Secure data has been cleared"):
            secure_data.get_bytes()
    
    def test_secure_bytes_manual_clear(self):
        """Test manual data clearing."""
        data = b"test_data"
        secure_data = SecureBytes(data)
        secure_data.clear()
        
        with pytest.raises(RuntimeError, match="Secure data has been cleared"):
            secure_data.get_bytes()
    
    def test_secure_bytes_cleanup_on_deletion(self):
        """Test data cleanup on object deletion."""
        data = b"test_data"
        secure_data = SecureBytes(data)
        retrieved_data = secure_data.get_bytes()
        
        # Delete the object
        del secure_data
        gc.collect()
        
        # Original data should be unchanged (this is a reference)
        assert retrieved_data == data
