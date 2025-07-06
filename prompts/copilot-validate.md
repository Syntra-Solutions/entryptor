# Validate Code Quality with GitHub Copilot

Use this prompt template in **GitHub Copilot Chat** to validate and improve code quality using the project's standards.

## Prompt Template

```
I need you to validate and improve the code quality of my recent changes. Please follow our project standards and fix any issues found.

**PROJECT STANDARDS:**
Read these files to understand our quality requirements:
- `PLANNING.md` - Quality gates and development workflow
- `COPILOT.md` - Code style and conventions
- `examples/` - Patterns to follow for consistency

**VALIDATION PROCESS:**

### 1. Code Style & Formatting
Run and fix any issues:
```bash
ruff check . --fix
ruff format .
```

### 2. Type Checking
Ensure all type hints are correct:
```bash
mypy .
```

### 3. Test Coverage
Run tests and check coverage:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### 4. Pattern Consistency
Review code against our established patterns:
- File organization follows `PLANNING.md` structure
- Import style is consistent with examples
- Function/class naming follows conventions
- Docstrings use Google style format
- Error handling follows project patterns

### 5. Architecture Review
Check integration with existing codebase:
- New code fits established architecture
- Dependencies are properly managed
- Configuration follows existing patterns
- No duplicate functionality

**SPECIFIC AREAS TO VALIDATE:**

[Specify particular files, functions, or areas you want validated]

**WHAT TO FIX:**

### Code Quality Issues:
- Style violations (ruff will catch most)
- Missing or incorrect type hints
- Missing docstrings for public functions
- Overly complex functions (>50 lines)
- Files approaching 500 line limit

### Test Quality Issues:
- Missing tests for new functionality
- Tests that don't follow naming conventions
- Low test coverage areas
- Missing edge case or error tests

### Pattern Violations:
- Code that doesn't follow examples/ patterns
- Inconsistent import styles
- Non-standard error handling
- Configuration that should be environment variables

### Integration Issues:
- Breaking changes to existing interfaces
- Missing updates to related documentation
- Inconsistent with project architecture

**IMPROVEMENT SUGGESTIONS:**

After validation, suggest:
1. **Performance improvements** where applicable
2. **Better error handling** if needed
3. **Code organization** improvements
4. **Test strategy** enhancements
5. **Documentation** updates needed

**VALIDATION REPORT:**

Please provide:
- ✅/❌ for each validation step
- Specific issues found and how to fix them
- Suggested improvements for better code quality
- Commands to run to verify fixes
- Updated task status for `TASK.md`

Run the validation commands and fix issues iteratively until all quality gates pass.
```

## Quick Validation Prompt

For faster validation of smaller changes:

```
@GitHub Copilot, please validate this code against our project standards from `PLANNING.md` and `COPILOT.md`:

[paste code or specify files]

Check for:
- Style issues (run `ruff check .`)
- Type hints (run `mypy .`) 
- Test coverage
- Pattern consistency with `examples/`
- Missing documentation

Fix any issues found.
```

## Usage Instructions

1. **Use after implementing features** or making significant changes
2. **Copy the full prompt** for comprehensive validation
3. **Use the quick prompt** for smaller changes
4. **Run suggested commands** and report results back
5. **Fix issues iteratively** until all gates pass
6. **Update TASK.md** with completed validation

## Common Issues to Check

### Style & Formatting:
- Inconsistent indentation or spacing
- Long lines (>88 characters with ruff)
- Missing trailing commas in multi-line structures
- Inconsistent quote usage

### Type Hints:
- Missing return type annotations
- Missing parameter type hints
- Using `Any` instead of specific types
- Incorrect generic types

### Testing:
- Missing tests for new functions/classes
- Tests not following `test_[function]_[scenario]` naming
- Missing assertions or weak test cases
- Not testing error conditions

### Documentation:
- Missing docstrings for public functions
- Outdated README.md sections
- Missing inline comments for complex logic
- No examples for new features

## Example Workflow

```
You: [Use validation prompt]

Copilot: I'll validate your code. First, let me check the style:
Run: `ruff check . --fix`

You: No issues found.

Copilot: Great! Now type checking:
Run: `mypy .`

You: Found 3 missing type hints in user.py

Copilot: I'll fix those type hints...
[provides corrections]

You: Fixed! Tests now?

Copilot: Let's run the tests:
Run: `pytest tests/ -v --cov=src --cov-report=term-missing`

[Continue until all validation passes]
```

This ensures your code meets project standards before committing!
