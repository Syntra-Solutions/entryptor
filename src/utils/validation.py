"""Password validation utilities."""

import re
from typing import List, Tuple

from ..config.models import ValidationResult


def validate_password(password: str) -> ValidationResult:
    """
    Validate password strength and return detailed results.

    Args:
        password: Password to validate

    Returns:
        ValidationResult with validation status and details
    """
    if not password:
        return ValidationResult(
            is_valid=False, error_message="Password cannot be empty", strength_score=0
        )

    # Check individual requirements
    requirements = [
        (len(password) >= 12, "Password must be at least 12 characters long"),
        (
            re.search(r"[A-Z]", password) is not None,
            "Password must contain at least one uppercase letter",
        ),
        (
            re.search(r"[a-z]", password) is not None,
            "Password must contain at least one lowercase letter",
        ),
        (
            re.search(r"\d", password) is not None,
            "Password must contain at least one number",
        ),
        (
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is not None,
            "Password must contain at least one special character",
        ),
    ]

    # Find first failed requirement
    for requirement_met, error_message in requirements:
        if not requirement_met:
            return ValidationResult(
                is_valid=False,
                error_message=error_message,
                strength_score=calculate_password_strength(password),
            )

    return ValidationResult(
        is_valid=True,
        error_message="",
        strength_score=calculate_password_strength(password),
    )


def calculate_password_strength(password: str) -> int:
    """
    Calculate password strength score (0-100).

    Args:
        password: Password to evaluate

    Returns:
        Strength score from 0-100
    """
    if not password:
        return 0

    score = 0

    # Length score (up to 40 points)
    if len(password) >= 12:
        score += 20
    if len(password) >= 16:
        score += 10
    if len(password) >= 20:
        score += 10

    # Character diversity (up to 40 points)
    if re.search(r"[A-Z]", password):
        score += 10
    if re.search(r"[a-z]", password):
        score += 10
    if re.search(r"\d", password):
        score += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 10

    # Additional complexity (up to 20 points)
    if len(set(password)) > len(password) * 0.5:  # Character variety
        score += 10
    if not re.search(r"(.)\1{2,}", password):  # No repeated characters
        score += 10

    return min(score, 100)


def get_password_requirements() -> List[Tuple[str, str]]:
    """
    Get list of password requirements for display.

    Returns:
        List of (requirement_key, requirement_description) tuples
    """
    return [
        ("length", "At least 12 characters"),
        ("uppercase", "At least one uppercase letter"),
        ("lowercase", "At least one lowercase letter"),
        ("number", "At least one number"),
        ("special", "At least one special character"),
    ]


def check_password_requirements(password: str) -> List[Tuple[str, bool]]:
    """
    Check which password requirements are met.

    Args:
        password: Password to check

    Returns:
        List of (requirement_key, is_met) tuples
    """
    requirements = [
        ("length", len(password) >= 12),
        ("uppercase", re.search(r"[A-Z]", password) is not None),
        ("lowercase", re.search(r"[a-z]", password) is not None),
        ("number", re.search(r"\d", password) is not None),
        ("special", re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is not None),
    ]

    return requirements
