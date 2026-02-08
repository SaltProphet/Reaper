# Getting Started with REAPER

Welcome to REAPER! This guide will help you get up and running quickly.

## What is REAPER?

REAPER is a **plugin-driven signal processing pipeline** inspired by biological systems. It detects "problem friction" signals from various sources, scores them by priority, and executes appropriate actions—all through a modular, extensible architecture.

Think of it as a **nervous system for problem detection**: Senses gather signals, the brain scores them, and actions respond.

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Basic understanding of Python
- (Optional) Git for cloning the repository

## Installation

### Option 1: Install from Source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/SaltProphet/Reaper.git
cd Reaper

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Option 2: Quick Install (Future - PyPI)

```bash
# Coming soon
pip install reaper
```

## Your First REAPER Program

### Step 1: Create a Simple Script

Create a file called `my_first_reaper.py`:

```python
from reaper import PluginManager
from pipeline.sight import SightPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.action import ActionPlugin

# Initialize the plugin manager
pm = PluginManager()

# Register plugins
pm.register_plugin(SightPlugin(), name="sight")
pm.register_plugin(ScoringPlugin(), name="scoring")
pm.register_plugin(ActionPlugin(), name="action")

print("REAPER initialized successfully! ✓")

# Detect signals
signals = pm.detect_sight(source="test-source")
print(f"Detected {len(signals)} signals")

# Score the first signal
if signals:
    scored = pm.score_signal(signals[0])[0]
    print(f"Signal score: {scored.score:.2f}")
    
    # Execute action
    result = pm.execute_action(scored)[0]
    print(f"Action {'succeeded' if result.success else 'failed'}")
```

### Step 2: Run It

```bash
python my_first_reaper.py
```

You should see output indicating signals were detected, scored, and acted upon!

## Running the Example

REAPER comes with a complete example demonstrating all five senses:

```bash
python example_runner.py
```

This runs a full pipeline:
1. **Sight** detects visual signals
2. **Hearing** detects textual signals
3. **Touch** detects interaction signals
4. **Taste** detects quality signals
5. **Smell** detects pattern signals
6. All signals are **scored**
7. High-priority signals trigger **actions**

## Understanding the Architecture

### The 5-Sense Pipeline

REAPER organizes signal detection into five biological senses:

| Sense | Purpose | Example Use Cases |
|-------|---------|-------------------|
| **Sight** | Visual detection | Screenshots, UI elements, visual patterns |
| **Hearing** | Text/audio detection | Logs, messages, conversations, transcripts |
| **Touch** | Interaction detection | Clicks, API calls, user events |
| **Taste** | Quality detection | Metrics, measurements, quality samples |
| **Smell** | Pattern detection | Anomalies, trends, correlations |

### The Pipeline Flow

```
1. DETECTION → Senses detect raw signals
2. SCORING   → Signals are evaluated for priority
3. ACTION    → High-priority signals trigger responses
```

### Core Principles

- **Separation of Concerns**: Never mix detection, scoring, and action
- **No Hard-Coding**: Always parameterize sources
- **Type Safety**: Use Pydantic models for all data
- **Plugin-Driven**: Everything is a replaceable plugin

## Creating Your First Plugin

### Simple Detection Plugin

Create a file called `my_plugin.py`:

```python
import pluggy
from reaper.models import Signal, SenseType
from typing import List

hookimpl = pluggy.HookimplMarker("reaper")

class MyHearingPlugin:
    """Detects signals from text sources."""
    
    @hookimpl
    def reaper_hearing_detect(self, source: str) -> List[Signal]:
        # In a real plugin, you'd fetch data from the source
        # For now, we'll create a mock signal
        
        return [
            Signal(
                sense_type=SenseType.HEARING,
                source=source,
                raw_data={
                    "text": f"Sample text from {source}",
                    "timestamp": "2024-01-01T00:00:00Z"
                }
            )
        ]

# Test it
if __name__ == "__main__":
    from reaper import PluginManager
    
    pm = PluginManager()
    pm.register_plugin(MyHearingPlugin(), name="my-hearing")
    
    signals = pm.detect_hearing(source="my-text-feed")
    print(f"Detected {len(signals)} signals")
    print(f"First signal: {signals[0].raw_data}")
```

Run it:

```bash
python my_plugin.py
```

