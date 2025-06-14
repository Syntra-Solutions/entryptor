# Changelog

All notable changes to Entryptor will be documented in this file.

## [1.0.0-alpha] - 2025-06-13
### Added
- Initial release
- Basic file encryption/decryption functionality
- Modern glass-like UI with drag and drop
- Password-based encryption using Fernet
- File extension preservation options

## [1.0.1-alpha] - 2025-06-13
### Added
- Password strength validation
- Secure memory handling
- File extension preservation options
- Copyright notice and version display
- Changelog tracking

### Security
- Added password requirements:
  - Minimum 12 characters
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Special characters
- Implemented secure password memory handling
- Added secure memory wiping after operations

### UI/UX
- Added dropdown for extension preservation options
- Added version and copyright information
- Improved error messages and validation feedback

## [1.0.0-beta] - 2025-06-14
### Added
- Live password requirements icons below encryption password input, with real-time color change for each requirement
- Live confirmation check icon below confirmation password input, with real-time color change when passwords match
- Two-line input containers for password and confirmation fields, with horizontal line and icon row inside the container
- Unified border and background styling for password containers and DropBox widgets (encryption and decryption)
- Updated test cases to cover password requirements UI and confirmation icon behavior

### Fixed
- Improved centering and alignment of icon symbols and help button
- Ensured icons and lines are visually contained within input containers
- Removed custom icon references from build spec for compatibility 

### Known Issues - planned to be resolved in 1.0.1-beta
- File extension preserve setting is not working as intended
- Settings icon is missing in this version