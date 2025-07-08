"""Main application entry point for Entryptor."""

import sys
import os

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from .gui.main_window import MainWindow
from .config.constants import APP_NAME
from .utils.resources import get_icon_path


def setup_application() -> QApplication:
    """
    Set up the QApplication with proper configuration.
    
    Returns:
        Configured QApplication instance
    """
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("Syntra for Business Solutions")
    
    # Set application icon if available
    icon_path = get_icon_path("entryptor.icns")
    if not icon_path:
        icon_path = get_icon_path("entryptor.svg")
    if not icon_path:
        icon_path = get_icon_path("entryptor.png")
    
    if icon_path and os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Set application style
    app.setStyle("Fusion")  # Use Fusion style for better cross-platform consistency
    
    return app


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    """
    Handle uncaught exceptions by showing an error dialog.
    
    Args:
        exc_type: Exception type
        exc_value: Exception value
        exc_traceback: Exception traceback
    """
    if issubclass(exc_type, KeyboardInterrupt):
        # Handle Ctrl+C gracefully
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    # Create a simple error dialog
    app = QApplication.instance()
    if app:
        error_msg = f"An unexpected error occurred:\\n\\n{exc_type.__name__}: {exc_value}"
        
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Unexpected Error")
        msg_box.setText("An unexpected error occurred.")
        msg_box.setDetailedText(error_msg)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
    
    # Call the default handler
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


def main() -> int:
    """
    Main application entry point.
    
    Returns:
        Application exit code
    """
    try:
        # Set up exception handling
        sys.excepthook = handle_exception
        
        # Create application
        app = setup_application()
        
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        # Center the window on screen
        screen = app.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            window_geometry = main_window.frameGeometry()
            center_point = screen_geometry.center()
            window_geometry.moveCenter(center_point)
            main_window.move(window_geometry.topLeft())
        
        # Start event loop
        return app.exec()
        
    except Exception as e:
        # Fallback error handling if GUI fails to start
        print(f"Failed to start application: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
