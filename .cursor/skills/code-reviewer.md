# Code Reviewer Skill

<!-- Thanks to: @rsionnach/sloppylint for inspiration on code review workflows -->

Review contributions to DeepLint effectively. This skill helps maintainers and contributors review PRs with quality and consistency.

## Review Philosophy

DeepLint code reviews focus on:

1. **Correctness** - Does it work? Are there edge cases?
2. **Simplicity** - Is it the minimal change needed?
3. **Testing** - Is it well-tested?
4. **No false positives** - Are there false detections?
5. **Documentation** - Is it documented?

## Quick Review Checklist

### Every PR Should Have:
- [ ] Clear description of what changed and why
- [ ] Tests that pass (check CI)
- [ ] No false positives demonstrated
- [ ] Documentation updated (if needed)
- [ ] Minimal, focused changes
- [ ] Follows project conventions

### Common Issues to Look For:
- [ ] Regex patterns without word boundaries (`\b`)
- [ ] Missing language attribute on non-Python patterns
- [ ] Pattern not registered in `__init__.py`
- [ ] Tests only check detection, not non-detection
- [ ] Fixtures missing negative examples
- [ ] Hardcoded line numbers in tests

## Review by Change Type

### 1. New Pattern Review

#### What to Check:

**Pattern Definition:**
```python
# Good: Clear, specific pattern
class MutableDefaultArg(BasePattern):
    id = "mutable_default_arg"  # Unique, descriptive
    severity = Severity.CRITICAL  # Appropriate level
    axis = "quality"  # Correct axis
    message = "Mutable default argument - use None instead"  # Actionable
```

**Common Issues:**
- ❌ Pattern ID conflicts with existing pattern
- ❌ Severity doesn't match impact (mutable default is CRITICAL, not LOW)
- ❌ Message isn't actionable ("Bad code" vs "Use None instead")
- ❌ Axis doesn't match pattern type

#### Testing:

**Good Test Structure:**
```python
def test_pattern_detected():
    """Test detection of actual problematic code."""
    issues = scan_fixture("pattern_test.py")
    pattern_issues = [i for i in issues if i.pattern_id == "pattern_name"]
    assert len(pattern_issues) >= 1  # Flexible count

def test_pattern_no_false_positives():
    """Test that good code isn't flagged."""
    issues = scan_fixture("pattern_test.py")
    pattern_issues = [i for i in issues if i.pattern_id == "pattern_name"]
    # Should only detect bad cases, not good ones
    assert len(pattern_issues) == 3  # Exact count if fixture is fixed
```

**Look for:**
- ✅ Both positive and negative test cases
- ✅ Fixture file with clear comments marking what should/shouldn't detect
- ✅ Edge cases tested (empty file, nested structures, etc.)
- ❌ Tests that only check count without verifying content
- ❌ Missing tests for false positives

#### Fixtures:

**Good Fixture Structure:**
```python
# tests/fixtures/python/mutable_defaults.py

# ===== SHOULD DETECT =====

def bad_list_default(items=[]):  # Mutable default
    items.append(1)

def bad_dict_default(config={}):  # Mutable default
    config['key'] = 'value'

# ===== SHOULD NOT DETECT =====

def good_none_default(items=None):  # Correct pattern
    if items is None:
        items = []

def good_no_default(items):  # No default
    items.append(1)
```

**Look for:**
- ✅ Clear separation of positive/negative cases
- ✅ Real-world examples, not trivial
- ✅ Edge cases (empty, None, complex nesting)
- ❌ Only positive cases (must test false positives!)
- ❌ Unrealistic examples

#### Registration:

```python
# src/sloppy/patterns/__init__.py or language-specific __init__.py

from .hallucinations import MutableDefaultArg  # ✅ Import added

PYTHON_PATTERNS = [
    # ... existing ...
    MutableDefaultArg(),  # ✅ Instance added to list
]
```

**Look for:**
- ❌ Pattern not imported
- ❌ Pattern not added to appropriate list
- ❌ Wrong language list (Python pattern in GO_PATTERNS)

