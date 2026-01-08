# Getting Started Skill

<!-- Thanks to: @rsionnach/sloppylint for inspiration on contributor onboarding -->

Welcome to DeepLint! This skill helps you make your first contribution to the project.

## Quick Setup

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/del-zhenwu/deeplint.git
cd deeplint

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### 2. Verify Installation

```bash
# Run tests to ensure everything works
pytest tests/ -v

# Try the CLI
deeplint --version
deeplint --help

# Scan the project itself (meta!)
deeplint src/
```

### 3. Explore the Codebase

```
deeplint/
├── src/sloppy/           # Main package
│   ├── cli.py            # Command-line interface
│   ├── detector.py       # Main detection orchestration
│   ├── patterns/         # Pattern definitions
│   │   ├── __init__.py   # Pattern registry
│   │   ├── base.py       # Base classes
│   │   ├── noise.py      # Python noise patterns
│   │   ├── hallucinations.py  # Python quality patterns
│   │   ├── style.py      # Python style patterns
│   │   ├── structure.py  # Python structural patterns
│   │   ├── go/           # Go patterns
│   │   └── js/           # JavaScript/TypeScript patterns
│   └── analyzers/        # Language-specific analyzers
├── tests/                # Test suite
│   ├── test_patterns/    # Pattern tests
│   ├── fixtures/         # Test code samples
│   └── conftest.py       # Test fixtures
└── .cursor/skills/       # You are here!
```

## Your First Contribution

### Option 1: Fix a Bug

