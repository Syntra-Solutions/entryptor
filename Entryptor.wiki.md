# Entryptor Project Wiki

## Overview
Entryptor is a cross-platform file encryption and decryption application built with Python and PyQt6. It provides a modern, user-friendly interface for securely encrypting and decrypting files using strong cryptography. The app supports both password-based and keyfile-based encryption modes, with options for preserving original file extensions.

## Features
- **Drag-and-drop file encryption and decryption**
- **Password-based encryption** with real-time password strength feedback
- **Keyfile-based encryption** for advanced users
- **Extension preservation**: Optionally keep the original file extension after decryption
- **Modern, dark-themed UI** with animated feedback
- **Integrated help and settings dialogs**
- **Secure password handling**: Passwords are wiped from memory after use

## Usage
1. **Encrypt a File**
   - Drag a file into the "Drop file to encrypt" area.
   - Enter and confirm a strong password (or use a keyfile if enabled in settings).
   - Click "Encrypt" and choose where to save the encrypted file.

2. **Decrypt a File**
   - Drag an encrypted file into the "Drop file to decrypt" area.
   - Enter the password or provide the keyfile used for encryption.
   - Click "Decrypt" and choose where to save the decrypted file.

3. **Settings**
   - Click the gear icon to open settings.
   - Choose between password or keyfile mode.
   - Select whether to preserve the original file extension.

4. **Help**
   - Click the "?" button for detailed usage instructions and troubleshooting.

## Architecture
- **entryptor.py**: Main application logic and UI
- **app_env.py**: Centralized app metadata (version, app name, company, copyright)
- **entryptor.spec**: PyInstaller spec file for building standalone executables
- **requirements.txt**: Python dependencies
- **HELP.md, README.md, TEST_CASES.md**: Documentation

## Security Notes
- Uses PBKDF2-HMAC-SHA256 for key derivation
- Uses Fernet (symmetric encryption) from the `cryptography` library
- Passwords are never stored and are securely wiped from memory
- Keyfile mode uses a fixed salt for compatibility (can be improved for higher security)

## Building and Distribution
- Build a standalone app using PyInstaller:
  ```sh
  pyinstaller entryptor.spec
  ```
- The output will be in the `dist-alpha/Entryptor` directory

## Contribution & Issue Tracking
- Code is managed in both GitHub and Azure DevOps repositories
- Work items are tracked in Azure Boards (reference with `AB#<id>` in commit messages)
- Please see `README.md` for contribution guidelines

## License
Entryptor is licensed under the MIT License. See `LICENSE` for details.

---
For more details, see the in-app help or contact the maintainers.
