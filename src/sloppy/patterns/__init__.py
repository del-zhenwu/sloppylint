"""Pattern registry."""

from sloppy.patterns.base import BasePattern
from sloppy.patterns.go import GO_NOISE_PATTERNS, GO_STYLE_PATTERNS
from sloppy.patterns.hallucinations import HALLUCINATION_PATTERNS
from sloppy.patterns.js import JS_NOISE_PATTERNS, JS_STYLE_PATTERNS
from sloppy.patterns.noise import NOISE_PATTERNS
from sloppy.patterns.structure import STRUCTURE_PATTERNS
from sloppy.patterns.style import STYLE_PATTERNS


def get_all_patterns() -> list[BasePattern]:
    """Get all registered patterns."""
    return [
        # Python patterns
        *NOISE_PATTERNS,
        *HALLUCINATION_PATTERNS,
        *STYLE_PATTERNS,
        *STRUCTURE_PATTERNS,
        # Go patterns
        *GO_NOISE_PATTERNS,
        *GO_STYLE_PATTERNS,
        # JavaScript/TypeScript patterns
        *JS_NOISE_PATTERNS,
        *JS_STYLE_PATTERNS,
    ]


__all__ = ["get_all_patterns", "BasePattern"]
