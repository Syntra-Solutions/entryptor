# Generate PRP with GitHub Copilot

Use this prompt template in **GitHub Copilot Chat** to generate comprehensive Product Requirements Prompts (PRPs) for feature implementation.

## Prompt Template

```
I need you to create a comprehensive Product Requirements Prompt (PRP) for implementing a feature. This PRP should include all necessary context for successful implementation.

**STEP 1: Read Project Context**
Please read these files to understand my project:
- `PLANNING.md` - Project architecture and conventions
- `COPILOT.md` - GitHub Copilot specific rules  
- `TASK.md` - Current work tracking
- `examples/` directory - Code patterns to follow

**STEP 2: Feature Request**
Here's what I want to build:

[PASTE YOUR INITIAL.md CONTENT HERE]

**STEP 3: Generate Comprehensive PRP**
Using the template from `PRPs/templates/prp_base.md`, create a PRP that includes:

### Required Sections:
1. **Goal** - Clear implementation target
2. **Why** - Business value and integration points  
3. **What** - User-visible behavior and technical requirements
4. **Success Criteria** - Measurable outcomes

### Context Sections:
5. **Documentation & References** - URLs and file references I need
6. **Current vs Desired Codebase** - File structure changes
7. **Known Gotchas** - Library quirks and common issues
8. **Implementation Blueprint** - Data models and task breakdown
9. **Validation Loop** - Executable quality gates

### Critical Requirements:
- **Reference existing patterns** from my `examples/` directory
- **Include specific file paths** for patterns to follow
- **Provide executable validation commands** (ruff, mypy, pytest)
- **Break down into ordered tasks** with clear dependencies
- **Include error handling patterns** from existing code
- **Specify integration points** with current architecture

**STEP 4: Research Enhancement**
If you need additional context:
- Search for similar implementations online
- Reference official documentation for libraries
- Identify common pitfalls for this type of feature

**STEP 5: Quality Score**
Rate the PRP confidence level (1-10) for one-pass implementation success.

Generate a PRP that will enable successful feature implementation through comprehensive context engineering.
```

## Usage Instructions

1. **Copy the prompt above** into GitHub Copilot Chat
2. **Replace the placeholder** with your actual feature request from `INITIAL.md`
3. **Let Copilot analyze** your project structure and patterns
4. **Review the generated PRP** and save it to `PRPs/your-feature-name.md`
5. **Use the implementation prompt** (`copilot-implement.md`) with the generated PRP

## Tips for Better Results

- **Be specific** in your feature request
- **Reference existing files** by name when possible
- **Ask follow-up questions** if the PRP seems incomplete
- **Request clarification** on any unclear implementation steps
- **Validate the approach** against your project conventions

## Example Usage

```
@GitHub Copilot, I need you to create a comprehensive PRP...
[paste template above]

Here's what I want to build:
- A user authentication system with JWT tokens
- Integration with existing FastAPI endpoints  
- Database models using SQLAlchemy
- Unit tests following our existing patterns
```

The generated PRP will become your comprehensive implementation guide!
