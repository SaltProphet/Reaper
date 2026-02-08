# REAPER

**Modular, biological pipeline for harvesting "problem friction" signals; plugin-driven and operator-ready.**

REAPER is a Python 3.11+ plugin-driven system that detects, scores, and acts on signals via a 5-sense pipeline architecture inspired by biological systems.

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

## License

MIT