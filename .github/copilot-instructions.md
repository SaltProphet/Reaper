# Copilot Instructions for REAPER

## Project Philosophy

REAPER is a modular, biological pipeline for harvesting "problem friction" signals. The system is plugin-driven, type-safe, and operator-ready.

### Core Principles

1. **Plugin-Driven Architecture**: All functionality via Pluggy plugins - never hard-code sources
2. **Type-Safe Data**: All data structures use Pydantic v2 models with strict validation
3. **Separation of Concerns**: Never mix pipeline roles (detection, scoring, action)
4. **No Hard-Coding**: Sources and implementations are never hard-coded in core
5. **Extensibility First**: Add new plugins without modifying core

## Code Conventions

### Plugin Development
- Always use `pluggy.HookimplMarker("reaper")` decorator
- Never hard-code data sources - accept source as parameter
- Keep pipeline roles separate: detection, scoring, and action are distinct
- All plugins must follow hookspecs defined in `reaper/hookspecs.py`

### Data Validation
- Use Pydantic v2 models for all data structures
- Enforce strict validation with appropriate field types
- Signal scores must be in range 0.0-1.0

### Testing
- Run tests with `pytest -v --cov=reaper --cov=pipeline`
- Write tests in separate files: `test_models.py`, `test_plugin_manager.py`, `test_pipeline_stubs.py`
- Maintain 95%+ code coverage

### Linting
- Repo uses Ruff with rules: E, F, I, N, W
- Run linting before commits to avoid CI failures
- Unused imports and formatting issues will fail CI

### CI/CD Security
- GitHub Actions workflows must have explicit permissions block
- Use `permissions: contents: read` at workflow and job level
- Follow principle of least privilege

## Pipeline Architecture

The 5-sense pipeline represents distinct stages:

1. **Sight** - Visual detection of signals
2. **Hearing** - Audio/textual detection of signals
3. **Touch** - Physical/interaction detection of signals
4. **Taste** - Quality/sampling detection of signals
5. **Smell** - Pattern/anomaly detection of signals
6. **Action** - Execute actions on scored signals

Each sense is isolated and fully documented in `/pipeline/`.

## Contributing Guidelines

When suggesting code changes:
1. Respect the plugin architecture - don't violate core principles
2. Include appropriate Pydantic validation
3. Add tests for new functionality
4. Update documentation if adding new features
5. Follow the roadmap phases (see [Roadmap](../../Roadmap))

## Common Patterns

### Creating a Detection Plugin
```python
import pluggy
from reaper.models import Signal, SenseType

hookimpl = pluggy.HookimplMarker("reaper")

class MyPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str):
        return [Signal(
            sense_type=SenseType.SIGHT,
            source=source,  # Never hard-code!
            raw_data={"key": "value"}
        )]
```

### Creating a Scoring Plugin
```python
import pluggy
from reaper.models import Signal, ScoredSignal

hookimpl = pluggy.HookimplMarker("reaper")

class MyScorer:
    @hookimpl
    def reaper_score_signal(self, signal: Signal):
        return ScoredSignal(
            signal=signal,
            score=0.75,  # 0.0-1.0 range
            analysis={"method": "custom"},
            tags=["custom"]
        )
```

## Automation Opportunities

- **Documentation**: Use GitHub Spark to auto-generate changelogs from commits
- **PR Reviews**: Leverage Copilot for code review automation
- **Plugin Testing**: Automate plugin validation against hookspecs
- **Roadmap Updates**: Keep roadmap in sync with completed milestones

## Resources

- [README.md](../../README.md) - Project overview and quick start
- [Roadmap](../../Roadmap) - Development phases and timeline
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Contributor guidelines
- Issues/Projects - Track progress and next actions
