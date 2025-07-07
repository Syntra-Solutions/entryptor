"""Application constants for Entryptor2."""

VERSION = "2.0.0"
COPYRIGHT_YEAR = "2025"
APP_NAME = "Entryptor"
COMPANY_NAME = "Syntra for Business Solutions"

# Encryption constants
SALT_SIZE = 16
PBKDF2_ITERATIONS = 100000
CHUNK_SIZE = 64 * 1024  # 64KB chunks for large files

# File extensions
ENCRYPTED_EXTENSION = ".enc"
KEYFILE_EXTENSION = ".key"

# Settings keys
SETTINGS_ENCRYPTION_MODE = "encryption_mode"
SETTINGS_EXTENSION_OPTION = "extension_option"
