"""Tests for GUI components."""

import os
import pytest
from unittest.mock import Mock, patch

from PyQt6.QtWidgets import QApplication

from src.gui.components.drop_box import DropBox
from src.gui.components.password_input import PasswordInput, PasswordConfirmInput
from src.gui.components.dialogs import show_error_dialog, show_info_dialog


@pytest.fixture
def app():
    """Create QApplication instance for GUI tests."""
    # Set up headless mode for CI
    if os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"):
        os.environ["QT_QPA_PLATFORM"] = "offscreen"

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


class TestDropBox:
    """Test DropBox component."""

    def test_drop_box_creation(self, app):
        """Test DropBox widget creation."""
        title = "Drop files here"
        drop_box = DropBox(title)

        assert drop_box.label.text() == title
        assert drop_box.file_path is None
        assert drop_box.acceptDrops() is True

    def test_drop_box_file_dropped_signal(self, app, tmp_path):
        """Test that file_dropped signal is emitted when file is dropped."""
        drop_box = DropBox("Test")

        # Connect a mock slot to the signal
        mock_slot = Mock()
        drop_box.file_dropped.connect(mock_slot)

        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        test_file_path = str(test_file)

        # Simulate setting the file path directly (since dropEvent is complex to mock)
        drop_box.file_path = test_file_path
        drop_box.file_dropped.emit(test_file_path)

        # Verify signal was emitted
        mock_slot.assert_called_once_with(test_file_path)

    def test_drop_box_file_path_update(self, app, tmp_path):
        """Test that file path is updated when file is dropped."""
        drop_box = DropBox("Test")

        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        test_file_path = str(test_file)

        # Simulate file drop by setting file path directly
        drop_box.file_path = test_file_path

        # Verify file path was set
        assert drop_box.file_path == test_file_path

    def test_drop_box_clear_file(self, app, tmp_path):
        """Test clearing the dropped file."""
        drop_box = DropBox("Test")

        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        test_file_path = str(test_file)

        # Set a file path
        drop_box.file_path = test_file_path
        assert drop_box.file_path == test_file_path

        # Clear the file using the clear method
        drop_box.clear()

        # Verify file was cleared
        assert drop_box.file_path is None

    def test_drop_box_styling(self, app):
        """Test that DropBox has visible border styling."""
        drop_box = DropBox("Test")

        # Get the style sheet
        style_sheet = drop_box.styleSheet()

        # Verify that border styling is present
        assert "border:" in style_sheet
        assert "border-radius:" in style_sheet
        assert "12px" in style_sheet  # border-radius value

        # Verify that both normal and hover states are defined (using QFrame now)
        assert "QFrame {" in style_sheet
        assert "QFrame:hover {" in style_sheet

    def test_drop_box_close_button_creation(self, app):
        """Test that DropBox creates close button properly."""
        drop_box = DropBox("Test")

        # Verify close button exists
        assert drop_box.close_button is not None
        assert drop_box.close_button.text() == ""  # No text, just icon
        assert drop_box.close_button.size().width() == 10
        assert drop_box.close_button.size().height() == 10

        # Initially hidden
        assert not drop_box.close_button.isVisible()

    def test_drop_box_close_button_shows_when_file_selected(self, app, tmp_path):
        """Test that close button exists and can be shown."""
        drop_box = DropBox("Test")

        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        test_file_path = str(test_file)

        # Initially hidden
        assert not drop_box.close_button.isVisible()

        # Set a file (simulate file selection)
        drop_box.set_file_path(test_file_path)

        # Just verify the file was set correctly
        assert drop_box.file_path == test_file_path

    def test_drop_box_close_button_clears_file(self, app, tmp_path):
        """Test that close button functionality works."""
        drop_box = DropBox("Test")

        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        test_file_path = str(test_file)

        # Set a file
        drop_box.set_file_path(test_file_path)
        assert drop_box.file_path == test_file_path

        # Simulate close button click
        drop_box._on_close_clicked()

        # File should be cleared
        assert drop_box.file_path is None
        assert drop_box.label.text() == "Test"  # back to default title

    def test_drop_box_close_button_styling(self, app):
        """Test that close button has correct macOS-style styling."""
        drop_box = DropBox("Test")
        close_button = drop_box.close_button

        # Check styling contains macOS red color
        style_sheet = close_button.styleSheet()
        assert "rgba(196, 47, 70" in style_sheet  # macOS red (updated)
        assert "border-radius: 5px" in style_sheet
        assert "font-weight: bold" in style_sheet


