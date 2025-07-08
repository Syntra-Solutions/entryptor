"""Drag and drop widget for file selection."""

import os
from typing import Optional

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QColor, QFont
from PyQt6.QtWidgets import QGraphicsDropShadowEffect


class DropBox(QFrame):
    """Custom widget for drag-and-drop file selection."""

    file_dropped = pyqtSignal(str)

    def __init__(self, title: str, parent: Optional[QWidget] = None) -> None:
        """
        Initialize drop box widget.

        Args:
            title: Display title for the drop box
            parent: Parent widget
        """
        super().__init__(parent)
        self.file_path: Optional[str] = None
        self.original_extension: Optional[str] = None
        self.default_title = title
        self.close_button: Optional[QPushButton] = None
        self._setup_ui(title)
        self._setup_drag_drop()

    def _setup_ui(self, title: str) -> None:
        """Set up the user interface."""
        self.setAcceptDrops(True)
        self.setMinimumSize(300, 200)

        # Use QFrame built-in styling for borders
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setMidLineWidth(0)

        # Set up subtle, minimalistic styling
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(45, 45, 45, 0.8);
                border: 1px solid rgba(120, 120, 120, 0.6);
                border-radius: 12px;
                margin: 1px;
            }
            QFrame:hover {
                border: 2px solid rgba(150, 150, 150, 0.8);
                background-color: rgba(55, 55, 55, 0.9);
                border-radius: 12px;
            }
        """)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Create label
        self.label = QLabel(title)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)

        # Set label styling
        font = QFont()
        font.setPointSize(14)
        font.setWeight(QFont.Weight.Normal)
        self.label.setFont(font)

        self.label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                background: transparent;
                border: none;
                padding: 10px;
            }
        """)

        layout.addWidget(self.label)
        self.setLayout(layout)

        # Create close button (hidden initially)
        self._setup_close_button()

    def _setup_drag_drop(self) -> None:
        """Set up drag and drop functionality."""
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: Optional[QDragEnterEvent]) -> None:
        """Handle drag enter events."""
        if event is None:
            return

        mime_data = event.mimeData()
        if mime_data is None:
            event.ignore()
            return

        if mime_data.hasUrls():
            # Check if any of the URLs are files
            for url in mime_data.urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if os.path.isfile(file_path):
                        event.acceptProposedAction()
                        return

        event.ignore()

    def dropEvent(self, event: Optional[QDropEvent]) -> None:
        """Handle drop events."""
        if event is None:
            return

        mime_data = event.mimeData()
        if mime_data is None:
            return

        if not mime_data.hasUrls():
            return

        # Get the first file from the dropped URLs
        for url in mime_data.urls():
            if url.isLocalFile():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path):
                    self.file_path = file_path
                    self.original_extension = os.path.splitext(file_path)[1]

                    # Update label to show filename
                    filename = os.path.basename(file_path)
                    self.label.setText(filename)

                    # Show close button when file is selected
                    if self.close_button:
                        self.close_button.show()

                    # Emit signal
                    self.file_dropped.emit(file_path)
                    break

    def set_file_path(self, file_path: str) -> None:
        """
        Set file path programmatically.

        Args:
            file_path: Path to the file
        """
        if os.path.isfile(file_path):
            self.file_path = file_path
            self.original_extension = os.path.splitext(file_path)[1]
            filename = os.path.basename(file_path)
            self.label.setText(filename)

            # Show close button when file is set
            if self.close_button:
                self.close_button.show()

    def set_file_name(self, file_name: str) -> None:
        """
        Set display filename.

        Args:
            file_name: Name to display
        """
        self.label.setText(file_name)

    def clear(self) -> None:
        """Clear the current file selection."""
        self.file_path = None
        self.original_extension = None
        # Reset label text to default title
        self.label.setText(self.default_title)

        # Hide close button when file is cleared
        if self.close_button:
            self.close_button.hide()

    def get_file_path(self) -> Optional[str]:
        """
        Get the current file path.

        Returns:
            Current file path or None if no file selected
        """
        return self.file_path

    def get_original_extension(self) -> Optional[str]:
        """
        Get the original file extension.

        Returns:
            Original file extension or None if no file selected
        """
        return self.original_extension

    def has_file(self) -> bool:
        """
        Check if a file is currently selected.

        Returns:
            True if file is selected, False otherwise
        """
        return self.file_path is not None and os.path.isfile(self.file_path)

    def _setup_close_button(self) -> None:
        """Set up the close button for file deselection."""
        self.close_button = QPushButton("")
        self.close_button.setParent(self)
        self.close_button.setFixedSize(10, 10)

        # macOS-style close button styling
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(196, 47, 70, 0.9);
                border: none;
                border-radius: 5px;
                color: white;
                font-size: 12px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgba(227, 20, 52, 1.0);
            }
            QPushButton:pressed {
                background-color: rgba(143, 13, 33, 1.0);
            }
        """)

        # Position in top-left corner
        self.close_button.move(8, 8)

        # Connect click signal
        self.close_button.clicked.connect(self._on_close_clicked)

        # Initially hidden
        self.close_button.hide()

    def _on_close_clicked(self) -> None:
        """Handle close button click to deselect file."""
        self.clear()
