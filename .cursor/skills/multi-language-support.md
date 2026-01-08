# Multi-Language Support Skill

<!-- Thanks to: @rsionnach/sloppylint for inspiration on language detection patterns -->

Add support for new programming languages or expand existing language support in DeepLint.

## Current Language Support

| Language | Extension | Detection Method | Status |
|----------|-----------|------------------|--------|
| Python | .py, .pyw | AST + Regex | ✅ Full support |
| Go | .go | Regex | ✅ Basic support |
| JavaScript | .js, .jsx, .mjs, .cjs | Regex | ✅ Good support |
| TypeScript | .ts, .tsx | Regex | ✅ Good support |

## Adding a New Language

### Step 1: Assess Feasibility

**Consider:**
- Is there Python AST parsing available? (e.g., via `ast` module)
- Can we use regex patterns effectively?
- Are there common AI mistakes in this language?
- Is there community interest?

**Good candidates:**
- Rust - Many Python developers learning it
- Java - AI generates lots of Java code
- C# - Similar to Java, AI patterns overlap
- PHP - Web development, AI often gets it wrong
- Ruby - DSL heavy, AI struggles with idioms

### Step 2: Update Language Detection

Edit `src/sloppy/language_detector.py`:

```python
LANGUAGE_EXTENSIONS = {
    'python': {'.py', '.pyw'},
    'go': {'.go'},
    'javascript': {'.js', '.jsx', '.mjs', '.cjs'},
    'typescript': {'.ts', '.tsx'},
    'rust': {'.rs'},  # New language
}

def detect_language(file_path: Path) -> str:
    """Detect programming language from file extension."""
    suffix = file_path.suffix.lower()
    
    for language, extensions in LANGUAGE_EXTENSIONS.items():
        if suffix in extensions:
            return language
    
    return 'unknown'
```

### Step 3: Create Pattern Directory

```bash
mkdir -p src/sloppy/patterns/rust
touch src/sloppy/patterns/rust/__init__.py
touch src/sloppy/patterns/rust/noise.py
touch src/sloppy/patterns/rust/style.py
```

### Step 4: Implement Patterns

#### Example: Rust Debug Print Pattern

```python
# src/sloppy/patterns/rust/noise.py

import re
from sloppy.patterns.base import RegexPattern, Severity

class RustDebugPrint(RegexPattern):
    """Detect debug print statements in Rust code."""
    
    id = "rust_debug_print"
    severity = Severity.MEDIUM
    axis = "noise"
    message = "Debug print statement - consider using tracing or log crate"
    language = "rust"
    
    pattern = re.compile(
        r'\b(println!|dbg!|print!)\s*\([^)]*"(debug|DEBUG|test|TEST)\b',
        re.IGNORECASE
    )

class RustTodoComment(RegexPattern):
    """Detect TODO comments in Rust code."""
    
    id = "rust_todo_comment"
    severity = Severity.LOW
    axis = "noise"
    message = "TODO comment - track in issue tracker instead"
    language = "rust"
    
    pattern = re.compile(
        r'//\s*(TODO|FIXME|XXX|HACK)[\s:]',
        re.IGNORECASE
    )
```

#### Example: Rust Style Pattern

```python
# src/sloppy/patterns/rust/style.py

import re
from sloppy.patterns.base import RegexPattern, Severity

class RustPanicInProduction(RegexPattern):
    """Detect panic! in production code."""
    
    id = "rust_panic"
    severity = Severity.HIGH
    axis = "style"
    message = "panic! should be avoided in library code - use Result instead"
    language = "rust"
    
    pattern = re.compile(
        r'\bpanic!\s*\(',
        re.MULTILINE
    )

class RustUnwrapAbuse(RegexPattern):
    """Detect excessive .unwrap() usage."""
    
    id = "rust_unwrap_abuse"
    severity = Severity.MEDIUM
    axis = "style"
    message = "Consider using ? operator or proper error handling instead of .unwrap()"
    language = "rust"
    
    pattern = re.compile(
        r'\.unwrap\s*\(\)',
        re.MULTILINE
    )
```

### Step 5: Register Patterns

```python
# src/sloppy/patterns/rust/__init__.py

from .noise import RustDebugPrint, RustTodoComment
from .style import RustPanicInProduction, RustUnwrapAbuse

RUST_PATTERNS = [
    RustDebugPrint(),
    RustTodoComment(),
    RustPanicInProduction(),
    RustUnwrapAbuse(),
]
```

### Step 6: Update Main Pattern Registry

```python
# src/sloppy/patterns/__init__.py

from .rust import RUST_PATTERNS  # Import new language patterns

def get_patterns(languages: set[str] = None) -> list[BasePattern]:
    """Get patterns for specified languages."""
    all_patterns = {
        'python': PYTHON_PATTERNS,
        'go': GO_PATTERNS,
        'javascript': JS_PATTERNS,
        'typescript': JS_PATTERNS,  # JS and TS share patterns
        'rust': RUST_PATTERNS,  # Add new language
    }
    
    if languages is None:
        # Return all patterns
        return [p for patterns in all_patterns.values() for p in patterns]
    
    # Filter by language
    result = []
    for lang in languages:
        if lang in all_patterns:
            result.extend(all_patterns[lang])
    return result
```

