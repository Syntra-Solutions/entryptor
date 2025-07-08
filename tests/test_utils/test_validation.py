"""Tests for validation utilities."""

from src.utils.validation import (
    validate_password,
    calculate_password_strength,
    get_password_requirements,
    check_password_requirements,
)


class TestPasswordValidation:
    """Test password validation functions."""

    def test_validate_password_strong_password(self):
        """Test validation of strong password."""
        strong_password = "MyStr0ngP@ssw0rd!"

        result = validate_password(strong_password)
        assert result.is_valid is True
        assert result.error_message == ""
        assert result.strength_score > 0

    def test_validate_password_empty_password(self):
        """Test validation of empty password."""
        result = validate_password("")
        assert result.is_valid is False
        assert "Password cannot be empty" in result.error_message
        assert result.strength_score == 0

    def test_validate_password_too_short(self):
        """Test validation of too short password."""
        result = validate_password("Short1!")
        assert result.is_valid is False
        assert "Password must be at least 12 characters long" in result.error_message

    def test_validate_password_no_uppercase(self):
        """Test validation of password without uppercase."""
        result = validate_password("mylongpassword123!")
        assert result.is_valid is False
        assert (
            "Password must contain at least one uppercase letter"
            in result.error_message
        )

    def test_validate_password_no_lowercase(self):
        """Test validation of password without lowercase."""
        result = validate_password("MYLONGPASSWORD123!")
        assert result.is_valid is False
        assert (
            "Password must contain at least one lowercase letter"
            in result.error_message
        )

    def test_validate_password_no_digit(self):
        """Test validation of password without digit."""
        result = validate_password("MyLongPassword!!")
        assert result.is_valid is False
        assert "Password must contain at least one number" in result.error_message

    def test_validate_password_no_special_char(self):
        """Test validation of password without special character."""
        result = validate_password("MyLongPassword123")
        assert result.is_valid is False
        assert (
            "Password must contain at least one special character"
            in result.error_message
        )

    def test_validate_password_minimal_valid(self):
        """Test validation of minimal valid password."""
        minimal_password = "MyPassword1!"

        result = validate_password(minimal_password)
        assert result.is_valid is True
        assert result.error_message == ""

    def test_validate_password_unicode_characters(self):
        """Test validation of password with unicode characters."""
        unicode_password = "MyStr0ng🔒Pässw0rd!"

        result = validate_password(unicode_password)
        assert result.is_valid is True
        assert result.error_message == ""

    def test_validate_password_long_password(self):
        """Test validation of very long password."""
        long_password = "A" * 50 + "a" * 50 + "1" + "!"

        result = validate_password(long_password)
        assert result.is_valid is True
        assert result.error_message == ""

    def test_calculate_password_strength_weak(self):
        """Test password strength calculation for weak password."""
        weak_password = "password"

        strength = calculate_password_strength(weak_password)
        assert 0 <= strength <= 100
        assert strength < 50  # Should be low for weak password

    def test_calculate_password_strength_strong(self):
        """Test password strength calculation for strong password."""
        strong_password = "MyStr0ngP@ssw0rd!"

        strength = calculate_password_strength(strong_password)
        assert 0 <= strength <= 100
        assert strength > 70  # Should be high for strong password

    def test_calculate_password_strength_empty(self):
        """Test password strength calculation for empty password."""
        strength = calculate_password_strength("")
        assert strength == 0

    def test_get_password_requirements(self):
        """Test getting password requirements."""
        requirements = get_password_requirements()

        assert isinstance(requirements, list)
        assert len(requirements) > 0

        # Check that all requirements are tuples with description and example
        for req in requirements:
            assert isinstance(req, tuple)
            assert len(req) == 2
            assert isinstance(req[0], str)  # Description
            assert isinstance(req[1], str)  # Example

    def test_check_password_requirements_all_met(self):
        """Test checking requirements for password that meets all."""
        strong_password = "MyStr0ngP@ssw0rd!"

        results = check_password_requirements(strong_password)

        assert isinstance(results, list)
        assert len(results) > 0

        # All requirements should be met
        for desc, met in results:
            assert isinstance(desc, str)
            assert isinstance(met, bool)
            assert met is True

    def test_check_password_requirements_some_not_met(self):
        """Test checking requirements for password that doesn't meet all."""
        weak_password = "password"

        results = check_password_requirements(weak_password)

        assert isinstance(results, list)
        assert len(results) > 0

        # Some requirements should not be met
        met_count = sum(1 for _, met in results if met)
        total_count = len(results)
        assert met_count < total_count

    def test_check_password_requirements_empty_password(self):
        """Test checking requirements for empty password."""
        results = check_password_requirements("")

        assert isinstance(results, list)
        assert len(results) > 0

        # Most requirements should not be met for empty password
        met_count = sum(1 for _, met in results if met)
        assert met_count == 0  # No requirements should be met for empty password
