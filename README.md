<!-- TODO: Add CLI demo GIF here -->

<div align="center">
  <h1>🧠 DeepLint</h1>
  <p><strong>Detect AI-generated code anti-patterns in your multi-language codebase.</strong></p>
  <p><em>Catches AI-specific anti-patterns that traditional linters miss</em></p>
</div>

[![PyPI](https://img.shields.io/pypi/v/deeplint?style=for-the-badge)](https://pypi.org/project/deeplint/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## ⚡ Quick Start

```bash
pip install deeplint
deeplint .

# Output:
# CRITICAL (2 issues)
# ============================================================
#   src/api.py:23  mutable_default_arg
#     Mutable default argument - use None instead
#     > def process(items=[]):
#
#   src/db.py:15  bare_except
#     Bare except catches everything including SystemExit
#     > except:
#
# DEEPLINT INDEX
# ══════════════════════════════════════════════════
# Information Utility (Noise)    : 24 pts
# Information Quality (Lies)     : 105 pts
# Style / Taste (Soul)           : 31 pts
# Structural Issues              : 45 pts
# ──────────────────────────────────────────────────
# TOTAL SLOP SCORE               : 205 pts
#
# Verdict: SLOPPY
```

---

## 🌐 Multi-Language Support

DeepLint automatically detects and scans multiple programming languages in your codebase:

| Language | File Extensions | Status |
|----------|----------------|--------|
| **Python** | `.py`, `.pyw` | ✅ Full support (AST + patterns) |
| **JavaScript** | `.js`, `.jsx`, `.mjs`, `.cjs` | ✅ Pattern detection |
| **TypeScript** | `.ts`, `.tsx` | ✅ Pattern detection |
| **Go** | `.go` | ✅ Pattern detection |

### Automatic Detection

By default, DeepLint **automatically detects** which languages are present in your project:

```bash
# Scans all supported languages found in the directory
deeplint .

# Output shows detected languages:
# Scanned languages: javascript, python, typescript
```

### Manual Language Override

Advanced users can override automatic detection with the `--language` flag:

```bash
# Scan only Python files
deeplint src/ --language python

# Scan multiple specific languages
deeplint src/ --language javascript,typescript

# Case-insensitive language names
deeplint src/ --language Python,JavaScript
```

This is useful when:
- You want to focus on specific languages in a polyglot codebase
- You need faster scans by limiting scope
- You're debugging language-specific issues

---

## 🤔 Why DeepLint Exists

Traditional linters catch style and syntax issues. But AI-generated code introduces **new failure patterns** they weren't designed to detect:

- **Hallucinated imports** - packages and functions that don't exist
- **Cross-language leakage** - `.push()`, `.equals()`, `.length` in Python
- **Placeholder code** - `pass`, `TODO`, functions that do nothing
- **Confident wrongness** - code that looks right but fails at runtime

DeepLint targets these AI-specific patterns that escape Pylint, Flake8, ESLint, and code review.

### Frontend-Focused Detection

Building on insights from [KarpeSlop](https://github.com/CodeDeficient/KarpeSlop), DeepLint includes **30 TypeScript/JavaScript patterns** specifically designed for modern frontend frameworks:

- **React Hooks Anti-patterns** - `useEffect` with derived state, empty deps, stale closures
- **TypeScript Type Safety** - `any` type abuse, unsafe assertions, missing generics  
- **Hallucinated Imports** - React APIs from wrong packages (e.g., `useRouter` from 'react')
- **Frontend-Specific Issues** - IIFE wrappers, nested ternaries, magic CSS values

---

## 🎯 What It Catches

### The Three Axes of AI Slop

| Axis | What It Detects | Examples |
|------|-----------------|----------|
| 📢 **Noise** | Debug artifacts, redundant comments | `print()`, `# increment x` above `x += 1` |
| 🤥 **Lies** | Hallucinations, placeholders | `def process(): pass`, mutable defaults |
| 💀 **Soul** | Over-engineering, bad style | God functions, deep nesting, hedging comments |
| 🏗️ **Structure** | Anti-patterns | Bare except, star imports, single-method classes |

---

## 📥 What You Put In

```bash
# Automatic language detection - scans all supported languages
deeplint .

# Scan a specific directory
deeplint src/

# Scan specific files
deeplint app.py utils.py

# Language-specific scanning
deeplint src/ --language python              # Python only
deeplint src/ --language javascript,typescript  # JS/TS only

# Only high severity issues
deeplint --severity high

# CI mode - exit 1 if issues found
deeplint --ci --max-score 50

# Export JSON report
deeplint --output report.json
```

---

## 📤 What You Get Out

| Output | Description |
|--------|-------------|
| 🎯 **Issues by Severity** | Critical, High, Medium, Low |
| 📊 **Slop Score** | Points breakdown by axis |
| 📋 **Verdict** | CLEAN / ACCEPTABLE / SLOPPY / DISASTER |
| 📁 **JSON Report** | Machine-readable for CI/CD |

---

## 🔍 Pattern Examples

### Critical Severity

```python
# 🚨 mutable_default_arg - AI's favorite mistake
def process_items(items=[]):  # Bug: shared state between calls
    items.append(1)
    return items

# ✅ Fix: Use None and initialize inside
def process_items(items=None):
    if items is None:
        items = []
    items.append(1)
    return items
```

```python
# 🚨 bare_except - Catches SystemExit, KeyboardInterrupt
try:
    risky_operation()
except:  # Bug: swallows Ctrl+C!
    pass

# ✅ Fix: Catch specific exceptions
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
```

### High Severity

```python
# 🚨 pass_placeholder - AI gave up
def validate_email(email):
    pass  # TODO: implement

# 🚨 hedging_comment - AI uncertainty
x = calculate()  # should work hopefully
```

### TypeScript/React Patterns (KarpeSlop-Inspired)

```typescript
// 🚨 hallucinated_react_import - AI hallucinating package locations
import { useRouter, Link } from 'react';  // Bug: These are from 'next/router' and 'next/link'

// ✅ Fix: Import from correct packages
import { useRouter } from 'next/router';
import Link from 'next/link';
```

```typescript
// 🚨 ts_any_type_usage - TypeScript type safety bypass
function processData(data: any): any {  // Bug: Loses all type safety
    return data.someProp;
}

// ✅ Fix: Use proper types or unknown
function processData<T>(data: T): T {
    return data;
}
```

```typescript
// 🚨 js_useEffect_derived_state - React anti-pattern
useEffect(() => {
    setDerived(name.toUpperCase());  // Bug: Unnecessary re-render
}, [name]);

// ✅ Fix: Use useMemo for derived state
const derived = useMemo(() => name.toUpperCase(), [name]);
```

```typescript
// 🚨 js_setState_in_loop - Multiple re-renders
for (let i = 0; i < items.length; i++) {
    setTotal(total + items[i]);  // Bug: Re-renders on each iteration
}

// ✅ Fix: Batch the update
const newTotal = items.reduce((sum, item) => sum + item, 0);
setTotal(newTotal);
```

---

## 💰 The Value

<div align="center">
  <h3>🔍 Catch AI mistakes before they hit production</h3>
</div>

### Why This Matters

| Problem | Impact | DeepLint Catches |
|---------|--------|----------------|
| Mutable defaults | Shared state bugs | ✅ Critical alert |
| Bare except | Swallows Ctrl+C | ✅ Critical alert |
| Placeholder functions | Runtime failures | ✅ High alert |
| Hallucinated imports | ImportError in prod | ✅ High alert |
| Wrong language patterns | JS/Java/Ruby/Go/C#/PHP in Python | ✅ High alert |
| Unused imports | Code bloat | ✅ Medium alert |
| Dead code | Maintenance burden | ✅ Medium alert |
| Copy-paste code | Maintenance nightmare | ✅ Medium alert |

### Research Says

- **20% of AI package imports** reference non-existent libraries — *DeepLint catches these*
- **LLMs leak patterns** from other languages they were trained on — *DeepLint catches 100+ of these*
- **66% of developers** say AI code is "almost right" (the dangerous kind)

---

## 🛠️ CLI Commands

```bash
deeplint .                    # 🔍 Scan current directory (auto-detect languages)
deeplint src/ tests/          # 📁 Scan multiple directories

# Language selection
deeplint --language python    # 🐍 Scan Python only
deeplint --language js,ts     # 📜 Scan JavaScript & TypeScript
deeplint -l go                # 🚀 Scan Go only

# Severity & reporting
deeplint --severity high      # ⚡ Only critical/high issues
deeplint --lenient            # 🎯 Same as --severity high
deeplint --strict             # 🔬 Report everything
deeplint --ci                 # 🚦 Exit 1 if any issues
deeplint --max-score 50       # 📊 Exit 1 if score > 50
deeplint --output report.json # 📋 Export JSON report

# Filtering
deeplint --ignore "tests/*"   # 🚫 Exclude patterns
deeplint --disable magic_number # ⏭️ Skip specific checks
deeplint --version            # 📌 Show version
```

---

## ✅ Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🌐 **Multi-Language Support** | Python, JavaScript, TypeScript, Go | ✅ Auto-detection |
| 🔍 **Smart Detection** | Automatic language identification | ✅ Done |
| 🎯 **Manual Override** | `--language` flag for specific languages | ✅ Done |
| 🤥 **Hallucinated Imports** | Detect non-existent packages | ✅ Done |
| 📦 **Unused Imports** | AST-based detection (Python) | ✅ Done |
| 💀 **Dead Code** | Unused functions/classes | ✅ Done |
| 🔄 **Duplicate Detection** | Cross-file copy-paste | ✅ Done |
| 🎨 **Rich Output** | Colors and tables (optional) | ✅ Done |
| ⚙️ **Config Support** | pyproject.toml configuration | ✅ Done |

### Cross-Language Pattern Detection

LLMs are trained on code from many languages. When generating code, they sometimes produce patterns from other languages:

| Language | Example Mistakes | Correct Alternative |
|----------|------------------|---------------------|
| **JavaScript** | `.push()`, `.length`, `.forEach()` | `.append()`, `len()`, `for` loop |
| **Java** | `.equals()`, `.toString()`, `.isEmpty()` | `==`, `str()`, `not obj` |
| **Ruby** | `.each`, `.nil?`, `.first`, `.last` | `for` loop, `is None`, `[0]`, `[-1]` |
| **Go** | `fmt.Println()`, `nil` | `print()`, `None` |
| **C#** | `.Length`, `.Count`, `.ToLower()` | `len()`, `len()`, `.lower()` |
| **PHP** | `strlen()`, `array_push()`, `explode()` | `len()`, `.append()`, `.split()` |

---

## 🚫 What DeepLint Is Not

DeepLint does **not** replace:
- Human code review
- Traditional linters (Pylint, Flake8, Ruff)
- Type checkers (mypy, pyright)
- Security scanners (Bandit, Semgrep)

It **complements** them by catching patterns these tools miss—patterns uniquely common in AI-generated code.

---

## 📦 Installation

```bash
# Install from PyPI
pip install deeplint

# With colored output (recommended)
pip install deeplint[rich]

# With all optional features
pip install deeplint[all]

# Or install from source for development
git clone https://github.com/del-zhenwu/deeplint.git
cd deeplint
pip install -e ".[dev]"
```

---

## ⚙️ Configuration

Configure via `pyproject.toml`:

```toml
[tool.deeplint]
ignore = ["tests/*", "migrations/*"]
disable = ["magic_number", "debug_print"]
severity = "medium"
max-score = 100
ci = false
format = "detailed"  # or "compact" or "json"
```

---

## 🤝 Contributing

```bash
git clone https://github.com/del-zhenwu/deeplint.git
cd deeplint
pip install -e ".[dev]"
pytest tests/ -v  # 99 tests should pass
```

See [AGENTS.md](AGENTS.md) for coding conventions and pattern implementation guide.

---

## 📄 License

MIT

---

## 🙏 Acknowledgments

### Inspiration
- [KarpeSlop](https://github.com/CodeDeficient/KarpeSlop) - The original AI Slop Linter for TypeScript
- Andrej Karpathy's commentary on AI-generated code quality

### Research
- [Counterfeit Code](https://counterfeit-code.github.io/) - MIT research on "looks right but doesn't work" patterns
- [Package Hallucinations](https://arxiv.org/abs/2406.10279) - USENIX study on hallucinated dependencies
