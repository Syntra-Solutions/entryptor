# Code Examples for Context Engineering

This directory contains **code patterns and examples** that GitHub Copilot will reference when implementing features. The quality of examples directly impacts implementation quality.

## 📁 Recommended Example Structure

```
examples/
├── README.md                 # This file
├── basic/                    # Simple patterns
│   ├── function_example.py   # Well-documented function
│   ├── class_example.py      # Class with proper structure
│   └── config_example.py     # Configuration pattern
├── testing/                  # Test patterns
│   ├── test_example.py       # Unit test examples
│   ├── conftest.py          # Pytest configuration
│   └── mocking_example.py    # How to mock external services
├── api/                      # API patterns (if applicable)
│   ├── endpoint_example.py   # FastAPI/Flask endpoint
│   ├── middleware_example.py # Middleware pattern
│   └── error_handling.py     # Error response patterns
├── data/                     # Data handling patterns
│   ├── model_example.py      # Pydantic/SQLAlchemy models
│   ├── validation_example.py # Input validation
│   └── serialization.py      # Data serialization
└── cli/                      # CLI patterns (if applicable)
    ├── command_example.py     # CLI command structure
    └── argument_parsing.py    # Argument handling
```

## 🎯 What Makes Good Examples

### ✅ Good Example Characteristics:
- **Complete and functional** - code that actually works
- **Well-documented** - clear docstrings and comments
- **Follows conventions** - shows your preferred patterns
- **Handles errors** - demonstrates proper error handling
- **Includes tests** - shows how to test the pattern
- **Real-world focused** - solves actual problems

### ❌ Poor Example Characteristics:
- Incomplete code snippets
- No documentation or comments
- Inconsistent with project style
- Missing error handling
- No test coverage
- Overly simplistic toy examples

## 📝 Example Templates

### Function Example Template:
```python
# examples/basic/function_example.py
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def process_user_data(
    user_id: str, 
    data: dict, 
    validate: bool = True
) -> Optional[dict]:
    """
    Process user data with validation and error handling.
    
    This example shows our standard pattern for:
    - Input validation
    - Error handling with logging
    - Type hints and documentation
    - Return value patterns
    
    Args:
        user_id: Unique user identifier
        data: User data dictionary to process
        validate: Whether to run validation checks
        
    Returns:
        Processed data dictionary or None if processing fails
        
    Raises:
        ValueError: If user_id is invalid
        ValidationError: If data validation fails
    """
    # PATTERN: Always validate inputs first
    if not user_id or not isinstance(user_id, str):
        raise ValueError("user_id must be a non-empty string")
    
    try:
        # PATTERN: Log important operations
        logger.info(f"Processing data for user {user_id}")
        
        # PATTERN: Early return for edge cases
        if not data:
            logger.warning(f"No data provided for user {user_id}")
            return None
            
        # PATTERN: Validation when requested
        if validate:
            _validate_user_data(data)
            
        # PATTERN: Main processing logic
        processed_data = {
            "user_id": user_id,
            "processed_at": datetime.utcnow().isoformat(),
            "data": _transform_data(data)
        }
        
        logger.info(f"Successfully processed data for user {user_id}")
        return processed_data
        
    except Exception as e:
        # PATTERN: Log errors with context
        logger.error(f"Failed to process data for user {user_id}: {e}")
        raise  # Re-raise to let caller handle

def _validate_user_data(data: dict) -> None:
    """Private helper function - our naming convention."""
    # Validation logic here
    pass

def _transform_data(data: dict) -> dict:
    """Private helper function - our transformation pattern."""
    # Transformation logic here
    return data
```

## 🚀 Getting Started

### If you have NO examples yet:
1. **Start with one good example** from your existing codebase
2. **Document it thoroughly** with comments explaining patterns
3. **Add more examples** as you build features
4. **Refine based on results** - if Copilot doesn't follow a pattern, improve the example

### If you have existing code:
1. **Choose your best files** that represent good patterns
2. **Copy them to examples/** with thorough documentation
3. **Add comments** explaining WHY things are done certain ways
4. **Include both success and error handling patterns**

## 💡 Pro Tips

- **Quality over quantity** - 3 excellent examples > 10 mediocre ones
- **Update examples** as your patterns evolve
- **Include anti-patterns** with comments explaining what NOT to do
- **Test your examples** - make sure they actually work
- **Reference examples** in your prompts: "following the pattern in `examples/api/endpoint_example.py`"

Remember: GitHub Copilot will mirror these patterns, so make them exemplary of your best practices!
