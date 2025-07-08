"""Main application window for Entryptor."""

from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QDialog
)
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

from .components.drop_box import DropBox
from .components.password_input import PasswordInput, PasswordConfirmInput
from .components.dialogs import SettingsDialog, HelpDialog, show_error_dialog, show_info_dialog
from ..crypto.encryption import (
    encrypt_file_with_password, encrypt_file_with_keyfile,
    decrypt_file_with_password, decrypt_file_with_keyfile
)
from ..crypto.secure_memory import SecurePassword
from ..config.models import EncryptionMode, ExtensionOption
from ..config.constants import APP_NAME, VERSION
from ..config.settings import load_settings, save_settings
from ..utils.resources import get_icon_path


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        
        # Application state - load from settings
        self.current_settings = load_settings()
        
        # File paths
        self.encrypt_file_path: Optional[str] = None
        self.decrypt_file_path: Optional[str] = None
        self.keyfile_path: Optional[str] = None
        self.decrypt_keyfile_path: Optional[str] = None
        
        # GUI components
        self.encrypt_dropbox: Optional[DropBox] = None
        self.decrypt_dropbox: Optional[DropBox] = None
        self.keyfile_dropbox: Optional[DropBox] = None
        self.decrypt_keyfile_dropbox: Optional[DropBox] = None
        
        self.password_input: Optional[PasswordInput] = None
        self.password_confirm: Optional[PasswordConfirmInput] = None
        self.decrypt_password_input: Optional[PasswordInput] = None
        
        self.encrypt_button: Optional[QPushButton] = None
        self.decrypt_button: Optional[QPushButton] = None
        
        self._setup_ui()
        self._connect_signals()
        
        # Apply initial settings to UI
        self._update_ui_for_mode()
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Window properties
        self.setWindowTitle(f"{APP_NAME} v{VERSION}")
        self.setMinimumSize(900, 600)
        
        # Main styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QPushButton {
                padding: 12px 24px;
                background-color: #007AFF;
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)
        
        # Content layout (horizontal split)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(40)
        
        # Left side - Encryption
        left_layout = self._create_encryption_section()
        content_layout.addLayout(left_layout, 1)
        
        # Right side - Decryption  
        right_layout = self._create_decryption_section()
        content_layout.addLayout(right_layout, 1)
        
        main_layout.addLayout(content_layout)
        
        # Bottom buttons
        bottom_layout = self._create_bottom_section()
        main_layout.addLayout(bottom_layout)
    
    def _create_encryption_section(self) -> QVBoxLayout:
        """Create the encryption section UI."""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Encrypt Files")
        title.setFixedHeight(40)
        title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
                padding-top: 5px;
            }
        """)
        layout.addWidget(title)
        
        # File drop box
        self.encrypt_dropbox = DropBox("Drag file here to encrypt")
        layout.addWidget(self.encrypt_dropbox)
        
        # Keyfile drop box (initially hidden)
        self.keyfile_dropbox = DropBox("Drag keyfile here")
        self.keyfile_dropbox.setVisible(False)
        layout.addWidget(self.keyfile_dropbox)
        
        # Password inputs (initially visible)
        self.password_input = PasswordInput("Enter encryption password")
        layout.addWidget(self.password_input)
        
        self.password_confirm = PasswordConfirmInput()
        layout.addWidget(self.password_confirm)
        
        # Encrypt button
        self.encrypt_button = QPushButton("Encrypt File")
        self.encrypt_button.setEnabled(False)
        self.encrypt_button.setMinimumHeight(45)
        self.encrypt_button.setMaximumHeight(45)
        layout.addWidget(self.encrypt_button)
        
        return layout
    
    def _create_decryption_section(self) -> QVBoxLayout:
        """Create the decryption section UI."""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Decrypt Files")
        title.setFixedHeight(40)
        title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
                padding-top: 5px;
            }
        """)
        layout.addWidget(title)
        
        # File drop box
        self.decrypt_dropbox = DropBox("Drag encrypted file here")
        layout.addWidget(self.decrypt_dropbox)
        
        # Keyfile drop box (initially hidden)
        self.decrypt_keyfile_dropbox = DropBox("Drag keyfile here")
        self.decrypt_keyfile_dropbox.setVisible(False)
        layout.addWidget(self.decrypt_keyfile_dropbox)
        
        # Password input (initially visible) - no validation for decryption
        self.decrypt_password_input = PasswordInput("Enter decryption password", show_validation=False)
        layout.addWidget(self.decrypt_password_input)
        
        # Decrypt button
        self.decrypt_button = QPushButton("Decrypt File")
        self.decrypt_button.setEnabled(False)
        self.decrypt_button.setMinimumHeight(45)
        self.decrypt_button.setMaximumHeight(45)
        layout.addWidget(self.decrypt_button)
        
        return layout
    
    def _create_bottom_section(self) -> QHBoxLayout:
        """Create the bottom button section."""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 20, 0, 0)
        
        # Left spacer
        layout.addStretch()
        
        # Help button
        help_button = QPushButton("?")
        help_button.setFixedSize(28, 28)
        help_button.setStyleSheet("""
            QPushButton {
                border-radius: 14px;
                font-size: 14px;
                font-weight: bold;
                background-color: #555555;
                color: white;
                text-align: center;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)
        
        # Add shadow to help button
        help_shadow = QGraphicsDropShadowEffect()
        help_shadow.setBlurRadius(6)
        help_shadow.setColor(QColor(0, 0, 0, 100))
        help_shadow.setOffset(0, 1)
        help_button.setGraphicsEffect(help_shadow)
        
        layout.addWidget(help_button)
        layout.addSpacing(4)
        
        # Settings button
        settings_button = QPushButton()
        settings_button.setFixedSize(28, 28)
        settings_button.setStyleSheet(help_button.styleSheet())
        
        # Try to load gear icon
        gear_icon_path = get_icon_path("gear.png")
        if gear_icon_path:
            settings_button.setIcon(QIcon(gear_icon_path))
            settings_button.setIconSize(QSize(14, 14))
        else:
            settings_button.setText("⚙")
        
        # Add shadow to settings button
        settings_shadow = QGraphicsDropShadowEffect()
        settings_shadow.setBlurRadius(6)
        settings_shadow.setColor(QColor(0, 0, 0, 100))
        settings_shadow.setOffset(0, 1)
        settings_button.setGraphicsEffect(settings_shadow)
        
        layout.addWidget(settings_button)
        
        # Store button references for signal connection
        self.help_button = help_button
        self.settings_button = settings_button
        
        return layout
    
    def _connect_signals(self) -> None:
        """Connect widget signals to their handlers."""
        # File drop signals
        if self.encrypt_dropbox:
            self.encrypt_dropbox.file_dropped.connect(self._on_encrypt_file_dropped)
        if self.decrypt_dropbox:
            self.decrypt_dropbox.file_dropped.connect(self._on_decrypt_file_dropped)
        if self.keyfile_dropbox:
            self.keyfile_dropbox.file_dropped.connect(self._on_keyfile_dropped)
        if self.decrypt_keyfile_dropbox:
            self.decrypt_keyfile_dropbox.file_dropped.connect(self._on_decrypt_keyfile_dropped)
        
        # Password signals
        if self.password_input:
            self.password_input.password_changed.connect(self._on_encrypt_password_changed)
            self.password_input.validation_changed.connect(self._update_encrypt_button_state)
        
        if self.password_confirm:
            self.password_confirm.password_changed.connect(self._on_confirm_password_changed)
            self.password_confirm.match_changed.connect(self._update_encrypt_button_state)
        
        if self.decrypt_password_input:
            self.decrypt_password_input.password_changed.connect(self._update_decrypt_button_state)
        
        # Button signals
        if self.encrypt_button:
            self.encrypt_button.clicked.connect(self._on_encrypt_clicked)
        if self.decrypt_button:
            self.decrypt_button.clicked.connect(self._on_decrypt_clicked)
        
        # Menu button signals
        if hasattr(self, 'help_button'):
            self.help_button.clicked.connect(self._show_help)
        if hasattr(self, 'settings_button'):
            self.settings_button.clicked.connect(self._show_settings)
    
    def _on_encrypt_file_dropped(self, file_path: str) -> None:
        """Handle file dropped for encryption."""
        self.encrypt_file_path = file_path
        self._update_encrypt_button_state()
    
    def _on_decrypt_file_dropped(self, file_path: str) -> None:
        """Handle file dropped for decryption."""
        self.decrypt_file_path = file_path
        self._update_decrypt_button_state()
    
    def _on_keyfile_dropped(self, file_path: str) -> None:
        """Handle keyfile dropped for encryption."""
        self.keyfile_path = file_path
        self._update_encrypt_button_state()
    
    def _on_decrypt_keyfile_dropped(self, file_path: str) -> None:
        """Handle keyfile dropped for decryption."""
        self.decrypt_keyfile_path = file_path
        self._update_decrypt_button_state()
    
    def _on_encrypt_password_changed(self, password: str) -> None:
        """Handle encryption password change."""
        if self.password_confirm:
            self.password_confirm.set_reference_password(password)
        self._update_encrypt_button_state()
    
    def _on_confirm_password_changed(self, password: str) -> None:
        """Handle confirmation password change."""
        self._update_encrypt_button_state()
    
    def _update_encrypt_button_state(self) -> None:
        """Update the encrypt button enabled state."""
        if not self.encrypt_button:
            return
        
        # Check if file is selected
        has_file = self.encrypt_file_path is not None
        
        if self.current_settings.encryption_mode == EncryptionMode.PASSWORD:
            # Password mode: need valid password and confirmation
            password_valid = bool(self.password_input and self.password_input.is_valid())
            passwords_match = bool(self.password_confirm and self.password_confirm.passwords_match())
            has_valid_password = password_valid and passwords_match
            can_encrypt = has_file and has_valid_password
        else:
            # Keyfile mode: need keyfile
            has_keyfile = self.keyfile_path is not None
            can_encrypt = has_file and has_keyfile
        
        self.encrypt_button.setEnabled(can_encrypt)
    
    def _update_decrypt_button_state(self) -> None:
        """Update the decrypt button enabled state."""
        if not self.decrypt_button:
            return
        
        # Check if file is selected
        has_file = self.decrypt_file_path is not None
        
        if self.current_settings.encryption_mode == EncryptionMode.PASSWORD:
            # Password mode: need password
            password_length = len(self.decrypt_password_input.get_password()) if self.decrypt_password_input else 0
            has_password = password_length > 0
            can_decrypt = has_file and has_password
        else:
            # Keyfile mode: need keyfile
            has_keyfile = self.decrypt_keyfile_path is not None
            can_decrypt = has_file and has_keyfile
        
        self.decrypt_button.setEnabled(can_decrypt)
    
    def _on_encrypt_clicked(self) -> None:
        """Handle encrypt button click."""
        if not self.encrypt_file_path:
            show_error_dialog(self, "Error", "Please select a file to encrypt.")
            return
        
        try:
            if self.current_settings.encryption_mode == EncryptionMode.PASSWORD:
                self._encrypt_with_password()
            else:
                self._encrypt_with_keyfile()
        except Exception as e:
            show_error_dialog(self, "Encryption Error", f"Failed to encrypt file: {str(e)}")
    
    def _encrypt_with_password(self) -> None:
        """Encrypt file using password."""
        if not self.password_input or not self.encrypt_file_path:
            return
        
        password_text = self.password_input.get_password()
        preserve_extension = self.current_settings.extension_option == ExtensionOption.PRESERVE
        
        with SecurePassword(password_text) as secure_password:
            result = encrypt_file_with_password(
                self.encrypt_file_path,
                secure_password,
                preserve_extension=preserve_extension
            )
        
        if result.success:
            show_info_dialog(self, "Success", f"File encrypted successfully:\\n{result.output_path}")
            self._reset_encryption_form()
        else:
            show_error_dialog(self, "Encryption Error", result.error_message or "Unknown error")
    
    def _encrypt_with_keyfile(self) -> None:
        """Encrypt file using keyfile."""
        if not self.keyfile_path or not self.encrypt_file_path:
            return
        
        preserve_extension = self.current_settings.extension_option == ExtensionOption.PRESERVE
        
        result = encrypt_file_with_keyfile(
            self.encrypt_file_path,
            self.keyfile_path,
            preserve_extension=preserve_extension
        )
        
        if result.success:
            show_info_dialog(self, "Success", f"File encrypted successfully:\\n{result.output_path}")
            self._reset_encryption_form()
        else:
            show_error_dialog(self, "Encryption Error", result.error_message or "Unknown error")
    
    def _on_decrypt_clicked(self) -> None:
        """Handle decrypt button click."""
        if not self.decrypt_file_path:
            show_error_dialog(self, "Error", "Please select a file to decrypt.")
            return
        
        try:
            if self.current_settings.encryption_mode == EncryptionMode.PASSWORD:
                self._decrypt_with_password()
            else:
                self._decrypt_with_keyfile()
        except Exception as e:
            show_error_dialog(self, "Decryption Error", f"Failed to decrypt file: {str(e)}")
    
    def _decrypt_with_password(self) -> None:
        """Decrypt file using password."""
        if not self.decrypt_password_input or not self.decrypt_file_path:
            return
        
        password_text = self.decrypt_password_input.get_password()
        
        with SecurePassword(password_text) as secure_password:
            result = decrypt_file_with_password(
                self.decrypt_file_path,
                secure_password
            )
        
        if result.success:
            show_info_dialog(self, "Success", f"File decrypted successfully:\\n{result.output_path}")
            self._reset_decryption_form()
        else:
            show_error_dialog(self, "Decryption Error", result.error_message or "Unknown error")
    
    def _decrypt_with_keyfile(self) -> None:
        """Decrypt file using keyfile."""
        if not self.decrypt_keyfile_path or not self.decrypt_file_path:
            return
        
        result = decrypt_file_with_keyfile(
            self.decrypt_file_path,
            self.decrypt_keyfile_path
        )
        
        if result.success:
            show_info_dialog(self, "Success", f"File decrypted successfully:\\n{result.output_path}")
            self._reset_decryption_form()
        else:
            show_error_dialog(self, "Decryption Error", result.error_message or "Unknown error")
    
    def _reset_encryption_form(self) -> None:
        """Reset the encryption form."""
        self.encrypt_file_path = None
        self.keyfile_path = None
        
        if self.encrypt_dropbox:
            self.encrypt_dropbox.clear()
        if self.keyfile_dropbox:
            self.keyfile_dropbox.clear()
        if self.password_input:
            self.password_input.clear()
        if self.password_confirm:
            self.password_confirm.clear()
        
        self._update_encrypt_button_state()
    
    def _reset_decryption_form(self) -> None:
        """Reset the decryption form."""
        self.decrypt_file_path = None
        self.decrypt_keyfile_path = None
        
        if self.decrypt_dropbox:
            self.decrypt_dropbox.clear()
        if self.decrypt_keyfile_dropbox:
            self.decrypt_keyfile_dropbox.clear()
        if self.decrypt_password_input:
            self.decrypt_password_input.clear()
        
        self._update_decrypt_button_state()
    
    def _show_settings(self) -> None:
        """Show the settings dialog."""
        current_extension = (
            "Preserve original extension" 
            if self.current_settings.extension_option == ExtensionOption.PRESERVE 
            else "Manual extension selection"
        )
        use_keyfile = self.current_settings.encryption_mode == EncryptionMode.KEYFILE
        
        dialog = SettingsDialog(current_extension, use_keyfile, self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Update settings
            self.current_settings.encryption_mode = dialog.get_encryption_mode()
            self.current_settings.extension_option = dialog.get_extension_option_enum()
            
            # Save settings
            save_settings(self.current_settings)
            
            # Update UI based on new settings
            self._update_ui_for_mode()
    
    def _update_ui_for_mode(self) -> None:
        """Update UI elements based on current encryption mode."""
        is_keyfile_mode = self.current_settings.encryption_mode == EncryptionMode.KEYFILE
        
        # Show/hide appropriate elements
        if self.keyfile_dropbox:
            self.keyfile_dropbox.setVisible(is_keyfile_mode)
        if self.decrypt_keyfile_dropbox:
            self.decrypt_keyfile_dropbox.setVisible(is_keyfile_mode)
        
        if self.password_input:
            self.password_input.setVisible(not is_keyfile_mode)
        if self.password_confirm:
            self.password_confirm.setVisible(not is_keyfile_mode)
        if self.decrypt_password_input:
            self.decrypt_password_input.setVisible(not is_keyfile_mode)
        
        # Update button states
        self._update_encrypt_button_state()
        self._update_decrypt_button_state()
        
        # Clear forms when switching modes
        self._reset_encryption_form()
        self._reset_decryption_form()
    
    def _show_help(self) -> None:
        """Show the help dialog."""
        dialog = HelpDialog(self)
        dialog.exec()
