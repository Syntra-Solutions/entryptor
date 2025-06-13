# Entryptor

A secure file encryption and decryption application for macOS, featuring a modern GUI with drag-and-drop functionality.

## Features

- 🔒 Strong encryption using AES-256-GCM
- 🔑 Password-based key derivation (PBKDF2)
- 🎯 Modern, intuitive GUI with drag-and-drop support
- 📦 File extension preservation options
- 🔐 Secure memory handling
- 🛡️ Password strength validation

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
2. Drag and drop files onto the application window
3. Enter your password
4. Choose encryption/decryption options
5. Click "Encrypt" or "Decrypt"

## Security Features

- AES-256-GCM encryption for file security
- PBKDF2 key derivation with 100,000 iterations
- Secure memory handling for sensitive data
- Password strength validation
- Secure file extension handling

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