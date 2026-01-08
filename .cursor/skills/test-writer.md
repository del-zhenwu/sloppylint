# Test Writer Skill

<!-- Thanks to: @rsionnach/sloppylint for inspiration on testing workflows -->

Write comprehensive tests for DeepLint detection patterns. This skill ensures your patterns work correctly and don't produce false positives.

## Prerequisites

- Pattern already implemented (see [pattern-creator.md](./pattern-creator.md))
- Familiarity with pytest
- Understanding of the pattern you're testing

## Testing Philosophy

DeepLint tests must verify:

1. **Detection** - Pattern catches what it should
2. **Non-detection** - Pattern doesn't flag correct code (no false positives)
3. **Edge cases** - Handles unusual but valid inputs
4. **Error handling** - Gracefully handles malformed input

## Test Organization

```
tests/
├── test_patterns/          # Python pattern tests
│   ├── test_noise.py
│   ├── test_hallucinations.py
│   ├── test_style.py
│   └── test_structure.py
├── test_go_patterns.py     # Go pattern tests
├── test_js_patterns.py     # JavaScript/TypeScript pattern tests
├── test_karpeslop_patterns.py  # React-specific tests
└── fixtures/               # Test code samples
    ├── python/
    ├── go/
    └── js/
```

## Step-by-Step Workflow

### Step 1: Create Test Fixtures

Test fixtures are code samples that your pattern should analyze.

#### Fixture Guidelines

1. **Positive cases** - Code that SHOULD trigger the pattern
2. **Negative cases** - Similar code that should NOT trigger
3. **Edge cases** - Boundary conditions
4. **Real examples** - Actual AI-generated code when possible

#### Example: Python Fixture

```python
# tests/fixtures/python/mutable_defaults.py

# ===== SHOULD DETECT =====

def bad_list_default(items=[]):
    """Mutable list default - classic AI mistake."""
    items.append(1)
    return items

def bad_dict_default(config={}):
    """Mutable dict default."""
    config['key'] = 'value'
    return config

def bad_set_default(tags=set()):
    """Mutable set default."""
    tags.add('new')
    return tags

# ===== SHOULD NOT DETECT =====

def good_none_default(items=None):
    """Correct pattern using None."""
    if items is None:
        items = []
    items.append(1)
    return items

def good_immutable_default(count=0, name="default"):
    """Immutable defaults are fine."""
    return count + 1, name.upper()

def good_no_defaults(items):
    """No defaults at all."""
    items.append(1)
    return items
```

#### Example: Go Fixture

```go
// tests/fixtures/go/debug_prints.go

package main

import "fmt"

// ===== SHOULD DETECT =====

func debugFunction() {
    fmt.Println("debug: starting process")
    fmt.Printf("DEBUG: value = %d\n", 42)
    fmt.Print("test: running test case")
}

// ===== SHOULD NOT DETECT =====

func productionFunction() {
    fmt.Println("Process completed successfully")
    fmt.Printf("Result: %d\n", 42)
    // Regular logging is fine
    fmt.Println("Application started")
}
```

#### Example: JavaScript/TypeScript Fixture

```typescript
// tests/fixtures/js/hallucinated_imports.ts

// ===== SHOULD DETECT =====

// Wrong: useRouter is from next/router, not react
import { useState, useRouter } from 'react';

// Wrong: Link is from next/link, not react
import { useEffect, Link } from 'react';

// Wrong: Multiple Next.js APIs from react
import { useRouter, Link, Head } from 'react';

// ===== SHOULD NOT DETECT =====

// Correct: React hooks from react
import { useState, useEffect, useMemo } from 'react';

// Correct: Next.js APIs from correct packages
import { useRouter } from 'next/router';
import Link from 'next/link';
import Head from 'next/head';

// Correct: Mixed imports done right
import React, { useState } from 'react';
```

### Step 2: Write Test Functions

#### Python Pattern Test Template

