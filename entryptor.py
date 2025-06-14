import sys
import os
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog,
                            QGraphicsDropShadowEffect, QMessageBox, QComboBox, QCheckBox,
                            QTextBrowser, QDialog)
from PyQt6.QtCore import Qt, QMimeData, QPointF, QUrl, QSize
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QColor, QIcon, QFont
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import json
import weakref
import gc
from PyQt6.QtWidgets import QStyle

# Version information
VERSION = "1.0.1"
COPYRIGHT_YEAR = "2025"
COMPANY_NAME = "Syntra for Business Solutions"

def validate_password(password: str) -> tuple[bool, str]:
    """
    Validates password strength.
    Returns (is_valid, error_message)
    """
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, ""

class SecurePassword:
    """Wrapper class for secure password handling"""
    def __init__(self, password: str):
        self._password = password.encode()
    
    def get_bytes(self) -> bytes:
        return self._password
    
    def __del__(self):
        # Securely wipe the password from memory
        if hasattr(self, '_password'):
            self._password = b'\x00' * len(self._password)
            del self._password
        gc.collect()

class DropBox(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumSize(300, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 0.7);
                border-radius: 15px;
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(QPointF(0, 0))
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout()
        self.label = QLabel(title)
        self.label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 16px;
                background: transparent;
            }
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        self.setLayout(layout)
        self.file_path = None
        self.original_extension = None

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        files = event.mimeData().urls()
        if files:
            self.file_path = files[0].toLocalFile()
            self.original_extension = os.path.splitext(self.file_path)[1]
            self.label.setText(os.path.basename(self.file_path))

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Entryptor Help")
        self.setMinimumSize(800, 600)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create text browser
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setFont(QFont("Arial", 11))
        
        # Load help content
        try:
            with open("HELP.md", "r", encoding="utf-8") as f:
                help_content = f.read()
                self.text_browser.setMarkdown(help_content)
        except Exception as e:
            self.text_browser.setPlainText(f"Error loading help content: {str(e)}")
        
        layout.addWidget(self.text_browser)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)

