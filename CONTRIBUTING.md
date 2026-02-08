# Contributing to REAPER

Thank you for your interest in contributing to REAPER! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Plugin Development](#plugin-development)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Getting Help](#getting-help)

## Code of Conduct

Be respectful, inclusive, and considerate. We want to maintain a welcoming environment for all contributors.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Reaper.git
   cd Reaper
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/SaltProphet/Reaper.git
   ```

## Development Setup

### Option 1: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Verify installation
pytest
python example_runner.py
```

### Option 2: GitHub Codespaces (Recommended)

1. Click "Code" → "Codespaces" → "Create codespace on main"
2. Wait for environment to build (dependencies auto-installed)
3. Start coding!

See [GITHUB_ADVANCED_TOOLS.md](GITHUB_ADVANCED_TOOLS.md) for detailed Codespaces setup.

### Option 3: VS Code Dev Containers

1. Install "Dev Containers" extension
2. Open repository in VS Code
3. Command Palette → "Dev Containers: Reopen in Container"

## Making Changes

### Branch Naming

Create a descriptive branch name:
- `feature/your-feature-name`
- `bugfix/issue-description`
- `plugin/plugin-name`
- `docs/what-you-are-documenting`

```bash
git checkout -b feature/github-issue-detector
```

### Commit Messages

Follow conventional commit format:
- `feat: Add GitHub issue detection plugin`
- `fix: Resolve scoring calculation error`
- `docs: Update plugin development guide`
- `test: Add tests for smell pipeline`
- `refactor: Simplify plugin manager logic`

## Plugin Development

### Core Principles

1. **Never hard-code sources** - Always accept source as parameter
2. **Use Pydantic models** - Signal, ScoredSignal, ActionResult
3. **Separation of concerns** - Don't mix detection, scoring, and action
4. **Use Pluggy hookimpl** - All plugins use `@hookimpl` decorator

### Creating a Detection Plugin

```python
import pluggy
from reaper.models import Signal, SenseType

hookimpl = pluggy.HookimplMarker("reaper")

class MyDetectionPlugin:
    """Detects signals from [source description]."""
    
    @hookimpl
    def reaper_sight_detect(self, source: str) -> list[Signal]:
        """
        Detect visual signals from the specified source.
        
        Args:
            source: Source identifier (never hard-coded!)
            
        Returns:
            List of Signal objects
        """
        # Your detection logic here
        signals = []
        
        # Example signal
        signals.append(
            Signal(
                sense_type=SenseType.SIGHT,
                source=source,
                raw_data={"detected": "data"}
            )
        )
        
        return signals
```

### Creating a Scoring Plugin

```python
import pluggy
from reaper.models import Signal, ScoredSignal

hookimpl = pluggy.HookimplMarker("reaper")

class MyScoringPlugin:
    """Scores signals based on [criteria]."""
    
    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        """
        Score a signal.
        
        Args:
            signal: Signal to score
            
        Returns:
            ScoredSignal with score between 0.0 and 1.0
        """
        # Calculate score (must be 0.0 to 1.0)
        score = self._calculate_score(signal)
        
        return ScoredSignal(
            signal=signal,
            score=score,
            analysis={"method": "description"},
            tags=["tag1", "tag2"]
        )
    
    def _calculate_score(self, signal: Signal) -> float:
        # Your scoring logic
        return 0.5
```

### Creating an Action Plugin

```python
import pluggy
from reaper.models import ScoredSignal, ActionResult

hookimpl = pluggy.HookimplMarker("reaper")

class MyActionPlugin:
    """Executes actions based on scored signals."""
    
    @hookimpl
    def reaper_execute_action(self, signal: ScoredSignal) -> ActionResult:
        """
        Execute action on a scored signal.
        
        Args:
            signal: ScoredSignal to act on
            
        Returns:
            ActionResult with execution status
        """
        try:
            # Your action logic
            self._execute(signal)
            
            return ActionResult(
                signal=signal,
                success=True,
                action_type="my_action",
                metadata={"details": "success"}
            )
        except Exception as e:
            return ActionResult(
                signal=signal,
                success=False,
                action_type="my_action",
                metadata={"error": str(e)}
            )
```

### Plugin File Location

- Place detection plugins in `pipeline/`
- Name files descriptively: `github_issues.py`, `slack_messages.py`
- Update `example_runner.py` if adding new reference plugins

## Testing

### Writing Tests

Create tests in `tests/` directory:

```python
import pytest
from reaper.models import Signal, SenseType
from my_plugin import MyPlugin

def test_detection_returns_signals():
    """Test that detection returns Signal objects."""
    plugin = MyPlugin()
    signals = plugin.reaper_sight_detect(source="test-source")
    
    assert len(signals) > 0
    assert isinstance(signals[0], Signal)
    assert signals[0].sense_type == SenseType.SIGHT
    assert signals[0].source == "test-source"

def test_detection_handles_empty_source():
    """Test that detection handles missing data gracefully."""
    plugin = MyPlugin()
    signals = plugin.reaper_sight_detect(source="nonexistent")
    
    # Should return empty list, not raise exception
    assert signals == []
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=reaper --cov=pipeline

# Run specific test file
pytest tests/test_my_plugin.py

# Run specific test
pytest tests/test_my_plugin.py::test_detection_returns_signals

# Run with verbose output
pytest -v
```

### Test Coverage Requirements

- Aim for >80% coverage for new code
- Test both success and failure cases
- Test edge cases and validation
- Mock external dependencies

## Code Style

### Linting

REAPER uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Check formatting without changing files
ruff format --check .
```

### Style Guidelines

- **Line length**: 100 characters maximum
- **Type hints**: Required for all functions/methods
- **Docstrings**: Required for public functions/classes
- **Imports**: Organized (stdlib → third-party → local)
- **Naming**:
  - Classes: `PascalCase`
  - Functions/methods: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`

### Using GitHub Copilot

If you have GitHub Copilot:
1. Check `.github/copilot-instructions.md` for project-specific guidance
2. Use Copilot Chat for plugin generation: `/explain`, `/fix`, `/tests`
3. Review all suggestions before accepting

See [GITHUB_ADVANCED_TOOLS.md](GITHUB_ADVANCED_TOOLS.md) for Copilot setup.

## Submitting Changes

### Pre-Submission Checklist

- [ ] Code passes linting: `ruff check .`
- [ ] Code is formatted: `ruff format .`
- [ ] All tests pass: `pytest`
- [ ] New features have tests
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] PR template filled out completely

