# Entryptor2 Help Guide

## Overview

Entryptor2 is a secure file encryption and decryption application for macOS that provides strong AES-256-GCM encryption with support for both password-based and keyfile-based authentication. The application features a modern, intuitive drag-and-drop interface designed for ease of use while maintaining the highest security standards.

## Quick Start

### 1. Launch Entryptor2
```bash
python -m src.main
```

The main window displays two sections:
- **Left side**: File encryption
- **Right side**: File decryption

### 2. Choose Your Encryption Mode
Click the **Settings** button (⚙️) to select between:
- **Password Mode**: Uses a password you create
- **Keyfile Mode**: Uses a file as the encryption key

### 3. Encrypt a File
**Password Mode:**
1. Drag and drop your file onto the left drop zone
2. Enter a strong password (see requirements below)
3. Confirm your password
4. Click "Encrypt File"

**Keyfile Mode:**
1. Drag and drop your file onto the file drop zone
2. Drag and drop your keyfile onto the keyfile drop zone
3. Click "Encrypt File"

### 4. Decrypt a File
**Password Mode:**
1. Drag and drop the encrypted file onto the right drop zone
2. Enter the decryption password
3. Click "Decrypt File"

**Keyfile Mode:**
1. Drag and drop the encrypted file onto the file drop zone
2. Drag and drop the keyfile onto the keyfile drop zone
3. Click "Decrypt File"

## Password Requirements

For password-based encryption, your password must meet these security criteria:

