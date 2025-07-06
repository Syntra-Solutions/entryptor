# GitHub Copilot Context Engineering - Quick Reference

## 🚀 Quick Start Workflow

### 1. Setup Project (One Time)
- [ ] Customize `COPILOT.md` with your project rules
- [ ] Update `PLANNING.md` with your architecture
- [ ] Add code examples to `examples/` directory
- [ ] Set current tasks in `TASK.md`

### 2. Implement Any Feature
- [ ] Write feature request in `INITIAL.md`
- [ ] Use `prompts/copilot-generate-prp.md` → Create PRP
- [ ] Use `prompts/copilot-implement.md` → Build feature  
- [ ] Use `prompts/copilot-validate.md` → Ensure quality

## 📁 Key Files

| File | Purpose |
|------|---------|
| `COPILOT.md` | Global rules for GitHub Copilot |
| `PLANNING.md` | Project architecture & patterns |
| `TASK.md` | Current work tracking |
| `INITIAL.md` | Feature request template |
| `examples/` | Code patterns to follow |
| `prompts/` | Structured prompts for Copilot |
| `PRPs/` | Generated implementation blueprints |

## 🤖 GitHub Copilot Chat Prompts

### Generate PRP
```
Copy from: prompts/copilot-generate-prp.md
Purpose: Create comprehensive implementation blueprint
Input: Your feature request from INITIAL.md
Output: PRP saved to PRPs/feature-name.md
```

### Implement Feature  
```
Copy from: prompts/copilot-implement.md
Purpose: Build feature with validation loops
Input: Generated PRP
Output: Working code that passes all quality gates
```

### Validate Quality
```
Copy from: prompts/copilot-validate.md  
Purpose: Check code quality and fix issues
Input: Files/code to validate
Output: Quality improvements and fixes
```

## ✅ Quality Gates

Run these commands to validate your code:

```bash
# Style & formatting
ruff check . --fix && ruff format .

# Type checking
mypy .

# Tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing
```

## 🎯 Success Pattern

1. **Read project context** (PLANNING.md, COPILOT.md, TASK.md)
2. **Follow existing patterns** from examples/
3. **Implement incrementally** with validation loops
4. **Test continuously** - don't wait until the end
5. **Update task tracking** as you progress

## 💡 Tips for Better Results

### With GitHub Copilot:
- **Reference files by name** - Copilot can see your codebase
- **Use structured prompts** from prompts/ directory
- **Be specific** about patterns to follow
- **Ask for validation commands** and run them
- **Request incremental changes** rather than large rewrites

### Context Engineering:
- **More examples = better results** in examples/
- **Specific patterns** beat generic instructions
- **Validation loops** ensure working code
- **Comprehensive context** reduces back-and-forth

## 🔧 Common Commands

```bash
# Start new feature
cp INITIAL.md INITIAL-myfeature.md
# Edit INITIAL-myfeature.md with your requirements
# Use copilot-generate-prp.md prompt with your requirements

# Validate existing code  
ruff check . --fix
mypy .
pytest tests/ -v

# Update dependencies
pip freeze > requirements.txt
```

## 📚 Template Files

- `INITIAL.md` - Feature request template
- `PRPs/templates/prp_base.md` - PRP template  
- `prompts/copilot-*.md` - Copilot prompt templates
- `examples/` - Your code patterns (populate this!)

---

**Remember**: The power is in the context! The more examples and patterns you provide, the better GitHub Copilot will implement features according to your conventions.
