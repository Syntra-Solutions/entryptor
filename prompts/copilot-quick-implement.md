# Quick Feature Implementation with GitHub Copilot

Use this streamlined prompt for **simple features** that don't need full PRP generation.

## When to Use This Prompt
- Adding a single function or class
- Small bug fixes or improvements
- Simple API endpoints
- Basic CRUD operations
- Configuration changes

## Quick Implementation Prompt

```
I need to implement a simple feature following our project patterns.

**PROJECT CONTEXT:**
- Read `PLANNING.md` for our architecture and conventions
- Follow patterns from `COPILOT.md` for code style
- Use examples from `examples/` directory as reference

**FEATURE REQUEST:**
[Describe your simple feature - 1-3 sentences]

**REQUIREMENTS:**
- Follow existing code patterns exactly
- Add appropriate tests following our test structure
- Ensure type hints and docstrings
- Run validation: `ruff check . --fix && mypy . && pytest`

**QUICK VALIDATION:**
After implementation:
1. Code follows patterns from `examples/`
2. All quality gates pass
3. Feature works as expected
4. Tests cover happy path and edge cases

Please implement this incrementally with validation at each step.
```

## Usage Examples

### Simple Function Addition:
```
Add a `calculate_tax(amount: float, rate: float) -> float` function to `src/utils/calculations.py` following our existing calculation patterns.
```

### Basic API Endpoint:
```
Add a GET `/health` endpoint to our FastAPI app that returns {"status": "healthy", "timestamp": "ISO-8601"} following our existing endpoint patterns.
```

### Configuration Change:
```
Add a `MAX_RETRIES` configuration variable to our settings with default value 3, following our existing config patterns.
```

This prompt is perfect for features that take 5-15 minutes to implement!