- **Minimum 12 characters**
- **At least 1 uppercase letter** (A-Z)
- **At least 1 lowercase letter** (a-z)
- **At least 1 number** (0-9)
- **At least 1 special character** (!@#$%^&*, etc.)

**Visual Feedback**: Circular indicators below the password field show which requirements are met in real-time. A green checkmark appears when your confirmation password matches.

## Encryption Modes

### Password Mode
- **Security**: Uses PBKDF2 key derivation with 100,000 iterations
- **Convenience**: Only requires remembering a password
- **Best for**: Personal files, documents, and general use

### Keyfile Mode
- **Security**: Uses the keyfile contents directly as encryption material
- **Keyfile Requirements**: Minimum 64 bytes, any file type
- **Best for**: Maximum security scenarios, shared encryption keys
- **Note**: Keep your keyfile secure and backed up

## Settings Configuration

Access settings via the **Settings** button (⚙️):

### Encryption Mode
- Toggle between Password and Keyfile modes
- Changes apply immediately to the interface

### File Extension Handling
- **Preserve Extension**: Keeps the original file extension after decryption
- **Manual Selection**: Allows custom extension selection during save
- **Available in both modes**: Works with password and keyfile encryption

## Security Features

### Encryption Standards
- **Algorithm**: AES-256-GCM (Advanced Encryption Standard)
- **Key Size**: 256-bit keys for maximum security
- **Authentication**: Built-in integrity verification
- **Salt**: Unique random salt for each encrypted file

### Memory Security
- **Automatic cleanup**: Passwords are securely wiped from memory
- **No plaintext storage**: Passwords never stored in plain text
- **Secure handling**: All sensitive operations use secure memory management

### File Integrity
- **Verification**: Each encrypted file includes integrity checks
- **Corruption detection**: Automatically detects tampered or corrupted files
- **Metadata protection**: File information is encrypted and authenticated

## File Handling

### Supported File Types
- **Any file type**: Documents, images, videos, archives, etc.
- **Size limits**: No artificial size restrictions (limited by available disk space)
- **Multiple files**: Encrypt files one at a time for maximum security

### Output Files
- **Extension**: Encrypted files use `.encrypted` extension
- **Location**: Choose save location for each encrypted file
- **Naming**: Original filename is preserved with new extension

### Extension Preservation
- **Automatic**: Original extension embedded in encrypted file
- **Restoration**: Automatically restored during decryption
- **Override**: Option to manually select extension if needed

## User Interface Features

### Drag and Drop
- **File Drop Zones**: Clearly marked areas for file selection
- **Visual Feedback**: Drop zones highlight when files are dragged over
- **Multiple Support**: Separate zones for files and keyfiles

### Visual Indicators
- **Password Strength**: Real-time validation with circular indicators
- **Button States**: Encrypt/Decrypt buttons enable when requirements are met
- **Progress Feedback**: Clear success and error messages

### Help and Settings
- **Help Button** (?): Opens this help guide
- **Settings Button** (⚙️): Access configuration options
- **Compact Design**: Smaller buttons positioned for easy access

## Troubleshooting

### Common Issues

#### File Won't Encrypt
- **Check file accessibility**: Ensure the file isn't opened in another application
- **Verify permissions**: Make sure you have read access to the source file
- **Disk space**: Confirm sufficient space for the encrypted output
- **Password requirements**: Ensure password meets all security criteria
- **Keyfile selection**: In keyfile mode, verify both file and keyfile are selected

#### File Won't Decrypt
- **Correct password**: Verify you're using the exact password from encryption
- **Keyfile match**: Ensure you're using the same keyfile used for encryption
- **File corruption**: Check if the encrypted file has been modified or corrupted
- **Mode matching**: Verify you're using the same mode (password/keyfile) as encryption

#### Password Issues
- **Case sensitivity**: Passwords are case-sensitive
- **Special characters**: Ensure special characters are entered correctly
- **Caps Lock**: Check if Caps Lock is accidentally enabled
- **Copy/paste**: Avoid copying passwords that might include hidden characters

#### Interface Problems
- **Application restart**: Try closing and reopening the application
- **File permissions**: Ensure you have write access to the destination folder
- **System resources**: Close other applications if system is running low on memory

### Error Messages

#### "File not found"
- The selected file path is no longer valid
- File may have been moved, renamed, or deleted

#### "Invalid password"
- Password doesn't match the one used for encryption
- Check for typos, case sensitivity, or Caps Lock

#### "Corrupted keyfile"
- Keyfile has been modified since encryption
- Keyfile may be corrupted or the wrong file

#### "Insufficient permissions"
- No write access to the destination folder
- Try selecting a different save location

## Best Practices

### Password Security
1. **Use unique passwords**: Don't reuse passwords from other accounts
2. **Password managers**: Consider using a password manager for complex passwords
3. **Avoid personal info**: Don't use easily guessable personal information
4. **Regular updates**: Change passwords periodically for sensitive files

### Keyfile Security
1. **Secure storage**: Store keyfiles separately from encrypted files
2. **Multiple backups**: Keep secure backups of keyfiles
3. **Access control**: Limit who has access to keyfiles
4. **Unique keyfiles**: Use different keyfiles for different files

### File Management
1. **Backup originals**: Keep secure backups before encryption
2. **Test decryption**: Verify encrypted files can be decrypted before deleting originals
3. **Secure deletion**: Use secure delete tools for sensitive original files
4. **Organization**: Maintain clear naming and organization for encrypted files

### System Security
1. **Keep updated**: Regularly update Entryptor2 and your operating system
2. **Secure environment**: Use encryption in a secure, malware-free environment
3. **Physical security**: Secure your computer when not in use
4. **Network safety**: Avoid encryption/decryption over untrusted networks

## Technical Information

### Encryption Specifications
- **Algorithm**: AES-256-GCM
- **Key Derivation**: PBKDF2-HMAC-SHA256 (100,000 iterations)
- **Salt Length**: 16 bytes (128 bits)
- **Authentication**: Galois/Counter Mode built-in authentication

### File Format
Encrypted files contain:
1. **Salt**: Random salt for key derivation
2. **Metadata**: File information and settings
3. **Encrypted data**: Your original file content
4. **Authentication tag**: Integrity verification

### System Requirements
- **macOS**: 10.14 or later
- **Python**: 3.8 or later
- **Dependencies**: PyQt6, cryptography library
- **Disk space**: Minimal (encrypted files are similar size to originals)

## Privacy and Security

### Data Handling
- **No telemetry**: No data collection or transmission
- **Local processing**: All encryption/decryption happens on your device
- **No cloud**: No cloud storage or external services used
- **Memory cleanup**: Sensitive data is securely wiped from memory

### Security Audit
- **Open source**: Code is available for security review
- **Standard algorithms**: Uses well-established cryptographic standards
- **Regular updates**: Security improvements are regularly incorporated

## Support and Updates

### Getting Help
- **This guide**: Reference this help for common questions
- **GitHub repository**: Visit the project repository for additional documentation
- **Issue reporting**: Report bugs or request features through GitHub

### Updates
- **Check regularly**: Keep Entryptor2 updated for latest security features
- **Release notes**: Review release notes for new features and security improvements
- **Backward compatibility**: Newer versions can decrypt files from older versions

### Contributing
- **Open source**: Contributions welcome through GitHub
- **Security focus**: All contributions are reviewed for security implications
- **Documentation**: Help improve documentation and user guides

---

**Remember**: Keep your passwords and keyfiles secure. They cannot be recovered if lost, and your encrypted files will be permanently inaccessible without them.
