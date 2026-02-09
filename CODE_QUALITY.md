# Code Quality Guidelines

This document defines code quality standards, practices, and policies for REAPER. All contributions must adhere to these guidelines to ensure maintainability, security, and reliability.

## Table of Contents

- [Overview](#overview)
- [Linting and Formatting](#linting-and-formatting)
- [Type Checking](#type-checking)
- [Forbidden Practices](#forbidden-practices)
- [Security Standards](#security-standards)
- [Testing Requirements](#testing-requirements)
- [Performance Standards](#performance-standards)
- [Code Review Checklist](#code-review-checklist)

## Overview

**Quality Gates** (must pass before merge):
- ✅ All tests pass (pytest)
- ✅ Code coverage ≥95%
- ✅ Ruff linting passes
- ✅ Ruff formatting check passes
- ✅ CodeQL security scan passes
- ✅ No secrets in code
- ✅ Documentation updated

## Linting and Formatting

### Ruff Configuration

REAPER uses [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting.

**Configuration** (in `pyproject.toml`):
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
ignore = []
```

### Running Ruff

```bash
# Check formatting (fails if changes needed)
ruff format --check .

# Auto-format code
ruff format .

# Check linting (shows issues)
ruff check .

# Auto-fix linting issues (safe fixes only)
ruff check --fix .

# Check specific file
ruff check reaper/models.py
```

### Pre-Commit Hooks

Ruff runs automatically on commit:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

**Pre-commit will:**
- Format your code with Ruff
- Run linting checks
- Exit with error if fixes needed (so you can review)

### Formatting Standards

**Line Length**: Maximum 100 characters
- Exceptions: Long strings, URLs, imports

**Imports**: Organized automatically by Ruff
```python
# Standard library
import os
from datetime import datetime

# Third-party
import pluggy
from pydantic import BaseModel

# Local
from reaper.models import Signal
```

**Quotes**: Prefer double quotes (automatically enforced)
```python
source = "my-source"  # ✅ Good
source = 'my-source'  # ✅ Also accepted, but Ruff will convert
```

**Trailing Commas**: Used in multi-line collections
```python
# ✅ Good
my_list = [
    "item1",
    "item2",
    "item3",
]

# ❌ Bad (Ruff will fix)
my_list = [
    "item1",
    "item2",
    "item3"
]
```

## Type Checking

### Type Hints Required

All functions must have type hints:

```python
# ✅ Good
def detect_signals(source: str, limit: int = 10) -> list[Signal]:
    """Detect signals from source."""
    return []

# ❌ Bad (missing type hints)
def detect_signals(source, limit=10):
    return []
```

### Pydantic Models

Use Pydantic for all data structures:

```python
# ✅ Good
from pydantic import BaseModel, Field

class MyData(BaseModel):
    source: str = Field(..., description="Source identifier")
    count: int = Field(default=0, ge=0)

# ❌ Bad (no validation)
class MyData:
    def __init__(self, source, count=0):
        self.source = source
        self.count = count
```

### Generic Types

Use modern type syntax (Python 3.11+):

```python
# ✅ Good (Python 3.11+)
def process_signals(signals: list[Signal]) -> dict[str, Any]:
    pass

# ❌ Bad (old style)
from typing import List, Dict
def process_signals(signals: List[Signal]) -> Dict[str, Any]:
    pass
```

## Forbidden Practices

These practices are **never** allowed in REAPER code:

### 1. Hard-Coded Sources ❌

**Problem**: Hard-coding sources makes plugins inflexible and core non-reusable.

```python
# ❌ FORBIDDEN
@hookimpl
def reaper_sight_detect(self, source: str):
    # Ignoring the parameter and hard-coding!
    return [Signal(source="my-camera-1")]

# ✅ CORRECT
@hookimpl
def reaper_sight_detect(self, source: str):
    # Using the parameter
    return [Signal(source=source)]
```

**Enforcement**: CodeQL query detects this pattern. CI will fail.

### 2. Mixing Pipeline Roles ❌

**Problem**: Violates separation of concerns, makes code untestable and unmaintainable.

```python
# ❌ FORBIDDEN - Detection plugin that also scores
@hookimpl
def reaper_sight_detect(self, source: str):
    signal = Signal(sense_type=SenseType.SIGHT, source=source)
    # DON'T score here!
    score = self.calculate_score(signal)
    return [ScoredSignal(signal=signal, score=score)]  # Wrong return type!

# ✅ CORRECT - Detection only
@hookimpl
def reaper_sight_detect(self, source: str):
    return [Signal(sense_type=SenseType.SIGHT, source=source)]

# ✅ CORRECT - Scoring in separate plugin
@hookimpl
def reaper_score_signal(self, signal: Signal):
    score = self.calculate_score(signal)
    return ScoredSignal(signal=signal, score=score)
```

### 3. Skipping Pydantic Validation ❌

**Problem**: Bypassing validation defeats type safety and can cause runtime errors.

```python
# ❌ FORBIDDEN
signal_dict = {"sense_type": "sight", "source": "test"}
# Treating dict as Signal

# ✅ CORRECT
signal = Signal(sense_type=SenseType.SIGHT, source="test")
```

### 4. Secrets in Code ❌

**Problem**: Security vulnerability, credential exposure.

```python
# ❌ FORBIDDEN
API_KEY = "sk-1234567890abcdef"
WEBHOOK_URL = "https://discord.com/api/webhooks/..."

# ✅ CORRECT
import os
API_KEY = os.environ["MY_PLUGIN_API_KEY"]
WEBHOOK_URL = os.environ.get("MY_PLUGIN_WEBHOOK_URL")
```

**Enforcement**: 
- Pre-commit hook scans for common secret patterns
- CodeQL scans for hard-coded credentials
- Manual review of PR diffs

### 5. Modifying Core Files for Plugins ❌

**Problem**: Breaks plugin architecture, creates coupling.

```python
# ❌ FORBIDDEN
# Adding plugin-specific code to reaper/models.py
class Signal(BaseModel):
    # ...
    reddit_specific_field: str  # NO!

# ✅ CORRECT
# Plugin-specific models in plugin file
class RedditSignalData(BaseModel):
    post_id: str
    subreddit: str

# Use raw_data or metadata in Signal
signal = Signal(
    sense_type=SenseType.SIGHT,
    source=source,
    raw_data=RedditSignalData(post_id="123", subreddit="python").model_dump()
)
```

### 6. Wrong Hook Names ❌

**Problem**: Plugin won't be called, silent failure.

```python
# ❌ FORBIDDEN - Wrong name!
@hookimpl
def reaper_execute_action(self, scored_signal: ScoredSignal):
    pass

# ✅ CORRECT - Use exact hookspec name
@hookimpl
def reaper_action_execute(self, scored_signal: ScoredSignal):
    pass
```

**Correct hook names:**
- `reaper_sight_detect`
- `reaper_hearing_detect`
- `reaper_touch_detect`
- `reaper_taste_detect`
- `reaper_smell_detect`
- `reaper_score_signal`
- `reaper_action_execute` (NOT reaper_execute_action!)

### 7. Missing @hookimpl Decorator ❌

**Problem**: Plugin won't be registered, silent failure.

```python
# ❌ FORBIDDEN - Missing decorator
class MyPlugin:
    def reaper_sight_detect(self, source: str):
        return [Signal(...)]

# ✅ CORRECT
hookimpl = pluggy.HookimplMarker("reaper")

class MyPlugin:
    @hookimpl  # Required!
    def reaper_sight_detect(self, source: str):
        return [Signal(...)]
```

## Security Standards

### 1. Dependency Security

**Dependabot Configuration**: Automatically checks for vulnerable dependencies.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Before Adding Dependencies:**
1. Check for known vulnerabilities
2. Verify maintenance status
3. Review license compatibility
4. Assess necessity (prefer stdlib when possible)

### 2. CodeQL Security Scanning

**What CodeQL Checks:**
- SQL injection vulnerabilities
- Path traversal issues
- Command injection
- Hard-coded credentials
- Insecure randomness
- Custom REAPER rules (hard-coded sources, etc.)

**Viewing Results:**
```bash
# Locally (requires CodeQL CLI)
codeql database analyze --format=sarif-latest

# On GitHub
# Navigate to Security > Code scanning alerts
```

**Required**: All high and critical severity alerts must be resolved before merge.

### 3. Secrets Management

**Environment Variables**: Only acceptable way to pass secrets.

```python
# ✅ CORRECT
import os

class MyPlugin:
    def __init__(self):
        self.api_key = os.environ["MY_PLUGIN_API_KEY"]
        self.endpoint = os.environ.get(
            "MY_PLUGIN_ENDPOINT",
            "https://api.example.com"  # Default OK if not sensitive
        )
```

**Documentation**: Document required env vars in:
1. Plugin README
2. `.env.example` (with placeholder values)
3. Plugin docstring

### 4. Input Validation

**Always validate external input:**

```python
# ✅ CORRECT
from pydantic import BaseModel, Field, HttpUrl

class WebhookConfig(BaseModel):
    url: HttpUrl  # Validates URL format
    timeout: int = Field(default=30, ge=1, le=300)  # Range validation

# In plugin
config = WebhookConfig(url=user_input_url, timeout=user_timeout)
# Pydantic raises ValidationError if invalid
```

### 5. Error Handling

**Don't expose sensitive information in errors:**

```python
# ❌ BAD
except requests.RequestException as e:
    raise RuntimeError(f"Failed to call {self.api_key}: {e}")  # Exposes secret!

# ✅ GOOD
except requests.RequestException as e:
    logger.error(f"API call failed: {e}", exc_info=True)
    raise RuntimeError("API call failed") from e
```

## Testing Requirements

### Coverage Requirements

**Minimum Coverage**: 95% for all code
- Core (`reaper/`): Must maintain 95%+
- Plugins (`pipeline/`): Must maintain 95%+
- Tests (`tests/`): Not included in coverage

**Checking Coverage:**
```bash
# Generate coverage report
pytest --cov=reaper --cov=pipeline --cov-report=term-missing

# Generate HTML report
pytest --cov=reaper --cov=pipeline --cov-report=html
open htmlcov/index.html
```

### Test Organization

**Test Files**: Mirror source structure
```
reaper/
  models.py
  hookspecs.py
tests/
  test_models.py
  test_hookspecs.py
```

**Test Naming**: Descriptive and consistent
```python
def test_signal_validation_with_valid_data():
    """Test Signal creation with valid input."""
    pass

def test_signal_validation_rejects_invalid_sense_type():
    """Test Signal rejects invalid sense_type."""
    pass
```

### Test Categories

**1. Unit Tests** (required for all code):
```python
def test_signal_creation():
    signal = Signal(
        sense_type=SenseType.SIGHT,
        source="test",
    )
    assert signal.source == "test"
```

**2. Integration Tests** (required for plugins with external deps):
```python
@pytest.mark.integration
@pytest.mark.skipif(not os.environ.get("REDDIT_API_KEY"), reason="No API key")
def test_reddit_plugin_real_api():
    plugin = RedditPlugin()
    signals = plugin.reaper_sight_detect(source="python")
    assert len(signals) > 0
```

**3. Edge Case Tests** (required):
```python
def test_score_signal_clamps_score_above_one():
    """Ensure scores >1.0 are clamped to 1.0."""
    # Test edge cases!
    pass
```

### Mocking External Dependencies

**Required**: Mock all external APIs in unit tests.

```python
import pytest
from unittest.mock import Mock, patch

def test_reddit_plugin_with_mock():
    with patch("praw.Reddit") as mock_reddit:
        mock_reddit.return_value.subreddit.return_value.hot.return_value = [
            Mock(id="123", title="Test")
        ]
        
        plugin = RedditPlugin()
        signals = plugin.reaper_sight_detect(source="python")
        
        assert len(signals) == 1
        assert signals[0].raw_data["post_id"] == "123"
```

### Testing Validation

**Test both valid and invalid inputs:**

```python
def test_scored_signal_valid_score():
    """Test ScoredSignal accepts score in range."""
    signal = Signal(sense_type=SenseType.SIGHT, source="test")
    scored = ScoredSignal(signal=signal, score=0.5)
    assert scored.score == 0.5

def test_scored_signal_rejects_score_above_one():
    """Test ScoredSignal rejects score > 1.0."""
    signal = Signal(sense_type=SenseType.SIGHT, source="test")
    with pytest.raises(ValidationError):
        ScoredSignal(signal=signal, score=1.5)
```

## Performance Standards

### Benchmarking

**Benchmark Critical Paths**: Use pytest-benchmark for performance-sensitive code.

```python
def test_signal_creation_performance(benchmark):
    """Benchmark Signal creation."""
    result = benchmark(
        Signal,
        sense_type=SenseType.SIGHT,
        source="test"
    )
    assert result.source == "test"
```

**Performance Tests Location**: `benchmarks/` directory

### Performance Targets

**Signal Creation**: <1ms per signal
**Batch Creation**: <0.5ms per signal (using `create_batch()`)
**Plugin Registration**: <10ms per plugin
**Hook Invocation**: <0.1ms overhead per hook

### Optimization Guidelines

1. **Use `Signal.create_batch()`** for bulk operations (30-40% faster)
2. **Cache expensive operations** (API calls, computations)
3. **Profile before optimizing** (use cProfile or py-spy)
4. **Document performance characteristics** in docstrings

```python
def expensive_operation(self, items: list[str]) -> list[Signal]:
    """
    Process items into signals.
    
    Performance: O(n) where n is len(items)
    Benchmark: ~0.5ms per item on typical hardware
    """
    pass
```

## Code Review Checklist

### For All PRs

#### Architecture & Design
- [ ] Follows plugin architecture (no hard-coding)
- [ ] Respects separation of concerns (detection/scoring/action separate)
- [ ] Uses Pydantic models for data
- [ ] Proper hook names and decorators

#### Code Quality
- [ ] Passes Ruff formatting check
- [ ] Passes Ruff linting check
- [ ] Type hints on all functions
- [ ] No forbidden practices used
- [ ] Appropriate error handling

#### Testing
- [ ] Tests included for new code
- [ ] Coverage ≥95% maintained
- [ ] Edge cases tested
- [ ] External deps mocked in unit tests

#### Security
- [ ] No secrets in code
- [ ] CodeQL scan passes
- [ ] Input validation present
- [ ] Dependencies are secure

#### Documentation
- [ ] Docstrings on all public functions/classes
- [ ] README updated if needed
- [ ] Comments explain "why", not "what"
- [ ] Examples included for new features

### For Plugin PRs

Additional checks:

- [ ] Plugin README included with setup instructions
- [ ] Environment variables documented in `.env.example`
- [ ] Plugin follows template structure
- [ ] Example usage in docstring
- [ ] Integration tests (or explanation why not needed)
- [ ] Error messages are helpful

### For Core Changes

Additional checks (requires maintainer approval):

- [ ] Backward compatibility maintained
- [ ] Migration guide provided (if breaking)
- [ ] Architecture Decision Record (ADR) created
- [ ] Impact on existing plugins assessed
- [ ] Performance impact measured

## CI/CD Pipeline

### GitHub Actions Workflow

**On Every PR:**
1. Run pytest with coverage
2. Run Ruff formatting check
3. Run Ruff linting check
4. Run CodeQL security scan
5. Check for secrets (via pre-commit)

**On Merge to Main:**
- All of the above
- Upload coverage to Codecov
- Generate documentation
- Tag release (if version changed)

### Local Pre-Merge Checklist

Run these before pushing:

```bash
# 1. Format code
ruff format .

# 2. Fix linting
ruff check --fix .

# 3. Run tests with coverage
pytest -v --cov=reaper --cov=pipeline

# 4. Check coverage threshold
# Should see: "TOTAL ... 95%+" in output

# 5. Run pre-commit hooks
pre-commit run --all-files
```

If all pass locally, CI should pass.

## Exceptions and Waivers

### Requesting Exceptions

Some rules may need exceptions in rare cases.

**Process:**
1. Document why exception is needed
2. Propose alternative mitigation
3. Get approval from maintainer
4. Document in code with comment

```python
# EXCEPTION APPROVED: Issue #123
# Reason: Legacy API requires hard-coded endpoint
# Mitigation: Documented in README, will be removed in v2.0
LEGACY_ENDPOINT = "https://old-api.example.com"
```

### Temporary Coverage Waivers

If coverage temporarily drops below 95%:
1. Create issue to track fix
2. Add comment in CI config with issue number
3. Must be fixed within 2 releases

## Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [REAPER Contributing Guide](CONTRIBUTING.md)
- [REAPER Agent Roles](REAPER_AGENT_ROLES.md)

## Questions?

Ask in [GitHub Discussions - Q&A](https://github.com/SaltProphet/Reaper/discussions/categories/q-and-a)

---

**Remember**: Quality is not negotiable. These standards exist to keep REAPER maintainable, secure, and reliable for all users.
