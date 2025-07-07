"""Core encryption and decryption functionality."""

import json
import os
from typing import Optional, Dict, Any

from cryptography.fernet import Fernet

from .secure_memory import SecurePassword, SecureBytes
from .key_derivation import derive_key_from_password, derive_key_from_keyfile
from ..config.constants import ENCRYPTED_EXTENSION, CHUNK_SIZE
from ..config.models import EncryptionResult, FileMetadata, EncryptionMode


class EncryptionError(Exception):
    """Custom exception for encryption operations."""

    pass


class DecryptionError(Exception):
    """Custom exception for decryption operations."""

    pass


def encrypt_file_with_password(
    file_path: str,
    password: SecurePassword,
    output_path: Optional[str] = None,
    preserve_extension: bool = True,
) -> EncryptionResult:
    """
    Encrypt a file using password-based encryption.

    Args:
        file_path: Path to the file to encrypt
        password: Secure password wrapper
        output_path: Optional output path. If None, uses input path + .enc
        preserve_extension: Whether to preserve original extension in metadata

    Returns:
        EncryptionResult with success status and output path
    """
    try:
        if not os.path.exists(file_path):
            return EncryptionResult(
                success=False, error_message=f"File not found: {file_path}"
            )

        # Generate key and salt
        key, salt = derive_key_from_password(password)

        # Prepare metadata
        original_extension = (
            os.path.splitext(file_path)[1] if preserve_extension else ""
        )
        metadata = FileMetadata(original_extension=original_extension, version="2.0.0")

        # Determine output path
        if output_path is None:
            output_path = file_path + ENCRYPTED_EXTENSION

        # Encrypt file
        with SecureBytes(key) as secure_key:
            fernet = Fernet(secure_key.get_bytes())

            with open(file_path, "rb") as infile, open(output_path, "wb") as outfile:
                # Write salt first
                outfile.write(salt)

                # Write metadata
                metadata_json = json.dumps(
                    {
                        "original_extension": metadata.original_extension,
                        "version": metadata.version,
                        "encryption_mode": EncryptionMode.PASSWORD.value,
                    }
                ).encode("utf-8")
                metadata_length = len(metadata_json)
                outfile.write(metadata_length.to_bytes(4, byteorder="big"))
                outfile.write(metadata_json)

                # Encrypt file content in chunks
                while True:
                    chunk = infile.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    encrypted_chunk = fernet.encrypt(chunk)
                    outfile.write(len(encrypted_chunk).to_bytes(4, byteorder="big"))
                    outfile.write(encrypted_chunk)

        return EncryptionResult(success=True, output_path=output_path)

    except Exception as e:
        return EncryptionResult(
            success=False, error_message=f"Encryption failed: {str(e)}"
        )


def encrypt_file_with_keyfile(
    file_path: str,
    keyfile_path: str,
    output_path: Optional[str] = None,
    preserve_extension: bool = True,
) -> EncryptionResult:
    """
    Encrypt a file using keyfile-based encryption.

    Args:
        file_path: Path to the file to encrypt
        keyfile_path: Path to the keyfile
        output_path: Optional output path. If None, uses input path + .enc
        preserve_extension: Whether to preserve original extension in metadata

    Returns:
        EncryptionResult with success status and output path
    """
    try:
        if not os.path.exists(file_path):
            return EncryptionResult(
                success=False, error_message=f"File not found: {file_path}"
            )

        # Derive key from keyfile
        key = derive_key_from_keyfile(keyfile_path)

        # Prepare metadata
        original_extension = (
            os.path.splitext(file_path)[1] if preserve_extension else ""
        )
        metadata = FileMetadata(original_extension=original_extension, version="2.0.0")

        # Determine output path
        if output_path is None:
            output_path = file_path + ENCRYPTED_EXTENSION

        # Encrypt file
        with SecureBytes(key) as secure_key:
            fernet = Fernet(secure_key.get_bytes())

            with open(file_path, "rb") as infile, open(output_path, "wb") as outfile:
                # Write metadata (no salt for keyfile mode)
                metadata_json = json.dumps(
                    {
                        "original_extension": metadata.original_extension,
                        "version": metadata.version,
                        "encryption_mode": EncryptionMode.KEYFILE.value,
                    }
                ).encode("utf-8")
                metadata_length = len(metadata_json)
                outfile.write(metadata_length.to_bytes(4, byteorder="big"))
                outfile.write(metadata_json)

                # Encrypt file content in chunks
                while True:
                    chunk = infile.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    encrypted_chunk = fernet.encrypt(chunk)
                    outfile.write(len(encrypted_chunk).to_bytes(4, byteorder="big"))
                    outfile.write(encrypted_chunk)

        return EncryptionResult(success=True, output_path=output_path)

    except Exception as e:
        return EncryptionResult(
            success=False, error_message=f"Encryption failed: {str(e)}"
        )