Congratulations! You've created your first REAPER plugin! 🎉

## Testing Your Code

REAPER uses [pytest](https://docs.pytest.org/) for testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=reaper --cov=pipeline

# Run specific test file
pytest tests/test_models.py
```

### Writing Tests for Your Plugin

Create `test_my_plugin.py`:

```python
from my_plugin import MyHearingPlugin
from reaper.models import SenseType

def test_my_hearing_plugin():
    plugin = MyHearingPlugin()
    signals = plugin.reaper_hearing_detect(source="test-source")
    
    assert len(signals) == 1
    assert signals[0].sense_type == SenseType.HEARING
    assert signals[0].source == "test-source"
    assert "text" in signals[0].raw_data
```

Run your test:

```bash
pytest test_my_plugin.py
```

## Project Structure

```
Reaper/
├── reaper/              # Core framework
│   ├── models.py        # Pydantic data models
│   ├── hookspecs.py     # Plugin hook specifications
│   └── plugin_manager.py # Plugin management
├── pipeline/            # Reference plugin implementations
│   ├── sight.py         # Sight detection stub
│   ├── hearing.py       # Hearing detection stub
│   ├── touch.py         # Touch detection stub
│   ├── taste.py         # Taste detection stub
│   ├── smell.py         # Smell detection stub
│   ├── scoring.py       # Scoring stub
│   └── action.py        # Action stub
├── tests/               # Test suite
├── public_docs/         # Documentation (you are here!)
├── examples/            # Example plugins and configs
├── example_runner.py    # Complete pipeline example
├── pyproject.toml       # Project configuration
└── README.md            # Main README
```

## Development Workflow

1. **Install in development mode**: `pip install -e ".[dev]"`
2. **Make your changes**: Edit code or add plugins
3. **Run tests**: `pytest` to ensure nothing breaks
4. **Run linter**: `ruff check .` to check code quality
5. **Format code**: `ruff format .` to auto-format
6. **Test manually**: Run `example_runner.py` or your own scripts

## Next Steps

Now that you're set up, here's what to explore next:

### For Learning
1. Read the [Architect's Curse](architects-curse.md) to understand REAPER's philosophy
2. Review the [Sense Isolation FAQ](sense-isolation-faq.md) for boundary rules
3. Check out the [examples/](../examples/) directory for real-world plugins

### For Building
1. Follow the [How to Create Plugins](how-to-create-plugins.md) guide
2. Study the [Operator Console Walkthrough](operator-console-walkthrough.md)
3. Browse the codebase in `reaper/` and `pipeline/`

### For Contributing
1. Check open [Issues](https://github.com/SaltProphet/Reaper/issues)
2. Read [CONTRIBUTING.md](../CONTRIBUTING.md) (if available)
3. Join [Discussions](https://github.com/SaltProphet/Reaper/discussions)
4. Submit a [Pull Request](https://github.com/SaltProphet/Reaper/pulls)

## Common Issues

### Import Errors

If you see `ModuleNotFoundError: No module named 'reaper'`:

```bash
# Make sure you installed the package
pip install -e .

# Or reinstall
pip uninstall reaper
pip install -e .
```

### Python Version Issues

REAPER requires Python 3.11+:

```bash
# Check your version
python --version

# If needed, use python3.11 explicitly
python3.11 -m venv venv
```

### Plugin Not Found

If your plugin isn't being called:

```python
# Make sure you registered it
pm.register_plugin(MyPlugin(), name="my-plugin")

# Check it was registered
print(pm.list_plugins())  # Should show your plugin
```

## Getting Help

- **Documentation**: You're reading it! Check other docs in `public_docs/`
- **Examples**: See `examples/` for working code
- **Discussions**: [GitHub Discussions](https://github.com/SaltProphet/Reaper/discussions)
- **Issues**: [Bug Reports](https://github.com/SaltProphet/Reaper/issues)

## Resources

- [Main README](../README.md) - Project overview
- [Roadmap](../Roadmap) - Future plans
- [LICENSE](../LICENSE) - MIT License
- [Pluggy Docs](https://pluggy.readthedocs.io/) - Plugin framework
- [Pydantic Docs](https://docs.pydantic.dev/latest/) - Data validation

---

**Welcome to REAPER! Happy coding! 🚀**
