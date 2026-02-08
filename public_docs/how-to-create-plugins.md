# How to Create Plugins for REAPER

## Overview

REAPER's plugin architecture is built on [Pluggy](https://pluggy.readthedocs.io/), allowing you to extend functionality without modifying the core framework. This guide will walk you through creating custom plugins for each sense and action type.

## Core Principles

Before creating plugins, understand these fundamental rules:

1. **Never Hard-Code Sources**: Sources must always be passed as parameters, never hard-coded
2. **Separation of Concerns**: Never mix detection, scoring, and action logic
3. **Type Safety**: Always use Pydantic models for data validation
4. **Plugin Independence**: Plugins should be self-contained and not depend on other plugins

## Plugin Types

### Detection Plugins (5 Senses)

Detection plugins implement one or more of the five senses:
- **Sight**: Visual detection of signals (UI, screenshots, visual patterns)
- **Hearing**: Audio/textual detection (conversations, transcripts, text)
- **Touch**: Physical/interaction detection (clicks, gestures, API calls)
- **Taste**: Quality/sampling detection (quality metrics, samples)
- **Smell**: Pattern/anomaly detection (trends, outliers, correlations)

### Scoring Plugins

Scoring plugins analyze signals and assign priority scores (0.0-1.0).

### Action Plugins

Action plugins execute responses based on scored signals.

## Creating a Detection Plugin

### Step 1: Import Required Components

```python
import pluggy
from reaper.models import Signal, SenseType
from typing import List

# Create the hookimpl marker
hookimpl = pluggy.HookimplMarker("reaper")
```

### Step 2: Define Your Plugin Class

```python
class MyCustomSightPlugin:
    """Detects signals from a custom visual source."""
    
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        """
        Detect visual signals from the specified source.
        
        Args:
            source: The source identifier (NEVER hard-code this!)
            
        Returns:
            List of detected Signal objects
        """
        # Your custom detection logic here
        signals = []
        
        # Example: Fetch data from the source
        data = self._fetch_from_source(source)
        
        # Create Signal objects
        for item in data:
            signal = Signal(
                sense_type=SenseType.SIGHT,
                source=source,  # Always use the provided source parameter
                raw_data={
                    "content": item.content,
                    "timestamp": item.timestamp,
                    "metadata": item.metadata
                }
            )
            signals.append(signal)
        
        return signals
    
    def _fetch_from_source(self, source: str):
        """Private helper method for fetching data."""
        # Implement your source-specific logic here
        pass
```

### Step 3: Register Your Plugin

```python
from reaper import PluginManager

# Initialize the plugin manager
pm = PluginManager()

# Register your plugin
pm.register_plugin(MyCustomSightPlugin(), name="my-custom-sight")

# Use it
signals = pm.detect_sight(source="my-visual-feed")
```

## Creating a Scoring Plugin

```python
import pluggy
from reaper.models import Signal, ScoredSignal
from typing import List

hookimpl = pluggy.HookimplMarker("reaper")

class MyCustomScorer:
    """Scores signals based on custom criteria."""
    
    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        """
        Score a signal based on custom analysis.
        
        Args:
            signal: The signal to score
            
        Returns:
            ScoredSignal with score between 0.0 and 1.0
        """
        # Analyze the signal
        score = self._calculate_score(signal)
        
        # Ensure score is in valid range
        score = max(0.0, min(1.0, score))
        
        return ScoredSignal(
            signal=signal,
            score=score,
            analysis={
                "method": "custom-algorithm",
                "factors": ["keyword_match", "sentiment"],
                "confidence": 0.85
            },
            tags=["custom-scored", "high-priority"] if score > 0.7 else ["custom-scored"]
        )
    
    def _calculate_score(self, signal: Signal) -> float:
        """Private method for score calculation."""
        # Implement your scoring logic
        pass
```

## Creating an Action Plugin

