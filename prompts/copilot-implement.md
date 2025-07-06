# Implement Feature with GitHub Copilot

Use this prompt template in **GitHub Copilot Chat** to implement features using generated PRPs with validation loops.

## Prompt Template

```
I need you to implement a feature using the comprehensive PRP below. Follow all patterns, validate continuously, and ensure working code.

**IMPLEMENTATION APPROACH:**
1. Read and understand the complete PRP context
2. Break down into manageable implementation steps  
3. Implement each step following project patterns
4. Validate after each step with quality gates
5. Fix any issues found during validation
6. Continue until all success criteria are met

**PROJECT CONTEXT:**
- Follow patterns from `PLANNING.md` and `COPILOT.md`
- Use existing code patterns from `examples/` directory
- Update `TASK.md` with progress and discoveries
- Maintain all project conventions and style

**PRP TO IMPLEMENT:**
[PASTE YOUR GENERATED PRP HERE]

**IMPLEMENTATION REQUIREMENTS:**

### Code Quality Standards:
- All code must pass: `ruff check . --fix && ruff format .`
- Type checking must pass: `mypy .`
- All tests must pass: `pytest tests/ -v`
- Follow existing patterns from `examples/` directory
- Maximum 500 lines per file (refactor if needed)

### Validation Loop Process:
1. **Implement** each task from the PRP blueprint
2. **Validate** using the quality gates provided
3. **Fix** any errors or style issues found
4. **Test** that functionality works as expected
5. **Iterate** until all validation passes

### File Organization:
- Follow the project structure defined in `PLANNING.md`
- Mirror test structure: `tests/` should mirror `src/`
- Use consistent imports and naming conventions
- Add docstrings for all public functions

### Task Tracking:
- Mark completed tasks in `TASK.md` as you finish them
- Add any discovered work to "Discovered During Work" section
- Note any blockers or decisions needed

**EXECUTION STEPS:**

1. **Start with data models** and core structures
2. **Implement business logic** following existing patterns  
3. **Add tests** for each component as you build
4. **Integrate** with existing codebase carefully
5. **Validate** continuously with provided commands
6. **Document** any new patterns or decisions

**VALIDATION COMMANDS TO RUN:**
```bash
# Style and formatting
ruff check . --fix
ruff format .

# Type checking  
mypy .

# Run tests
pytest tests/ -v --cov=src --cov-report=term-missing

# Integration test
[specific commands from PRP]
```

**SUCCESS CRITERIA:**
All checkboxes in the PRP success criteria must be complete before considering the task done.

Please implement this feature step by step, validating after each major component, and ensuring all quality gates pass.
```

## Usage Instructions

1. **Generate a PRP first** using `copilot-generate-prp.md`
2. **Copy this prompt** into GitHub Copilot Chat
3. **Paste your complete PRP** in the designated section
4. **Let Copilot implement** step by step with validation
5. **Run the validation commands** as Copilot suggests them
6. **Fix any issues** iteratively until all pass

## Validation Loop Example

```
You: [Use the implementation prompt above]

Copilot: I'll implement this step by step. Let me start with the data models...

[Copilot creates files]

Copilot: Now let's validate what we've built:
Run: `ruff check . --fix && mypy .`

You: [Run the commands and report results]

Copilot: Good! Now let's add the tests for these models...

[Continue this loop until complete]
```

## Tips for Success

- **Run validation commands** immediately when Copilot suggests them
- **Report back results** so Copilot can fix issues
- **Ask for clarification** if implementation seems off-pattern
- **Request specific file changes** rather than large code blocks
- **Keep conversations focused** on one component at a time
- **Use the project patterns** Copilot references from your examples

## Quality Gates

Always ensure these pass before marking tasks complete:
- ✅ Code style: `ruff check . --fix`
- ✅ Type checking: `mypy .`  
- ✅ Tests: `pytest tests/ -v`
- ✅ Integration: Feature works as specified
- ✅ Documentation: README updated if needed

The validation loop ensures working code on first try!
