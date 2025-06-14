# Entryptor Test Cases

## Functional Test Cases

### File Operations
1. **Basic Encryption**
   - Test encrypting a small text file (< 1MB)
   - Test encrypting a large file (> 100MB)
   - Test encrypting multiple files simultaneously
   - Test encrypting a file with special characters in name
   - Test encrypting a file with spaces in name

2. **Basic Decryption**
   - Test decrypting a recently encrypted file
   - Test decrypting with correct password
   - Test decrypting with incorrect password
   - Test decrypting multiple files simultaneously

3. **File Extension Handling**
   - Test encryption with extension preservation enabled
   - Test encryption with extension preservation disabled
   - Test decryption of files with preserved extensions
   - Test decryption of files without preserved extensions

4. **Drag and Drop Interface**
   - Test dragging single file to encryption area
   - Test dragging single file to decryption area
   - Test dragging multiple files to encryption area
   - Test dragging multiple files to decryption area
   - Test dragging invalid files (non-existent, corrupted)

### Password Management
1. **Password Validation**
   - Test password with minimum length (8 characters)
   - Test password with maximum length (128 characters)
   - Test password with all required character types
   - Test password missing required character types
   - Test password with special characters
   - Test password with spaces

2. **Password Confirmation**
   - Test matching password confirmation
   - Test non-matching password confirmation
   - Test empty password confirmation

### User Interface
1. **Window Operations**
   - Test window resizing
   - Test window minimizing/maximizing
   - Test window closing with active operations
   - Test window closing with saved files

2. **Progress Indication**
   - Test progress bar during encryption
   - Test progress bar during decryption
   - Test progress bar with large files
   - Test progress bar with multiple files

### Password Requirements UI

1. **Password Requirements Icons**
   - Verify that five gray, circular icons are displayed below the encryption password input field.
   - As the user types, each icon turns green when its requirement is met:
     - 12+ characters
     - At least one uppercase letter
     - At least one lowercase letter
     - At least one number
     - At least one special character
   - Icons remain gray for unmet requirements and green for met requirements.
   - Icons are visually contained within the input container, below a faint horizontal line.

2. **Password Confirmation Icon**
   - Verify that a single gray, circular checkmark icon is displayed below the confirmation password input field.
   - The icon turns green when the confirmation password matches the main password.
   - The icon remains gray if the passwords do not match or are empty.
   - The icon is visually contained within the input container, below a faint horizontal line.

## Non-Functional Test Cases

### Performance
1. **Response Time**
   - Test application startup time
   - Test UI responsiveness during encryption
   - Test UI responsiveness during decryption
   - Test memory usage during large file operations

2. **Resource Usage**
   - Test CPU usage during encryption
   - Test CPU usage during decryption
   - Test memory usage during encryption
   - Test memory usage during decryption
   - Test disk I/O performance

### Usability
1. **User Experience**
   - Test intuitive nature of drag-and-drop interface
   - Test clarity of error messages
   - Test clarity of success messages
   - Test accessibility of all controls
   - Test keyboard shortcuts (if any)

2. **Documentation**
   - Test clarity of README instructions
   - Test completeness of installation guide
   - Test accuracy of version information
   - Test clarity of error message explanations

### Compatibility
1. **System Requirements**
   - Test on different macOS versions
   - Test on different screen resolutions
   - Test with different Python versions
   - Test with different PyQt6 versions

## Security Test Cases

### Encryption
1. **Algorithm Implementation**
   - Test AES-256-GCM encryption strength
   - Test PBKDF2 key derivation
   - Test salt generation and usage
   - Test IV (Initialization Vector) generation

2. **Key Management**
   - Test secure key generation
   - Test secure key storage
   - Test secure key disposal
   - Test key derivation parameters

### Memory Security
1. **Sensitive Data Handling**
   - Test password memory wiping
   - Test key memory wiping
   - Test secure memory allocation
   - Test secure memory deallocation

2. **File Security**
   - Test secure file handling
   - Test secure temporary file creation
   - Test secure file deletion
   - Test file permission handling

### Input Validation
1. **Password Security**
   - Test password strength validation
   - Test password length validation
   - Test password character validation
   - Test password entropy

2. **File Validation**
   - Test file integrity checking
   - Test file corruption detection
   - Test file size validation
   - Test file type validation

### Attack Prevention
1. **Brute Force Protection**
   - Test password attempt limiting
   - Test rate limiting
   - Test timeout mechanisms

2. **Side Channel Attacks**
   - Test timing attack prevention
   - Test memory dump protection
   - Test cache attack prevention

## Test Environment Requirements

### Hardware Requirements
- Mac computer with Apple Silicon or Intel processor
- Minimum 8GB RAM
- Sufficient disk space for test files

### Software Requirements
- macOS 10.15 or later
- Python 3.8 or later
- PyQt6
- cryptography library

### Test Data Requirements
- Sample files of various sizes
- Files with different extensions
- Files with special characters in names
- Corrupted files for negative testing
- Large files for performance testing 