```python
# tests/test_patterns/test_hallucinations.py

import pytest
from pathlib import Path
from sloppy.detector import Detector
from sloppy.patterns.base import Severity


def test_mutable_default_arg_detected():
    """Test that mutable default arguments are detected."""
    detector = Detector()
    fixture_path = Path("tests/fixtures/python/mutable_defaults.py")
    
    issues = detector.scan_file(fixture_path)
    
    # Filter to just our pattern
    mutable_issues = [i for i in issues if i.pattern_id == "mutable_default_arg"]
    
    # Should detect at least 3 cases (list, dict, set)
    assert len(mutable_issues) >= 3, f"Expected 3+ issues, got {len(mutable_issues)}"
    
    # Should be CRITICAL severity
    for issue in mutable_issues:
        assert issue.severity == Severity.CRITICAL
        assert "mutable" in issue.message.lower()


def test_mutable_default_arg_no_false_positives():
    """Test that immutable defaults don't trigger false positives."""
    detector = Detector()
    fixture_path = Path("tests/fixtures/python/mutable_defaults.py")
    
    issues = detector.scan_file(fixture_path)
    mutable_issues = [i for i in issues if i.pattern_id == "mutable_default_arg"]
    
    # Check that good functions aren't flagged
    # We should have exactly 3 detections (list, dict, set), not more
    assert len(mutable_issues) == 3, (
        f"False positives detected: expected 3, got {len(mutable_issues)}"
    )


def test_mutable_default_arg_line_numbers():
    """Test that line numbers are reported correctly."""
    detector = Detector()
    fixture_path = Path("tests/fixtures/python/mutable_defaults.py")
    
    issues = detector.scan_file(fixture_path)
    mutable_issues = [i for i in issues if i.pattern_id == "mutable_default_arg"]
    
    # Sort by line number
    mutable_issues.sort(key=lambda x: x.line)
    
    # First issue should be on a reasonable line (not 0 or negative)
    assert mutable_issues[0].line > 0
```

#### Go/JS Pattern Test Template

```python
# tests/test_go_patterns.py

import pytest
from pathlib import Path
from sloppy.detector import Detector


def test_go_debug_print_detected():
    """Test that debug print statements in Go are detected."""
    detector = Detector()
    fixture_path = Path("tests/fixtures/go/debug_prints.go")
    
    issues = detector.scan_file(fixture_path)
    
    debug_issues = [i for i in issues if i.pattern_id == "go_debug_print"]
    
    # Should detect 3 debug statements
    assert len(debug_issues) >= 3, f"Expected 3+ debug prints, got {len(debug_issues)}"
    
    # Check language is set correctly
    for issue in debug_issues:
        assert issue.language == "go"


def test_go_debug_print_no_false_positives():
    """Test that regular Go logging doesn't trigger false positives."""
    detector = Detector()
    fixture_path = Path("tests/fixtures/go/debug_prints.go")
    
    issues = detector.scan_file(fixture_path)
    debug_issues = [i for i in issues if i.pattern_id == "go_debug_print"]
    
    # Should be exactly 3, not more (no false positives from production code)
    assert len(debug_issues) == 3
```

#### Multi-Language Test

```python
# tests/test_language_detector.py

def test_detector_handles_multiple_languages():
    """Test that detector correctly processes multiple languages."""
    from sloppy.detector import Detector
    from pathlib import Path
    
    detector = Detector()
    
    # Scan directory with mixed languages
    issues = detector.scan_directory(Path("tests/fixtures"))
    
    # Should find issues in all languages
    languages = {issue.language for issue in issues}
    assert "python" in languages
    assert "go" in languages
    assert "javascript" in languages
```

### Step 3: Test Edge Cases

Always test edge cases that might break your pattern:

```python
def test_mutable_default_empty_file():
    """Test handling of empty file."""
    detector = Detector()
    # Create temp empty file or use fixture
    issues = detector.scan_file(Path("tests/fixtures/python/empty.py"))
    assert issues == [] or all(i.pattern_id != "mutable_default_arg" for i in issues)


def test_mutable_default_syntax_error():
    """Test handling of file with syntax errors."""
    detector = Detector()
    # Should handle gracefully, not crash
    try:
        issues = detector.scan_file(Path("tests/fixtures/python/syntax_error.py"))
        # May return empty or partial results, but shouldn't crash
        assert isinstance(issues, list)
    except SyntaxError:
        # Acceptable - detector can reject malformed files
        pass


def test_mutable_default_nested_function():
    """Test detection in nested functions."""
    code = '''
def outer():
    def inner(items=[]):  # Should still detect
        items.append(1)
    return inner
'''
    # Test detection in nested context
    # ... implementation depends on your testing setup
```

### Step 4: Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_patterns/test_hallucinations.py -v

# Run specific test function
pytest tests/test_patterns/test_hallucinations.py::test_mutable_default_arg_detected -v

# Run with coverage
pytest tests/ --cov=src/sloppy --cov-report=term-missing

# Run tests for specific pattern (grep for test names)
pytest tests/ -k "mutable_default" -v
```

### Step 5: Check Coverage

Ensure your tests cover the pattern code:

```bash
# Generate coverage report
pytest tests/ --cov=src/sloppy/patterns --cov-report=html

# Open in browser
open htmlcov/index.html

# Look for your pattern file and ensure >90% coverage
```

### Step 6: Test Integration

Test that your pattern works in the full pipeline:

```bash
# Test on fixture
deeplint tests/fixtures/python/mutable_defaults.py

