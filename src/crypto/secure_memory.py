"""Secure memory handling for sensitive data."""

import gc
import weakref
from typing import Optional


class SecurePassword:
    """Wrapper class for secure password handling with memory cleanup."""

    def __init__(self, password: str) -> None:
        """
        Initialize secure password wrapper.

        Args:
            password: The password string to secure
        """
        self._password: Optional[bytes] = password.encode("utf-8")
        # Register for cleanup tracking
        self._cleanup_ref = weakref.ref(self, self._cleanup)

    def get_bytes(self) -> bytes:
        """
        Get password as bytes.

        Returns:
            Password bytes

        Raises:
            RuntimeError: If password has been cleared
        """
        if self._password is None:
            raise RuntimeError("Password has been cleared from memory")
        return self._password

    def clear(self) -> None:
        """Manually clear password from memory."""
        if self._password is not None:
            # Overwrite with zeros
            self._password = b"\x00" * len(self._password)
            self._password = None

    def __del__(self) -> None:
        """Cleanup when object is deleted."""
        self.clear()
        gc.collect()

    @staticmethod
    def _cleanup(weak_ref: weakref.ref) -> None:
        """Static cleanup method for weakref callback."""
        gc.collect()

    def __enter__(self) -> "SecurePassword":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with cleanup."""
        self.clear()


class SecureBytes:
    """Wrapper for secure handling of byte data."""

    def __init__(self, data: bytes) -> None:
        """
        Initialize secure bytes wrapper.

        Args:
            data: The bytes to secure
        """
        self._data: Optional[bytes] = data
        self._cleanup_ref = weakref.ref(self, self._cleanup)

    def get_bytes(self) -> bytes:
        """
        Get the secure bytes.

        Returns:
            The secured bytes

        Raises:
            RuntimeError: If data has been cleared
        """
        if self._data is None:
            raise RuntimeError("Secure data has been cleared from memory")
        return self._data

    def clear(self) -> None:
        """Manually clear data from memory."""
        if self._data is not None:
            # Overwrite with zeros
            self._data = b"\x00" * len(self._data)
            self._data = None

    def __del__(self) -> None:
        """Cleanup when object is deleted."""
        self.clear()
        gc.collect()

    @staticmethod
    def _cleanup(weak_ref: weakref.ref) -> None:
        """Static cleanup method for weakref callback."""
        gc.collect()

    def __enter__(self) -> "SecureBytes":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with cleanup."""
        self.clear()