### Step 7: Create Test Fixtures

```rust
// tests/fixtures/rust/debug_prints.rs

// ===== SHOULD DETECT =====

fn debug_function() {
    println!("debug: starting process");
    println!("DEBUG: value = {}", 42);
    dbg!(value);
    print!("test: running test");
}

// TODO: implement this function
fn todo_function() {
    // FIXME: handle edge case
    unimplemented!()
}

// ===== SHOULD NOT DETECT =====

fn production_function() {
    println!("Process completed successfully");
    println!("Result: {}", 42);
    // Regular logging is fine
    log::info!("Application started");
}
```

```rust
// tests/fixtures/rust/style_issues.rs

// ===== SHOULD DETECT =====

fn panic_abuse() {
    if condition {
        panic!("This is bad!");  // Should detect
    }
}

fn unwrap_abuse() {
    let value = some_option.unwrap();  // Should detect
    let result = some_result.unwrap(); // Should detect
}

// ===== SHOULD NOT DETECT =====

fn proper_error_handling() -> Result<(), Error> {
    let value = some_option.ok_or(Error::Missing)?;
    let result = some_result?;
    Ok(())
}
```

### Step 8: Write Tests

```python
# tests/test_rust_patterns.py

import pytest
from pathlib import Path
from sloppy.detector import Detector
from sloppy.patterns.base import Severity


def test_rust_debug_print_detected():
    """Test that debug prints in Rust are detected."""
    detector = Detector()
    fixture_path = Path("tests/fixtures/rust/debug_prints.rs")
    
    issues = detector.scan_file(fixture_path)
    
    debug_issues = [i for i in issues if i.pattern_id == "rust_debug_print"]
    assert len(debug_issues) >= 4, f"Expected 4+ debug prints, got {len(debug_issues)}"
    
    for issue in debug_issues:
        assert issue.language == "rust"
        assert issue.severity == Severity.MEDIUM


def test_rust_panic_detected():
    """Test that panic! usage is detected."""
    detector = Detector()
    fixture_path = Path("tests/fixtures/rust/style_issues.rs")
    
    issues = detector.scan_file(fixture_path)
    
    panic_issues = [i for i in issues if i.pattern_id == "rust_panic"]
    assert len(panic_issues) >= 1


def test_rust_unwrap_detected():
    """Test that .unwrap() abuse is detected."""
    detector = Detector()
    fixture_path = Path("tests/fixtures/rust/style_issues.rs")
    
    issues = detector.scan_file(fixture_path)
    
    unwrap_issues = [i for i in issues if i.pattern_id == "rust_unwrap_abuse"]
    assert len(unwrap_issues) >= 2


def test_rust_no_false_positives():
    """Test that proper Rust code doesn't trigger false positives."""
    detector = Detector()
    fixture_path = Path("tests/fixtures/rust/style_issues.rs")
    
    issues = detector.scan_file(fixture_path)
    
    # Should not detect issues in proper_error_handling function
    # This requires checking line numbers or code content
    for issue in issues:
        assert "proper_error_handling" not in issue.code
```

### Step 9: Update Documentation

Add to **AGENTS.md**:

```markdown
### Rust Patterns (4 total)

#### Noise (2)
- `rust_debug_print` - Debug print statements with "debug", "test", "temp"
- `rust_todo_comment` - TODO/FIXME/XXX/HACK comments

#### Style (2)
- `rust_panic` - panic! usage in production code
- `rust_unwrap_abuse` - Excessive .unwrap() instead of proper error handling
```

Add to **README.md**:

```markdown
| Language | File Extensions | Status |
|----------|----------------|--------|
| **Rust** | `.rs` | ✅ Pattern detection |
```

### Step 10: Test Integration

```bash
# Test on Rust fixture
deeplint tests/fixtures/rust/

# Should see Rust patterns detected
```

## Expanding Existing Language Support

### Adding More Python Patterns (AST-Based)

Since Python has full AST support, you can add sophisticated patterns:

```python
# Example: Detect missing error handling
class MissingErrorHandling(BasePattern):
    """Detect functions that call risky operations without try/except."""
    
    id = "missing_error_handling"
    severity = Severity.MEDIUM
    axis = "structure"
    message = "Risky operation without error handling"
    
    RISKY_FUNCTIONS = {'open', 'json.loads', 'requests.get', 'int', 'float'}
    
    def check_node(self, node: ast.FunctionDef) -> list[Issue]:
        issues = []
        
        # Find all call nodes
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                func_name = self._get_func_name(child)
                if func_name in self.RISKY_FUNCTIONS:
                    # Check if inside try/except
                    if not self._is_in_try_except(child, node):
                        issues.append(self.create_issue(child, code=func_name))
        
        return issues
```

### Adding More Go/JS/TS Patterns (Regex-Based)

Common AI mistakes in each language:

#### Go Pattern Ideas
- Missing error checks: `_, err := func()` without `if err != nil`
- Goroutine leaks: `go func()` without context or cleanup
- Channel patterns: Unbuffered channels in wrong contexts

