# GitHub Copilot Prompt Templates

## Generate PRP Template for Copilot

```
I need you to create a comprehensive Product Requirements Prompt (PRP) for implementing a feature. 

**Feature Request**: [Paste your INITIAL.md content here]

**Context to Include**:
1. Read these files from my codebase: [list key files]
2. Follow patterns from: [point to example files]
3. Use this tech stack: [your stack from PLANNING.md]
4. Follow these conventions: [paste relevant parts of PLANNING.md]

**Create a PRP that includes**:
- Complete implementation blueprint
- Step-by-step tasks
- Validation commands I can run
- All necessary context for implementation

**Template to follow**: [paste PRPs/templates/prp_base.md here]
```

## Execute PRP Template for Copilot

```
Implement this feature using the comprehensive PRP below:

[Paste your generated PRP here]

**Requirements**:
- Follow ALL patterns and conventions in the PRP
- Implement step-by-step as outlined
- Run validation commands after each step
- Fix any errors found during validation
- Ensure all success criteria are met

**Current codebase context**: [Copilot already has this]
**Project rules**: [paste relevant CLAUDE.md rules]
```
