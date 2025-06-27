import sys
import os
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog,
                            QGraphicsDropShadowEffect, QMessageBox, QComboBox, QCheckBox,
                            QTextBrowser, QDialog, QFrame, QGraphicsOpacityEffect,
                            QDialogButtonBox)  # Add this
from PyQt6.QtCore import Qt, QMimeData, QPointF, QUrl, QSize, QPropertyAnimation, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QColor, QIcon, QFont, QPixmap, QPainter
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
VERSION = "1.0.0-beta"
COPYRIGHT_YEAR = "2025"
COMPANY_NAME = "Syntra for Business Solutions"

# Gear icon helper function
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # Running as bundled exe
        return os.path.join(sys._MEIPASS, relative_path)
    # Running as script
    return os.path.join(os.path.abspath('.'), relative_path)

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
    file_dropped = pyqtSignal(str)

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumSize(300, 200)
        self.setStyleSheet("""
            background-color: rgba(30, 30, 30, 0.7);
            border: 1px solid rgba(62, 62, 62, 0.5);
            border-radius: 10px;
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
            self.file_dropped.emit(self.file_path)

    def set_file_name(self, file_name):
        self.label.setText(file_name)

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
    def __init__(self, current_option, use_keyfile=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Extension combo
        self.extension_combo = QComboBox()
        self.extension_combo.addItems([
            "Preserve original extension",
            "Manual extension selection"
        ])
        self.extension_combo.setCurrentText(current_option)
        
        # Keyfile toggle
        self.keyfile_toggle = QCheckBox("Use Keyfile instead of password")
        self.keyfile_toggle.setChecked(use_keyfile)
        
        # Layout
        ext_layout = QHBoxLayout()
        ext_layout.addWidget(QLabel("File Extension:"))
        ext_layout.addWidget(self.extension_combo)
        layout.addLayout(ext_layout)
        layout.addWidget(self.keyfile_toggle)
        
        # Connect toggle
        self.keyfile_toggle.toggled.connect(self._on_keyfile_toggled)
        self._on_keyfile_toggled(use_keyfile)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)

    def _on_keyfile_toggled(self, checked):
        self.extension_combo.setEnabled(not checked)
        if checked:
            self.extension_combo.setCurrentText("Manual extension selection")
        self.extension_combo.setStyleSheet("QComboBox:disabled { color: gray; }")
        self.extension_combo.setToolTip(
            "Extension preservation is not available in keyfile mode" if checked else ""
        )

    def get_extension_option(self):
        return self.extension_combo.currentText()

    def get_keyfile_option(self):
        return self.keyfile_toggle.isChecked()

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

        self.use_keyfile = False
        self.keyfile_dropbox = None
        self.decrypt_keyfile_dropbox = None
        self.keyfile_path = None
        self.decrypt_keyfile_path = None

        # Add to __init__
        self.file_path = None
        self.decrypt_file_path = None

        # Add default setting
        self.extension_preservation_option = "Preserve original extension"

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
        
        # --- Password requirements icons ---
        def make_circle_icon(met, symbol, opacity=0.5):
            pixmap = QPixmap(24, 24)
            pixmap.fill(QColor(0, 0, 0, 0))
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            border_color = QColor("#218838") if met else QColor(128, 128, 128, int(255*opacity))
            text_color = QColor("#218838") if met else QColor(128, 128, 128, int(255*opacity))
            painter.setPen(border_color)
            painter.setBrush(QColor(0, 0, 0, 0))  # Transparent fill
            painter.drawEllipse(2, 2, 20, 20)
            painter.setPen(text_color)
            font = QFont("Helvetica Neue", 11, QFont.Weight.Normal)
            if not font.exactMatch():
                font = QFont("Arial", 11, QFont.Weight.Normal)
            painter.setFont(font)
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(symbol)
            text_height = metrics.height()
            x = (pixmap.width() - text_width) // 2
            y = (pixmap.height() + text_height) // 2 - metrics.descent()
            painter.drawText(x, y, symbol)
            painter.end()
            return QIcon(pixmap)

        # --- Password input container with icons inside ---
        # Encryption password container
        pw_container = QWidget()
        pw_container.setStyleSheet("""
            background-color: rgba(30, 30, 30, 0.7);
            border: 1px solid rgba(62, 62, 62, 0.5);
            border-radius: 10px;
        """)
        pw_vlayout = QVBoxLayout(pw_container)
        pw_vlayout.setContentsMargins(12, 8, 12, 8)
        pw_vlayout.setSpacing(0)
        self.encrypt_password.setMinimumHeight(28)
        self.encrypt_password.setStyleSheet("background: transparent; border: none;")
        pw_vlayout.addWidget(self.encrypt_password)
        pw_vlayout.addSpacing(10)
        pw_line = QFrame()
        pw_line.setFrameShape(QFrame.Shape.HLine)
        pw_line.setFrameShadow(QFrame.Shadow.Plain)
        pw_line.setStyleSheet("background: #444; color: #444; min-height: 1px; max-height: 1px; border: none;")
        pw_vlayout.addWidget(pw_line)
        pw_vlayout.addSpacing(15)
        pw_icon_row = QWidget()
        pw_icon_row.setStyleSheet("background: transparent; border: none;")
        pw_icon_layout = QHBoxLayout(pw_icon_row)
        pw_icon_layout.setContentsMargins(0, 0, 0, 0)
        pw_icon_layout.setSpacing(6)
        self.pw_icon_labels = []
        pw_reqs = [("len", "12"), ("up", "A"), ("low", "a"), ("num", "1"), ("spec", "#")]
        for key, symbol in pw_reqs:
            label = QLabel()
            label.setPixmap(make_circle_icon(False, symbol).pixmap(24,24))
            self.pw_icon_labels.append(label)
            pw_icon_layout.addWidget(label)
        pw_icon_layout.addStretch()
        pw_vlayout.addWidget(pw_icon_row)

        # Confirmation password container
        confirm_container = QWidget()
        confirm_container.setStyleSheet("""
            background-color: rgba(30, 30, 30, 0.7);
            border: 1px solid rgba(62, 62, 62, 0.5);
            border-radius: 10px;
        """)
        confirm_vlayout = QVBoxLayout(confirm_container)
        confirm_vlayout.setContentsMargins(12, 8, 12, 8)
        confirm_vlayout.setSpacing(0)
        self.encrypt_password_confirm.setMinimumHeight(28)
        self.encrypt_password_confirm.setStyleSheet("background: transparent; border: none;")
        confirm_vlayout.addWidget(self.encrypt_password_confirm)
        confirm_vlayout.addSpacing(10)
        confirm_line = QFrame()
        confirm_line.setFrameShape(QFrame.Shape.HLine)
        confirm_line.setFrameShadow(QFrame.Shadow.Plain)
        confirm_line.setStyleSheet("background: #444; color: #444; min-height: 1px; max-height: 1px; border: none;")
        confirm_vlayout.addWidget(confirm_line)
        confirm_vlayout.addSpacing(15)
        confirm_icon_row = QWidget()
        confirm_icon_row.setStyleSheet("background: transparent; border: none;")
        confirm_icon_layout = QHBoxLayout(confirm_icon_row)
        confirm_icon_layout.setContentsMargins(0, 0, 0, 0)
        confirm_icon_layout.setSpacing(6)
        self.pw_confirm_icon = QLabel()
        self.pw_confirm_icon.setPixmap(make_circle_icon(False, "✓").pixmap(24,24))
        confirm_icon_layout.addWidget(self.pw_confirm_icon)
        confirm_icon_layout.addStretch()
        confirm_vlayout.addWidget(confirm_icon_row)

        # Add widgets to left_layout with correct stretch
        left_layout.addWidget(self.encrypt_dropbox, 1)
        left_layout.addWidget(pw_container, 0)
        left_layout.addWidget(confirm_container, 0)
        left_layout.addWidget(self.encrypt_button, 0)

        # Set up opacity effects and store animations for password icons
        self.pw_icon_effects = []
        self.pw_icon_animations = []
        for label in self.pw_icon_labels:
            effect = QGraphicsOpacityEffect()
            label.setGraphicsEffect(effect)
            effect.setOpacity(0.5)
            self.pw_icon_effects.append(effect)
            self.pw_icon_animations.append(None)

        # Set up opacity effect for confirmation icon
        self.pw_confirm_effect = QGraphicsOpacityEffect()
        self.pw_confirm_icon.setGraphicsEffect(self.pw_confirm_effect)
        self.pw_confirm_effect.setOpacity(0.5)
        self.pw_confirm_animation = None

        # Live update icons as user types, with fade animation
        def update_pw_icons():
            pw = self.encrypt_password.text()
            checks = [
                len(pw) >= 12,
                any(c.isupper() for c in pw),
                any(c.islower() for c in pw),
                any(c.isdigit() for c in pw),
                any(c in '!@#$%^&*(),.?":{}|<>' for c in pw)
            ]
            for i, ok in enumerate(checks):
                symbol = pw_reqs[i][1]
                self.pw_icon_labels[i].setPixmap(make_circle_icon(ok, symbol, 0.5 if not ok else 1.0).pixmap(24,24))
                # Animate opacity
                target_opacity = 1.0 if ok else 0.5
                effect = self.pw_icon_effects[i]
                if effect.opacity() != target_opacity:
                    anim = QPropertyAnimation(effect, b'opacity')
                    anim.setDuration(200)
                    anim.setStartValue(effect.opacity())
                    anim.setEndValue(target_opacity)
                    anim.start()
                    self.pw_icon_animations[i] = anim  # Store to prevent GC
        self.encrypt_password.textChanged.connect(update_pw_icons)

        def update_confirm_icon():
            pw = self.encrypt_password.text()
            confirm = self.encrypt_password_confirm.text()
            ok = pw and (pw == confirm)
            self.pw_confirm_icon.setPixmap(make_circle_icon(ok, "✓", 0.5 if not ok else 1.0).pixmap(24,24))
            # Animate opacity
            target_opacity = 1.0 if ok else 0.5
            effect = self.pw_confirm_effect
            if effect.opacity() != target_opacity:
                anim = QPropertyAnimation(effect, b'opacity')
                anim.setDuration(200)
                anim.setStartValue(effect.opacity())
                anim.setEndValue(target_opacity)
                anim.start()
                self.pw_confirm_animation = anim  # Store to prevent GC
        self.encrypt_password.textChanged.connect(update_confirm_icon)
        self.encrypt_password_confirm.textChanged.connect(update_confirm_icon)

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

        # Create keyfile dropboxes (initially hidden)
        self.keyfile_dropbox = DropBox("Drop keyfile here")
        self.decrypt_keyfile_dropbox = DropBox("Drop keyfile here")
        self.keyfile_dropbox.hide()
        self.decrypt_keyfile_dropbox.hide()

        # Add keyfile dropboxes to layouts after password fields
        left_layout.addWidget(self.keyfile_dropbox)
        right_layout.addWidget(self.decrypt_keyfile_dropbox)

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
                qproperty-alignment: 'AlignCenter';
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
        help_button.setStyleSheet(help_button.styleSheet())
        help_button.setContentsMargins(0, 0, 0, 0)
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
        gear_icon = resource_path('gear.png')
        settings_button.setIcon(QIcon(gear_icon))
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

        # Connect keyfile drop signals
        self.keyfile_dropbox.file_dropped.connect(self.handle_keyfile_drop)
        self.decrypt_keyfile_dropbox.file_dropped.connect(self.handle_decrypt_keyfile_drop)

        # Add to setup_ui
        self.encrypt_dropbox.file_dropped.connect(self.handle_file_drop)
        self.decrypt_dropbox.file_dropped.connect(self.handle_decrypt_drop)

    def handle_file_drop(self, file_path):
        # For encryption file
        self.file_path = file_path
        self.encrypt_dropbox.set_file_name(os.path.basename(file_path))

    def handle_decrypt_drop(self, file_path):
        # For decryption file
        self.decrypt_file_path = file_path
        self.decrypt_dropbox.set_file_name(os.path.basename(file_path))

    def handle_keyfile_drop(self, file_path):
        self.keyfile_path = file_path
        self.keyfile_dropbox.set_file_name(os.path.basename(file_path))

    def handle_decrypt_keyfile_drop(self, file_path):
        self.decrypt_keyfile_path = file_path
        self.decrypt_keyfile_dropbox.set_file_name(os.path.basename(file_path))

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

    def create_metadata(self, original_path, preserve_extension):
        """Create metadata for encrypted file"""
        return {
            "original_extension": os.path.splitext(original_path)[1] if preserve_extension else "",
            "keyfile_mode": True
        }

    def get_save_path(self, source_path, is_encryption=True, metadata=None):
        if is_encryption:
            if self.use_keyfile:
                suggested_name = os.path.splitext(source_path)[0] + '.enf'
                file_filter = "Encrypted Files (*.enf)"
            else:
                suggested_name = source_path + '.encrypted'
                file_filter = "Encrypted Files (*.encrypted)"
        else:
            # Decryption
            base_name = os.path.splitext(source_path)[0]
            if metadata and metadata.get("preserve_extension", False):
                original_extension = metadata.get("original_extension", "")
                suggested_name = base_name + original_extension
                file_filter = f"Original File (*{original_extension})"
            else:
                suggested_name = base_name
                file_filter = "All Files (*.*)"

        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save File",
            suggested_name,
            file_filter
        )

        # Force extension preservation if enabled
        if file_path and not is_encryption and metadata and metadata.get("preserve_extension", False):
            original_extension = metadata.get("original_extension", "")
            if original_extension and not file_path.endswith(original_extension):
                file_path += original_extension

        return file_path

    def encrypt_file(self):
        if self.use_keyfile:
            if not self.file_path or not self.keyfile_path:
                QMessageBox.warning(self, "Error", "Please select both a file and a keyfile")
                return
            try:
                # Debug print
                print(f"Original file: {self.file_path}")
                print(f"Extension preservation: {self.extension_preservation_option}")
                
                # Create metadata
                metadata = {
                    "original_extension": os.path.splitext(self.file_path)[1] if self.extension_preservation_option == "Preserve original extension" else "",
                    "keyfile_mode": True,
                    "preserve_extension": self.extension_preservation_option == "Preserve original extension"
                }
                
                # Debug print
                print(f"Metadata: {metadata}")
                
                # Get save location
                save_path = self.get_save_path(self.file_path, is_encryption=True)
                if not save_path:
                    return

                # Read keyfile and encrypt
                with open(self.keyfile_path, 'rb') as kf:
                    key_data = kf.read()
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'fixed_salt',
                    iterations=100000,
                    backend=default_backend()
                )
                key = base64.urlsafe_b64encode(kdf.derive(key_data))
                fernet = Fernet(key)

                # Read file content
                with open(self.file_path, 'rb') as f:
                    file_data = f.read()
                
                # Encode file data as base64
                encoded_content = base64.b64encode(file_data).decode('utf-8')
                
                # Combine metadata and encoded content
                combined_data = {
                    'metadata': metadata,
                    'content': encoded_content
                }
                
                # Encrypt combined data
                encrypted_data = fernet.encrypt(json.dumps(combined_data).encode())
                
                with open(save_path, 'wb') as f:
                    f.write(encrypted_data)
                
                QMessageBox.information(self, "Success", "File encrypted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Encryption failed: {str(e)}")
        else:
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
                metadata = {
                    'preserve_extension': self.extension_preservation_option == "Preserve original extension",
                    'original_extension': os.path.splitext(self.encrypt_dropbox.file_path)[1] if self.extension_preservation_option == "Preserve original extension" else ""
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
        if self.use_keyfile:
            if not self.decrypt_file_path or not self.decrypt_keyfile_path:
                QMessageBox.warning(self, "Error", "Please select both encrypted file and keyfile")
                return
            try:
                print(f"Decrypting file: {self.decrypt_file_path}")
                print(f"Extension preservation setting: {self.extension_preservation_option}")
                
                with open(self.decrypt_keyfile_path, 'rb') as kf:
                    key_data = kf.read()
                
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'fixed_salt',
                    iterations=100000,
                    backend=default_backend()
                )
                key = base64.urlsafe_b64encode(kdf.derive(key_data))
                fernet = Fernet(key)

                with open(self.decrypt_file_path, 'rb') as f:
                    encrypted_data = f.read()
                
                decrypted_json = fernet.decrypt(encrypted_data).decode('utf-8')
                decrypted_data = json.loads(decrypted_json)
                metadata = decrypted_data['metadata']
                print(f"Decrypted metadata: {metadata}")
                
                content = base64.b64decode(decrypted_data['content'])

                # Ensure extension preservation
                base_name = os.path.splitext(self.decrypt_file_path)[0].replace('.enf', '')
                original_extension = metadata.get("original_extension", "")
                preserve_extension = metadata.get("preserve_extension", False)
                
                print(f"Base name: {base_name}")
                print(f"Original extension: {original_extension}")
                print(f"Preserve extension: {preserve_extension}")

                if preserve_extension and original_extension:
                    suggested_name = base_name + original_extension
                    file_filter = f"Original File (*{original_extension})"
                else:
                    suggested_name = base_name
                    file_filter = "All Files (*.*)"

                save_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save Decrypted File",
                    suggested_name,
                    file_filter
                )

                if save_path:
                    # Force extension preservation
                    if preserve_extension and original_extension:
                        if not save_path.endswith(original_extension):
                            save_path = save_path + original_extension
                    
                    print(f"Final save path: {save_path}")
                    
                    with open(save_path, 'wb') as f:
                        f.write(content)
                    
                    QMessageBox.information(self, "Success", "File decrypted successfully!")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Decryption failed: {str(e)}")
        else:
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
        dlg = SettingsDialog(self.extension_preservation_option, self.use_keyfile, self)
        result = dlg.exec()  # Use exec() instead of exec_()
        if result == QDialog.DialogCode.Accepted:
            self.extension_preservation_option = dlg.get_extension_option()
            self.use_keyfile = dlg.get_keyfile_option()
            self.toggle_keyfile_mode()

    def toggle_keyfile_mode(self):
        if self.use_keyfile:
            # Hide password fields
            self.encrypt_password.hide()
            self.encrypt_password_confirm.hide()
            self.decrypt_password.hide()
            # Show keyfile dropboxes
            self.keyfile_dropbox.show()
            self.decrypt_keyfile_dropbox.show()
        else:
            # Show password fields
            self.encrypt_password.show()
            self.encrypt_password_confirm.show()
            self.decrypt_password.show()
            # Hide keyfile dropboxes
            self.keyfile_dropbox.hide()
            self.decrypt_keyfile_dropbox.hide()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main View")
        self.setGeometry(100, 100, 800, 600)

        # Set main view background color
        self.background_color = "#f0f0f0"
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.background_color};
            }}
        """)

        # Open settings window
        settings_button = QPushButton("Open Settings")
        settings_button.clicked.connect(self.open_settings)
        layout = QVBoxLayout()
        layout.addWidget(settings_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.exec()


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 400, 300)

        # Hardcode the background color to match the main view
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0; /* Same as Main View */
            }
        """)

        # Example layout and content
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings"))
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EntryptorApp()
    window.show()
    sys.exit(app.exec())