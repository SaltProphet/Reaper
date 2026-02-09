# REAPER

[![CI](https://github.com/SaltProphet/Reaper/actions/workflows/ci.yml/badge.svg)](https://github.com/SaltProphet/Reaper/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/SaltProphet/Reaper/branch/main/graph/badge.svg)](https://codecov.io/gh/SaltProphet/Reaper)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Modular, biological pipeline for harvesting "problem friction" signals; plugin-driven and operator-ready.**

REAPER is a Python 3.11+ plugin-driven system that detects, scores, and acts on signals via a 5-sense pipeline architecture inspired by biological systems.

📚 **[Documentation](public_docs/)** | 🚀 **[Getting Started](public_docs/getting-started.md)** | 🔌 **[Plugin Guide](public_docs/how-to-create-plugins.md)** | 💬 **[Discussions](https://github.com/SaltProphet/Reaper/discussions)** | 🗺️ **[Phase 2 Plan](PHASE_2_PLAN.md)** | 🤖 **[Copilot Prompts](COPILOT_PROMPTS_INDEX.md)**

## Architecture

### 5-Sense Pipeline

Each sense represents one job in the pipeline:

1. **Sight** - Visual detection of signals
2. **Hearing** - Audio/textual detection of signals  
3. **Touch** - Physical/interaction detection of signals
4. **Taste** - Quality/sampling detection of signals
5. **Smell** - Pattern/anomaly detection of signals
6. **Action** - Execute actions on scored signals

### Core Principles

- **Plugin-Driven**: All functionality via [Pluggy](https://pluggy.readthedocs.io/) plugins
- **Type-Safe**: Data validation with [Pydantic v2](https://docs.pydantic.dev/latest/)
- **No Hard-Coding**: Sources and implementations are never hard-coded in core
- **Separation of Concerns**: Never mix pipeline roles (detection, scoring, action)
- **Extensible**: Add new plugins without modifying core

## Installation

```bash
# Install from source
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/SaltProphet/Reaper.git
cd Reaper

# Install the package
pip install -e .

# Or install with dev dependencies (recommended for contributors)
pip install -e ".[dev]"
```

### 2. Run the Example

```bash
# Run the complete pipeline example
python example_runner.py
```

This demonstrates:
- ✅ All 5 sense plugins detecting signals
- ✅ Scoring plugin evaluating signals
- ✅ Action plugin executing on signals
- ✅ Complete end-to-end pipeline flow

### 3. Create Your First Plugin

```python
from reaper import PluginManager
from pipeline.sight import SightPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.action import ActionPlugin

# Initialize plugin manager
pm = PluginManager()

# Register plugins
pm.register_plugin(SightPlugin(), name="sight")
pm.register_plugin(ScoringPlugin(), name="scoring")
pm.register_plugin(ActionPlugin(), name="action")

# Detect signals (source is plugin-specific, never hard-coded)
signals = pm.detect_sight(source="my-visual-source")

# Score signals
scored = pm.score_signal(signals[0])[0]

# Execute actions
result = pm.execute_action(scored)[0]
print(f"Action {'succeeded' if result.success else 'failed'}")
```

**What's happening here?**
1. `PluginManager` coordinates all plugins
2. Plugins implement hook specifications (detection, scoring, action)
3. `source` parameter is plugin-specific (never hard-coded in core)
4. Data flows through type-safe Pydantic models
5. Multiple plugins can handle the same hook

### 4. Verify Installation

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=reaper --cov=pipeline

# Expected: 136 tests passing, 96%+ coverage
```

## Troubleshooting

### Common Issues

**Import Error: No module named 'reaper'**
```bash
# Solution: Install in editable mode
pip install -e .
```

**Import Error: No module named 'pluggy' or 'pydantic'**
```bash
# Solution: Install dependencies
pip install pluggy pydantic
```

**Tests Failing**
```bash
# Check if you're in the correct directory
pwd  # Should show .../Reaper

# Reinstall in editable mode
pip uninstall -y reaper
pip install -e .

# Run tests
pytest -v
```

**Coverage Not 96%+**
```bash
# Make sure all test files are included
pytest --cov=reaper --cov=pipeline --cov-report=term-missing

# Check which lines are missing coverage
# Note: hookspecs.py will show some uncovered lines (pass statements) - this is expected
```

**Example Runner Not Working**
```bash
# Verify Python version (requires 3.11+)
python --version

# Reinstall dependencies
pip install -e .

# Run with verbose output
python -v example_runner.py
```

**Ruff Linting Errors**
```bash
# Install ruff
pip install ruff

# Check formatting
ruff format --check .

# Auto-fix formatting
ruff format .

# Check linting
ruff check .

# Auto-fix linting issues
ruff check --fix .
```

### Getting Help

- 📖 **Documentation**: Check [public_docs/](public_docs/) for guides
- 💬 **Discussions**: Ask in [GitHub Discussions](https://github.com/SaltProphet/Reaper/discussions)
- 🐛 **Bugs**: Report using [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml)
- 🔌 **Plugin Help**: See [Plugin Development Guide](public_docs/how-to-create-plugins.md)

## Running the Example

```bash
python example_runner.py
```

This demonstrates all 5 senses plus action in a complete pipeline.

## Creating Custom Plugins

### Detection Plugin Example

```python
import pluggy
from reaper.models import Signal, SenseType

hookimpl = pluggy.HookimplMarker("reaper")

class MyCustomPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str):
        # Your custom detection logic
        return [
            Signal(
                sense_type=SenseType.SIGHT,
                source=source,  # Never hard-code!
                raw_data={"detected": "custom data"}
            )
        ]
```

### Scoring Plugin Example

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

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=reaper --cov=pipeline
```

## Project Structure

```
Reaper/
├── reaper/              # Core framework
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
└── example_runner.py    # Example usage
```

## Development

The stubs in `/pipeline/` are reference implementations. To add real functionality:

1. Create a new plugin implementing the appropriate hookspecs
2. Register it with the PluginManager
3. Never hard-code sources or mix pipeline roles
4. Always use Pydantic models for data validation

## Contributing

We welcome contributions! Here's how to get started:

### Quick Start

**Use GitHub Codespaces** for instant setup:
1. Click "Code" → "Create codespace"
2. Everything is pre-configured (Python 3.11, dependencies, tools)
3. Start coding immediately!

**Or contribute locally**:
- See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
- Check [Roadmap](Roadmap) for current priorities
- Browse [open issues](https://github.com/SaltProphet/Reaper/issues) for tasks

### Ways to Contribute

- 🐛 **Report bugs**: Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml)
- ✨ **Suggest features**: Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.yml)
- 🔌 **Build plugins**: Use our [plugin submission template](.github/ISSUE_TEMPLATE/plugin_submission.yml)
- 📖 **Improve docs**: Documentation PRs are always welcome
- 💬 **Join discussions**: Share ideas in [GitHub Discussions](https://github.com/SaltProphet/Reaper/discussions)

### Community & Collaboration

- **Discussions**: Q&A, plugin marketplace, ideas
- **GitHub Projects**: Track roadmap progress
- **GitHub Spaces**: Collaborative design sessions
- **Copilot Integration**: AI-assisted development with project-specific instructions

See our guides:
- [Projects Guide](.github/PROJECTS_GUIDE.md)
- [Spaces Guide](.github/SPACES_GUIDE.md)
- [Spark Automation Guide](.github/SPARK_AUTOMATION_GUIDE.md)
- [Copilot Instructions](.github/copilot-instructions.md)

## License

MIT
