# Pattern Creator Skill

<!-- Thanks to: @rsionnach/sloppylint for inspiration on pattern detection workflows -->

Create new AI slop detection patterns for DeepLint. This skill guides you through adding patterns for Python, Go, JavaScript, and TypeScript.

## Prerequisites

- Familiarity with the target language
- Understanding of AST concepts (for Python patterns)
- Knowledge of regex (for Go/JS/TS patterns)
- Read [AGENTS.md](../../AGENTS.md) for project conventions

## Pattern Types

DeepLint detects patterns across four axes:

1. **Noise** - Redundant information (debug code, obvious comments)
2. **Quality** - Incorrect information (hallucinations, placeholders, bugs)
3. **Style** - Poor taste (god functions, overconfident comments)
4. **Structure** - Anti-patterns (bare except, unused imports)

## Step-by-Step Workflow

### Step 1: Identify the Pattern

**What to detect:**
- Common mistakes in AI-generated code
- Language-specific anti-patterns
- Cross-language pattern leakage
- Runtime bugs that look correct

**Example patterns to inspire you:**
```python
# Mutable default argument (Python)
def process(items=[]):  # Bug: shared state
    items.append(1)

# React import hallucination (JS/TS)
import { useRouter } from 'react';  # Bug: should be 'next/router'

# Python pattern in Go
if err.nil?  // Bug: Go doesn't have .nil?
```

### Step 2: Choose Implementation Method

#### For Python: AST-Based or Regex

**Use AST when:**
- Detecting syntax structures (function defs, imports, try/except)
- Checking variable assignments
- Analyzing control flow

**Use Regex when:**
- Detecting comment patterns
- Finding string patterns
- Cross-language pattern detection

#### For Go/JS/TS: Regex-Based

All non-Python patterns use regex matching on source text.

### Step 3: Implement the Pattern

#### Python AST Pattern

Create in appropriate file: `src/sloppy/patterns/{noise|hallucinations|style|structure}.py`

```python
from sloppy.patterns.base import BasePattern, Issue, Severity

class MutableDefaultArg(BasePattern):
    """Detect mutable default arguments in function definitions."""
    
    id = "mutable_default_arg"
    severity = Severity.CRITICAL
    axis = "quality"  # noise | quality | style | structure
    message = "Mutable default argument - use None instead"
    
    def check_node(self, node: ast.FunctionDef) -> list[Issue]:
        """Check a function definition for mutable defaults."""
        issues = []
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                code = ast.unparse(default) if hasattr(ast, 'unparse') else ast.dump(default)
                issues.append(self.create_issue(
                    node=node,
                    code=code,
                    line=node.lineno
                ))
        return issues
```

#### Python Regex Pattern

```python
import re
from sloppy.patterns.base import RegexPattern, Severity

class OverconfidentComment(RegexPattern):
    """Detect overconfident language in comments."""
    
    id = "overconfident_comment"
    severity = Severity.MEDIUM
    axis = "style"
    message = "Overconfident comment - avoid 'obviously', 'clearly', 'simply'"
    
    pattern = re.compile(
        r'#\s*(obviously|clearly|simply|just|easy|trivial)\b',
        re.IGNORECASE
    )
```

#### Go Pattern

Create in: `src/sloppy/patterns/go/{noise|style}.py`

```python
import re
from sloppy.patterns.base import RegexPattern, Severity

class GoDebugPrint(RegexPattern):
    """Detect debug print statements in Go code."""
    
    id = "go_debug_print"
    severity = Severity.MEDIUM
    axis = "noise"
    message = "Debug print statement - remove before production"
    language = "go"
    
    pattern = re.compile(
        r'\bfmt\.Print(ln|f)?\s*\([^)]*"(debug|DEBUG|test|TEST)\b',
        re.IGNORECASE
    )
```

#### JavaScript/TypeScript Pattern

Create in: `src/sloppy/patterns/js/{noise|style|hallucinations|react|typescript|structure}.py`

```python
import re
from sloppy.patterns.base import RegexPattern, Severity

class HallucinatedReactImport(RegexPattern):
    """Detect React APIs imported from wrong packages."""
    
    id = "js_hallucinated_react_import"
    severity = Severity.HIGH
    axis = "quality"
    message = "Hallucinated import - useRouter and Link are from Next.js packages"
    language = "javascript"  # Also applies to TypeScript
    
    pattern = re.compile(
        r'import\s+\{[^}]*(useRouter|Link)[^}]*\}\s+from\s+[\'"]react[\'"]',
        re.MULTILINE
    )
```

### Step 4: Register the Pattern

#### Python Patterns

Add to `src/sloppy/patterns/__init__.py`:

```python
from .noise import MutableDefaultArg  # Import your pattern

PYTHON_PATTERNS = [
    # ... existing patterns ...
    MutableDefaultArg(),  # Add your pattern
]
```

#### Go Patterns

Add to `src/sloppy/patterns/go/__init__.py`:

```python
from .noise import GoDebugPrint

GO_PATTERNS = [
    # ... existing patterns ...
    GoDebugPrint(),
]
```

#### JS/TS Patterns

Add to `src/sloppy/patterns/js/__init__.py`:

```python
from .hallucinations import HallucinatedReactImport

JS_PATTERNS = [
    # ... existing patterns ...
    HallucinatedReactImport(),
]
```

### Step 5: Create Test Fixtures

Create test files in `tests/fixtures/{python|go|js}/`:

