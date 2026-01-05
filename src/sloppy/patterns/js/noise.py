"""JavaScript/TypeScript - Information Utility (Noise) patterns."""

import re

from sloppy.patterns.base import RegexPattern, Severity


class JSDebugConsole(RegexPattern):
    """Detect debug console statements in JS/TS."""

    id = "js_debug_console"
    severity = Severity.MEDIUM
    axis = "noise"
    message = "Debug console statement - remove before production"
    pattern = re.compile(
        r'\bconsole\.(log|debug|info|warn|error)\s*\([^)]*["\']?(debug|DEBUG|test|TEST|temp|TEMP)\b'
    )


class JSTodoComment(RegexPattern):
    """Detect TODO comments in JS/TS."""

    id = "js_todo_comment"
    severity = Severity.LOW
    axis = "noise"
    message = "TODO comment - track in issue tracker instead"
    pattern = re.compile(r"//\s*(TODO|FIXME|XXX|HACK)\s*:", re.IGNORECASE)


class JSRedundantComment(RegexPattern):
    """Detect redundant comments in JS/TS."""

    id = "js_redundant_comment"
    severity = Severity.MEDIUM
    axis = "noise"
    message = "Redundant comment restating obvious code"
    pattern = re.compile(
        r"//\s*(increment|decrement|set|assign|return|get|initialize|init|create)\s+\w+\s*$",
        re.IGNORECASE,
    )


class JSCommentedCode(RegexPattern):
    """Detect commented-out code in JS/TS."""

    id = "js_commented_code"
    severity = Severity.MEDIUM
    axis = "noise"
    message = "Commented-out code - remove or use version control"
    pattern = re.compile(
        r"//\s*(const|let|var|function|if\s*\(|for\s*\(|while\s*\(|return\s+)",
        re.IGNORECASE,
    )


JS_NOISE_PATTERNS = [
    JSDebugConsole(),
    JSTodoComment(),
    JSRedundantComment(),
    JSCommentedCode(),
]
