# Cursor Skills for DeepLint

<!-- Thanks to: @rsionnach/sloppylint for inspiration on cursor skills structure -->

This directory contains Cursor Skills - reusable AI-assisted workflows tailored for the DeepLint project. These skills help developers work more efficiently by providing context-specific guidance for common tasks.

## What are Cursor Skills?

Cursor Skills are markdown documents that provide:
- **Task-specific guidance** - Step-by-step instructions for common workflows
- **Project context** - DeepLint-specific conventions and patterns
- **Best practices** - Proven approaches for quality contributions
- **Quick references** - Essential information at your fingertips

## Available Skills

### Core Development Skills

1. **[pattern-creator.md](./pattern-creator.md)** - Create new AI slop detection patterns
   - Covers Python, Go, JavaScript, and TypeScript patterns
   - Includes testing requirements and best practices
   - Examples for all pattern types (noise, quality, style, structure)

2. **[test-writer.md](./test-writer.md)** - Write comprehensive tests for patterns
   - Test organization and structure
   - Fixture creation guidelines
   - Coverage requirements

3. **[multi-language-support.md](./multi-language-support.md)** - Add support for new languages
   - Language detection integration
   - Pattern implementation guide
   - Testing multilingual features

### Workflow Skills

4. **[code-reviewer.md](./code-reviewer.md)** - Review DeepLint contributions
   - What to look for in PRs
   - Common issues and fixes
   - Quality checklist

5. **[getting-started.md](./getting-started.md)** - Quick start for new contributors
   - Project setup
   - First contribution guide
   - Development workflow

## How to Use Cursor Skills

### In Cursor IDE

1. **Reference a skill**: When working on a task, open the relevant skill file
2. **Follow the workflow**: Use the skill as a checklist and guide
3. **Adapt as needed**: Skills are templates - adjust to your specific needs

### With AI Assistants

Skills can be referenced when prompting AI assistants:
```
"Following the pattern-creator.md skill, help me create a new pattern 
to detect excessive use of global variables in Python code"
```

### As Documentation

Even without Cursor IDE, these skills serve as:
- Onboarding documentation for new contributors
- Quick reference guides for experienced developers
- Living documentation that evolves with the project

## Contributing to Skills

Skills should be:
- **Clear and concise** - Easy to follow step-by-step
- **Example-rich** - Show, don't just tell
- **Up-to-date** - Reflect current project structure and conventions
- **Tested** - Workflows should actually work

To add or improve a skill:
1. Create or edit the markdown file in `.cursor/skills/`
2. Follow the existing format and structure
3. Include practical examples from DeepLint
4. Test the workflow yourself
5. Submit a PR with your changes

## Acknowledgments

The concept of Cursor Skills for code quality tools was inspired by the [@rsionnach/sloppylint](https://github.com/rsionnach/sloppylint) project. We're grateful for the open-source community's approach to sharing development workflows and best practices.

## Learn More

- **DeepLint Documentation**: [AGENTS.md](../../AGENTS.md)
- **Main README**: [README.md](../../README.md)
- **Contributing Guide**: See AGENTS.md for detailed conventions