# Should see your pattern's output
# Example output:
# CRITICAL (3 issues)
# ============================================================
#   tests/fixtures/python/mutable_defaults.py:3  mutable_default_arg
#     Mutable default argument - use None instead
#     > def bad_list_default(items=[]):
```

## Common Test Patterns

### Testing Severity

```python
def test_pattern_severity():
    """Test that pattern has correct severity."""
    from sloppy.patterns.hallucinations import MutableDefaultArg
    
    pattern = MutableDefaultArg()
    assert pattern.severity == Severity.CRITICAL
```

### Testing Message Content

```python
def test_pattern_message():
    """Test that error message is helpful."""
    detector = Detector()
    issues = detector.scan_file(Path("tests/fixtures/python/mutable_defaults.py"))
    
    mutable_issues = [i for i in issues if i.pattern_id == "mutable_default_arg"]
    
    for issue in mutable_issues:
        # Message should mention the problem
        assert "mutable" in issue.message.lower()
        assert "none" in issue.message.lower() or "fix" in issue.message.lower()
```

### Testing Code Snippets

```python
def test_pattern_includes_code():
    """Test that issue includes code snippet."""
    detector = Detector()
    issues = detector.scan_file(Path("tests/fixtures/python/mutable_defaults.py"))
    
    mutable_issues = [i for i in issues if i.pattern_id == "mutable_default_arg"]
    
    for issue in mutable_issues:
        # Should include the problematic code
        assert issue.code is not None
        assert len(issue.code) > 0
```

### Parametrized Tests

For testing multiple similar cases:

```python
@pytest.mark.parametrize("language,fixture,pattern_id,expected_count", [
    ("python", "mutable_defaults.py", "mutable_default_arg", 3),
    ("go", "debug_prints.go", "go_debug_print", 3),
    ("javascript", "hallucinated_imports.ts", "js_hallucinated_react_import", 3),
])
def test_pattern_detection(language, fixture, pattern_id, expected_count):
    """Parametrized test for multiple patterns."""
    detector = Detector()
    fixture_path = Path(f"tests/fixtures/{language}/{fixture}")
    
    issues = detector.scan_file(fixture_path)
    pattern_issues = [i for i in issues if i.pattern_id == pattern_id]
    
    assert len(pattern_issues) >= expected_count
```

## Testing Best Practices

### DO:
- ✅ Test both detection and non-detection
- ✅ Use realistic examples from AI-generated code
- ✅ Test edge cases (empty files, syntax errors, nested structures)
- ✅ Verify line numbers and code snippets
- ✅ Check severity and message content
- ✅ Test cross-file behavior for structural patterns
- ✅ Use descriptive test names (`test_what_it_tests`)

### DON'T:
- ❌ Test only happy path (must test false positives!)
- ❌ Use trivial examples that don't reflect real code
- ❌ Ignore edge cases
- ❌ Forget to test error handling
- ❌ Write tests that depend on other tests
- ❌ Hardcode line numbers (fixtures may change)
- ❌ Skip documentation for complex tests

## Debugging Test Failures

### Test Passes But Should Fail

Pattern is too lenient:
1. Check regex boundaries (`\b`)
2. Verify AST node type checking
3. Add more specific conditions

### Test Fails But Should Pass

Pattern is too strict:
1. Check for false positives in fixtures
2. Review regex capturing groups
3. Verify node attribute checks

### Inconsistent Results

1. Check file encoding handling
2. Verify line ending handling (\\n vs \\r\\n)
3. Review regex flags (MULTILINE, DOTALL)

## Test Coverage Goals

- **Pattern code**: >90% coverage
- **Detector code**: >85% coverage
- **All axes**: Noise, Quality, Style, Structure
- **All languages**: Python, Go, JavaScript, TypeScript

## Resources

- **pytest docs**: https://docs.pytest.org/
- **Existing tests**: `tests/test_patterns/` for examples
- **conftest.py**: Shared fixtures and utilities
- **AGENTS.md**: Testing conventions and guidelines

## Checklist

Before submitting your tests:

- [ ] Positive test cases (detects what it should)
- [ ] Negative test cases (no false positives)
- [ ] Edge cases tested
- [ ] Line numbers verified
- [ ] Severity checked
- [ ] Message content validated
- [ ] Integration test passed (run `deeplint` on fixture)
- [ ] Coverage >90% for pattern code
- [ ] All tests pass locally
- [ ] Test names are descriptive

## Questions?

- Check [pattern-creator.md](./pattern-creator.md) for pattern implementation
- Review existing tests in `tests/` for examples
- See [AGENTS.md](../../AGENTS.md) for conventions
- Ask in GitHub issues or discussions
