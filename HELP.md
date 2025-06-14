# Entryptor Help Guide

## Quick Start

1. **Launch Entryptor**
   - Double-click the Entryptor app in your Applications folder
   - The main window will appear with two drop zones

2. **Encrypt a File**
   - Drag and drop your file onto the left drop zone
   - Enter a strong password (8+ characters, including uppercase, lowercase, numbers, and symbols)
   - Confirm your password
   - Choose whether to preserve the file extension
   - Select where to save the encrypted file

3. **Decrypt a File**
   - Drag and drop your encrypted file onto the right drop zone
   - Enter the password used for encryption
   - Select where to save the decrypted file

## Password Requirements

Your password must meet these criteria:
- Minimum 12 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

There are requirements indicators when password is entered.

## Options

### File Extension Handling
- **Preserve Extension**: Keeps the original file extension
- **Hide Extension**: Removes the original extension for additional security

### Security Features
- AES-256-GCM encryption
- PBKDF2 key derivation
- Secure memory handling
- Password strength validation

## Important Notes

- Always remember your password - it cannot be recovered if lost
- Keep backups of your original files
- Store encrypted files securely
- Never share your password

## Troubleshooting

### Common Issues

1. **File Won't Encrypt**
   - Check if the file is not corrupted
   - Ensure you have write permissions
   - Verify sufficient disk space

2. **File Won't Decrypt**
   - Verify the correct password
   - Check if the file is properly encrypted
   - Ensure the file is not corrupted

3. **Password Not Accepted**
   - Check password requirements
   - Ensure Caps Lock is off
   - Verify no extra spaces

## Security Best Practices

1. **Password Management**
   - Use a password manager
   - Create unique passwords
   - Never reuse passwords

2. **File Handling**
   - Encrypt sensitive files immediately
   - Store encrypted files securely
   - Delete original files after encryption

3. **System Security**
   - Keep your system updated
   - Use antivirus software
   - Lock your computer when away

## Support

If you need additional help:
- Visit our GitHub repository
- Check the documentation
- Report issues through GitHub

## Updates

- Keep Entryptor updated for the latest security features
- Check for updates regularly
- Read release notes for new features 