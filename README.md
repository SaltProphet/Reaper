# REAPER

[![CI](https://github.com/SaltProphet/Reaper/actions/workflows/ci.yml/badge.svg)](https://github.com/SaltProphet/Reaper/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/SaltProphet/Reaper/branch/main/graph/badge.svg)](https://codecov.io/gh/SaltProphet/Reaper)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Modular, biological pipeline for harvesting "problem friction" signals; plugin-driven and operator-ready.**

REAPER is a Python 3.11+ plugin-driven system that detects, scores, and acts on signals via a 5-sense pipeline architecture inspired by biological systems.

📚 **[Documentation](public_docs/)** | 🚀 **[Getting Started](public_docs/getting-started.md)** | 🔌 **[Plugin Guide](public_docs/how-to-create-plugins.md)** | 💬 **[Discussions](https://github.com/SaltProphet/Reaper/discussions)**

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

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

## Contributing

We welcome contributions! Here's how to get started:

1. **Read the Docs**: Start with [Getting Started](public_docs/getting-started.md) and [Architect's Curse](public_docs/architects-curse.md)
2. **Pick an Issue**: Browse [open issues](https://github.com/SaltProphet/Reaper/issues) or start a [discussion](https://github.com/SaltProphet/Reaper/discussions)
3. **Submit a Plugin**: Share your plugin via [Plugin Submission](https://github.com/SaltProphet/Reaper/issues/new?template=plugin_submission.yml)
4. **Improve Docs**: Help make REAPER more accessible

See [CONTRIBUTING.md](CONTRIBUTING.md) for complete guidelines.

## Community

- 💬 **[Discussions](https://github.com/SaltProphet/Reaper/discussions)** - Ask questions, share ideas
- 🐛 **[Issue Tracker](https://github.com/SaltProphet/Reaper/issues)** - Report bugs, request features
- 🔌 **[Plugin Marketplace](https://github.com/SaltProphet/Reaper/issues?q=label%3Aplugin)** - Discover and share plugins
- 📚 **[Documentation](public_docs/)** - Comprehensive guides and references

## Quick Links

- [Getting Started Guide](public_docs/getting-started.md) - Your first steps
- [Plugin Development Guide](public_docs/how-to-create-plugins.md) - Create plugins
- [Sense Isolation FAQ](public_docs/sense-isolation-faq.md) - Understand boundaries
- [Operator Console Walkthrough](public_docs/operator-console-walkthrough.md) - Run pipelines
- [Architect's Curse](public_docs/architects-curse.md) - Philosophy and vision
- [Examples Directory](examples/) - Real-world examples

## License

MIT
