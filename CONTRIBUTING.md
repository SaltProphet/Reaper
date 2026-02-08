# Contributing to REAPER

Thank you for your interest in contributing to REAPER! This guide will help you get started with development, whether you're fixing bugs, adding features, or creating plugins.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Architecture](#project-architecture)
- [Making Changes](#making-changes)
- [Plugin Development](#plugin-development)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Community](#community)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect differing viewpoints and experiences
- Accept responsibility and learn from mistakes

## Getting Started

### Quick Start with Codespaces

The fastest way to start contributing is using GitHub Codespaces:

1. Click the "Code" button on the repository
2. Select "Create codespace on main"
3. Wait for the environment to initialize
4. Start coding!

The Codespace comes pre-configured with:
- Python 3.11
- All dependencies installed
- VS Code extensions (Ruff, Copilot, Python)
- Recommended settings

### Local Development Setup

If you prefer local development:

```bash
# Clone the repository
git clone https://github.com/SaltProphet/Reaper.git
cd Reaper

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Verify installation
pytest
```

## Project Architecture

REAPER follows a modular, plugin-driven architecture:

### Core Components

- **`reaper/models.py`**: Pydantic v2 data models (Signal, ScoredSignal, etc.)
- **`reaper/hookspecs.py`**: Pluggy hook specifications
- **`reaper/plugin_manager.py`**: Plugin registration and management

### Pipeline

The 5-sense pipeline in `/pipeline/`:

1. **Sight** (`sight.py`) - Visual detection
2. **Hearing** (`hearing.py`) - Audio/text detection
3. **Touch** (`touch.py`) - Interaction detection
4. **Taste** (`taste.py`) - Quality/sampling detection
5. **Smell** (`smell.py`) - Pattern/anomaly detection
6. **Action** (`action.py`) - Execute actions

Each is a reference implementation showing plugin structure.

### Core Principles

**Must follow:**
- ✅ Plugin-driven: All functionality via Pluggy plugins
- ✅ Type-safe: Pydantic v2 for data validation
- ✅ No hard-coding: Sources passed as parameters
- ✅ Separation of concerns: Don't mix pipeline roles
- ✅ Extensible: Add plugins without modifying core

**Must avoid:**
- ❌ Hard-coded data sources
- ❌ Mixing detection, scoring, and action logic
- ❌ Skipping data validation
- ❌ Breaking plugin API compatibility

## Making Changes

### Before You Start

1. **Check existing issues**: See if someone is already working on it
2. **Create an issue**: Describe what you want to do
3. **Get feedback**: Discuss approach with maintainers
4. **Check the roadmap**: Align with current phase ([Roadmap](Roadmap))

### Branch Naming

Use descriptive branch names:

- `feature/add-discord-plugin`
- `fix/scoring-range-validation`
- `docs/improve-readme`
- `refactor/plugin-manager-cleanup`

### Commit Messages

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

**Examples**:
- `feat(sight): add Reddit ingestor plugin`
- `fix(scoring): ensure score is within 0.0-1.0 range`
- `docs(readme): add plugin development examples`
- `test(models): add validation tests for Signal`

## Plugin Development

### Creating a Detection Plugin

```python
import pluggy
from reaper.models import Signal, SenseType

hookimpl = pluggy.HookimplMarker("reaper")

class MyDetectionPlugin:
    """Detects signals from [source]."""
    
    @hookimpl
    def reaper_[sense]_detect(self, source: str):
        """
        Detect signals from the specified source.
        
        Args:
            source: The source identifier (never hard-coded!)
        
        Returns:
            List of Signal objects
        """
        # Your detection logic here
        return [
            Signal(
                sense_type=SenseType.[SENSE],
                source=source,
                raw_data={"detected": "data"}
            )
        ]
```

**Available hooks**:
- `reaper_sight_detect`
- `reaper_hearing_detect`
- `reaper_touch_detect`
- `reaper_taste_detect`
- `reaper_smell_detect`

### Creating a Scoring Plugin

```python
import pluggy
from reaper.models import Signal, ScoredSignal

hookimpl = pluggy.HookimplMarker("reaper")

class MyScoringPlugin:
    """Scores signals based on [criteria]."""
    
    @hookimpl
    def reaper_score_signal(self, signal: Signal):
        """
        Score a signal.
        
        Args:
            signal: Signal to score
        
        Returns:
            ScoredSignal with score in range 0.0-1.0
        """
        score = self.calculate_score(signal)
        
        return ScoredSignal(
            signal=signal,
            score=max(0.0, min(1.0, score)),  # Ensure range
            analysis={"method": "my_method"},
            tags=["my-tag"]
        )
```

### Creating an Action Plugin

```python
import pluggy
from reaper.models import ScoredSignal, ActionResult

hookimpl = pluggy.HookimplMarker("reaper")

class MyActionPlugin:
    """Executes actions on scored signals."""
    
    @hookimpl
    def reaper_execute_action(self, scored_signal: ScoredSignal):
        """
        Execute action on a scored signal.
        
        Args:
            scored_signal: Scored signal to act on
        
        Returns:
            ActionResult indicating success/failure
        """
        try:
            # Your action logic here
            return ActionResult(
                success=True,
                action_type="my_action",
                details={"result": "success"}
            )
        except Exception as e:
            return ActionResult(
                success=False,
                action_type="my_action",
                details={"error": str(e)}
            )
```

### Plugin Checklist

Before submitting a plugin:

- [ ] Uses `@hookimpl` decorator
- [ ] Does NOT hard-code sources
- [ ] Uses Pydantic models for data
- [ ] Includes docstrings
- [ ] Has unit tests
- [ ] Follows separation of concerns
- [ ] Documented in code comments

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest -v --cov=reaper --cov=pipeline

# Run specific test file
pytest tests/test_models.py

# Run specific test
pytest tests/test_models.py::test_signal_validation
```

### Writing Tests

Place tests in `/tests/` directory:

```python
import pytest
from reaper.models import Signal, SenseType

def test_my_feature():
    """Test description."""
    signal = Signal(
        sense_type=SenseType.SIGHT,
        source="test-source",
        raw_data={"test": "data"}
    )
    
    assert signal.source == "test-source"
    assert signal.sense_type == SenseType.SIGHT
```

### Test Coverage

- Maintain 95%+ coverage
- Test happy paths and edge cases
- Test validation errors
- Mock external dependencies

## Submitting Changes

### Pull Request Process

1. **Update your branch**:
   ```bash
   git checkout main
   git pull origin main
   git checkout your-branch
   git merge main
   ```

2. **Run tests and linting**:
   ```bash
   pytest -v --cov=reaper --cov=pipeline
   ruff check .
   ```

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: your descriptive message"
   ```

4. **Push to your fork**:
   ```bash
   git push origin your-branch
   ```

5. **Create Pull Request**:
   - Use the PR template
   - Link related issues
   - Describe your changes clearly
   - Add screenshots if applicable

### PR Review Checklist

Your PR will be reviewed for:

- [ ] Follows REAPER core principles
- [ ] Includes tests
- [ ] Passes all CI checks
- [ ] Documentation updated
- [ ] No hard-coded sources
- [ ] Proper Pydantic validation
- [ ] Clear commit messages
- [ ] No breaking changes (or documented)

### Getting Help

If your PR needs changes:
- Read the review comments carefully
- Ask questions if anything is unclear
- Make requested changes
- Push updates (no need for new PR)

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions, ideas, plugin marketplace
- **GitHub Projects**: Track development progress
- **GitHub Spaces**: Collaborative design sessions

### How to Get Involved

**For Beginners**:
- Look for issues labeled `good-first-issue`
- Improve documentation
- Add tests for existing code
- Fix typos and formatting

**For Experienced Contributors**:
- Create new plugins
- Improve core functionality
- Review PRs
- Mentor newcomers

**For Designers**:
- Design operator console UI
- Create documentation visuals
- Improve user experience

**For Technical Writers**:
- Improve documentation
- Write tutorials
- Create plugin guides

### Plugin Marketplace

Share your plugin ideas in [Discussions](https://github.com/SaltProphet/Reaper/discussions):

1. Use the "Plugin Marketplace" category
2. Describe your plugin concept
3. Get community feedback
4. Collaborate on design
5. Implement and submit PR

### Recognition

Contributors are recognized in:
- Release notes
- CONTRIBUTORS file (coming soon)
- Community updates
- Project credits

## Resources

- **Documentation**: [README.md](README.md)
- **Roadmap**: [Roadmap](Roadmap)
- **Copilot Guide**: [.github/copilot-instructions.md](.github/copilot-instructions.md)
- **Projects Guide**: [.github/PROJECTS_GUIDE.md](.github/PROJECTS_GUIDE.md)
- **Spaces Guide**: [.github/SPACES_GUIDE.md](.github/SPACES_GUIDE.md)
- **Spark Automation**: [.github/SPARK_AUTOMATION_GUIDE.md](.github/SPARK_AUTOMATION_GUIDE.md)

## Questions?

- **General questions**: [GitHub Discussions - Q&A](https://github.com/SaltProphet/Reaper/discussions/categories/q-and-a)
- **Plugin ideas**: [GitHub Discussions - Plugin Marketplace](https://github.com/SaltProphet/Reaper/discussions/categories/plugin-marketplace)
- **Bug reports**: [GitHub Issues](https://github.com/SaltProphet/Reaper/issues)

---

**Thank you for contributing to REAPER!** Your efforts help build a better signal detection and action system for everyone.
