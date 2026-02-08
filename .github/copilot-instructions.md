# GitHub Copilot Instructions for REAPER

## Project Master Brief

**REAPER** is a modular, biological pipeline for harvesting "problem friction" signals. It's a Python 3.11+ plugin-driven system that detects, scores, and acts on signals via a 5-sense pipeline architecture inspired by biological systems.

### Core Architecture

REAPER uses a **5-Sense Pipeline** where each sense represents one job:

1. **Sight** - Visual detection of signals
2. **Hearing** - Audio/textual detection of signals  
3. **Touch** - Physical/interaction detection of signals
4. **Taste** - Quality/sampling detection of signals
5. **Smell** - Pattern/anomaly detection of signals
6. **Action** - Execute actions on scored signals

### Critical Design Principles

When working on REAPER, **ALWAYS** follow these core principles:

#### 1. Plugin-Driven Everything
- All functionality is implemented via [Pluggy](https://pluggy.readthedocs.io/) plugins
- Use `@hookimpl` decorator for all plugin implementations
- Use `@hookspec` decorator for hook specifications in `reaper/hookspecs.py`
- Never implement business logic in the core framework

#### 2. No Hard-Coding
- **NEVER** hard-code sources in core or plugin code
- Sources must always be passed as parameters (e.g., `source="my-source"`)
- Plugin implementations decide what the source means
- Core framework is agnostic to source details

#### 3. Strict Separation of Concerns
- **NEVER** mix pipeline roles (detection, scoring, action)
- Each sense plugin does ONE thing: detect signals
- Scoring plugins only score, never detect
- Action plugins only execute actions, never score
- This separation is architectural and must be maintained

#### 4. Type Safety with Pydantic v2
- All data structures use [Pydantic v2](https://docs.pydantic.dev/latest/) models
- Use strict validation for all inputs and outputs
- Models are in `reaper/models.py`: `Signal`, `ScoredSignal`, `ActionResult`
- Always validate data at boundaries

#### 5. Extensibility First
- New plugins should be addable without modifying core code
- Use the plugin manager to register/unregister plugins dynamically
- Follow the stub implementations in `/pipeline/` as reference

### Code Standards

#### Linting
- Use **Ruff** with rules: E, F, I, N, W (configured in `pyproject.toml`)
- Line length: 100 characters
- Target: Python 3.11+
- Run `python -m ruff check .` before committing
- Run `python -m ruff check . --fix` to auto-fix issues

#### Testing
- Use **pytest** for all tests
- Test files: `test_*.py` in `/tests/`
- Run tests: `pytest` or `pytest -v` for verbose
- Coverage: `pytest --cov=reaper --cov=pipeline`
- Maintain 100% test coverage for core modules

#### Project Structure
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
│   ├── workflows/       # CI/CD workflows
│   └── copilot-instructions.md  # This file
└── example_runner.py    # Example usage
```

### Plugin Development Guidelines

#### Creating a Detection Plugin
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

#### Creating a Scoring Plugin
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

### Common Tasks

#### Adding a New Sense
1. Add hookspec to `reaper/hookspecs.py`
2. Add method to `PluginManager` in `reaper/plugin_manager.py`
3. Create stub implementation in `/pipeline/`
4. Add tests in `/tests/test_pipeline_stubs.py`
5. Update README.md with new sense documentation

#### Modifying Core Models
1. Update models in `reaper/models.py`
2. Ensure Pydantic validation is correct
3. Update all affected plugins
4. Update tests in `tests/test_models.py`
5. Run full test suite

#### Adding Dependencies
1. Add to `dependencies` in `pyproject.toml` for core deps
2. Add to `dev` in `[project.optional-dependencies]` for dev deps
3. Keep dependencies minimal - this is a lightweight framework
4. Document why the dependency is needed

### Testing Checklist

Before any PR or commit:
- [ ] `pytest` passes all tests
- [ ] `python -m ruff check .` shows no errors
- [ ] `python example_runner.py` runs successfully
- [ ] New code has test coverage
- [ ] Documentation is updated if needed

### Anti-Patterns to Avoid

❌ **DO NOT:**
- Hard-code sources anywhere in code
- Mix detection, scoring, and action logic in one plugin
- Modify core without updating tests
- Add business logic to the core framework
- Skip Pydantic validation
- Use `Any` type annotations when specific types exist
- Create circular dependencies between modules

✅ **DO:**
- Accept sources as parameters
- Keep plugins focused on one responsibility
- Use type hints everywhere
- Validate all inputs with Pydantic
- Write tests for new functionality
- Follow the stub implementations as templates
- Keep the core framework minimal and extensible

### Current Phase: Alpha

We are in **Phase 1: Core Architecture** (see `Roadmap` file):
- Core 5-sense pipeline scaffolded ✅
- Pydantic models defined ✅
- Pluggy plugin loader implemented ✅
- Reference stub implementations created ✅
- Testing infrastructure in place ✅
- Documentation complete ✅

### Next Steps

Focus areas for contributors:
1. Create real-world plugin implementations (Reddit, Discord, RSS ingestors)
2. Expand test coverage with integration tests
3. Build example applications using REAPER
4. Improve documentation with more examples
5. Add performance benchmarking

### Questions?

Refer to:
- `README.md` for user documentation
- `Roadmap` for project phases
- `example_runner.py` for usage examples
- Test files in `/tests/` for implementation examples

---

**Remember**: REAPER is about **modularity**, **extensibility**, and **clean separation of concerns**. Every change should make it easier to add new plugins without touching the core.
