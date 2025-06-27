# Entryptor Help Guide

## Quick Start

1. **Launch Entryptor**
   - Double-click the Entryptor app or run `python entryptor.py`
   - The main window will appear with two drop zones: left for encryption, right for decryption

2. **Encrypt a File**
   - Drag and drop your file onto the left drop zone
   - Choose password or keyfile mode in the settings (gear icon)
     - **Password mode:** Enter a strong password and confirm it. Live circular icons below the password field show which requirements are met. A check icon appears when passwords match.
     - **Keyfile mode:** Drag and drop a keyfile in addition to your file. No password is required.
   - Choose whether to preserve the file extension (settings dialog)
   - Click "Encrypt" and select where to save the encrypted file

3. **Decrypt a File**
   - Drag and drop your encrypted file onto the right drop zone
   - In password mode: Enter the password used for encryption
   - In keyfile mode: Drag and drop the keyfile used for encryption
   - Click "Decrypt" and select where to save the decrypted file

## Password Requirements

Your password must meet these criteria:
- Minimum 12 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

Live circular icons below the password field indicate which requirements are met. The confirmation field shows a check icon when passwords match.

## Keyfile Mode
- Toggle keyfile mode in the settings dialog (gear icon)
- Drag and drop a keyfile in addition to your file
- No password entry is required
- Extension preservation is disabled in keyfile mode

## Settings Dialog
- Access via the gear icon in the top right
- Choose between password and keyfile mode
- Select file extension handling (preserve or manual)

## Help Dialog
- Access via the "?" button in the top right
- Shows this help guide and troubleshooting tips

## Options

### File Extension Handling
- **Preserve Extension**: Keeps the original file extension
- **Manual Selection**: Lets you choose the extension for the output file
- **Note:** Extension preservation is not available in keyfile mode

### Security Features
- AES-256-GCM encryption
- PBKDF2 key derivation (password mode)
- Secure memory handling
- Password strength validation with live feedback
- Keyfile-based encryption (no password required)

## Important Notes

- Always remember your password or keep your keyfile safe – they cannot be recovered if lost
- Keep backups of your original files
- Store encrypted files securely
- Never share your password or keyfile

## Troubleshooting

### Common Issues

1. **File Won't Encrypt**
   - Check if the file is not corrupted
   - Ensure you have write permissions
   - Verify sufficient disk space
   - In keyfile mode, make sure both file and keyfile are selected

2. **File Won't Decrypt**
   - Verify the correct password or keyfile
   - Check if the file is properly encrypted
   - Ensure the file is not corrupted

3. **Password Not Accepted**
   - Check password requirements (see above)
   - Ensure Caps Lock is off
   - Verify no extra spaces

4. **Keyfile Not Accepted**
   - Make sure you are in keyfile mode (settings dialog)
   - Ensure the keyfile is not corrupted or empty

## Security Best Practices

1. **Password/Keyfile Management**
   - Use a password manager or secure storage for keyfiles
   - Create unique passwords
   - Never reuse passwords or keyfiles

2. **File Handling**
   - Encrypt sensitive files immediately
   - Store encrypted files and keyfiles securely
   - Delete original files after encryption if needed

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