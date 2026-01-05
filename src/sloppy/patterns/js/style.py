"""JavaScript/TypeScript - Style/Taste patterns."""

import re

from sloppy.patterns.base import RegexPattern, Severity


class JSOverconfidentComment(RegexPattern):
    """Detect overconfident comments in JS/TS."""

    id = "js_overconfident_comment"
    severity = Severity.MEDIUM
    axis = "style"
    message = "Overconfident comment - code should speak for itself"
    pattern = re.compile(
        r"//\s*(obviously|clearly|simply|just|easy|trivial|of course)\b",
        re.IGNORECASE,
    )


class JSHedgingComment(RegexPattern):
    """Detect hedging/uncertain comments in JS/TS."""

    id = "js_hedging_comment"
    severity = Severity.HIGH
    axis = "style"
    message = "Hedging comment indicates AI uncertainty - verify implementation"
    pattern = re.compile(
        r"//\s*(should work|hopefully|probably|might|try this|i think)\b",
        re.IGNORECASE,
    )


class JSPythonPatterns(RegexPattern):
    """Detect Python patterns leaked into JS/TS code."""

    id = "js_python_pattern"
    severity = Severity.HIGH
    axis = "style"
    message = "Python pattern in JS/TS code - use JavaScript idioms"
    # Only detecting patterns that are clearly Python-specific and invalid in JS
    pattern = re.compile(
        r'(\.append\()',
        re.IGNORECASE,
    )


class JSVarKeyword(RegexPattern):
    """Detect outdated var keyword in JS/TS."""

    id = "js_var_keyword"
    severity = Severity.MEDIUM
    axis = "style"
    message = "Use 'const' or 'let' instead of 'var'"
    pattern = re.compile(r'\bvar\s+\w+\s*=')


JS_STYLE_PATTERNS = [
    JSOverconfidentComment(),
    JSHedgingComment(),
    JSPythonPatterns(),
    JSVarKeyword(),
]
