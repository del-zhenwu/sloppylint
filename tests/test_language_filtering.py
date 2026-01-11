"""Tests for language-specific pattern filtering.

Ensures that patterns only run on files of the appropriate language.
"""

from pathlib import Path

from deeplint.detector import Detector
from deeplint.patterns import get_all_patterns

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _get_python_only_pattern_ids() -> set[str]:
    """Get pattern IDs that are Python-only (not Go or JS/TS specific).
    
    Returns:
        Set of pattern IDs for Python-only patterns
    """
    return {
        p.id for p in get_all_patterns() 
        if not p.id.startswith("go_") 
        and not p.id.startswith("js_")
        and not p.id.startswith("ts_")
        and (p.supported_languages is None or "python" in p.supported_languages)
    }


class TestLanguageSpecificFiltering:
    """Test that patterns are filtered by language."""

    def test_go_patterns_not_applied_to_python(self) -> None:
        """Go patterns should not be applied to Python files."""
        # This Python file uses .append() which is valid Python
        # but would trigger go_python_pattern if not filtered properly
        python_file = Path(__file__).parent / "corpus" / "false_positives" / "valid_python_methods.py"
        
        detector = Detector(languages=["python"])
        issues = detector.scan([python_file])
        
        # Should not find go_python_pattern issues
        go_pattern_issues = [i for i in issues if i.pattern_id.startswith("go_")]
        assert len(go_pattern_issues) == 0, f"Go patterns should not trigger on Python files: {go_pattern_issues}"

    def test_js_patterns_not_applied_to_python(self) -> None:
        """JavaScript patterns should not be applied to Python files."""
        # This Python file uses .append() which is valid Python
        # but would trigger js_python_pattern if not filtered properly
        python_file = Path(__file__).parent / "corpus" / "false_positives" / "valid_python_methods.py"
        
        detector = Detector(languages=["python"])
        issues = detector.scan([python_file])
        
        # Should not find js_python_pattern issues
        js_pattern_issues = [i for i in issues if i.pattern_id.startswith("js_")]
        assert len(js_pattern_issues) == 0, f"JS patterns should not trigger on Python files: {js_pattern_issues}"

    def test_python_patterns_not_applied_to_go(self) -> None:
        """Python patterns should not be applied to Go files."""
        go_file = FIXTURES_DIR / "go" / "clean_code.go"
        
        detector = Detector(languages=["go"])
        issues = detector.scan([go_file])
        
        # Filter to only Python-specific patterns
        python_only_pattern_ids = _get_python_only_pattern_ids()
        
        python_pattern_issues = [i for i in issues if i.pattern_id in python_only_pattern_ids]
        assert len(python_pattern_issues) == 0, f"Python-only patterns should not trigger on Go files: {python_pattern_issues}"

    def test_python_patterns_not_applied_to_js(self) -> None:
        """Python patterns should not be applied to JavaScript files."""
        js_file = FIXTURES_DIR / "js" / "clean_code.js"
        
        detector = Detector(languages=["javascript"])
        issues = detector.scan([js_file])
        
        # Filter to only Python-specific patterns
        python_only_pattern_ids = _get_python_only_pattern_ids()
        
        python_pattern_issues = [i for i in issues if i.pattern_id in python_only_pattern_ids]
        assert len(python_pattern_issues) == 0, f"Python-only patterns should not trigger on JS files: {python_pattern_issues}"

    def test_multi_language_scan_filters_correctly(self) -> None:
        """When scanning multiple languages, each file gets the right patterns."""
        # Scan both Python and Go files
        python_file = Path(__file__).parent / "corpus" / "false_positives" / "valid_python_methods.py"
        go_file = FIXTURES_DIR / "go" / "clean_code.go"
        
        detector = Detector(languages=["python", "go"])
        issues = detector.scan([python_file, go_file])
        
        # Get issues by file
        python_issues = [i for i in issues if i.file == python_file]
        go_issues = [i for i in issues if i.file == go_file]
        
        # Python file should not have Go patterns
        go_patterns_in_python = [i for i in python_issues if i.pattern_id.startswith("go_")]
        assert len(go_patterns_in_python) == 0, "Go patterns should not trigger on Python files in multi-language scan"
        
        # Go file should not have Python-only patterns
        python_only_pattern_ids = _get_python_only_pattern_ids()
        python_patterns_in_go = [i for i in go_issues if i.pattern_id in python_only_pattern_ids]
        assert len(python_patterns_in_go) == 0, "Python-only patterns should not trigger on Go files in multi-language scan"
