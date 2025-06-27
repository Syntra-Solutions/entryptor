# Entryptor

A secure file encryption and decryption application for macOS, featuring a modern GUI with drag-and-drop functionality, password and keyfile modes, and robust extension handling.

## Features

- 🔒 Strong encryption using AES-256-GCM
- 🔑 Password-based key derivation (PBKDF2)
- 🗝️ Keyfile-based encryption and decryption (no password required)
- 🎯 Modern, intuitive GUI with drag-and-drop support for both files and keyfiles
- 📦 File extension preservation options (preserve or hide original extension)
- ⚙️ Settings dialog for extension and keyfile mode selection
- ❓ Built-in help dialog ("?" button)
- 🛡️ Live password strength validation with visual indicators
- 🔐 Secure memory handling for sensitive data
- 🖥️ Native macOS look and feel

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/Syntra-Solutions/entryptor.git
cd entryptor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python entryptor.py
```

### Pre-built Binaries

Download the latest release from the [Releases](https://github.com/Syntra-Solutions/entryptor/releases) page.

## Usage

1. Launch Entryptor
2. Drag and drop files onto the left (encrypt) or right (decrypt) drop zone
3. Choose between password or keyfile mode in the settings (gear icon)
   - In password mode: Enter and confirm your password (live icons show requirements)
   - In keyfile mode: Drag and drop a keyfile in addition to your file
4. Choose whether to preserve the file extension (settings dialog)
5. Click "Encrypt" or "Decrypt"
6. Select where to save the output file

### Settings Dialog
- Access via the gear icon in the top right
- Choose between password and keyfile mode
- Select file extension handling (preserve or manual)

### Help Dialog
- Access via the "?" button in the top right
- Shows built-in help and troubleshooting

### Password Requirements
- Minimum 12 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character
- Live circular icons below the password field indicate which requirements are met
- Confirmation password field shows a check icon when passwords match

### Keyfile Mode
- Toggle in settings dialog
- Drag and drop a keyfile in addition to your file
- No password required
- Extension preservation is disabled in keyfile mode

## Security Features

- AES-256-GCM encryption for file security
- PBKDF2 key derivation with 100,000 iterations
- Secure memory handling for sensitive data
- Password strength validation with live feedback
- Secure file extension handling
- Keyfile-based encryption (optionally disables password entry)

## Development

### Requirements

- Python 3.8+
- PyQt6
- cryptography

### Building from Source

1. Install build dependencies:
```bash
pip install pyinstaller
```

2. Build the application:
```bash
pyinstaller entryptor.spec
```

The built application will be available in the `dist` directory.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Version History

See [CHANGELOG.md](CHANGELOG.md) for a list of changes in each version.

## Acknowledgments

- PyQt6 for the GUI framework
- cryptography library for encryption functionality