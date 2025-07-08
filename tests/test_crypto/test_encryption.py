"""Tests for encryption functionality."""

import os
import tempfile

from src.crypto.encryption import (
    encrypt_file_with_password,
    decrypt_file_with_password,
    encrypt_file_with_keyfile,
    decrypt_file_with_keyfile,
)
from src.crypto.secure_memory import SecurePassword


class TestEncryption:
    """Test encryption and decryption functions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_content = b"This is test content for encryption testing."
        self.password = SecurePassword("test_password")
        self.keyfile_data = b"test_keyfile_data_must_be_at_least_32_bytes_long"

    def teardown_method(self):
        """Clean up test fixtures."""
        if hasattr(self, "password"):
            self.password.clear()

    def test_encrypt_decrypt_with_password_roundtrip(self):
        """Test complete encrypt/decrypt cycle with password."""
        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            input_file.write(self.test_content)
            input_file_path = input_file.name

        try:
            with tempfile.NamedTemporaryFile(delete=False) as encrypted_file:
                encrypted_file_path = encrypted_file.name

            with tempfile.NamedTemporaryFile(delete=False) as decrypted_file:
                decrypted_file_path = decrypted_file.name

            # Encrypt
            encrypt_result = encrypt_file_with_password(
                input_file_path, self.password, encrypted_file_path
            )
            assert encrypt_result.success is True
            assert encrypt_result.output_path == encrypted_file_path

            # Decrypt
            decrypt_result = decrypt_file_with_password(
                encrypted_file_path, self.password, decrypted_file_path
            )
            assert decrypt_result.success is True
            assert decrypt_result.output_path == decrypted_file_path

            # Verify
            with open(decrypted_file_path, "rb") as f:
                decrypted_content = f.read()

            assert decrypted_content == self.test_content

        finally:
            # Clean up
            for path in [input_file_path, encrypted_file_path, decrypted_file_path]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_encrypt_decrypt_with_keyfile_roundtrip(self):
        """Test complete encrypt/decrypt cycle with keyfile."""
        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            input_file.write(self.test_content)
            input_file_path = input_file.name

        with tempfile.NamedTemporaryFile(delete=False) as keyfile:
            keyfile.write(self.keyfile_data)
            keyfile_path = keyfile.name

        try:
            with tempfile.NamedTemporaryFile(delete=False) as encrypted_file:
                encrypted_file_path = encrypted_file.name

            with tempfile.NamedTemporaryFile(delete=False) as decrypted_file:
                decrypted_file_path = decrypted_file.name

            # Encrypt
            encrypt_result = encrypt_file_with_keyfile(
                input_file_path, keyfile_path, encrypted_file_path
            )
            assert encrypt_result.success is True
            assert encrypt_result.output_path == encrypted_file_path

            # Decrypt
            decrypt_result = decrypt_file_with_keyfile(
                encrypted_file_path, keyfile_path, decrypted_file_path
            )
            assert decrypt_result.success is True
            assert decrypt_result.output_path == decrypted_file_path

            # Verify
            with open(decrypted_file_path, "rb") as f:
                decrypted_content = f.read()

            assert decrypted_content == self.test_content

        finally:
            # Clean up
            for path in [
                input_file_path,
                keyfile_path,
                encrypted_file_path,
                decrypted_file_path,
            ]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_encrypt_file_with_password_creates_different_output(self):
        """Test that encrypting same file twice produces different output."""
        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            input_file.write(self.test_content)
            input_file_path = input_file.name

        try:
            with tempfile.NamedTemporaryFile(delete=False) as encrypted_file1:
                encrypted_file1_path = encrypted_file1.name

            with tempfile.NamedTemporaryFile(delete=False) as encrypted_file2:
                encrypted_file2_path = encrypted_file2.name

            # Encrypt same file twice
            encrypt_result1 = encrypt_file_with_password(
                input_file_path, self.password, encrypted_file1_path
            )
            assert encrypt_result1.success is True

            encrypt_result2 = encrypt_file_with_password(
                input_file_path, self.password, encrypted_file2_path
            )
            assert encrypt_result2.success is True

            # Read encrypted files
            with open(encrypted_file1_path, "rb") as f:
                encrypted_content1 = f.read()

            with open(encrypted_file2_path, "rb") as f:
                encrypted_content2 = f.read()

            # Should be different due to random salt
            assert encrypted_content1 != encrypted_content2

        finally:
            # Clean up
            for path in [input_file_path, encrypted_file1_path, encrypted_file2_path]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_decrypt_with_wrong_password_fails(self):
        """Test that decrypting with wrong password fails."""
        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            input_file.write(self.test_content)
            input_file_path = input_file.name

        try:
            with tempfile.NamedTemporaryFile(delete=False) as encrypted_file:
                encrypted_file_path = encrypted_file.name

            with tempfile.NamedTemporaryFile(delete=False) as decrypted_file:
                decrypted_file_path = decrypted_file.name

            # Encrypt with one password
            encrypt_result = encrypt_file_with_password(
                input_file_path, self.password, encrypted_file_path
            )
            assert encrypt_result.success is True

            # Try to decrypt with different password
            wrong_password = SecurePassword("wrong_password")
            try:
                decrypt_result = decrypt_file_with_password(
                    encrypted_file_path, wrong_password, decrypted_file_path
                )
                assert decrypt_result.success is False
                assert "Decryption failed" in decrypt_result.error_message
            finally:
                wrong_password.clear()

        finally:
            # Clean up
            for path in [input_file_path, encrypted_file_path, decrypted_file_path]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_encrypt_nonexistent_file_fails(self):
        """Test that encrypting non-existent file fails."""
        nonexistent_path = "/nonexistent/path/file.txt"
        output_path = "/tmp/output.enc"

        result = encrypt_file_with_password(
            nonexistent_path, self.password, output_path
        )
        assert result.success is False
        assert "File not found" in result.error_message

    def test_decrypt_nonexistent_file_fails(self):
        """Test that decrypting non-existent file fails."""
        nonexistent_path = "/nonexistent/path/file.enc"
        output_path = "/tmp/output.txt"

        result = decrypt_file_with_password(
            nonexistent_path, self.password, output_path
        )
        assert result.success is False
        assert "File not found" in result.error_message

    def test_encrypt_empty_file(self):
        """Test encrypting empty file."""
        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            input_file_path = input_file.name

        try:
            with tempfile.NamedTemporaryFile(delete=False) as encrypted_file:
                encrypted_file_path = encrypted_file.name

            with tempfile.NamedTemporaryFile(delete=False) as decrypted_file:
                decrypted_file_path = decrypted_file.name

            # Encrypt empty file
            encrypt_result = encrypt_file_with_password(
                input_file_path, self.password, encrypted_file_path
            )
            assert encrypt_result.success is True

            # Decrypt
            decrypt_result = decrypt_file_with_password(
                encrypted_file_path, self.password, decrypted_file_path
            )
            assert decrypt_result.success is True

            # Verify
            with open(decrypted_file_path, "rb") as f:
                decrypted_content = f.read()

            assert decrypted_content == b""

        finally:
            # Clean up
            for path in [input_file_path, encrypted_file_path, decrypted_file_path]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_encrypt_with_cleared_password_fails(self):
        """Test that encrypting with cleared password fails."""
        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            input_file.write(self.test_content)
            input_file_path = input_file.name

        try:
            with tempfile.NamedTemporaryFile(delete=False) as encrypted_file:
                encrypted_file_path = encrypted_file.name

            # Clear password
            self.password.clear()

            result = encrypt_file_with_password(
                input_file_path, self.password, encrypted_file_path
            )
            assert result.success is False
            assert "Encryption failed" in result.error_message

        finally:
            # Clean up
            for path in [input_file_path, encrypted_file_path]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_decrypt_corrupted_file_fails(self):
        """Test that decrypting corrupted file fails."""
        with tempfile.NamedTemporaryFile(delete=False) as corrupted_file:
            corrupted_file.write(b"This is not encrypted data")
            corrupted_file_path = corrupted_file.name

        try:
            with tempfile.NamedTemporaryFile(delete=False) as decrypted_file:
                decrypted_file_path = decrypted_file.name

            result = decrypt_file_with_password(
                corrupted_file_path, self.password, decrypted_file_path
            )
            assert result.success is False
            assert "Decryption failed" in result.error_message

        finally:
            # Clean up
            for path in [corrupted_file_path, decrypted_file_path]:
                if os.path.exists(path):
                    os.unlink(path)
