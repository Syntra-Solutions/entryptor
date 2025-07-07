"""Password input widget with validation and visual feedback."""

from typing import Optional, List

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QByteArray
from PyQt6.QtGui import QFont, QColor, QPixmap, QPainter, QIcon
from PyQt6.QtWidgets import QGraphicsOpacityEffect

from ...utils.validation import validate_password, check_password_requirements


class PasswordInput(QWidget):
    """Password input widget with real-time validation and visual feedback."""
    
    password_changed = pyqtSignal(str)
    validation_changed = pyqtSignal(bool)  # True if password is valid
    
    def __init__(self, placeholder: str = "Enter password", show_validation: bool = True, parent: Optional[QWidget] = None) -> None:
        """
        Initialize password input widget.
        
        Args:
            placeholder: Placeholder text for the input
            show_validation: Whether to show validation indicators
            parent: Parent widget
        """
        super().__init__(parent)
        self.placeholder = placeholder
        self.show_validation = show_validation
        self.password_input: Optional[QLineEdit] = None
        self.requirement_labels: List[QLabel] = []
        self.requirement_effects: List[QGraphicsOpacityEffect] = []
        self.requirement_animations: List[QPropertyAnimation] = []
        self._setup_ui()
        if self.show_validation:
            self._setup_validation()
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Main container
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 0.7);
                border: 1px solid rgba(62, 62, 62, 0.5);
                border-radius: 10px;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(0)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(self.placeholder)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(28)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #ffffff;
                font-size: 14px;
                padding: 5px;
            }
            QLineEdit::placeholder {
                color: #888888;
            }
        """)
        
        main_layout.addWidget(self.password_input)
        main_layout.addSpacing(10)
        
        # Separator line (always add for visual consistency)
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Plain)
        separator.setStyleSheet("""
            QFrame {
                background: #444444;
                color: #444444;
                min-height: 1px;
                max-height: 1px;
                border: none;
            }
        """)
        main_layout.addWidget(separator)
        main_layout.addSpacing(15)
        
        # Add validation indicators only if validation is enabled
        if self.show_validation:
            # Requirements row
            requirements_widget = QWidget()
            requirements_widget.setStyleSheet("background: transparent; border: none;")
            requirements_layout = QHBoxLayout(requirements_widget)
            requirements_layout.setContentsMargins(0, 0, 0, 0)
            requirements_layout.setSpacing(6)
            
            # Create requirement indicators
            requirements = [
                ("len", "12"),
                ("up", "A"),
                ("low", "a"),
                ("num", "1"),
                ("spec", "#")
            ]
            
            for req_key, symbol in requirements:
                label = QLabel()
                label.setPixmap(self._create_requirement_icon(False, symbol).pixmap(24, 24))
                label.setFixedSize(24, 24)
                
                # Set up opacity effect for animations
                effect = QGraphicsOpacityEffect()
                effect.setOpacity(0.3)
                label.setGraphicsEffect(effect)
                
                # Create animation
                property_name = QByteArray()
                property_name.append(b"opacity")
                animation = QPropertyAnimation(effect, property_name)
                animation.setDuration(300)
                animation.setEasingCurve(QEasingCurve.Type.OutCubic)
                
                self.requirement_labels.append(label)
                self.requirement_effects.append(effect)
                self.requirement_animations.append(animation)
                
                requirements_layout.addWidget(label)
            
            requirements_layout.addStretch()
            main_layout.addWidget(requirements_widget)
        
        self.setLayout(main_layout)
    
    def _setup_validation(self) -> None:
        """Set up password validation."""
        if self.password_input:
            self.password_input.textChanged.connect(self._on_password_changed)
    
    def _on_password_changed(self, text: str) -> None:
        """Handle password text changes."""
        # Validate password
        validation_result = validate_password(text)
        
        # Update requirement indicators
        requirements = check_password_requirements(text)
        for i, (req_key, is_met) in enumerate(requirements):
            if i < len(self.requirement_labels):
                self._update_requirement_indicator(i, is_met)
        
        # Emit signals
        self.password_changed.emit(text)
        self.validation_changed.emit(validation_result.is_valid)
    
    def _update_requirement_indicator(self, index: int, is_met: bool) -> None:
        """Update a requirement indicator."""
        if index >= len(self.requirement_effects) or index >= len(self.requirement_animations):
            return
        
        effect = self.requirement_effects[index]
        animation = self.requirement_animations[index]
        
        # Set target opacity
        target_opacity = 1.0 if is_met else 0.3
        
        # Animate opacity change
        animation.setStartValue(effect.opacity())
        animation.setEndValue(target_opacity)
        animation.start()
        
        # Update icon color
        if index < len(self.requirement_labels):
            label = self.requirement_labels[index]
            # Get symbol from current pixmap or use default
            symbols = ["12", "A", "a", "1", "#"]
            symbol = symbols[index] if index < len(symbols) else "?"
            label.setPixmap(self._create_requirement_icon(is_met, symbol).pixmap(24, 24))
    
    def _create_requirement_icon(self, met: bool, symbol: str) -> QIcon:
        """Create a requirement indicator icon."""
        # Create a 24x24 pixmap
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        # Set up painter
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Colors
        if met:
            border_color = QColor("#28a745")  # Green
            text_color = QColor("#28a745")
        else:
            border_color = QColor(128, 128, 128)  # Gray
            text_color = QColor(128, 128, 128)
        
        # Draw circle (centered in 24x24, with 2px margin)
        circle_x, circle_y, circle_size = 2, 2, 20
        painter.setPen(border_color)
        painter.setBrush(QColor(0, 0, 0, 0))  # Transparent fill
        painter.drawEllipse(circle_x, circle_y, circle_size, circle_size)
        
        # Draw text centered within the circle bounds (not the pixmap)
        painter.setPen(text_color)
        font = QFont("Arial", 10, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Calculate text position to center within circle
        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(symbol)
        
        # Center within the circle area
        circle_center_x = circle_x + circle_size // 2
        circle_center_y = circle_y + circle_size // 2
        text_x = circle_center_x - text_width // 2
        text_y = circle_center_y + metrics.ascent() // 2 - metrics.descent() // 2
        
        painter.drawText(text_x, text_y, symbol)
        painter.end()
        
        return QIcon(pixmap)
    
    def get_password(self) -> str:
        """
        Get the current password.
        
        Returns:
            Current password text
        """
        return self.password_input.text() if self.password_input else ""
    
    def set_password(self, password: str) -> None:
        """
        Set the password text.
        
        Args:
            password: Password to set
        """
        if self.password_input:
            self.password_input.setText(password)
    
    def clear(self) -> None:
        """Clear the password input."""
        if self.password_input:
            self.password_input.clear()
    
    def is_valid(self) -> bool:
        """
        Check if current password is valid.
        
        Returns:
            True if password meets all requirements
        """
        return validate_password(self.get_password()).is_valid
    
    def set_placeholder(self, placeholder: str) -> None:
        """
        Set placeholder text.
        
        Args:
            placeholder: New placeholder text
        """
        self.placeholder = placeholder
        if self.password_input:
            self.password_input.setPlaceholderText(placeholder)


class PasswordConfirmInput(QWidget):
    """Password confirmation input widget."""
    
    password_changed = pyqtSignal(str)
    match_changed = pyqtSignal(bool)  # True if passwords match
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initialize password confirmation input."""
        super().__init__(parent)
        self.password_input: Optional[QLineEdit] = None
        self.match_indicator: Optional[QLabel] = None
        self.match_effect: Optional[QGraphicsOpacityEffect] = None
        self.reference_password = ""
        self._setup_ui()
        self._setup_validation()
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Main container
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 0.7);
                border: 1px solid rgba(62, 62, 62, 0.5);
                border-radius: 10px;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(0)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Confirm password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(28)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #ffffff;
                font-size: 14px;
                padding: 5px;
            }
            QLineEdit::placeholder {
                color: #888888;
            }
        """)
        
        main_layout.addWidget(self.password_input)
        main_layout.addSpacing(10)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Plain)
        separator.setStyleSheet("""
            QFrame {
                background: #444444;
                color: #444444;
                min-height: 1px;
                max-height: 1px;
                border: none;
            }
        """)
        main_layout.addWidget(separator)
        main_layout.addSpacing(15)
        
        # Match indicator
        indicator_widget = QWidget()
        indicator_widget.setStyleSheet("background: transparent; border: none;")
        indicator_layout = QHBoxLayout(indicator_widget)
        indicator_layout.setContentsMargins(0, 0, 0, 0)
        indicator_layout.setSpacing(6)
        
        self.match_indicator = QLabel()
        self.match_indicator.setPixmap(self._create_match_icon(False).pixmap(24, 24))
        self.match_indicator.setFixedSize(24, 24)
        
        # Set up opacity effect
        self.match_effect = QGraphicsOpacityEffect()
        self.match_effect.setOpacity(0.3)
        self.match_indicator.setGraphicsEffect(self.match_effect)
        
        indicator_layout.addWidget(self.match_indicator)
        indicator_layout.addStretch()
        main_layout.addWidget(indicator_widget)
        
        self.setLayout(main_layout)
    
    def _setup_validation(self) -> None:
        """Set up password validation."""
        if self.password_input:
            self.password_input.textChanged.connect(self._on_password_changed)
    
    def _on_password_changed(self, text: str) -> None:
        """Handle password text changes."""
        passwords_match = text == self.reference_password and len(text) > 0
        
        # Update match indicator
        self._update_match_indicator(passwords_match)
        
        # Emit signals
        self.password_changed.emit(text)
        self.match_changed.emit(passwords_match)
    
    def _update_match_indicator(self, matches: bool) -> None:
        """Update the match indicator."""
        if self.match_indicator and self.match_effect:
            # Update opacity
            self.match_effect.setOpacity(1.0 if matches else 0.3)
            
            # Update icon
            self.match_indicator.setPixmap(self._create_match_icon(matches).pixmap(24, 24))
    
    def _create_match_icon(self, matches: bool) -> QIcon:
        """Create a match indicator icon."""
        # Create a 24x24 pixmap
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        # Set up painter
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Colors
        if matches:
            border_color = QColor("#28a745")  # Green
            text_color = QColor("#28a745")
        else:
            border_color = QColor(128, 128, 128)  # Gray
            text_color = QColor(128, 128, 128)
        
        # Draw circle (centered in 24x24, with 2px margin)
        circle_x, circle_y, circle_size = 2, 2, 20
        painter.setPen(border_color)
        painter.setBrush(QColor(0, 0, 0, 0))  # Transparent fill
        painter.drawEllipse(circle_x, circle_y, circle_size, circle_size)
        
        # Draw checkmark centered within the circle bounds
        painter.setPen(text_color)
        font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(font)
        
        symbol = "✓"
        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(symbol)
        
        # Center within the circle area
        circle_center_x = circle_x + circle_size // 2
        circle_center_y = circle_y + circle_size // 2
        text_x = circle_center_x - text_width // 2
        text_y = circle_center_y + metrics.ascent() // 2 - metrics.descent() // 2
        
        painter.drawText(text_x, text_y, symbol)
        painter.end()
        
        return QIcon(pixmap)
    
    def set_reference_password(self, password: str) -> None:
        """
        Set the reference password to compare against.
        
        Args:
            password: Reference password
        """
        self.reference_password = password
        # Re-validate current input
        if self.password_input:
            self._on_password_changed(self.password_input.text())
    
    def get_password(self) -> str:
        """
        Get the current password.
        
        Returns:
            Current password text
        """
        return self.password_input.text() if self.password_input else ""
    
    def clear(self) -> None:
        """Clear the password input."""
        if self.password_input:
            self.password_input.clear()
    
    def passwords_match(self) -> bool:
        """
        Check if passwords match.
        
        Returns:
            True if passwords match
        """
        current = self.get_password()
        return current == self.reference_password and len(current) > 0