### 2. Bug Fix Review

#### What to Check:

1. **Does it fix the issue?**
   - Run the test case from the issue
   - Verify the fix solves the problem

2. **Does it introduce new bugs?**
   - Check if fix is too broad
   - Look for edge cases that might break

3. **Is it minimal?**
   - Could it be simpler?
   - Does it change more than necessary?

**Example - Fixing False Positive:**

```python
# Before: Too broad
pattern = re.compile(r'print\(')  # Matches print_report()

# After: More specific
pattern = re.compile(r'\bprint\s*\(')  # Only matches print()
```

**Look for:**
- ✅ Test demonstrating the bug
- ✅ Fix is targeted and minimal
- ✅ Existing tests still pass
- ❌ Fix introduces new false positives
- ❌ Fix is too complex for the problem

### 3. Documentation Review

#### What to Check:

**README.md Changes:**
- ✅ Accurate description of features
- ✅ Examples work as shown
- ✅ Up-to-date with code

**AGENTS.md Changes:**
- ✅ Pattern registry is complete
- ✅ Conventions are clear
- ✅ Examples are correct

**Cursor Skills:**
- ✅ Step-by-step workflows
- ✅ Practical examples
- ✅ Referenced files exist

**Look for:**
- ❌ Outdated examples
- ❌ Incorrect code samples
- ❌ Missing patterns from registry
- ❌ Broken links

### 4. Performance Changes

#### What to Check:

1. **Benchmarks**
   - Are performance claims backed by data?
   - Test on large codebases

2. **Complexity**
   - Does it avoid O(n²) operations?
   - Are regex patterns efficient?

3. **Memory Usage**
   - Does it load entire files?
   - Are results cached appropriately?

**Look for:**
- ✅ Performance measurements provided
- ✅ Efficient algorithms (O(n) vs O(n²))
- ❌ Loading all files into memory
- ❌ Regex catastrophic backtracking

## Regex Pattern Review

### Common Regex Issues

#### 1. Missing Word Boundaries

```python
# Bad: Matches "print_report"
pattern = re.compile(r'print\(')

# Good: Only matches "print("
pattern = re.compile(r'\bprint\s*\(')
```

#### 2. Catastrophic Backtracking

```python
# Bad: Can cause exponential time
pattern = re.compile(r'(a+)+b')

# Good: Linear time
pattern = re.compile(r'a+b')
```

#### 3. Case Sensitivity

```python
# Good: Catches DEBUG, debug, Debug
pattern = re.compile(r'\bdebug\b', re.IGNORECASE)
```

#### 4. Multiline Patterns

```python
# For cross-line patterns
pattern = re.compile(r'pattern.*spans.*lines', re.MULTILINE | re.DOTALL)
```

### Testing Regex Patterns

**Recommended approach:**
1. Test on https://regex101.com with sample code
2. Create fixture with edge cases
3. Run tests to verify behavior
4. Check for false positives in real codebases

## AST Pattern Review

### Common AST Issues

#### 1. Not Handling All Node Types

```python
# Bad: Only checks FunctionDef
def check_node(self, node: ast.FunctionDef):
    ...

# Good: Also checks AsyncFunctionDef, Lambda
def check_node(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
    ...
```

#### 2. Not Using ast.unparse

```python
# Bad: Shows internal representation
code = ast.dump(node)

# Good: Shows actual code
code = ast.unparse(node) if hasattr(ast, 'unparse') else ast.dump(node)
```

#### 3. Not Checking Attributes

```python
# Bad: Assumes attributes exist
if node.decorator_list[0]:  # May raise IndexError

# Good: Check first
if node.decorator_list and len(node.decorator_list) > 0:
```

## Providing Feedback

### Positive Feedback Template

```
Great work! I particularly like:
- ✅ [Specific thing done well]
- ✅ [Another good point]

Minor suggestions:
- 💡 [Optional improvement]

Once [blocking issue] is addressed, this is ready to merge.
```

### Constructive Feedback Template