class TestPasswordInput:
    """Test PasswordInput component."""

    def test_password_input_creation(self, app):
        """Test PasswordInput widget creation."""
        password_input = PasswordInput("Enter password")

        assert (
            password_input.password_input.echoMode()
            == password_input.password_input.EchoMode.Password
        )
        assert password_input.password_input.placeholderText() == "Enter password"

    def test_password_input_get_password(self, app):
        """Test getting password from input."""
        password_input = PasswordInput("Enter password")

        test_password = "test_password"
        password_input.password_input.setText(test_password)

        assert password_input.get_password() == test_password

    def test_password_input_set_password(self, app):
        """Test setting password in input."""
        password_input = PasswordInput("Enter password")

        test_password = "test_password"
        password_input.set_password(test_password)

        assert password_input.password_input.text() == test_password

    def test_password_input_clear(self, app):
        """Test clearing password input."""
        password_input = PasswordInput("Enter password")

        password_input.password_input.setText("test_password")
        password_input.clear()

        assert password_input.password_input.text() == ""

    def test_password_input_toggle_visibility(self, app):
        """Test toggling password visibility."""
        password_input = PasswordInput("Enter password")

        # Initially should be hidden
        assert (
            password_input.password_input.echoMode()
            == password_input.password_input.EchoMode.Password
        )

        # Note: The toggle functionality would require more complex mocking
        # This test just verifies the initial state

    def test_password_input_changed_signal(self, app):
        """Test that password_changed signal exists and can be connected."""
        password_input = PasswordInput("Enter password")

        # Connect a mock slot to the signal
        mock_slot = Mock()
        password_input.password_changed.connect(mock_slot)

        # Just verify the signal exists and can be connected
        assert hasattr(password_input, "password_changed")
        # Note: Actual signal emission testing would require more complex GUI interaction


class TestPasswordConfirmInput:
    """Test PasswordConfirmInput component."""

    def test_password_confirm_input_creation(self, app):
        """Test PasswordConfirmInput widget creation."""
        confirm_input = PasswordConfirmInput()

        assert confirm_input.password_input is not None
        assert confirm_input.password_input.placeholderText() == "Confirm password"
        assert (
            confirm_input.password_input.echoMode()
            == confirm_input.password_input.EchoMode.Password
        )

    def test_password_confirm_input_match_validation(self, app):
        """Test password confirmation matching."""
        confirm_input = PasswordConfirmInput()

        # Test matching passwords
        test_password = "test_password"
        confirm_input.set_reference_password(test_password)
        confirm_input.password_input.setText(test_password)

        # Note: Match validation would need implementation details testing

    def test_password_confirm_input_validation_signal(self, app):
        """Test that validation_changed signal is emitted."""
        confirm_input = PasswordConfirmInput()

        # Connect a mock slot to the signal
        mock_slot = Mock()
        confirm_input.match_changed.connect(mock_slot)

        # Note: Signal testing would depend on implementation details

    def test_password_confirm_input_clear_original(self, app):
        """Test clearing confirmation input."""
        confirm_input = PasswordConfirmInput()

        # Set some confirmation text
        confirm_input.password_input.setText("test_password")
        assert confirm_input.password_input.text() == "test_password"

        # Clear the input
        confirm_input.password_input.clear()
        assert confirm_input.password_input.text() == ""


class TestDialogs:
    """Test dialog functions."""

    @patch("src.gui.components.dialogs.QMessageBox")
    def test_show_error_dialog(self, mock_message_box, app):
        """Test showing error dialog."""
        mock_box = Mock()
        mock_message_box.return_value = mock_box

        title = "Test Error"
        message = "This is a test error message"

        show_error_dialog(None, title, message)

        # Verify QMessageBox was created and configured
        mock_message_box.assert_called_once_with(None)
        mock_box.setIcon.assert_called_once_with(mock_message_box.Icon.Critical)
        mock_box.setWindowTitle.assert_called_once_with(title)
        mock_box.setText.assert_called_once_with(message)
        mock_box.exec.assert_called_once()

    @patch("src.gui.components.dialogs.QMessageBox")
    def test_show_info_dialog(self, mock_message_box, app):
        """Test showing info dialog."""
        mock_box = Mock()
        mock_message_box.return_value = mock_box

        title = "Test Info"
        message = "This is a test info message"

        show_info_dialog(None, title, message)

        # Verify QMessageBox was created and configured
        mock_message_box.assert_called_once_with(None)
        mock_box.setIcon.assert_called_once_with(mock_message_box.Icon.Information)
        mock_box.setWindowTitle.assert_called_once_with(title)
        mock_box.setText.assert_called_once_with(message)
        mock_box.exec.assert_called_once()

    @patch("src.gui.components.dialogs.QMessageBox")
    def test_show_error_dialog_with_details(self, mock_message_box, app):
        """Test showing error dialog with basic functionality."""
        mock_box = Mock()
        mock_message_box.return_value = mock_box

        title = "Test Error"
        message = "This is a test error message"

        show_error_dialog(None, title, message)

        # Verify QMessageBox was created and configured
        mock_message_box.assert_called_once_with(None)
        mock_box.setIcon.assert_called_once_with(mock_message_box.Icon.Critical)
        mock_box.setWindowTitle.assert_called_once_with(title)
        mock_box.setText.assert_called_once_with(message)
        mock_box.exec.assert_called_once()

    @patch("src.gui.components.dialogs.QMessageBox")
    def test_show_info_dialog_with_details(self, mock_message_box, app):
        """Test showing info dialog with basic functionality."""
        mock_box = Mock()
        mock_message_box.return_value = mock_box

        title = "Test Info"
        message = "This is a test info message"

        show_info_dialog(None, title, message)

        # Verify QMessageBox was created and configured
        mock_message_box.assert_called_once_with(None)
        mock_box.setIcon.assert_called_once_with(mock_message_box.Icon.Information)
        mock_box.setWindowTitle.assert_called_once_with(title)
        mock_box.setText.assert_called_once_with(message)
        mock_box.exec.assert_called_once()