### Creating a Pull Request

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open Pull Request** on GitHub:
   - Use descriptive title
   - Fill out PR template completely
   - Link related issues
   - Select reviewers if known

3. **CI Checks**: Ensure all automated checks pass
   - Tests
   - Linting
   - Plugin validation

4. **Address Review Comments**:
   - Respond to all comments
   - Make requested changes
   - Push updates to same branch

5. **Merge**: Maintainer will merge when approved

## Getting Help

### Resources

- **Documentation**: [README.md](README.md)
- **Advanced Tools Guide**: [GITHUB_ADVANCED_TOOLS.md](GITHUB_ADVANCED_TOOLS.md)
- **Example Code**: [example_runner.py](example_runner.py)
- **Models Reference**: [reaper/models.py](reaper/models.py)
- **Hook Specs**: [reaper/hookspecs.py](reaper/hookspecs.py)

### Ask Questions

- **GitHub Discussions**: For questions and ideas
- **Issues**: For bugs and feature requests (use templates)
- **PR Comments**: For code-specific discussions

### Common Issues

**Q: My plugin isn't being detected**
- Ensure you're using `@hookimpl` decorator
- Check hook method name matches hookspec
- Verify plugin is registered with PluginManager

**Q: Tests failing with Pydantic errors**
- Use Pydantic v2 models
- Ensure all required fields provided
- Check type hints match model definition

**Q: Linting errors**
- Run `ruff check --fix .` to auto-fix
- Check line length (<100 chars)
- Ensure imports are organized

**Q: How do I debug a plugin?**
- Use Python debugger: `import pdb; pdb.set_trace()`
- Add print statements (remove before PR)
- Use VS Code debugger with breakpoints

## Project Structure

```
Reaper/
├── .devcontainer/           # Codespaces configuration
├── .github/
│   ├── workflows/           # CI/CD workflows
│   ├── ISSUE_TEMPLATE/      # Issue templates
│   ├── copilot-instructions.md  # Copilot guidance
│   └── pull_request_template.md
├── docs/                    # Additional documentation
├── examples/                # Example integrations
├── pipeline/                # Reference plugin implementations
│   ├── sight.py            # Sight detection stub
│   ├── hearing.py          # Hearing detection stub
│   ├── touch.py            # Touch detection stub
│   ├── taste.py            # Taste detection stub
│   ├── smell.py            # Smell detection stub
│   ├── scoring.py          # Scoring stub
│   └── action.py           # Action stub
├── reaper/                  # Core framework
│   ├── models.py           # Pydantic data models
│   ├── hookspecs.py        # Pluggy hook specifications
│   └── plugin_manager.py   # Plugin management
├── tests/                   # Test suite
│   ├── test_models.py      # Model tests
│   ├── test_plugin_manager.py
│   └── test_pipeline_stubs.py
├── .gitignore
├── LICENSE
├── README.md               # Main documentation
├── CONTRIBUTING.md         # This file
├── GITHUB_ADVANCED_TOOLS.md  # Advanced tools guide
├── example_runner.py       # Example usage
└── pyproject.toml          # Project configuration
```

## Recognition

Contributors will be recognized in:
- GitHub Contributors page
- Release notes for significant contributions
- README acknowledgments (for major features)

---

Thank you for contributing to REAPER! 🎯

For questions, open a [GitHub Discussion](https://github.com/SaltProphet/Reaper/discussions).
