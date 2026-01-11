"""Go language - Style/Taste patterns."""

import re

from deeplint.patterns.base import RegexPattern, Severity


class GoOverconfidentComment(RegexPattern):
    """Detect overconfident comments in Go."""

    id = "go_overconfident_comment"
    severity = Severity.MEDIUM
    axis = "style"
    message = "Overconfident comment - code should speak for itself"
    supported_languages = ["go"]
    # Removed "just", "simply", "easy" - too common in natural language
    pattern = re.compile(
        r"//\s*(obviously|clearly|trivial|of course)\b",
        re.IGNORECASE,
    )


class GoHedgingComment(RegexPattern):
    """Detect hedging/uncertain comments in Go."""

    id = "go_hedging_comment"
    severity = Severity.HIGH
    axis = "style"
    message = "Hedging comment indicates AI uncertainty - verify implementation"
    supported_languages = ["go"]
    # Removed "probably", "might" - can be legitimate in context
    pattern = re.compile(
        r"//\s*(should work|hopefully|try this|i think)\b",
        re.IGNORECASE,
    )


GO_STYLE_PATTERNS = [
    GoOverconfidentComment(),
    GoHedgingComment(),
]