class SettingsDialog(QDialog):
    def __init__(self, current_extension_option, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(400, 250)
        layout = QVBoxLayout()

        # Extension handling option
        self.extension_combo = QComboBox()
        self.extension_combo.addItems(["Preserve original extension (Less secure)", "Manual extension selection (More secure)"])
        self.extension_combo.setCurrentText(current_extension_option)
        layout.addWidget(QLabel("Extension handling:"))
        layout.addWidget(self.extension_combo)

        # Spacer
        layout.addStretch()

        # Footer
        copyright_label = QLabel(f"© {COPYRIGHT_YEAR} {COMPANY_NAME}")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def get_extension_option(self):
        return self.extension_combo.currentText()

class EntryptorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Entryptor v{VERSION}")
        self.setMinimumSize(800, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QLineEdit {
                padding: 10px;
                background-color: rgba(30, 30, 30, 0.7);
                border: 1px solid rgba(62, 62, 62, 0.5);
                border-radius: 10px;
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #007AFF;
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QComboBox {
                padding: 10px;
                background-color: rgba(30, 30, 30, 0.7);
                border: 1px solid rgba(62, 62, 62, 0.5);
                border-radius: 10px;
                color: #ffffff;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QLabel#copyright {
                color: rgba(255, 255, 255, 0.5);
                font-size: 12px;
                background: transparent;
            }
        """)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Create content layout for the main area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Create left column (Encryption)
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setSpacing(15)
        
        self.encrypt_dropbox = DropBox("Drop file to encrypt")
        self.encrypt_password = QLineEdit()
        self.encrypt_password.setPlaceholderText("Enter encryption password")
        self.encrypt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.encrypt_password_confirm = QLineEdit()
        self.encrypt_password_confirm.setPlaceholderText("Confirm password")
        self.encrypt_password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(self.encrypt_file)
        
        left_layout.addWidget(self.encrypt_dropbox)
        left_layout.addWidget(self.encrypt_password)
        left_layout.addWidget(self.encrypt_password_confirm)
        left_layout.addWidget(self.encrypt_button)

        # Create right column (Decryption)
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setSpacing(15)
        
        self.decrypt_dropbox = DropBox("Drop file to decrypt")
        self.decrypt_password = QLineEdit()
        self.decrypt_password.setPlaceholderText("Enter decryption password")
        self.decrypt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.decrypt_file)
        
        right_layout.addWidget(self.decrypt_dropbox)
        right_layout.addWidget(self.decrypt_password)
        right_layout.addWidget(self.decrypt_button)

        # Add columns to content layout
        content_layout.addWidget(left_column)
        content_layout.addWidget(right_column)

        # Add content layout to main layout
        main_layout.addLayout(content_layout)

        # Add help and settings buttons
        help_button = QPushButton("?")
        help_button.setMinimumSize(32, 32)
        help_button.setMaximumSize(32, 32)
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #808080;
                color: white;
                border: 2px solid #606060;
                border-radius: 16px;
                padding: 0px;
                font-weight: bold;
                font-size: 20px;
                font-family: Arial;
            }
            QPushButton:hover {
                background-color: #606060;
                border: 2px solid #404040;
            }
            QPushButton:pressed {
                background-color: #505050;
                border: 2px solid #303030;
            }
        """)
        help_shadow = QGraphicsDropShadowEffect()
        help_shadow.setBlurRadius(15)
        help_shadow.setColor(QColor(0, 0, 0, 100))
        help_shadow.setOffset(0, 2)
        help_button.setGraphicsEffect(help_shadow)
        help_button.clicked.connect(self.show_help)

        # Settings button with gear icon
        settings_button = QPushButton()
        settings_button.setMinimumSize(32, 32)
        settings_button.setMaximumSize(32, 32)
        settings_button.setStyleSheet(help_button.styleSheet())
        settings_shadow = QGraphicsDropShadowEffect()
        settings_shadow.setBlurRadius(15)
        settings_shadow.setColor(QColor(0, 0, 0, 100))
        settings_shadow.setOffset(0, 2)
        settings_button.setGraphicsEffect(settings_shadow)
        settings_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        settings_button.setIconSize(QSize(20, 20))
        settings_button.clicked.connect(self.show_settings)

        # Add help and settings buttons to layout
        help_settings_layout = QHBoxLayout()
        help_settings_layout.setContentsMargins(0, 0, 0, 0)
        help_settings_layout.setSpacing(8)
        help_settings_layout.addStretch()
        help_settings_layout.addWidget(help_button)
        help_settings_layout.addWidget(settings_button)
        main_layout.addLayout(help_settings_layout)

    def show_error(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec()

    def derive_key(self, password: SecurePassword, salt: bytes = None) -> tuple[bytes, bytes]:
        if salt is None:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.get_bytes()))
        return key, salt

    def encrypt_file(self):
        if not self.encrypt_dropbox.file_path or not self.encrypt_password.text() or not self.encrypt_password_confirm.text():
            return
        if self.encrypt_password.text() != self.encrypt_password_confirm.text():
            self.show_error("Passwords do not match.")
            return
        # Validate password strength
        is_valid, error_message = validate_password(self.encrypt_password.text())
        if not is_valid:
            self.show_error(error_message)
            return
        try:
            # Read the file
            with open(self.encrypt_dropbox.file_path, 'rb') as f:
                data = f.read()
            # Create secure password wrapper
            secure_password = SecurePassword(self.encrypt_password.text())
            # Generate key and salt
            key, salt = self.derive_key(secure_password)
            f = Fernet(key)
            # Encrypt the data
            encrypted_data = f.encrypt(data)
            # Create metadata
            preserve_ext = getattr(self, 'extension_preservation_option', "Preserve original extension") == "Preserve original extension"
            metadata = {
                'preserve_extension': preserve_ext,
                'original_extension': self.encrypt_dropbox.original_extension if preserve_ext else None
            }
            metadata_bytes = json.dumps(metadata).encode()
            # Save the encrypted file
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Encrypted File", "", "Encrypted Files (*.enc)"
            )
            if save_path:
                if not save_path.endswith('.enc'):
                    save_path += '.enc'
                with open(save_path, 'wb') as f:
                    f.write(salt + len(metadata_bytes).to_bytes(4, 'big') + metadata_bytes + encrypted_data)
                self.encrypt_dropbox.label.setText("Drop file to encrypt")
                self.encrypt_dropbox.file_path = None
                self.encrypt_dropbox.original_extension = None
                self.encrypt_password.clear()
                self.encrypt_password_confirm.clear()
        except Exception as e:
            self.show_error(f"Encryption error: {str(e)}")
        finally:
            # Ensure secure password is wiped
            if 'secure_password' in locals():
                del secure_password
            gc.collect()

    def decrypt_file(self):
        if not self.decrypt_dropbox.file_path or not self.decrypt_password.text():
            return
            
        # Validate password strength
        is_valid, error_message = validate_password(self.decrypt_password.text())
        if not is_valid:
            self.show_error(error_message)
            return
            
        try:
            # Read the encrypted file
            with open(self.decrypt_dropbox.file_path, 'rb') as f:
                data = f.read()

            # Extract salt, metadata length, metadata, and encrypted data
            salt = data[:16]
            metadata_length = int.from_bytes(data[16:20], 'big')
            metadata = json.loads(data[20:20+metadata_length].decode())
            encrypted_data = data[20+metadata_length:]

            # Create secure password wrapper
            secure_password = SecurePassword(self.decrypt_password.text())
            
            # Generate key
            key, _ = self.derive_key(secure_password, salt)
            f = Fernet(key)

            # Decrypt the data
            decrypted_data = f.decrypt(encrypted_data)

            # Determine file extension
            if metadata.get('preserve_extension', False):
                original_extension = metadata.get('original_extension', '')
                file_filter = f"All Files (*{original_extension})"
            else:
                original_extension = ''
                file_filter = "All Files (*.*)"

            # Save the decrypted file
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Decrypted File", "", file_filter
            )
            if save_path:
                if metadata.get('preserve_extension', False) and not save_path.endswith(original_extension):
                    save_path += original_extension
                with open(save_path, 'wb') as f:
                    f.write(decrypted_data)
                self.decrypt_dropbox.label.setText("Drop file to decrypt")
                self.decrypt_dropbox.file_path = None
                self.decrypt_password.clear()

        except Exception:
            self.show_error("Incorrect password or corrupted file.")
        finally:
            # Ensure secure password is wiped
            if 'secure_password' in locals():
                del secure_password
            gc.collect()

    def show_help(self):
        help_dialog = HelpDialog(self)
        help_dialog.exec()

    def show_settings(self):
        # Show the settings dialog and update extension handling if saved
        current_option = getattr(self, 'extension_preservation_option', "Preserve original extension")
        dlg = SettingsDialog(current_option, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.extension_preservation_option = dlg.get_extension_option()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EntryptorApp()
    window.show()
    sys.exit(app.exec()) 