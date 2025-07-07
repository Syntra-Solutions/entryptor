"""Integration tests for Entryptor2."""

import os
import tempfile

from src.crypto.encryption import encrypt_file_with_password, decrypt_file_with_password
from src.crypto.secure_memory import SecurePassword
from src.utils.file_utils import get_file_size


def test_end_to_end_encryption():
    """Test complete encryption/decryption workflow."""
    # Create test data
    test_data = b"Hello, this is a test file for encryption!\n" * 100
    
    with tempfile.NamedTemporaryFile(delete=False) as test_file:
        test_file.write(test_data)
        test_file_path = test_file.name
    
    try:
        # Create encrypted file path
        encrypted_file_path = test_file_path + ".encrypted"
        decrypted_file_path = test_file_path + ".decrypted"
        
        # Test password
        password = "TestPassword123!"
        
        # Encrypt the file
        with SecurePassword(password) as secure_password:
            result = encrypt_file_with_password(test_file_path, secure_password, encrypted_file_path)
        
        # Verify encryption was successful
        assert result.success
        assert result.output_path == encrypted_file_path
        
        # Verify encrypted file exists and is different size
        assert os.path.exists(encrypted_file_path)
        original_size = get_file_size(test_file_path)
        encrypted_size = get_file_size(encrypted_file_path)
        assert encrypted_size != original_size
        
        # Decrypt the file
        with SecurePassword(password) as secure_password:
            result = decrypt_file_with_password(encrypted_file_path, secure_password, decrypted_file_path)
        
        # Verify decryption was successful
        assert result.success
        assert result.output_path == decrypted_file_path
        
        # Verify decrypted file exists and matches original
        assert os.path.exists(decrypted_file_path)
        
        with open(decrypted_file_path, 'rb') as f:
            decrypted_data = f.read()
        
        assert decrypted_data == test_data
        
        print("✓ End-to-end encryption test passed successfully")
        
    finally:
        # Clean up
        for file_path in [test_file_path, encrypted_file_path, decrypted_file_path]:
            if os.path.exists(file_path):
                os.unlink(file_path)


def test_key_derivation_consistency():
    """Test that key derivation is consistent."""
    from src.crypto.key_derivation import derive_key_from_password, generate_salt
    
    password = "TestPassword123!"
    salt = generate_salt()
    
    # Generate key multiple times with same password and salt
    with SecurePassword(password) as secure_password:
        key1 = derive_key_from_password(secure_password, salt)
        key2 = derive_key_from_password(secure_password, salt)
        
        assert key1 == key2
        print("✓ Key derivation consistency test passed")


def test_file_utilities():
    """Test file utility functions."""
    from src.utils.file_utils import get_file_extension, get_file_basename, is_valid_file_path
    import tempfile
    
    # Test file extension
    assert get_file_extension("test.txt") == ".txt"
    assert get_file_extension("test.tar.gz") == ".gz"
    assert get_file_extension("test") == ""
    
    # Test file basename
    assert get_file_basename("test.txt") == "test"
    assert get_file_basename("/path/to/test.txt") == "test"
    
    # Test path validation with actual file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"test content")
        temp_file_path = temp_file.name
    
    try:
        assert is_valid_file_path(temp_file_path)
        assert not is_valid_file_path("nonexistent_file.txt")
    finally:
        os.unlink(temp_file_path)
    
    print("✓ File utilities test passed")


def test_password_validation():
    """Test password validation."""
    from src.utils.validation import validate_password, calculate_password_strength
    
    # Test strong password
    strong_password = "StrongPassword123!"
    result = validate_password(strong_password)
    assert result.is_valid
    
    # Test weak password
    weak_password = "weak"
    result = validate_password(weak_password)
    assert not result.is_valid
    
    # Test password strength calculation
    strength = calculate_password_strength(strong_password)
    assert strength > 0.7
    
    print("✓ Password validation test passed")


if __name__ == "__main__":
    print("Running integration tests...")
    
    test_end_to_end_encryption()
    test_key_derivation_consistency()
    test_file_utilities()
    test_password_validation()
    
    print("\n✅ All integration tests passed successfully!")
