"""Key derivation utilities for encryption."""

import os
import base64
from typing import Tuple, Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

from .secure_memory import SecurePassword
from ..config.constants import SALT_SIZE, PBKDF2_ITERATIONS


def generate_salt(length: int = SALT_SIZE) -> bytes:
    """
    Generate a random salt for key derivation.
    
    Args:
        length: Length of salt in bytes (default: SALT_SIZE)
        
    Returns:
        Random salt bytes
    """
    return os.urandom(length)


def derive_key_from_password(
    password: SecurePassword, salt: Optional[bytes] = None
) -> Tuple[bytes, bytes]:
    """
    Derive encryption key from password using PBKDF2.

    Args:
        password: Secure password wrapper
        salt: Optional salt bytes. If None, generates random salt

    Returns:
        Tuple of (key, salt) as bytes

    Raises:
        ValueError: If password is empty
    """
    password_bytes = password.get_bytes()
    if not password_bytes:
        raise ValueError("Password cannot be empty")

    if salt is None:
        salt = os.urandom(SALT_SIZE)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
        backend=default_backend(),
    )

    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key, salt


def derive_key_from_keyfile(keyfile_path: str) -> bytes:
    """
    Derive encryption key from keyfile.

    Args:
        keyfile_path: Path to the keyfile

    Returns:
        Derived key as bytes

    Raises:
        FileNotFoundError: If keyfile doesn't exist
        ValueError: If keyfile is empty or invalid
    """
    if not os.path.exists(keyfile_path):
        raise FileNotFoundError(f"Keyfile not found: {keyfile_path}")

    with open(keyfile_path, "rb") as f:
        keyfile_data = f.read()

    if not keyfile_data:
        raise ValueError("Keyfile is empty")

    if len(keyfile_data) < 32:
        raise ValueError("Keyfile must be at least 32 bytes")

    # Use the keyfile data directly as key material
    # Hash it to ensure consistent length
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(keyfile_data)
    key_material = digest.finalize()

    return base64.urlsafe_b64encode(key_material)


def generate_keyfile(output_path: str) -> None:
    """
    Generate a new keyfile with random data.

    Args:
        output_path: Path where to save the keyfile

    Raises:
        OSError: If file cannot be written
    """
    # Generate 256 bytes of random data
    key_data = os.urandom(256)

    with open(output_path, "wb") as f:
        f.write(key_data)

    # Set restrictive permissions (readable only by owner)
    os.chmod(output_path, 0o600)


def validate_keyfile(keyfile_path: str) -> bool:
    """
    Validate if a keyfile is usable.

    Args:
        keyfile_path: Path to the keyfile

    Returns:
        True if keyfile is valid, False otherwise
    """
    try:
        derive_key_from_keyfile(keyfile_path)
        return True
    except (FileNotFoundError, ValueError):
        return False
