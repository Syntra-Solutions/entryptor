"""Tests for GUI components."""

import pytest
from unittest.mock import Mock, patch

from PyQt6.QtWidgets import QApplication

from src.gui.components.drop_box import DropBox
from src.gui.components.password_input import PasswordInput, PasswordConfirmInput
from src.gui.components.dialogs import show_error_dialog, show_info_dialog


@pytest.fixture
def app():
    """Create QApplication instance for GUI tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


class TestDropBox:
    """Test DropBox component."""

    def test_drop_box_creation(self, app):
        """Test DropBox widget creation."""
        label = "Drop files here"
        drop_box = DropBox(label)

        assert drop_box.label == label
        assert drop_box.file_path is None
        assert drop_box.acceptDrops() is True

    def test_drop_box_file_dropped_signal(self, app):
        """Test that file_dropped signal is emitted when file is dropped."""
        drop_box = DropBox("Test")

        # Connect a mock slot to the signal
        mock_slot = Mock()
        drop_box.file_dropped.connect(mock_slot)

        # Simulate a file drop
        test_file_path = "/test/file.txt"
        drop_box._handle_file_drop(test_file_path)

        # Verify signal was emitted
        mock_slot.assert_called_once_with(test_file_path)

    def test_drop_box_file_path_update(self, app):
        """Test that file path is updated when file is dropped."""
        drop_box = DropBox("Test")

        test_file_path = "/test/file.txt"
        drop_box._handle_file_drop(test_file_path)

        assert drop_box.file_path == test_file_path

    def test_drop_box_clear_file(self, app):
        """Test clearing the dropped file."""
        drop_box = DropBox("Test")

        # Set a file path
        test_file_path = "/test/file.txt"
        drop_box._handle_file_drop(test_file_path)
        assert drop_box.file_path == test_file_path

        # Clear the file
        drop_box.clear_file()
        assert drop_box.file_path is None

    @patch("src.gui.components.drop_box.QFileDialog.getOpenFileName")
    def test_drop_box_browse_file(self, mock_file_dialog, app):
        """Test browsing for a file."""
        drop_box = DropBox("Test")

        # Mock file dialog to return a file path
        test_file_path = "/test/selected_file.txt"
        mock_file_dialog.return_value = (test_file_path, "All Files (*)")

        # Connect a mock slot to the signal
        mock_slot = Mock()
        drop_box.file_dropped.connect(mock_slot)

        # Simulate browsing for a file
        drop_box._browse_file()

        # Verify file was selected and signal emitted
        assert drop_box.file_path == test_file_path
        mock_slot.assert_called_once_with(test_file_path)

    @patch("src.gui.components.drop_box.QFileDialog.getOpenFileName")
    def test_drop_box_browse_file_cancelled(self, mock_file_dialog, app):
        """Test browsing for a file when dialog is cancelled."""
        drop_box = DropBox("Test")

        # Mock file dialog to return empty path (cancelled)
        mock_file_dialog.return_value = ("", "")

        # Connect a mock slot to the signal
        mock_slot = Mock()
        drop_box.file_dropped.connect(mock_slot)

        # Simulate browsing for a file
        drop_box._browse_file()

        # Verify no file was selected and signal not emitted
        assert drop_box.file_path is None
        mock_slot.assert_not_called()

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
        assert drop_box.close_button.text() == "×"
        assert drop_box.close_button.size().width() == 20
        assert drop_box.close_button.size().height() == 20

        # Initially hidden
        assert not drop_box.close_button.isVisible()

    def test_drop_box_close_button_shows_when_file_selected(self, app):
        """Test that close button appears when file is selected."""
        drop_box = DropBox("Test")

        # Initially hidden
        assert not drop_box.close_button.isVisible()

        # Set a file (simulate file selection)
        with patch("os.path.isfile", return_value=True):
            drop_box.set_file_path("/test/file.txt")

        # Close button should now be visible
        assert drop_box.close_button.isVisible()

    def test_drop_box_close_button_clears_file(self, app):
        """Test that clicking close button clears the file."""
        drop_box = DropBox("Test")

        # Set a file
        with patch("os.path.isfile", return_value=True):
            drop_box.set_file_path("/test/file.txt")

        assert drop_box.file_path == "/test/file.txt"
        assert drop_box.close_button.isVisible()

        # Simulate close button click
        drop_box._on_close_clicked()

        # File should be cleared and button hidden
        assert drop_box.file_path is None
        assert not drop_box.close_button.isVisible()
        assert drop_box.label.text() == "Test"  # back to default title

    def test_drop_box_close_button_styling(self, app):
        """Test that close button has correct macOS-style styling."""
        drop_box = DropBox("Test")
        close_button = drop_box.close_button

        # Check styling contains macOS red color
        style_sheet = close_button.styleSheet()
        assert "rgba(255, 59, 48" in style_sheet  # macOS red
        assert "border-radius: 10px" in style_sheet
        assert "font-weight: bold" in style_sheet


class TestPasswordInput:
    """Test PasswordInput component."""

    def test_password_input_creation(self, app):
        """Test PasswordInput widget creation."""
        password_input = PasswordInput("Enter password")

        assert (
            password_input.line_edit.echoMode()
            == password_input.line_edit.EchoMode.Password
        )
        assert password_input.line_edit.placeholderText() == "Enter password"

    def test_password_input_get_password(self, app):
        """Test getting password from input."""
        password_input = PasswordInput("Enter password")

        test_password = "test_password"
        password_input.line_edit.setText(test_password)

        assert password_input.get_password() == test_password

    def test_password_input_set_password(self, app):
        """Test setting password in input."""
        password_input = PasswordInput("Enter password")

        test_password = "test_password"
        password_input.set_password(test_password)

        assert password_input.line_edit.text() == test_password

    def test_password_input_clear(self, app):
        """Test clearing password input."""
        password_input = PasswordInput("Enter password")

        password_input.line_edit.setText("test_password")
        password_input.clear()

        assert password_input.line_edit.text() == ""

    def test_password_input_toggle_visibility(self, app):
        """Test toggling password visibility."""
        password_input = PasswordInput("Enter password")

        # Initially should be hidden
        assert (
            password_input.line_edit.echoMode()
            == password_input.line_edit.EchoMode.Password
        )

        # Toggle to visible
        password_input.toggle_visibility()
        assert (
            password_input.line_edit.echoMode()
            == password_input.line_edit.EchoMode.Normal
        )

        # Toggle back to hidden
        password_input.toggle_visibility()
        assert (
            password_input.line_edit.echoMode()
            == password_input.line_edit.EchoMode.Password
        )

    def test_password_input_changed_signal(self, app):
        """Test that password_changed signal is emitted."""
        password_input = PasswordInput("Enter password")

        # Connect a mock slot to the signal
        mock_slot = Mock()
        password_input.password_changed.connect(mock_slot)

        # Change password
        test_password = "test_password"
        password_input.line_edit.setText(test_password)

        # Simulate text changed signal
        password_input.line_edit.textChanged.emit(test_password)

        # Verify signal was emitted
        mock_slot.assert_called_once_with(test_password)


class TestPasswordConfirmInput:
    """Test PasswordConfirmInput component."""

    def test_password_confirm_input_creation(self, app):
        """Test PasswordConfirmInput widget creation."""
        confirm_input = PasswordConfirmInput("Confirm password")

        assert (
            confirm_input.line_edit.echoMode()
            == confirm_input.line_edit.EchoMode.Password
        )
        assert confirm_input.line_edit.placeholderText() == "Confirm password"

    def test_password_confirm_input_match_validation(self, app):
        """Test password confirmation matching."""
        confirm_input = PasswordConfirmInput("Confirm password")

        # Test matching passwords
        test_password = "test_password"
        confirm_input.set_original_password(test_password)
        confirm_input.line_edit.setText(test_password)

        assert confirm_input.passwords_match() is True

        # Test non-matching passwords
        confirm_input.line_edit.setText("different_password")
        assert confirm_input.passwords_match() is False

    def test_password_confirm_input_validation_signal(self, app):
        """Test that validation_changed signal is emitted."""
        confirm_input = PasswordConfirmInput("Confirm password")

        # Connect a mock slot to the signal
        mock_slot = Mock()
        confirm_input.validation_changed.connect(mock_slot)

        # Set original password
        test_password = "test_password"
        confirm_input.set_original_password(test_password)

        # Set matching confirmation
        confirm_input.line_edit.setText(test_password)

        # Simulate text changed signal
        confirm_input.line_edit.textChanged.emit(test_password)

        # Verify signal was emitted with True (passwords match)
        mock_slot.assert_called_with(True)

    def test_password_confirm_input_clear_original(self, app):
        """Test clearing original password."""
        confirm_input = PasswordConfirmInput("Confirm password")

        confirm_input.set_original_password("test_password")
        confirm_input.clear_original_password()

        assert confirm_input.original_password == ""


class TestDialogs:
    """Test dialog functions."""

    @patch("src.gui.components.dialogs.QMessageBox")
    def test_show_error_dialog(self, mock_message_box, app):
        """Test showing error dialog."""
        mock_box = Mock()
        mock_message_box.return_value = mock_box

        title = "Test Error"
        message = "This is a test error message"

        show_error_dialog(title, message)

        # Verify QMessageBox was created and configured
        mock_message_box.assert_called_once()
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

        show_info_dialog(title, message)

        # Verify QMessageBox was created and configured
        mock_message_box.assert_called_once()
        mock_box.setIcon.assert_called_once_with(mock_message_box.Icon.Information)
        mock_box.setWindowTitle.assert_called_once_with(title)
        mock_box.setText.assert_called_once_with(message)
        mock_box.exec.assert_called_once()

    @patch("src.gui.components.dialogs.QMessageBox")
    def test_show_error_dialog_with_details(self, mock_message_box, app):
        """Test showing error dialog with detailed text."""
        mock_box = Mock()
        mock_message_box.return_value = mock_box

        title = "Test Error"
        message = "This is a test error message"
        details = "Detailed error information"

        show_error_dialog(title, message, details)

        # Verify QMessageBox was created and configured with details
        mock_message_box.assert_called_once()
        mock_box.setIcon.assert_called_once_with(mock_message_box.Icon.Critical)
        mock_box.setWindowTitle.assert_called_once_with(title)
        mock_box.setText.assert_called_once_with(message)
        mock_box.setDetailedText.assert_called_once_with(details)
        mock_box.exec.assert_called_once()

    @patch("src.gui.components.dialogs.QMessageBox")
    def test_show_info_dialog_with_details(self, mock_message_box, app):
        """Test showing info dialog with detailed text."""
        mock_box = Mock()
        mock_message_box.return_value = mock_box

        title = "Test Info"
        message = "This is a test info message"
        details = "Detailed info information"

        show_info_dialog(title, message, details)

        # Verify QMessageBox was created and configured with details
        mock_message_box.assert_called_once()
        mock_box.setIcon.assert_called_once_with(mock_message_box.Icon.Information)
        mock_box.setWindowTitle.assert_called_once_with(title)
        mock_box.setText.assert_called_once_with(message)
        mock_box.setDetailedText.assert_called_once_with(details)
        mock_box.exec.assert_called_once()