#### JavaScript Pattern Ideas
- Missing await: `async function` calling other async without await
- Promise rejection: `.then()` without `.catch()`
- Memory leaks: Event listeners without cleanup

#### TypeScript Pattern Ideas
- Type assertions: `as any` abuse
- Missing null checks: Property access without optional chaining
- Enum abuse: String literals that should be enums

### Example: Advanced TypeScript Pattern

```python
class TypeScriptMissingNullCheck(RegexPattern):
    """Detect property access without null checking."""
    
    id = "ts_missing_null_check"
    severity = Severity.HIGH
    axis = "quality"
    message = "Property access may throw if object is null - use optional chaining (?.)"
    language = "typescript"
    
    # Matches: user.profile.name but not user?.profile?.name
    pattern = re.compile(
        r'\b\w+\.(?!\?)\w+\.(?!\?)\w+',  # Nested property access without ?.
        re.MULTILINE
    )
    
    def match(self, text: str, file_path: Path) -> list[Issue]:
        # Override to add context checking
        issues = super().match(text, file_path)
        
        # Filter out false positives (e.g., inside null checks)
        filtered = []
        for issue in issues:
            # Get surrounding lines
            lines = text.split('\n')
            line_idx = issue.line - 1
            
            # Check if inside if statement checking for null
            if line_idx > 0:
                prev_line = lines[line_idx - 1]
                if 'if' in prev_line and ('null' in prev_line or 'undefined' in prev_line):
                    continue  # Skip - it's in a null check
            
            filtered.append(issue)
        
        return filtered
```

## Testing Multi-Language Projects

### Test Auto-Detection

```python
def test_multilanguage_detection():
    """Test that detector handles multiple languages correctly."""
    detector = Detector()
    
    # Scan directory with mixed languages
    issues = detector.scan_directory(Path("tests/fixtures"))
    
    # Group by language
    by_language = {}
    for issue in issues:
        lang = issue.language
        by_language.setdefault(lang, []).append(issue)
    
    # Verify each language has issues
    assert 'python' in by_language
    assert 'go' in by_language
    assert 'javascript' in by_language
    assert 'rust' in by_language
    
    # Verify patterns are language-specific
    for lang, lang_issues in by_language.items():
        for issue in lang_issues:
            assert issue.language == lang
```

### Test Language Filtering

```python
def test_language_filter():
    """Test --language flag filters correctly."""
    detector = Detector(languages={'rust'})
    
    issues = detector.scan_directory(Path("tests/fixtures"))
    
    # Should only have Rust issues
    languages = {issue.language for issue in issues}
    assert languages == {'rust'}
```

## Common Patterns Across Languages

Some patterns apply to multiple languages:

### Debug/Logging Patterns
- Print statements with "debug", "test", "temp"
- Console.log in JavaScript (for production)
- fmt.Println in Go (for libraries)

### TODO Comments
- Almost universal: TODO, FIXME, XXX, HACK

### Overconfident Comments
- "obviously", "clearly", "simply"
- Language-independent wording

### Cross-Language Pattern Detection

Detect when AI mixes language patterns:

```python
class PythonInRust(RegexPattern):
    """Detect Python patterns in Rust code."""
    
    id = "rust_python_pattern"
    severity = Severity.HIGH
    axis = "quality"
    message = "Python pattern in Rust code"
    language = "rust"
    
    patterns = [
        re.compile(r'\.append\('),     # Python list method
        re.compile(r'\.len\(\)'),      # Python len() used as method
        re.compile(r'\bdef\s+\w+'),    # Python def keyword
        re.compile(r'\.split\(\)'),    # Python string method (should be .split_whitespace())
    ]
    
    def match(self, text: str, file_path: Path) -> list[Issue]:
        issues = []
        for pattern in self.patterns:
            for match in pattern.finditer(text):
                # ... create issues
        return issues
```

## Documentation Requirements

When adding language support:

1. **Update AGENTS.md** - Add pattern list
2. **Update README.md** - Add to supported languages table
3. **Add examples** - Show common patterns in README
4. **Update CLI help** - If adding new flags

## Checklist

- [ ] Language detection added to `language_detector.py`
- [ ] Pattern directory created (`patterns/LANGUAGE/`)
- [ ] At least 4-6 patterns implemented
- [ ] Patterns registered in `__init__.py`
- [ ] Test fixtures created
- [ ] Tests written and passing
- [ ] Integration tested with `deeplint`
- [ ] AGENTS.md updated
- [ ] README.md updated
- [ ] Examples added to documentation

## Resources

- **Language specifications**: Official docs for the language
- **Common mistakes**: Search for "common X mistakes" or "X anti-patterns"
- **AI-generated examples**: Generate code with AI and look for issues
- **Regex testing**: https://regex101.com/
- **Existing patterns**: `src/sloppy/patterns/` for examples

## Questions?

- Review existing language support in `patterns/go/` or `patterns/js/`
- See [pattern-creator.md](./pattern-creator.md) for pattern implementation
- Check [test-writer.md](./test-writer.md) for testing guidelines
- Ask in GitHub issues or discussions