```python
import pluggy
from reaper.models import ScoredSignal, ActionResult
from typing import List

hookimpl = pluggy.HookimplMarker("reaper")

class MyCustomAction:
    """Executes custom actions on scored signals."""
    
    @hookimpl
    def reaper_action_execute(self, scored_signal: ScoredSignal) -> ActionResult:
        """
        Execute an action based on a scored signal.
        
        Args:
            scored_signal: The signal with its score
            
        Returns:
            ActionResult indicating success/failure
        """
        try:
            # Execute your custom action
            self._perform_action(scored_signal)
            
            return ActionResult(
                signal=scored_signal,
                success=True,
                action_type="custom-action",
                result_data={
                    "signal_id": id(scored_signal.signal),
                    "score": scored_signal.score,
                    "action_taken": "notification_sent"
                }
            )
        except Exception as e:
            return ActionResult(
                signal=scored_signal,
                success=False,
                action_type="custom-action",
                error=str(e)
            )
    
    def _perform_action(self, scored_signal: ScoredSignal):
        """Private method for action execution."""
        # Implement your action logic
        pass
```

## Multi-Sense Plugins

You can implement multiple senses in one plugin:

```python
class MultiSensePlugin:
    """Plugin that implements multiple detection senses."""
    
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        # Sight detection logic
        pass
    
    @hookimpl
    def reaper_hearing_detect(self, source: str) -> List[Signal]:
        # Hearing detection logic
        pass
    
    @hookimpl
    def reaper_smell_detect(self, source: str) -> List[Signal]:
        # Smell detection logic
        pass
```

## Best Practices

### 1. Error Handling

Always handle errors gracefully:

```python
@hookimpl
def reaper_sight_detect(self, source: str) -> List[Signal]:
    try:
        return self._detect_signals(source)
    except Exception as e:
        print(f"Error detecting signals from {source}: {e}")
        return []  # Return empty list on error
```

### 2. Logging

Use logging for debugging and monitoring:

```python
import logging

logger = logging.getLogger(__name__)

class MyPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        logger.info(f"Detecting signals from source: {source}")
        signals = self._detect_signals(source)
        logger.info(f"Detected {len(signals)} signals")
        return signals
```

### 3. Configuration

Make your plugins configurable:

```python
class ConfigurablePlugin:
    def __init__(self, threshold: float = 0.5, max_signals: int = 100):
        self.threshold = threshold
        self.max_signals = max_signals
    
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        signals = self._detect_signals(source)
        return signals[:self.max_signals]
```

### 4. Testing

Always test your plugins:

```python
def test_my_plugin():
    plugin = MyCustomSightPlugin()
    signals = plugin.reaper_sight_detect(source="test-source")
    
    assert len(signals) > 0
    assert all(isinstance(s, Signal) for s in signals)
    assert all(s.sense_type == SenseType.SIGHT for s in signals)
```

## Common Patterns

### API Integration

```python
import requests

class APIPlugin:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @hookimpl
    def reaper_hearing_detect(self, source: str) -> List[Signal]:
        response = requests.get(
            f"https://api.example.com/{source}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        data = response.json()
        
        return [
            Signal(
                sense_type=SenseType.HEARING,
                source=source,
                raw_data=item
            )
            for item in data
        ]
```

### File-Based Detection

```python
import json
from pathlib import Path

class FilePlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        file_path = Path(source)
        
        if not file_path.exists():
            return []
        
        with open(file_path) as f:
            data = json.load(f)
        
        return [
            Signal(
                sense_type=SenseType.SIGHT,
                source=source,
                raw_data=item
            )
            for item in data
        ]
```

## Hook Specifications Reference

See [reaper/hookspecs.py](../reaper/hookspecs.py) for the complete list of available hooks:

- `reaper_sight_detect(source: str) -> List[Signal]`
- `reaper_hearing_detect(source: str) -> List[Signal]`
- `reaper_touch_detect(source: str) -> List[Signal]`
- `reaper_taste_detect(source: str) -> List[Signal]`
- `reaper_smell_detect(source: str) -> List[Signal]`
- `reaper_score_signal(signal: Signal) -> ScoredSignal`
- `reaper_action_execute(scored_signal: ScoredSignal) -> ActionResult`

## Next Steps

1. Review the [Sense Isolation FAQ](sense-isolation-faq.md) to understand sense boundaries
2. Check out the [examples directory](../examples/) for complete plugin implementations
3. Read the [Architect's Curse](architects-curse.md) for philosophical context
4. Submit your plugin to the [Plugin Marketplace](https://github.com/SaltProphet/Reaper/issues/new?template=plugin_submission.yml)

## Getting Help

- Open a [Discussion](https://github.com/SaltProphet/Reaper/discussions) for questions
- Check existing plugins in the [examples directory](../examples/)
- Review the [test suite](../tests/) for usage patterns
