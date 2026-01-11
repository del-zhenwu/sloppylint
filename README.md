<!-- TODO: Add CLI demo GIF here -->

<div align="center">
  <h1>🧠 DeepLint</h1>
  <p><strong>Multi-Language AI Slop Detector</strong></p>
  <p><em>Detect AI-generated code anti-patterns in Python, Go, JavaScript, and TypeScript</em></p>
</div>

[![PyPI](https://img.shields.io/pypi/v/deeplint?style=for-the-badge)](https://pypi.org/project/deeplint/)
[![Python >= 3.10](https://img.shields.io/badge/Python-%3E=3.10-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/del-zhenwu/deeplint/ci.yml?branch=main&style=for-the-badge&label=CI)](https://github.com/del-zhenwu/deeplint/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/Tests-114%20passing-brightgreen?style=for-the-badge)](https://github.com/del-zhenwu/deeplint/actions/workflows/ci.yml)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Usage](#usage)
- [Detection Axes](#detection-axes)
- [Supported Languages](#supported-languages)
- [Configuration](#configuration)
- [CI Integration](#ci-integration)
- [Contributing](#contributing)
- [Development](#development)
- [License](#license)

---

## 🎯 Overview

DeepLint is a specialized linter that detects "AI slop" - the over-engineering, hallucinations, dead code, and anti-patterns commonly produced by Large Language Models (LLMs). Inspired by [KarpeSlop](https://github.com/karpathy/karpeslop), DeepLint extends the concept to support multiple programming languages including Python, Go, JavaScript, and TypeScript.

Unlike traditional linters that focus on syntax and style violations, DeepLint identifies patterns that are specific to AI-generated code, such as:
- Redundant or misleading comments
- Hallucinated imports and APIs
- Overconfident or hedging language in comments
- Over-engineered solutions
- Debug code and placeholders left in production

## 📦 Requirements

- **Python >= 3.10**
- No external dependencies required for core functionality (uses stdlib only)
- Optional: `rich` for enhanced terminal output

## 🚀 Installation

### From PyPI (recommended)

```bash
pip install deeplint
```

### From source

```bash
git clone https://github.com/del-zhenwu/deeplint.git
cd deeplint
pip install -e .
```

### With optional dependencies

```bash
# For pretty terminal output
pip install "deeplint[rich]"

# For development
pip install "deeplint[dev]"

# For all optional features
pip install "deeplint[all]"
```

## ⚡ Quick Start

Scan your current directory:

```bash
deeplint .
```

Scan specific files or directories:

```bash
deeplint src/ tests/
deeplint myfile.py
```

Output as JSON:

```bash
deeplint . --output report.json --format json
```

Filter by severity:

```bash
deeplint . --severity high
```

## ✨ Features

- **Multi-language Support**: Python, Go, JavaScript, TypeScript
- **Three Detection Axes**: Noise, Quality (Lies), and Style (Soul)
- **82+ Pattern Detectors**: 46 for Python, 6 for Go, 30 for JavaScript/TypeScript
- **Zero Dependencies**: Core functionality uses only Python stdlib
- **Configurable**: Via CLI flags or `pyproject.toml`
- **CI/CD Ready**: Exit codes and JSON output for automation
- **Fast**: AST-based analysis for Python, regex-based for Go/JS/TS
- **No Code Execution**: Safe to run on untrusted code

## 📖 Usage

### Basic Usage

```bash
# Scan current directory
deeplint .

# Scan with higher severity threshold
deeplint src/ --severity critical

# Output detailed report
deeplint . --format detailed

# Save JSON report
deeplint . --output report.json --format json
```

### Advanced Options

```bash
# Filter by language
deeplint . --language python --language javascript

# Exclude patterns
deeplint . --ignore "tests/*" --ignore "*.min.js"

# Disable specific patterns
deeplint . --disable hallucinated_import --disable debug_print

# CI mode (exit 1 if issues found)
deeplint . --ci

# Set maximum slop score threshold
deeplint . --max-score 100 --ci
```

### CLI Reference

```
usage: deeplint [-h] [--output FILE] [--format {compact,detailed,json}]
              [--severity {low,medium,high,critical}]
              [--ignore PATTERN] [--disable PATTERN_ID]
              [--language LANG]
              [--strict | --lenient] [--ci] [--max-score N]
              [--version]
              [paths ...]

Multi-Language AI Slop Detector

positional arguments:
  paths                 Files or directories to scan (default: .)

options:
  -h, --help            Show help message
  --output FILE         Write JSON report to FILE
  --format FORMAT       Output format: compact, detailed, json
  --severity LEVEL      Minimum severity to report
  --ignore PATTERN      Glob pattern to exclude (repeatable)
  --disable ID          Disable specific pattern (repeatable)
  --language LANG       Target language(s): python, go, javascript, typescript
  --strict              Report all severities
  --lenient             Only critical and high
  --ci                  CI mode: exit 1 if issues found
  --max-score N         Exit 1 if slop score exceeds N
  --version             Show version
```

## 🎨 Detection Axes

DeepLint categorizes AI-generated anti-patterns into three axes:

### 1. 🔇 Noise (Information Utility)

Code elements that add no value or obscure meaning:
- Redundant comments that restate obvious code
- Debug print statements and breakpoints
- Commented-out code blocks
- Empty or generic docstrings
- TODO/FIXME placeholders

### 2. 🚨 Lies (Information Quality)

Code that makes false or unverified claims:
- Hallucinated imports (non-existent packages)
- Wrong standard library imports
- Hallucinated methods and APIs
- Deprecated API usage
- Assumption comments without verification
- Magic numbers and strings without context

### 3. 💀 Soul (Style/Taste)

Code that shows poor judgment or over-engineering:
- Overconfident comments ("obviously", "clearly", "trivially")
- Hedging comments ("should work", "hopefully", "probably")
- God functions (too long, too complex)
- Deep nesting (>4 levels)
- Single-letter variable names
- Inconsistent naming conventions

### 4. 🏗️ Structure

Architectural and organizational issues:
- God classes (too many methods)
- Single-method classes (under-abstraction)
- Unnecessary inheritance
- Unused or star imports
- Circular import risks
- Bare/broad exception handling
- Dead or unreachable code
- Duplicate code across files

## 🌍 Supported Languages

| Language | Extension | Analysis Type | Patterns |
|----------|-----------|---------------|----------|
| Python | `.py` | AST + Regex | 46 |
| Go | `.go` | Regex | 5 |
| JavaScript | `.js`, `.jsx` | Regex | 29 |
| TypeScript | `.ts`, `.tsx` | Regex | 29 |

**Language-Specific Pattern Filtering**: DeepLint automatically applies only the relevant patterns to each file based on its language. This ensures accurate detection across multi-language projects and prevents false positives.

### Python Patterns (46 total)

- **Noise (10)**: redundant_comment, empty_docstring, debug_print, etc.
- **Quality (14)**: hallucinated_import, wrong_stdlib_import, magic_number, etc.
- **Style (10)**: overconfident_comment, god_function, deep_nesting, etc.
- **Structure (12)**: unused_import, bare_except, duplicate_code, etc.

### Go Patterns (5 total)

- **Noise (3)**: go_debug_print, go_todo_comment, go_redundant_comment
- **Style (2)**: go_overconfident_comment, go_hedging_comment

### JavaScript/TypeScript Patterns (29 total)

- **Noise (8)**: js_debug_console, js_todo_comment, js_production_console_log, etc.
- **Quality (4)**: js_hallucinated_react_import, js_hallucinated_next_import, etc.
- **Style (6)**: js_overconfident_comment, js_var_keyword, js_nested_ternary_abuse, etc.
- **TypeScript (6)**: ts_any_type_usage, ts_unsafe_type_assertion, etc.
- **React (4)**: js_useEffect_derived_state, js_setState_in_loop, etc.
- **Structure (1)**: js_missing_error_handling

## ⚙️ Configuration

### Via pyproject.toml

```toml
[tool.deeplint]
exclude = ["tests/*", "migrations/*", "*.min.js"]
severity_threshold = "medium"
max_score = 100
```

### Via Command Line

Configuration can be provided via CLI flags (see [Usage](#usage) section).

## 🔄 CI Integration

### GitHub Actions

```yaml
- name: Run DeepLint
  run: |
    pip install deeplint
    deeplint . --ci --severity high --output report.json
```

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/del-zhenwu/deeplint
    rev: v0.0.2
    hooks:
      - id: deeplint
        args: [--severity, high]
```

### Exit Codes

- `0`: No issues found or all issues below severity threshold
- `1`: Issues found (when using `--ci` flag)
- `1`: Slop score exceeds threshold (when using `--max-score`)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/del-zhenwu/deeplint.git
cd deeplint

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/deeplint --cov-report=term-missing

# Run specific test file
pytest tests/test_patterns/test_hallucinations.py -v
```

### Code Style

- Follow PEP 8
- Use type hints for all function signatures
- Add docstrings for public functions (Google style)
- Keep functions under 50 lines where possible
- Run `black` and `isort` before committing

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check formatting
black --check src/ tests/
isort --check-only src/ tests/

# Run linters
ruff check src/ tests/
mypy src/deeplint
```

### Adding New Patterns

1. Choose the appropriate category file in `src/deeplint/patterns/`
2. Create a class inheriting from `BasePattern` or `RegexPattern`
3. Implement the detection logic
4. Add tests in `tests/test_patterns/`
5. Add fixture files in `tests/fixtures/` if needed
6. Update documentation

See [AGENTS.md](AGENTS.md) for detailed development guidelines.

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linters
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🛠️ Development

### Project Structure

```
deeplint/
├── src/deeplint/
│   ├── __init__.py          # Package init, version
│   ├── __main__.py          # Entry point: python -m deeplint
│   ├── cli.py               # CLI argument parsing
│   ├── detector.py          # Main orchestration
│   ├── languages.py         # Language detection
│   ├── scoring.py           # Slop score calculation
│   ├── reporter.py          # Output formatting
│   ├── config.py            # Configuration loading
│   ├── patterns/            # Detection patterns
│   │   ├── base.py
│   │   ├── noise.py
│   │   ├── hallucinations.py
│   │   ├── style.py
│   │   ├── structure.py
│   │   ├── go/              # Go patterns
│   │   └── js/              # JS/TS patterns
│   └── analyzers/           # Analysis engines
│       ├── ast_analyzer.py
│       ├── import_validator.py
│       └── duplicate_finder.py
├── tests/                   # Test suite
├── pyproject.toml          # Project metadata
└── README.md               # This file
```

### Building Documentation

```bash
# Generate API documentation (if sphinx added)
cd docs
make html
```

### Release Process

1. Update version in `src/deeplint/__init__.py`
2. Update version in `pyproject.toml`
3. Update CHANGELOG.md
4. Create git tag: `git tag v0.0.3`
5. Push tag: `git push origin v0.0.3`
6. GitHub Actions will build and publish to PyPI

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [KarpeSlop](https://github.com/karpathy/karpeslop) by Andrej Karpathy
- Built with ❤️ to improve code quality in the age of AI-assisted development

## 📞 Support

- 📫 [Issue Tracker](https://github.com/del-zhenwu/deeplint/issues)
- 💬 [Discussions](https://github.com/del-zhenwu/deeplint/discussions)
- 📖 [Documentation](https://github.com/del-zhenwu/deeplint/blob/main/AGENTS.md)

---

<div align="center">
  <sub>Made with 🧠 by the DeepLint team</sub>
</div>