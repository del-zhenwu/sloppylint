"""Axis 3: Style/Taste (Soul) patterns - AI-specific comment patterns."""

from __future__ import annotations

import re

from deeplint.patterns.base import RegexPattern, Severity


class OverconfidentComment(RegexPattern):
    """Detect overconfident comments indicating false certainty."""

    id = "overconfident_comment"
    severity = Severity.MEDIUM
    axis = "style"
    message = "Overconfident comment - verify claim before shipping"
    # Removed "just" and "simply" - too common in natural language
    # Removed "basically" - commonly used legitimately
    pattern = re.compile(
        r"#\s*(obviously|clearly|trivial|of course)\b",
        re.IGNORECASE,
    )


class HedgingComment(RegexPattern):
    """Detect hedging comments indicating uncertainty."""

    id = "hedging_comment"
    severity = Severity.HIGH
    axis = "style"
    message = "Hedging comment suggests uncertainty - verify code works"
    # Removed "probably", "seems to", "appears to" - can be legitimate in context
    pattern = re.compile(
        r"#\s*(should work|hopefully|might work|try this|i think)\b",
        re.IGNORECASE,
    )


class ApologeticComment(RegexPattern):
    """Detect apologetic comments."""

    id = "apologetic_comment"
    severity = Severity.MEDIUM
    axis = "style"
    message = "Apologetic comment - fix the issue instead of apologizing"
    # Removed "hack" - legitimate code convention for documenting workarounds
    pattern = re.compile(
        r"#\s*(sorry|hacky|ugly|bad|terrible|awful|gross|yuck|forgive)\b", re.IGNORECASE
    )


STYLE_PATTERNS = [
    OverconfidentComment(),
    HedgingComment(),
    ApologeticComment(),
]