#### Python Fixture Example
```python
# tests/fixtures/python/mutable_defaults.py

# This should be detected
def bad_function(items=[]):
    items.append(1)
    return items

# This should NOT be detected
def good_function(items=None):
    if items is None:
        items = []
    items.append(1)
    return items
```

#### Go Fixture Example
```go
// tests/fixtures/go/debug_prints.go

package main

import "fmt"

func processData() {
    // This should be detected
    fmt.Println("debug: processing data")
    
    // This should NOT be detected
    fmt.Println("Processing complete")
}
```

#### JS/TS Fixture Example
```typescript
// tests/fixtures/js/hallucinated_imports.ts

// This should be detected
import { useRouter, Link } from 'react';

// This should NOT be detected
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
```

### Step 6: Write Tests

#### Python Pattern Tests

Add to appropriate test file in `tests/test_patterns/`:

```python
def test_mutable_default_detected():
    """Test that mutable default arguments are detected."""
    from sloppy.detector import Detector
    
    detector = Detector()
    issues = detector.scan_file("tests/fixtures/python/mutable_defaults.py")
    
    mutable_issues = [i for i in issues if i.pattern_id == "mutable_default_arg"]
    assert len(mutable_issues) >= 1
    assert mutable_issues[0].severity == Severity.CRITICAL

def test_none_default_not_flagged():
    """Test that None defaults don't trigger false positives."""
    from sloppy.detector import Detector
    
    detector = Detector()
    issues = detector.scan_file("tests/fixtures/python/mutable_defaults.py")
    
    # Check that good_function doesn't trigger the pattern
    # This requires checking line numbers or more sophisticated analysis
```

#### Go/JS Pattern Tests

Add to `tests/test_go_patterns.py` or `tests/test_js_patterns.py`:

```python
def test_go_debug_print_detected():
    """Test that debug prints in Go are detected."""
    from sloppy.detector import Detector
    
    detector = Detector()
    issues = detector.scan_file("tests/fixtures/go/debug_prints.go")
    
    debug_issues = [i for i in issues if i.pattern_id == "go_debug_print"]
    assert len(debug_issues) >= 1
```

### Step 7: Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_patterns/test_hallucinations.py -v

# Run with coverage
pytest tests/ --cov=src/sloppy --cov-report=term-missing
```

### Step 8: Test Locally

```bash
# Test on your fixture file
deeplint tests/fixtures/python/mutable_defaults.py

# Test on real code
deeplint src/

# Test with specific severity
deeplint tests/fixtures/ --severity high
```

### Step 9: Document in AGENTS.md

Add your pattern to the pattern registry in [AGENTS.md](../../AGENTS.md):

```markdown
### Python Patterns (47 total)

#### Axis 2: Quality/Hallucinations (15)
- `mutable_default_arg` - Mutable default arguments (NEW!)
- ... existing patterns ...
```

## Tips & Best Practices

### Pattern Design

1. **Be specific** - Avoid overly broad patterns that cause false positives
2. **Include context** - Good error messages help developers fix issues
3. **Test edge cases** - What looks like a match might not be
4. **Consider language idioms** - Some patterns are idiomatic in some languages

### Regex Patterns

1. **Use word boundaries** (`\b`) to avoid partial matches
2. **Consider case sensitivity** - Use `re.IGNORECASE` when appropriate
3. **Test multiline patterns** - Use `re.MULTILINE` or `re.DOTALL` as needed
4. **Escape special characters** - `\(`, `\[`, `\.`, etc.

### AST Patterns

1. **Handle all node types** - Functions, methods, lambdas all need checking
2. **Check parent context** - Sometimes context matters
3. **Use `ast.unparse()`** - Show actual code, not abstract representation
4. **Visit recursively** - Don't forget nested structures

### Testing

1. **Test both detection AND non-detection** - False negatives and false positives
2. **Use real-world examples** - Actual AI-generated code is best
3. **Test edge cases** - Empty strings, None, nested structures
4. **Check line numbers** - Ensure issues point to the right place

### Common Pitfalls

- **Regex too broad** - Matches too much, causes false positives
- **Regex too narrow** - Misses valid cases
- **Not handling variations** - `fmt.Println()` vs `fmt.Print()` vs `fmt.Printf()`
- **Forgetting imports** - Pattern file must import all dependencies
- **Not registering pattern** - Pattern must be added to registry
- **Missing test fixtures** - Need both positive and negative examples

## Pattern Ideas

Looking for patterns to implement? Consider:

### Python
- Global variable abuse
- Circular import patterns
- Missing `__init__` in packages
- Incorrect use of `is` vs `==`
- Memory leaks (circular references)

### Go
- Missing error checks (`err != nil`)
- Goroutine leaks
- Channel usage anti-patterns
- Panic/recover abuse

### JavaScript/TypeScript
- Missing `await` on promises
- Incorrect `this` binding
- Memory leaks in closures
- XSS vulnerabilities in templates
- Missing null checks before property access

### Cross-Language
- SQL injection patterns
- Path traversal vulnerabilities
- Hardcoded credentials
- Insecure random number generation

## Resources

- **AGENTS.md** - Full development guide and conventions
- **tests/test_patterns/** - Example tests for all pattern types
- **src/sloppy/patterns/base.py** - Pattern base classes
- **Python AST docs** - https://docs.python.org/3/library/ast.html
- **Regex testing** - https://regex101.com/

## Questions?

- Check [AGENTS.md](../../AGENTS.md) for detailed conventions
- Look at existing patterns for examples
- Search tests for usage patterns
- Ask in GitHub issues or discussions
