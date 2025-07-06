# Project Planning & Architecture

## Project Overview
**Project Name**: [Your Project Name]
**Description**: [Brief description of what this project does]
**Type**: [e.g., CLI tool, Web API, Library, etc.]

## Architecture & Technology Stack

### Core Technologies
- **Language**: Python
- **Framework**: [e.g., FastAPI, Django, Flask, or "None - Pure Python"]
- **Database**: [e.g., PostgreSQL, SQLite, MongoDB, or "None"]
- **Testing**: pytest
- **Linting**: ruff + mypy
- **Environment**: python-dotenv

### Project Structure
```
project/
├── src/                    # Main source code
│   ├── __init__.py
│   ├── main.py            # Entry point
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   ├── utils/             # Utility functions
│   └── config/            # Configuration
├── tests/                 # Test files
├── examples/              # Code examples for context engineering
├── docs/                  # Documentation
├── requirements.txt       # Dependencies
├── .env.example          # Environment variables template
└── README.md             # Project documentation
```

## Coding Conventions

### File Organization
- **Max file length**: 500 lines
- **Module structure**: Clear separation by responsibility
- **Import style**: Absolute imports preferred, relative for local modules
- **Naming**: snake_case for functions/variables, PascalCase for classes

### Code Style
- **Formatting**: black (or ruff format)
- **Type hints**: Required for all functions
- **Docstrings**: Google style for all public functions
- **Error handling**: Specific exceptions, never bare `except:`

### Testing Patterns
- **Test structure**: Mirror src/ structure in tests/
- **Test naming**: `test_[function_name]_[scenario]`
- **Coverage**: Aim for 80%+ coverage
- **Mocking**: Use pytest fixtures and unittest.mock

## Dependencies & External Services

### Core Dependencies
```txt
# Add your actual dependencies here
pydantic>=2.0.0
python-dotenv>=1.0.0
pytest>=7.0.0
ruff>=0.1.0
mypy>=1.0.0
```

### External APIs
- [List any external APIs your project uses]
- [Include authentication requirements]
- [Note rate limits or usage constraints]

## Development Workflow

### Local Development
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure
6. Run tests: `pytest`

### Quality Gates
Before any commit/PR:
```bash
# Linting and formatting
ruff check . --fix
ruff format .

# Type checking
mypy .

# Tests
pytest tests/ -v --cov=src --cov-report=term-missing
```

## Common Patterns

### Error Handling
```python
# Use specific exceptions
class CustomError(Exception):
    """Specific error for this domain."""
    pass

# Log errors with context
import logging
logger = logging.getLogger(__name__)

try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    raise CustomError(f"Failed to process: {e}") from e
```

### Configuration Management
```python
# Use pydantic-settings for config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    debug: bool = False
    
    class Config:
        env_file = ".env"
```

### Async/Await Usage
- Use async/await consistently if needed
- Don't mix sync and async inappropriately
- Use `asyncio.run()` for entry points

## Known Gotchas

### Common Issues
- [List common problems in your domain]
- [Library-specific quirks]
- [Platform-specific issues]

### Anti-patterns to Avoid
- Hardcoded values instead of configuration
- Sync functions in async contexts
- Missing error handling
- Overly complex functions (>50 lines)

## Integration Points

### External Services
- [Document how to connect to external services]
- [Authentication setup]
- [Error handling for service failures]

### Data Flow
- [Describe how data flows through your system]
- [Input validation points]
- [Output formatting]

---

## Notes for AI Assistants

When working on this project:
1. **Always check this file first** to understand patterns
2. **Follow the established structure** - don't create new patterns without reason
3. **Use the testing patterns** described above
4. **Respect the quality gates** - all code must pass linting and tests
5. **Add new patterns here** if you establish them during development
6. **Follow GitHub Copilot workflow** from COPILOT.md for complex features

Last updated: [Today's date]
