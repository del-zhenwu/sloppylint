"""JavaScript/TypeScript language-specific patterns."""

from sloppy.patterns.js.hallucinations import JS_HALLUCINATION_PATTERNS
from sloppy.patterns.js.noise import JS_NOISE_PATTERNS
from sloppy.patterns.js.react import JS_REACT_PATTERNS
from sloppy.patterns.js.structure import JS_STRUCTURE_PATTERNS
from sloppy.patterns.js.style import JS_STYLE_PATTERNS
from sloppy.patterns.js.typescript import JS_TYPESCRIPT_PATTERNS

__all__ = [
    "JS_NOISE_PATTERNS",
    "JS_STYLE_PATTERNS",
    "JS_HALLUCINATION_PATTERNS",
    "JS_REACT_PATTERNS",
    "JS_TYPESCRIPT_PATTERNS",
    "JS_STRUCTURE_PATTERNS",
]