```
Thanks for the contribution! A few things to address:

**Blocking Issues:**
- ❌ [Must fix item 1]
- ❌ [Must fix item 2]

**Suggestions:**
- 💡 [Optional improvement]
- 💡 [Nice to have]

**Questions:**
- ❓ [Clarification needed]

Let me know if you need help with any of these!
```

### Request Changes Template

```
Thanks for the PR! Before merging, we need to address:

1. **False Positives**: [Explain the issue]
   ```python
   # This code shouldn't be flagged but is:
   def good_function():
       ...
   ```

2. **Test Coverage**: [What's missing]
   - Add test for [scenario]
   - Add fixture demonstrating [case]

3. **Documentation**: [What needs updating]
   - Update AGENTS.md pattern registry
   - Add example to README

Looking forward to your updates!
```

## Advanced Review Topics

### 1. Security Implications

**Check for:**
- Code execution vulnerabilities
- Path traversal issues
- Regex denial of service (ReDoS)
- Information disclosure

### 2. Backwards Compatibility

**Consider:**
- Does it break existing APIs?
- Will existing configs still work?
- Are there migration paths?

### 3. Cross-Language Consistency

**Verify:**
- Similar patterns across languages work similarly
- Severity levels are consistent
- Messages follow same format

## Testing the Review

### Local Testing

```bash
# Check out the PR branch
gh pr checkout [PR_NUMBER]

# Run tests
pytest tests/ -v

# Test manually
deeplint tests/fixtures/
deeplint src/

# Check specific pattern
pytest tests/ -k "pattern_name" -v

# Run on real code
deeplint ~/projects/some-python-project/
```

### CI Checks

Verify:
- ✅ All tests pass
- ✅ Coverage maintained/improved
- ✅ No new linting errors
- ✅ Documentation builds

## Common Review Comments

### Pattern Issues

```python
# Comment: Pattern too broad
"This pattern will match `print_report()`. Consider adding word boundaries: `\bprint\s*\(`"

# Comment: Missing language attribute
"Non-Python patterns need a `language` attribute: `language = 'go'`"

# Comment: Pattern not registered
"Don't forget to add this pattern to `PYTHON_PATTERNS` in `patterns/__init__.py`"
```

### Test Issues

```python
# Comment: Missing false positive test
"Please add a test verifying that correct code doesn't trigger this pattern. 
Example: A function with immutable defaults should not be flagged."

# Comment: Fragile test
"Avoid hardcoding line numbers as they may change. Use count assertions instead: 
`assert len(issues) == 3` rather than `assert issues[0].line == 42`"

# Comment: Missing edge cases
"Consider testing edge cases:
- Empty file
- Nested functions
- Async functions (if applicable)"
```

### Documentation Issues

```python
# Comment: Pattern not documented
"Please add this pattern to the pattern registry in AGENTS.md under the appropriate axis"

# Comment: Example needed
"Could you add an example to README.md showing what this pattern catches?"
```

## Review Quality Checklist

Before approving:
- [ ] Code is correct and handles edge cases
- [ ] Tests are comprehensive (positive and negative)
- [ ] No false positives demonstrated
- [ ] Documentation is updated
- [ ] Changes are minimal and focused
- [ ] CI passes
- [ ] Manually tested locally
- [ ] Security implications considered
- [ ] Backwards compatibility maintained

## After Approval

1. **Merge** - Use "Squash and merge" for clean history
2. **Thank contributor** - Positive feedback encourages more contributions
3. **Close related issues** - Link to merged PR
4. **Update milestones** - Track progress

## Resources

- **AGENTS.md** - Development conventions
- **pattern-creator.md** - Pattern implementation guide
- **test-writer.md** - Testing guidelines
- **CI logs** - Check why tests failed
- **GitHub PR template** - Standard PR structure

## Questions?

- Review existing PRs for examples
- Ask other maintainers for second opinions
- When in doubt, request clarification from contributor
- Better to ask for more tests than merge with false positives

## Remember

- Be kind and constructive
- Assume good intent
- Explain the "why" behind requests
- Thank contributors for their time
- Fast feedback is better than perfect feedback
