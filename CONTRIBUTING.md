# Contributing to REAPER

Thank you for your interest in contributing to REAPER! This guide will help you get started.

## Code Quality Requirements

REAPER's foundation is solid. All code must meet quality standards before submission.

### Before Submitting a PR

1. **Install pre-commit hooks** (one-time setup):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Run checks locally**:
   ```bash
   ruff check . --fix
   ruff format .
   pytest
   ```

3. **All commits must pass**:
   - Ruff formatting (`ruff format --check .`)
   - Ruff linting (`ruff check .`)
   - All tests (`pytest`)

**CI will reject PRs that don't meet these standards. Fix issues locally before pushing.**

## Development Setup

### Installation

```bash
# Clone the repository
git clone https://github.com/SaltProphet/Reaper.git
cd Reaper

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest -v --cov=reaper --cov=pipeline --cov-report=term-missing

# Run specific test file
pytest tests/test_models.py
```

### Code Style

REAPER uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Check formatting
ruff format --check .

# Format code
ruff format .

# Check for linting issues
ruff check .

# Auto-fix linting issues
ruff check . --fix
```

## Plugin Development

REAPER is plugin-driven. All functionality is implemented via [Pluggy](https://pluggy.readthedocs.io/) plugins.

### Core Principles

1. **Plugin-Driven Everything**: Use `@hookimpl` decorator for all plugin implementations
2. **No Hard-Coding**: Sources must always be passed as parameters (e.g., `source="my-source"`)
3. **Strict Separation of Concerns**: Never mix pipeline roles (detection, scoring, action)
4. **Type Safety**: All data structures use [Pydantic v2](https://docs.pydantic.dev/latest/) models
5. **Extensibility First**: New plugins should be addable without modifying core code

### Creating a Detection Plugin

```python
import pluggy
from reaper.models import Signal, SenseType

hookimpl = pluggy.HookimplMarker("reaper")

class MyCustomPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str):
        # Your custom detection logic
        # NEVER hard-code the source!
        return [
            Signal(
                sense_type=SenseType.SIGHT,
                source=source,  # Use the parameter
                raw_data={"detected": "custom data"}
            )
        ]
```

### Creating a Scoring Plugin

```python
import pluggy
from reaper.models import Signal, ScoredSignal

hookimpl = pluggy.HookimplMarker("reaper")

class MyScorer:
    @hookimpl
    def reaper_score_signal(self, signal: Signal):
        # Your custom scoring logic
        score = self.calculate_score(signal)
        return ScoredSignal(
            signal=signal,
            score=score,  # Must be 0.0-1.0
            analysis={"method": "custom"},
            tags=["custom-scored"]
        )
```

### Creating an Action Plugin

```python
import pluggy
from reaper.models import ScoredSignal, ActionResult

hookimpl = pluggy.HookimplMarker("reaper")

class MyActionPlugin:
    @hookimpl
    def reaper_action_execute(self, scored_signal: ScoredSignal):
        # Your custom action logic
        return ActionResult(
            signal=scored_signal.signal,
            action_type="custom_action",
            success=True,
            result_data={"executed": "custom action"}
        )
```

## Submitting Changes

### Pull Request Process

1. **Fork the repository** and create a new branch
2. **Make your changes** following the code quality requirements
3. **Run all checks locally** before pushing:
   ```bash
   ruff format .
   ruff check .
   pytest
   ```
4. **Commit your changes** with clear, descriptive messages
5. **Push to your fork** and submit a pull request

### Pull Request Guidelines

- Keep changes focused and minimal
- Include tests for new functionality
- Update documentation if needed
- Ensure all CI checks pass
- Reference any related issues

### Commit Messages

Write clear, concise commit messages:

```
Add Reddit detection plugin for Sight sense

- Implement reaper_sight_detect hook
- Add Pydantic models for Reddit posts
- Include tests with 100% coverage
- Update documentation with usage example
```

## Testing Guidelines

### Test Coverage

- Maintain 100% test coverage for core modules
- Write tests for all new functionality
- Use pytest fixtures for common setup
- Mock external dependencies

### Test Structure

```python
import pytest
from reaper.models import Signal, SenseType

def test_signal_creation():
    """Test that Signal can be created with valid data."""
    signal = Signal(
        sense_type=SenseType.SIGHT,
        source="test-source",
        raw_data={"key": "value"}
    )
    assert signal.sense_type == SenseType.SIGHT
    assert signal.source == "test-source"
```

## Project Structure

Understanding the codebase structure:

```
Reaper/
├── reaper/              # Core framework (DO NOT modify lightly)
│   ├── models.py        # Pydantic v2 models
│   ├── hookspecs.py     # Pluggy hook specifications
│   └── plugin_manager.py # Plugin management
├── pipeline/            # Pipeline stubs (reference implementations)
│   ├── sight.py         # Sight sense stub
│   ├── hearing.py       # Hearing sense stub
│   ├── touch.py         # Touch sense stub
│   ├── taste.py         # Taste sense stub
│   ├── smell.py         # Smell sense stub
│   ├── action.py        # Action sense stub
│   └── scoring.py       # Scoring stub
├── tests/               # Test suite
├── .github/             # GitHub configuration
│   └── workflows/       # CI/CD workflows
└── example_runner.py    # Example usage
```

## Anti-Patterns to Avoid

❌ **DO NOT:**
- Hard-code sources anywhere in code
- Mix detection, scoring, and action logic in one plugin
- Modify core without updating tests
- Add business logic to the core framework
- Skip Pydantic validation
- Use `Any` type annotations when specific types exist

✅ **DO:**
- Accept sources as parameters
- Keep plugins focused on one responsibility
- Use type hints everywhere
- Validate all inputs with Pydantic
- Write tests for new functionality
- Follow the stub implementations as templates

## Getting Help

- **Documentation**: See [README.md](README.md) for architecture and usage
- **Examples**: Check [example_runner.py](example_runner.py) for complete examples
- **Tests**: Review test files in `/tests/` for implementation patterns
- **Issues**: Open an issue for bugs or feature requests

## License

By contributing to REAPER, you agree that your contributions will be licensed under the MIT License.
