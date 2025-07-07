# Entryptor2 - Secure File Encryption Tool

A modern, secure file encryption application for macOS built with Python and PyQt6. Entryptor2 provides strong AES-256-GCM encryption with both password and keyfile authentication methods.

## Features

- **Strong Security**: AES-256-GCM encryption with PBKDF2 key derivation
- **Dual Authentication**: Support for both password and keyfile-based encryption
- **Modern GUI**: Clean, intuitive interface built with PyQt6
- **Drag & Drop**: Easy file selection with drag-and-drop functionality
- **Secure Memory**: Automatic memory cleanup for sensitive data
- **Cross-Platform**: Built for macOS with potential for Linux/Windows support

## Installation

### Requirements

- Python 3.9 or higher
- macOS 10.14 or higher
- 50MB of available disk space

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/your-username/entryptor2.git
cd entryptor2
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python -m src.main
```

## Usage

### Basic Encryption

1. **Launch Entryptor2**
   ```bash
   python -m src.main
   ```

2. **Select Encryption Mode**
   - Choose between "Password" and "Keyfile" modes
   - Password mode: Uses a password you provide
   - Keyfile mode: Uses a file as the encryption key

3. **Add Files**
   - Drag and drop files onto the encryption area
   - Or use the file browser to select files

4. **Set Password/Keyfile**
   - For password mode: Enter a strong password (12+ characters)
   - For keyfile mode: Select a keyfile (minimum 64 bytes)

5. **Encrypt**
   - Click "Encrypt File" to create the encrypted version
   - Encrypted files have a `.encrypted` extension

### Basic Decryption

1. **Switch to Decrypt Mode**
   - Use the mode toggle in the interface

2. **Add Encrypted File**
   - Drag and drop the `.encrypted` file

3. **Enter Password/Keyfile**
   - Provide the same password or keyfile used for encryption

4. **Decrypt**
   - Click "Decrypt File" to restore the original file

### Advanced Features

#### Password Strength Validation
- Minimum 12 characters
- Must contain uppercase, lowercase, numbers, and symbols
- Real-time strength indicator

#### Keyfile Requirements
- Minimum 64 bytes in size
- Can be any file type (image, document, etc.)
- Keep keyfiles secure and backed up

#### Security Features
- Automatic memory cleanup for passwords and keys
- Secure random salt generation
- File integrity verification
- Error handling for corrupted files

## Security Architecture

### Encryption Details
- **Algorithm**: AES-256-GCM (Galois/Counter Mode)
- **Key Derivation**: PBKDF2 with 100,000 iterations
- **Salt**: 16 bytes of cryptographically secure random data
- **Nonce**: 12 bytes of random data for each encryption

### File Format
Encrypted files contain:
1. File header with metadata
2. Salt for key derivation
3. Nonce for encryption
4. Encrypted file data
5. Authentication tag

### Memory Security
- Passwords are stored in secure memory objects
- Automatic cleanup on object destruction
- Memory overwriting for sensitive data

## Configuration

Settings are stored in `~/Library/Application Support/Entryptor/settings.json` on macOS.

### Available Settings
```json
{
  "encryption_mode": "password",
  "extension_option": "add",
  "remember_settings": true,
  "auto_delete_originals": false,
  "show_advanced_options": false
}
```

## Development

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test modules
python -m pytest tests/test_crypto/
python -m pytest tests/test_utils/

# Run with coverage
python -m pytest --cov=src/
```

### Code Quality
```bash
# Style checking
python -m ruff check src/ tests/

# Type checking
python -m mypy src/

# Auto-format code
python -m ruff format src/ tests/
```

### Project Structure
```
entryptor2/
├── src/
│   ├── main.py              # Application entry point
│   ├── crypto/              # Encryption/decryption modules
│   ├── gui/                 # PyQt6 GUI components
│   ├── utils/               # Utility functions
│   └── config/              # Configuration management
├── tests/                   # Unit and integration tests
├── examples/                # Example applications
└── requirements.txt         # Python dependencies
```

## Troubleshooting

### Common Issues

#### "Module not found" errors
Make sure you're in the project directory and the virtual environment is activated:
```bash
source .venv/bin/activate
export PYTHONPATH=$(pwd)
```

#### PyQt6 import errors
Try reinstalling PyQt6:
```bash
pip uninstall PyQt6
pip install PyQt6==6.7.0
```

#### Permission errors
Ensure the application has read/write permissions for the files you're trying to encrypt/decrypt.

#### Memory errors with large files
Large files are processed in chunks. If you encounter memory issues, try:
- Closing other applications
- Encrypting smaller files
- Increasing available system memory

### Performance Tips

- **Large Files**: Files over 1GB may take several minutes to encrypt/decrypt
- **SSD Storage**: Use SSD storage for better performance
- **Memory**: Ensure at least 1GB of available RAM for large files

## Security Considerations

### Password Security
- Use unique, strong passwords for each encrypted file
- Consider using a password manager
- Never share passwords over insecure channels

### Keyfile Security
- Store keyfiles separately from encrypted files
- Back up keyfiles securely
- Use unique keyfiles for different files

### File Handling
- Securely delete original files after encryption if needed
- Verify encrypted files before deleting originals
- Keep backups of important data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/your-username/entryptor2.git
cd entryptor2

# Create development environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Check code quality
python -m ruff check src/ tests/
python -m mypy src/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI
- Uses [cryptography](https://cryptography.io/) library for encryption
- Inspired by modern security practices and user experience design

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the examples in the `examples/` directory

---

**⚠️ Important Security Note**: This software is provided as-is. While it uses industry-standard encryption, please ensure you understand the security implications and have backups of your data before use.