1. **Find an issue**: Check [GitHub Issues](https://github.com/del-zhenwu/deeplint/issues)
2. **Reproduce**: Create a minimal test case
3. **Fix**: Make the smallest change possible
4. **Test**: Ensure tests pass
5. **Submit**: Create a PR with clear description

### Option 2: Add a New Pattern

Follow the [pattern-creator.md](./pattern-creator.md) skill:

1. **Identify** a common AI mistake
2. **Implement** the pattern
3. **Test** with fixtures
4. **Document** in AGENTS.md
5. **Submit** a PR

Example: Detect `except Exception as e: pass` (swallowing errors)

### Option 3: Improve Documentation

1. **Find gaps**: What confused you?
2. **Write**: Add examples and clarify
3. **Submit**: Documentation PRs are always welcome

### Option 4: Add Language Support

See [multi-language-support.md](./multi-language-support.md) for:
- Adding new language patterns
- Improving existing language detection
- Expanding coverage for Go/JS/TS

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-123
```

### 2. Make Changes

Follow these principles:
- **Small changes**: One feature/fix per PR
- **Test first**: Write test, see it fail, make it pass
- **Follow conventions**: See [AGENTS.md](../../AGENTS.md)

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_patterns/test_hallucinations.py -v

# Check coverage
pytest tests/ --cov=src/sloppy --cov-report=term-missing

# Test specific pattern
pytest tests/ -k "mutable_default" -v
```

### 4. Test Manually

```bash
# Test on real code
deeplint src/

# Test specific severity
deeplint src/ --severity high

# Test with JSON output
deeplint src/ --output report.json
cat report.json | python -m json.tool
```

### 5. Commit

```bash
git add .
git commit -m "Add pattern to detect X"

# Or for bug fixes
git commit -m "Fix false positive in Y pattern"
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a PR on GitHub with:
- Clear title
- Description of what changed
- Why the change is needed
- Test results

## Common Tasks

### Run DeepLint Locally

```bash
# As module
python -m sloppy src/

# As installed command
deeplint src/
```

### Add a New Pattern

See [pattern-creator.md](./pattern-creator.md) for complete guide.

Quick summary:
1. Create pattern class in appropriate file
2. Register in `patterns/__init__.py`
3. Add test fixture
4. Write tests
5. Run and verify

### Run Specific Tests

```bash
# One test file
pytest tests/test_patterns/test_noise.py -v

# One test function
pytest tests/test_patterns/test_noise.py::test_debug_print -v

# Pattern by name
pytest tests/ -k "debug_print" -v

# Failed tests only
pytest tests/ --lf -v
```

### Debug a Pattern

```bash
# Add print statements in pattern code
# Run specific test
pytest tests/test_patterns/test_noise.py::test_debug_print -v -s

# Or test directly
python -c "
from sloppy.patterns.noise import DebugPrint
pattern = DebugPrint()
# Test your pattern
"
```

### Update Documentation

Key files:
- **README.md**: User-facing documentation
- **AGENTS.md**: Developer documentation
- **.cursor/skills/**: Development workflows

## Code Style

DeepLint follows these conventions:

### Python Style
- **PEP 8**: Standard Python style
- **Type hints**: All function signatures
- **Docstrings**: Google style for public functions
- **No external deps**: Core uses stdlib only

### Example Pattern

```python
from sloppy.patterns.base import BasePattern, Issue, Severity

class MyPattern(BasePattern):
    """Detect something problematic.
    
    This pattern finds cases where...
    """
    
    id = "my_pattern"
    severity = Severity.HIGH
    axis = "quality"
    message = "Clear, actionable error message"
    
    def check_node(self, node: ast.FunctionDef) -> list[Issue]:
        """Check a function definition.
        
        Args:
            node: AST node to check
            
        Returns:
            List of issues found
        """
        issues = []
        # Detection logic here
        return issues
```

## Testing Requirements

Every pattern must have:
1. **Positive tests** - Detects what it should
2. **Negative tests** - No false positives
3. **Edge cases** - Handles unusual inputs
4. **Coverage** - >90% of pattern code

See [test-writer.md](./test-writer.md) for complete guide.

## Common Pitfalls

### 1. Pattern Too Broad
```python
# Bad: Matches too much
pattern = re.compile(r'print')  # Catches "print_report()"

# Good: Use word boundaries
pattern = re.compile(r'\bprint\b')
```

### 2. Forgetting to Register
```python
# Must add to patterns/__init__.py
from .noise import MyNewPattern

PYTHON_PATTERNS = [
    # ... existing ...
    MyNewPattern(),  # Don't forget!
]
```

### 3. Missing Language Attribute
```python
# For non-Python patterns
class GoPattern(RegexPattern):
    language = "go"  # Required!
```

### 4. Not Testing False Positives
```python
# Always test that good code isn't flagged
def test_no_false_positives():
    issues = scan_good_code()
    my_issues = [i for i in issues if i.pattern_id == "my_pattern"]
    assert len(my_issues) == 0  # Good code should not trigger
```

## Getting Help

### Resources
- **AGENTS.md**: Detailed development guide
- **Cursor Skills**: Task-specific workflows (you're reading one!)
- **Test Examples**: `tests/` directory
- **Pattern Examples**: `src/sloppy/patterns/`

### Ask for Help
- **GitHub Issues**: Questions about contribution
- **GitHub Discussions**: General questions
- **Pull Request**: Ask in PR comments

### Review Process
1. **Automated checks**: Tests must pass
2. **Code review**: Maintainer reviews code
3. **Feedback**: Address comments
4. **Merge**: Approved PRs get merged

## Next Steps

### After Your First Contribution

1. **Add more patterns**: See pattern ideas in [pattern-creator.md](./pattern-creator.md)
2. **Improve existing**: Reduce false positives
3. **Add languages**: Expand to new languages
4. **Help others**: Review PRs, answer questions

### Become a Regular Contributor

- Fix issues labeled "good first issue"
- Help with documentation
- Review other PRs
- Propose new features

### Advanced Topics

- [pattern-creator.md](./pattern-creator.md) - Create detection patterns
- [test-writer.md](./test-writer.md) - Write comprehensive tests
- [multi-language-support.md](./multi-language-support.md) - Add language support
- [code-reviewer.md](./code-reviewer.md) - Review contributions

## Checklist for First Contribution

- [ ] Repository cloned and dependencies installed
- [ ] Tests run successfully
- [ ] DeepLint CLI works
- [ ] Codebase explored
- [ ] Feature branch created
- [ ] Changes made following conventions
- [ ] Tests written and passing
- [ ] Manual testing done
- [ ] Documentation updated (if needed)
- [ ] Commit with clear message
- [ ] PR created with description

## Welcome!

We're excited to have you contribute to DeepLint. Every contribution, big or small, helps make AI-generated code better and safer.

Happy coding! 🚀
