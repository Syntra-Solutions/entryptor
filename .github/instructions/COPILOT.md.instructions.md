---
applyTo: '**'
---
# GitHub Copilot Context Engineering Rules

## 🔄 Project Awareness & Context
- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn't listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.
- **Reference these files** when GitHub Copilot needs context about project patterns.
- **When I push to remotes, first fill in the TASK.md if not done already and then go on to pushing**
- **We should always work on STAGING branch and push to 2 remotes on STAGING branch** the main branches on remotes will be merged manually on Azure and GitHub
- **Pushing to remote** we should always push to 2 remotes https://dev.azure.com/syntrasoftware/_git/Entryptor and https://github.com/Syntra-Solutions/entryptor

## 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
- **Use clear, consistent imports** (prefer absolute imports for main modules, relative for local packages).
- **Use python_dotenv and load_env()** for environment variables.

## 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case  
    - 1 failure case

## ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a "Discovered During Work" section.

## 📎 Style & Conventions
- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `ruff format`.
- **Use `pydantic` for data validation**.
- Use `FastAPI` for APIs and `SQLAlchemy` or `SQLModel` for ORM if applicable.
- Write **docstrings for every function** using the Google style:
  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```

## 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

## 🤖 GitHub Copilot Workflow
- **Use structured prompts** from the `prompts/` directory for consistency
- **Reference specific files** by name - Copilot can see your entire codebase
- **Follow the PRP methodology** for complex features
- **Use validation loops** - implement, test, fix, repeat until working
- **Always validate with the quality gates** defined in PLANNING.md

## 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.

---

## GitHub Copilot Specific Tips

### When Using Copilot Chat:
1. **Start conversations** by asking Copilot to read `PLANNING.md` and `TASK.md`
2. **Reference examples** by saying "following the pattern in `examples/filename.py`"
3. **Use the PRP prompts** from `prompts/` directory for complex features
4. **Ask for validation commands** and run them iteratively
5. **Request specific file updates** rather than large code blocks

### For Complex Features:
1. Use `prompts/copilot-generate-prp.md` to create comprehensive context
2. Use `prompts/copilot-implement.md` to execute with validation
3. Use `prompts/copilot-validate.md` to ensure quality

### Quality Control:
- Always ask Copilot to suggest validation commands
- Run tests after each significant change
- Use `ruff check` and `mypy` for code quality
- Ask Copilot to review against project conventions

## 🚨 Gotchas & Known Issues

### PyQt6 Widget Border Styling
**Issue**: Custom QWidget subclasses don't reliably display CSS borders when using class selectors in stylesheets.

**Problem**: 
```python
# This approach often fails to show borders
class DropBox(QWidget):
    def _setup_ui(self):
        self.setStyleSheet("""
            DropBox {
                border: 2px solid #ffffff;  # Often invisible
            }
        """)
```

**Solution**: Use `QFrame` as the base class instead of `QWidget`, and combine both QFrame's built-in border styling with CSS:
```python
# This approach works reliably
class DropBox(QFrame):
    def _setup_ui(self):
        # Use QFrame's built-in border support
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        
        # Plus CSS styling with QFrame selector
        self.setStyleSheet("""
            QFrame {
                border: 1px solid rgba(120, 120, 120, 0.6);  # Visible!
                border-radius: 12px;
            }
        """)
```

**Root Cause**: QWidget doesn't have native border support, while QFrame is specifically designed for displaying borders and frames.

### GitHub Actions Deprecated Versions & PyQt6 CI Issues
**Issue**: GitHub Actions frequently deprecates older versions, causing build failures. Additionally, PyQt6 has compatibility issues in CI environments.

**Problem**: 
```yaml
# This causes build failures due to deprecated versions
- uses: actions/upload-artifact@v3  # Deprecated!
- uses: actions/setup-python@v4    # Outdated
- uses: actions/cache@v3           # Outdated

# PyQt6 fails in CI with symbol linking errors
- name: Test PyQt6
  run: |
    python -c "import PyQt6.QtCore"  # Fails in CI
```

**Solution**: Always use latest stable versions and skip GUI tests in CI:
```yaml
# Use latest stable versions
- uses: actions/upload-artifact@v4
- uses: actions/setup-python@v5
- uses: actions/cache@v4
- uses: actions/checkout@v4

# Skip GUI tests in CI environments
- name: Run tests (skip GUI)
  run: |
    pytest tests/test_crypto/ tests/test_utils/ -k "not gui"
```

**Root Cause**: 
- GitHub regularly deprecates old action versions for security/performance
- PyQt6 has symbol linking issues (`__Z13lcPermissionsv`) on macOS CI runners
- CI environments don't have proper GUI display capabilities

**Monitoring**: Check [GitHub Changelog](https://github.blog/changelog/) for deprecation notices.

### macOS Security Warnings for Unsigned Apps
**Issue**: Users get "Python.framework is damaged" error when trying to run downloaded macOS apps.

**Problem**: 
```
"Python.framework" is damaged and can't be opened. You should move it to the Trash.
```

**Root Cause**: macOS Gatekeeper blocks unsigned applications by default. This is NOT a real problem - it's a security feature.

**Solution**: Provide clear user instructions (multiple methods):
```markdown
### Method 1: Right-Click to Open (Recommended)
1. **Don't double-click** the application
2. **Right-click** on `Entryptor.app` 
3. Select **"Open"** from the context menu
4. Click **"Open"** again in the security dialog

### Method 2: Terminal Command
```bash
xattr -cr Entryptor.app && open Entryptor.app
```

### Method 3: System Preferences
System Preferences → Security & Privacy → "Open Anyway"
```

**Prevention**: For production apps, you need:
- Apple Developer Program membership ($99/year)
- Code signing certificate
- Notarization process
- Automatic signing in CI/CD

**Documentation**: Always include macOS security instructions in README and build artifacts.