def decrypt_file_with_password(
    file_path: str, password: SecurePassword, output_path: Optional[str] = None
) -> EncryptionResult:
    """
    Decrypt a file using password-based decryption.

    Args:
        file_path: Path to the encrypted file
        password: Secure password wrapper
        output_path: Optional output path. If None, uses original extension

    Returns:
        EncryptionResult with success status and output path
    """
    try:
        if not os.path.exists(file_path):
            return EncryptionResult(
                success=False, error_message=f"File not found: {file_path}"
            )

        with open(file_path, "rb") as infile:
            # Read salt
            salt = infile.read(16)  # 16 bytes salt

            # Read metadata
            metadata_length = int.from_bytes(infile.read(4), byteorder="big")
            metadata_json = infile.read(metadata_length).decode("utf-8")
            metadata = json.loads(metadata_json)

            # Verify encryption mode
            if metadata.get("encryption_mode") != EncryptionMode.PASSWORD.value:
                return EncryptionResult(
                    success=False,
                    error_message="File was not encrypted with password mode",
                )

            # Derive key
            key, _ = derive_key_from_password(password, salt)

            # Determine output path
            if output_path is None:
                base_path = os.path.splitext(file_path)[0]
                if file_path.endswith(ENCRYPTED_EXTENSION):
                    base_path = base_path[: -len(ENCRYPTED_EXTENSION)]
                original_extension = metadata.get("original_extension", "")
                output_path = base_path + original_extension

            # Decrypt file
            with SecureBytes(key) as secure_key:
                fernet = Fernet(secure_key.get_bytes())

                with open(output_path, "wb") as outfile:
                    # Read and decrypt chunks
                    while True:
                        chunk_length_bytes = infile.read(4)
                        if not chunk_length_bytes:
                            break

                        chunk_length = int.from_bytes(
                            chunk_length_bytes, byteorder="big"
                        )
                        encrypted_chunk = infile.read(chunk_length)

                        if not encrypted_chunk:
                            break

                        decrypted_chunk = fernet.decrypt(encrypted_chunk)
                        outfile.write(decrypted_chunk)

        return EncryptionResult(success=True, output_path=output_path)

    except Exception as e:
        return EncryptionResult(
            success=False, error_message=f"Decryption failed: {str(e)}"
        )


def decrypt_file_with_keyfile(
    file_path: str, keyfile_path: str, output_path: Optional[str] = None
) -> EncryptionResult:
    """
    Decrypt a file using keyfile-based decryption.

    Args:
        file_path: Path to the encrypted file
        keyfile_path: Path to the keyfile
        output_path: Optional output path. If None, uses original extension

    Returns:
        EncryptionResult with success status and output path
    """
    try:
        if not os.path.exists(file_path):
            return EncryptionResult(
                success=False, error_message=f"File not found: {file_path}"
            )

        # Derive key from keyfile
        key = derive_key_from_keyfile(keyfile_path)

        with open(file_path, "rb") as infile:
            # Read metadata
            metadata_length = int.from_bytes(infile.read(4), byteorder="big")
            metadata_json = infile.read(metadata_length).decode("utf-8")
            metadata = json.loads(metadata_json)

            # Verify encryption mode
            if metadata.get("encryption_mode") != EncryptionMode.KEYFILE.value:
                return EncryptionResult(
                    success=False,
                    error_message="File was not encrypted with keyfile mode",
                )

            # Determine output path
            if output_path is None:
                base_path = os.path.splitext(file_path)[0]
                if file_path.endswith(ENCRYPTED_EXTENSION):
                    base_path = base_path[: -len(ENCRYPTED_EXTENSION)]
                original_extension = metadata.get("original_extension", "")
                output_path = base_path + original_extension

            # Decrypt file
            with SecureBytes(key) as secure_key:
                fernet = Fernet(secure_key.get_bytes())

                with open(output_path, "wb") as outfile:
                    # Read and decrypt chunks
                    while True:
                        chunk_length_bytes = infile.read(4)
                        if not chunk_length_bytes:
                            break

                        chunk_length = int.from_bytes(
                            chunk_length_bytes, byteorder="big"
                        )
                        encrypted_chunk = infile.read(chunk_length)

                        if not encrypted_chunk:
                            break

                        decrypted_chunk = fernet.decrypt(encrypted_chunk)
                        outfile.write(decrypted_chunk)

        return EncryptionResult(success=True, output_path=output_path)

    except Exception as e:
        return EncryptionResult(
            success=False, error_message=f"Decryption failed: {str(e)}"
        )


def get_file_metadata(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Extract metadata from an encrypted file.

    Args:
        file_path: Path to the encrypted file

    Returns:
        Metadata dictionary or None if file is not encrypted
    """
    try:
        with open(file_path, "rb") as infile:
            # Check if it's a password-encrypted file (starts with salt)
            first_bytes = infile.read(4)
            infile.seek(0)

            if len(first_bytes) == 4 and first_bytes != b"\x00\x00\x00\x00":
                # Could be metadata length, try keyfile format first
                try:
                    metadata_length = int.from_bytes(first_bytes, byteorder="big")
                    if (
                        metadata_length > 0 and metadata_length < 1024
                    ):  # Reasonable limit
                        metadata_json = infile.read(metadata_length).decode("utf-8")
                        return json.loads(metadata_json)
                except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
                    pass

                # Try password format (skip salt)
                infile.seek(16)  # Skip salt
                metadata_length = int.from_bytes(infile.read(4), byteorder="big")
                metadata_json = infile.read(metadata_length).decode("utf-8")
                return json.loads(metadata_json)

        return None

    except Exception:
        return None
