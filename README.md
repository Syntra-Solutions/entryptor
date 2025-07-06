# GitHub Copilot Context Engineering Framework

A comprehensive framework for Context Engineering with GitHub Copilot - the discipline of engineering context for AI coding assistants so they have the information necessary to get the job done end to end.

> **Context Engineering is 10x better than prompt engineering and 100x better than vibe coding.**

## 🚀 Quick Start

```bash
# 1. Clone this framework
git clone https://github.com/coleam00/Context-Engineering-Intro.git
cd Context-Engineering-Intro

# 2. Set up your project rules
# Edit COPILOT.md to add your project-specific guidelines

# 3. Add examples (critical for success!)
# Place relevant code examples in the examples/ folder

# 4. Create your feature request
# Edit INITIAL.md with your feature requirements

# 5. Use GitHub Copilot Chat with context
# Copy prompts/copilot-generate-prp.md into Copilot Chat
# Include your INITIAL.md content

# 6. Implement with generated context
# Use the comprehensive context in Copilot Chat
# Follow the validation loops for quality
```

## 📚 Table of Contents

- [What is Context Engineering?](#what-is-context-engineering)
- [Template Structure](#template-structure)
- [Step-by-Step Guide](#step-by-step-guide)
- [Writing Effective INITIAL.md Files](#writing-effective-initialmd-files)
- [The PRP Workflow](#the-prp-workflow)
- [Using Examples Effectively](#using-examples-effectively)
- [Best Practices](#best-practices)

## What is Context Engineering?

Context Engineering represents a paradigm shift from traditional prompt engineering:

### GitHub Copilot vs Traditional Prompting

**Traditional Prompting:**
- Focuses on clever wording and specific phrasing
- Limited to how you phrase a task
- Like giving someone a sticky note

**Context Engineering with GitHub Copilot:**
- A complete system for providing comprehensive context
- Includes documentation, examples, rules, patterns, and validation
- Like writing a full screenplay with all the details
- Leverages Copilot's codebase awareness with structured context

### Why Context Engineering Matters

1. **Reduces AI Failures**: Most agent failures aren't model failures - they're context failures
2. **Ensures Consistency**: AI follows your project patterns and conventions
3. **Enables Complex Features**: AI can handle multi-step implementations with proper context
4. **Self-Correcting**: Validation loops allow AI to fix its own mistakes

## Template Structure

```
github-copilot-context-engineering/
├── prompts/
│   ├── copilot-generate-prp.md   # GitHub Copilot prompt for generating PRPs
│   ├── copilot-implement.md      # GitHub Copilot prompt for implementation
│   └── copilot-validate.md       # GitHub Copilot prompt for validation
├── PRPs/
│   ├── templates/
│   │   └── prp_base.md          # Base template for PRPs
│   └── EXAMPLE_multi_agent_prp.md  # Example of a complete PRP
├── examples/                     # Your code examples (critical!)
├── COPILOT.md                   # Global rules for GitHub Copilot
├── PLANNING.md                  # Project architecture & patterns
├── TASK.md                      # Current work tracking
├── INITIAL.md                   # Template for feature requests
├── INITIAL_EXAMPLE.md           # Example feature request
└── README.md                    # This file
```

This template doesn't focus on RAG and tools with context engineering because I have a LOT more in store for that soon. ;)

## Step-by-Step Guide

### 1. Set Up Global Rules (COPILOT.md)

The `COPILOT.md` file contains project-wide rules that GitHub Copilot will follow in every conversation. The template includes:

- **Project awareness**: Reading planning docs, checking tasks
- **Code structure**: File size limits, module organization  
- **Testing requirements**: Unit test patterns, coverage expectations
- **Style conventions**: Language preferences, formatting rules
- **Documentation standards**: Docstring formats, commenting practices
- **GitHub Copilot workflow**: Specific tips for working with Copilot Chat

**You can use the provided template as-is or customize it for your project.**

### 2. Create Your Initial Feature Request

Edit `INITIAL.md` to describe what you want to build:

```markdown
## FEATURE:
[Describe what you want to build - be specific about functionality and requirements]

## EXAMPLES:
[List any example files in the examples/ folder and explain how they should be used]

## DOCUMENTATION:
[Include links to relevant documentation, APIs, or external resources]

## OTHER CONSIDERATIONS:
[Mention any gotchas, specific requirements, or things AI assistants commonly miss]
```

**See `INITIAL_EXAMPLE.md` for a complete example.**

### 3. Generate the PRP with GitHub Copilot

PRPs (Product Requirements Prompts) are comprehensive implementation blueprints that include:

- Complete context and documentation
- Implementation steps with validation
- Error handling patterns
- Test requirements

Use the structured prompt from `prompts/copilot-generate-prp.md` in GitHub Copilot Chat:

1. **Copy the prompt template** from `prompts/copilot-generate-prp.md`
2. **Paste your feature request** from `INITIAL.md` into the template
3. **Send to GitHub Copilot Chat** - Copilot will read your project files
4. **Review and save** the generated PRP to `PRPs/your-feature-name.md`

### 4. Implement with GitHub Copilot

Once generated, use the implementation prompt to build your feature:

1. **Use the prompt template** from `prompts/copilot-implement.md`
2. **Include your generated PRP** in the template
3. **Send to GitHub Copilot Chat** for step-by-step implementation
4. **Follow the validation loop** - implement, test, fix, repeat
5. **Run quality gates** after each step until all pass

## Writing Effective INITIAL.md Files

### Key Sections Explained

**FEATURE**: Be specific and comprehensive
- ❌ "Build a web scraper"
- ✅ "Build an async web scraper using BeautifulSoup that extracts product data from e-commerce sites, handles rate limiting, and stores results in PostgreSQL"

**EXAMPLES**: Leverage the examples/ folder
- Place relevant code patterns in `examples/`
- Reference specific files and patterns to follow
- Explain what aspects should be mimicked

**DOCUMENTATION**: Include all relevant resources
- API documentation URLs
- Library guides
- MCP server documentation
- Database schemas

**OTHER CONSIDERATIONS**: Capture important details
- Authentication requirements
- Rate limits or quotas
- Common pitfalls
- Performance requirements

## The GitHub Copilot Workflow

### How PRP Generation Works

The structured prompt follows this process:

1. **Context Analysis**
   - GitHub Copilot reads your `PLANNING.md`, `COPILOT.md`, and `TASK.md`
   - Analyzes your codebase patterns from `examples/`
   - Understands your project structure and conventions

2. **Feature Research**
   - Searches for similar implementations online
   - References relevant documentation
   - Identifies common patterns and pitfalls

3. **Blueprint Creation**
   - Creates step-by-step implementation plan
   - Includes validation gates and quality checks
   - Adds comprehensive context for successful implementation

4. **Quality Assessment**
   - Scores confidence level (1-10) for implementation success
   - Ensures all necessary context is included

### How Implementation Works

1. **Load Context**: Copilot reads the entire PRP
2. **Plan**: Creates detailed task breakdown  
3. **Execute**: Implements each component following patterns
4. **Validate**: Runs quality gates after each step
5. **Iterate**: Fixes any issues found during validation
6. **Complete**: Ensures all requirements met

See `PRPs/EXAMPLE_multi_agent_prp.md` for a complete example of what gets generated.

## Using Examples Effectively

The `examples/` folder is **critical** for success. AI coding assistants perform much better when they can see patterns to follow.

### What to Include in Examples

1. **Code Structure Patterns**
   - How you organize modules
   - Import conventions
   - Class/function patterns

2. **Testing Patterns**
   - Test file structure
   - Mocking approaches
   - Assertion styles

3. **Integration Patterns**
   - API client implementations
   - Database connections
   - Authentication flows

4. **CLI Patterns**
   - Argument parsing
   - Output formatting
   - Error handling

### Example Structure

```
examples/
├── README.md           # Explains what each example demonstrates
├── cli.py             # CLI implementation pattern
├── agent/             # Agent architecture patterns
│   ├── agent.py      # Agent creation pattern
│   ├── tools.py      # Tool implementation pattern
│   └── providers.py  # Multi-provider pattern
└── tests/            # Testing patterns
    ├── test_agent.py # Unit test patterns
    └── conftest.py   # Pytest configuration
```

## Best Practices

### 1. Be Explicit in INITIAL.md
- Don't assume the AI knows your preferences
- Include specific requirements and constraints
- Reference examples liberally

### 2. Provide Comprehensive Examples
- More examples = better implementations
- Show both what to do AND what not to do
- Include error handling patterns

### 3. Use Validation Gates
- PRPs include test commands that must pass
- AI will iterate until all validations succeed
- This ensures working code on first try

### 4. Leverage Documentation
- Include official API docs
- Add MCP server resources
- Reference specific documentation sections

### 5. Customize COPILOT.md
- Add your conventions
- Include project-specific rules
- Define coding standards

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Context Engineering Best Practices](https://www.philschmid.de/context-engineering)