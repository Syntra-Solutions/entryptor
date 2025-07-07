"""Application settings management."""

import json
import os
from typing import Optional

from .models import AppSettings, EncryptionMode, ExtensionOption
from ..utils.resources import get_settings_file_path
from ..utils.file_utils import ensure_directory_exists


class SettingsManager:
    """Manager for application settings persistence."""
    
    def __init__(self) -> None:
        """Initialize settings manager."""
        self.settings_file = get_settings_file_path()
        self._default_settings = AppSettings(
            encryption_mode=EncryptionMode.PASSWORD,
            extension_option=ExtensionOption.PRESERVE
        )
    
    def load_settings(self) -> AppSettings:
        """
        Load settings from file.
        
        Returns:
            AppSettings instance with loaded or default values
        """
        if not os.path.exists(self.settings_file):
            return self._default_settings
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parse settings with validation
            encryption_mode = EncryptionMode(data.get('encryption_mode', 'password'))
            extension_option = ExtensionOption(data.get('extension_option', 'preserve'))
            
            return AppSettings(
                encryption_mode=encryption_mode,
                extension_option=extension_option
            )
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # If settings file is corrupted, use defaults
            print(f"Warning: Failed to load settings: {e}. Using defaults.")
            return self._default_settings
    
    def save_settings(self, settings: AppSettings) -> bool:
        """
        Save settings to file.
        
        Args:
            settings: AppSettings instance to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure settings directory exists
            settings_dir = os.path.dirname(self.settings_file)
            if not ensure_directory_exists(settings_dir):
                return False
            
            # Convert to dictionary
            data = {
                'encryption_mode': settings.encryption_mode.value,
                'extension_option': settings.extension_option.value
            }
            
            # Write to file
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Warning: Failed to save settings: {e}")
            return False
    
    def reset_to_defaults(self) -> AppSettings:
        """
        Reset settings to defaults and save.
        
        Returns:
            Default AppSettings instance
        """
        self.save_settings(self._default_settings)
        return self._default_settings
    
    def get_default_settings(self) -> AppSettings:
        """
        Get default settings without loading from file.
        
        Returns:
            Default AppSettings instance
        """
        return AppSettings(
            encryption_mode=self._default_settings.encryption_mode,
            extension_option=self._default_settings.extension_option
        )


# Global settings manager instance
_settings_manager: Optional[SettingsManager] = None


def get_settings_manager() -> SettingsManager:
    """
    Get the global settings manager instance.
    
    Returns:
        SettingsManager instance
    """
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager


def load_settings() -> AppSettings:
    """
    Load application settings.
    
    Returns:
        Current application settings
    """
    return get_settings_manager().load_settings()


def save_settings(settings: AppSettings) -> bool:
    """
    Save application settings.
    
    Args:
        settings: Settings to save
        
    Returns:
        True if successful, False otherwise
    """
    return get_settings_manager().save_settings(settings)


def reset_settings() -> AppSettings:
    """
    Reset settings to defaults.
    
    Returns:
        Default settings
    """
    return get_settings_manager().reset_to_defaults()
