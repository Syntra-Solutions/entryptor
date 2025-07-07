"""Data models for Entryptor2."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EncryptionMode(Enum):
    """Encryption mode options."""

    PASSWORD = "password"
    KEYFILE = "keyfile"


class ExtensionOption(Enum):
    """File extension preservation options."""

    PRESERVE = "preserve"
    MANUAL = "manual"


@dataclass
class AppSettings:
    """Application settings data model."""

    encryption_mode: EncryptionMode
    extension_option: ExtensionOption


@dataclass
class FileMetadata:
    """Metadata stored in encrypted files."""

    original_extension: str
    version: str


@dataclass
class EncryptionResult:
    """Result of encryption/decryption operations."""

    success: bool
    output_path: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of password validation."""

    is_valid: bool
    error_message: str
    strength_score: int  # 0-100
