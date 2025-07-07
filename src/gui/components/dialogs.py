"""Dialog components for settings and help."""

import os
from typing import Optional

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QCheckBox,
    QPushButton, QTextBrowser, QDialogButtonBox, QMessageBox, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ...config.models import EncryptionMode, ExtensionOption
from ...utils.resources import get_help_file_path


class SettingsDialog(QDialog):
    """Settings dialog for configuring application preferences."""
    
    def __init__(
        self, 
        current_extension_option: str, 
        use_keyfile: bool = False, 
        parent: Optional[QWidget] = None
    ) -> None:
        """
        Initialize settings dialog.
        
        Args:
            current_extension_option: Current extension preservation option
            use_keyfile: Whether keyfile mode is enabled
            parent: Parent widget
        """
        super().__init__(parent)
        self.extension_combo: Optional[QComboBox] = None
        self.keyfile_toggle: Optional[QCheckBox] = None
        self._setup_ui(current_extension_option, use_keyfile)
        self._connect_signals()
    
    def _setup_ui(self, current_extension_option: str, use_keyfile: bool) -> None:
        """Set up the user interface."""
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Extension handling section
        extension_layout = QHBoxLayout()
        extension_label = QLabel("File Extension:")
        extension_label.setMinimumWidth(120)
        
        self.extension_combo = QComboBox()
        self.extension_combo.addItems([
            "Preserve original extension",
            "Manual extension selection"
        ])
        
        # Set current selection
        if current_extension_option == "Preserve original extension":
            self.extension_combo.setCurrentIndex(0)
        else:
            self.extension_combo.setCurrentIndex(1)
        
        extension_layout.addWidget(extension_label)
        extension_layout.addWidget(self.extension_combo)
        layout.addLayout(extension_layout)
        
        # Keyfile mode section
        self.keyfile_toggle = QCheckBox("Use Keyfile instead of password")
        self.keyfile_toggle.setChecked(use_keyfile)
        layout.addWidget(self.keyfile_toggle)
        
        # Info label
        info_label = QLabel(
            "Extension preservation is available in both password and keyfile modes."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #888888; font-size: 12px;")
        layout.addWidget(info_label)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
        # Connect signals 
        self._connect_signals()
    
    def _connect_signals(self) -> None:
        """Connect widget signals."""
        # No need to disable extension combo based on keyfile mode anymore
        pass
    
    def get_extension_option(self) -> str:
        """
        Get the selected extension option.
        
        Returns:
            Selected extension option text
        """
        return self.extension_combo.currentText() if self.extension_combo else ""
    
    def get_use_keyfile(self) -> bool:
        """
        Get keyfile mode setting.
        
        Returns:
            True if keyfile mode is enabled
        """
        return self.keyfile_toggle.isChecked() if self.keyfile_toggle else False
    
    def get_encryption_mode(self) -> EncryptionMode:
        """
        Get encryption mode enum value.
        
        Returns:
            EncryptionMode enum value
        """
        return EncryptionMode.KEYFILE if self.get_use_keyfile() else EncryptionMode.PASSWORD
    
    def get_extension_option_enum(self) -> ExtensionOption:
        """
        Get extension option enum value.
        
        Returns:
            ExtensionOption enum value
        """
        option_text = self.get_extension_option()
        return ExtensionOption.PRESERVE if "Preserve" in option_text else ExtensionOption.MANUAL


class HelpDialog(QDialog):
    """Help dialog for displaying application help content."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize help dialog.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.text_browser: Optional[QTextBrowser] = None
        self._setup_ui()
        self._load_help_content()
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("Entryptor Help")
        self.setMinimumSize(800, 600)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Text browser
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        
        # Set font
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.text_browser.setFont(font)
        
        layout.addWidget(self.text_browser)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _load_help_content(self) -> None:
        """Load help content from file."""
        help_file_path = get_help_file_path()
        
        if help_file_path and os.path.exists(help_file_path):
            try:
                with open(help_file_path, 'r', encoding='utf-8') as f:
                    help_content = f.read()
                    if self.text_browser:
                        self.text_browser.setMarkdown(help_content)
            except Exception as e:
                self._show_error(f"Error loading help content: {str(e)}")
        else:
            self._show_default_help()
    
    def _show_default_help(self) -> None:
        """Show default help content when help file is not available."""
        default_help = """
# Entryptor Help

## Overview
Entryptor is a secure file encryption and decryption application that provides strong AES-256 encryption with support for both password-based and keyfile-based encryption.

## Features
- **Strong Encryption**: Uses AES-256-GCM encryption
- **Password Mode**: PBKDF2 key derivation with customizable parameters
- **Keyfile Mode**: Use a keyfile instead of password for enhanced security
- **Drag & Drop**: Easy file selection through drag and drop
- **Extension Preservation**: Option to preserve original file extensions

## How to Use

### Encrypting Files
1. Select encryption mode (Password or Keyfile) in Settings
2. Drag and drop the file you want to encrypt
3. Enter a strong password or select a keyfile
4. Click "Encrypt" to create the encrypted file

### Decrypting Files
1. Drag and drop the encrypted file (.enc extension)
2. Enter the password or select the keyfile used for encryption
3. Click "Decrypt" to restore the original file

### Password Requirements
- At least 12 characters long
- Contains uppercase letters
- Contains lowercase letters
- Contains numbers
- Contains special characters

## Settings
- **Extension Preservation**: Choose whether to preserve original file extensions
- **Keyfile Mode**: Use a keyfile instead of password for encryption

## Security Notes
- Keep your passwords and keyfiles secure
- Use strong, unique passwords
- Store keyfiles in a secure location
- Encrypted files cannot be recovered without the correct password or keyfile

## Support
For additional support, please refer to the documentation or contact support.
        """
        
        if self.text_browser:
            self.text_browser.setMarkdown(default_help)
    
    def _show_error(self, message: str) -> None:
        """Show an error message."""
        if self.text_browser:
            self.text_browser.setPlainText(f"Error: {message}")


class AboutDialog(QDialog):
    """About dialog for displaying application information."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize about dialog.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("About Entryptor")
        self.setFixedSize(400, 300)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Application name
        app_name = QLabel("Entryptor")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        app_name.setFont(font)
        layout.addWidget(app_name)
        
        # Version
        version_label = QLabel("Version 2.0.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #888888;")
        layout.addWidget(version_label)
        
        # Description
        description = QLabel(
            "A secure file encryption and decryption application\\n"
            "featuring modern GUI with drag-and-drop functionality."
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Copyright
        copyright_label = QLabel("© 2025 Syntra for Business Solutions")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setStyleSheet("color: #888888; font-size: 12px;")
        layout.addWidget(copyright_label)
        
        layout.addStretch()
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)


def show_error_dialog(parent: Optional[QWidget], title: str, message: str) -> None:
    """
    Show an error dialog.
    
    Args:
        parent: Parent widget
        title: Dialog title
        message: Error message
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec()


def show_info_dialog(parent: Optional[QWidget], title: str, message: str) -> None:
    """
    Show an information dialog.
    
    Args:
        parent: Parent widget
        title: Dialog title
        message: Information message
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec()


def show_warning_dialog(parent: Optional[QWidget], title: str, message: str) -> bool:
    """
    Show a warning dialog with Yes/No buttons.
    
    Args:
        parent: Parent widget
        title: Dialog title
        message: Warning message
        
    Returns:
        True if user clicked Yes, False otherwise
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg_box.setDefaultButton(QMessageBox.StandardButton.No)
    
    result = msg_box.exec()
    return result == QMessageBox.StandardButton.Yes
