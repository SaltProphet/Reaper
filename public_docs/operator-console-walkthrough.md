# Operator Console Walkthrough

## Overview

The REAPER Operator Console is your command center for managing the signal detection and processing pipeline. This guide walks through the operator experience, from initialization to signal action.

## Console Modes

REAPER can be operated in several modes:

1. **Interactive Python**: Direct API usage (current implementation)
2. **CLI Mode**: Command-line interface (future)
3. **Web UI**: Browser-based console (future)

This walkthrough focuses on the current **Interactive Python** mode.

## Getting Started

### Step 1: Initialize the Environment

```bash
# Activate your environment
source venv/bin/activate  # or your preferred method

# Install REAPER
pip install -e .

# For development
pip install -e ".[dev]"
```

### Step 2: Create Your Operator Script

Create a file called `operator.py`:

```python
from reaper import PluginManager
from pipeline.sight import SightPlugin
from pipeline.hearing import HearingPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.action import ActionPlugin

# Initialize the plugin manager
pm = PluginManager()

# Register your pipeline plugins
pm.register_plugin(SightPlugin(), name="sight")
pm.register_plugin(HearingPlugin(), name="hearing")
pm.register_plugin(ScoringPlugin(), name="scoring")
pm.register_plugin(ActionPlugin(), name="action")

print("REAPER Operator Console initialized ✓")
```

### Step 3: Run the Console

```bash
python operator.py
```

## Basic Operations

### Detecting Signals

Each sense can detect signals from its specific source type:

```python
# Detect visual signals
sight_signals = pm.detect_sight(source="visual-feed-01")
print(f"Detected {len(sight_signals)} visual signals")

# Detect textual signals
hearing_signals = pm.detect_hearing(source="text-stream-01")
print(f"Detected {len(hearing_signals)} textual signals")

# Detect interaction signals
touch_signals = pm.detect_touch(source="event-stream-01")
print(f"Detected {len(touch_signals)} interaction signals")

# Detect quality signals
taste_signals = pm.detect_taste(source="metrics-feed-01")
print(f"Detected {len(taste_signals)} quality signals")

# Detect pattern signals
smell_signals = pm.detect_smell(source="analytics-feed-01")
print(f"Detected {len(smell_signals)} pattern signals")
```

### Scoring Signals

Once you have signals, score them to determine priority:

```python
# Score a single signal
signal = sight_signals[0]
scored_signal = pm.score_signal(signal)[0]

print(f"Signal score: {scored_signal.score:.2f}")
print(f"Analysis: {scored_signal.analysis}")
print(f"Tags: {scored_signal.tags}")
```

### Executing Actions

Based on the score, execute actions:

```python
# Execute action on scored signal
result = pm.execute_action(scored_signal)[0]

if result.success:
    print(f"Action succeeded: {result.action_type}")
    print(f"Details: {result.result_data}")
else:
    print(f"Action failed: {result.error}")
```

## Complete Pipeline Example

Here's a full operator workflow:

```python
def run_pipeline(pm: PluginManager, source: str):
    """Run a complete signal processing pipeline."""
    
    # 1. Detection Phase
    print(f"\n=== DETECTION from {source} ===")
    signals = pm.detect_sight(source=source)
    print(f"Detected {len(signals)} signals")
    
    if not signals:
        print("No signals detected")
        return
    
    # 2. Scoring Phase
    print("\n=== SCORING ===")
    scored_signals = []
    for signal in signals:
        scored = pm.score_signal(signal)[0]
        scored_signals.append(scored)
        print(f"Signal {id(signal)} → Score: {scored.score:.2f}")
    
    # 3. Filtering Phase
    print("\n=== FILTERING ===")
    threshold = 0.5
    high_priority = [s for s in scored_signals if s.score >= threshold]
    print(f"{len(high_priority)}/{len(scored_signals)} signals above threshold {threshold}")
    
    # 4. Action Phase
    print("\n=== ACTIONS ===")
    for scored_signal in high_priority:
        result = pm.execute_action(scored_signal)[0]
        status = "✓" if result.success else "✗"
        print(f"{status} Action: {result.action_type}")
    
    print("\n=== PIPELINE COMPLETE ===")

# Run the pipeline
run_pipeline(pm, source="production-feed")
```

## Advanced Operations

### Multi-Source Monitoring

Monitor multiple sources simultaneously:

```python
sources = [
    ("sight", "visual-feed-01"),
    ("sight", "visual-feed-02"),
    ("hearing", "text-stream-01"),
    ("touch", "event-stream-01"),
]

all_signals = []

for sense_type, source in sources:
    if sense_type == "sight":
        signals = pm.detect_sight(source=source)
    elif sense_type == "hearing":
        signals = pm.detect_hearing(source=source)
    elif sense_type == "touch":
        signals = pm.detect_touch(source=source)
    
    all_signals.extend(signals)
    print(f"Collected {len(signals)} signals from {source}")

print(f"\nTotal signals: {len(all_signals)}")
```

### Batch Processing

Process signals in batches:

```python
def batch_process(pm: PluginManager, signals: list, batch_size: int = 10):
    """Process signals in batches."""
    
    for i in range(0, len(signals), batch_size):
        batch = signals[i:i+batch_size]
        print(f"\nProcessing batch {i//batch_size + 1} ({len(batch)} signals)")
        
        # Score batch
        scored_batch = [pm.score_signal(s)[0] for s in batch]
        
        # Filter high priority
        high_priority = [s for s in scored_batch if s.score >= 0.7]
        
        # Execute actions
        for scored in high_priority:
            pm.execute_action(scored)
        
        print(f"Actioned {len(high_priority)} high-priority signals")

# Usage
signals = pm.detect_sight(source="bulk-feed")
batch_process(pm, signals, batch_size=20)
```

### Custom Filtering

Apply custom filters before action:

```python
def custom_filter(scored_signals: list, min_score: float, required_tags: list):
    """Filter signals by score and tags."""
    
    filtered = []
    for signal in scored_signals:
        if signal.score < min_score:
            continue
        
        if not all(tag in signal.tags for tag in required_tags):
            continue
        
        filtered.append(signal)
    
    return filtered

# Usage
scored = [pm.score_signal(s)[0] for s in signals]
critical = custom_filter(
    scored,
    min_score=0.8,
    required_tags=["critical", "urgent"]
)
print(f"Found {len(critical)} critical signals")
```

## Monitoring and Logging

### Basic Logging Setup

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("reaper.operator")

# Use in pipeline
logger.info("Starting pipeline")
signals = pm.detect_sight(source="feed-01")
logger.info(f"Detected {len(signals)} signals")
```

### Performance Monitoring

```python
import time

def timed_pipeline(pm: PluginManager, source: str):
    """Pipeline with performance timing."""
    
    start = time.time()
    
    # Detection
    detect_start = time.time()
    signals = pm.detect_sight(source=source)
    detect_time = time.time() - detect_start
    
    # Scoring
    score_start = time.time()
    scored = [pm.score_signal(s)[0] for s in signals]
    score_time = time.time() - score_start
    
    # Actions
    action_start = time.time()
    for s in scored:
        if s.score >= 0.5:
            pm.execute_action(s)
    action_time = time.time() - action_start
    
    total_time = time.time() - start
    
    print(f"\nPerformance Metrics:")
    print(f"  Detection: {detect_time:.2f}s ({len(signals)} signals)")
    print(f"  Scoring:   {score_time:.2f}s")
    print(f"  Actions:   {action_time:.2f}s")
    print(f"  Total:     {total_time:.2f}s")
```

## Error Handling

### Graceful Degradation

```python
import logging

logger = logging.getLogger(__name__)

def safe_pipeline(pm: PluginManager, source: str):
    """Pipeline with comprehensive error handling."""
    
    try:
        # Detection
        signals = pm.detect_sight(source=source)
        if not signals:
            logger.warning(f"No signals from {source}")
            return
        
        # Scoring
        scored_signals = []
        for signal in signals:
            try:
                scored = pm.score_signal(signal)[0]
                scored_signals.append(scored)
            except Exception as e:
                logger.error(f"Scoring failed for signal: {e}")
                continue
        
        # Actions
        for scored in scored_signals:
            if scored.score < 0.5:
                continue
            
            try:
                result = pm.execute_action(scored)[0]
                if not result.success:
                    logger.warning(f"Action failed: {result.error}")
            except Exception as e:
                logger.error(f"Action execution failed: {e}")
                continue
    
    except Exception as e:
        logger.critical(f"Pipeline failure: {e}")
        raise
```

## Configuration Management

### Operator Configuration File

Create a `config.yaml`:

```yaml
sources:
  sight:
    - name: "visual-feed-01"
      enabled: true
      priority: high
    - name: "visual-feed-02"
      enabled: true
      priority: medium
  
  hearing:
    - name: "text-stream-01"
      enabled: true
      priority: high

thresholds:
  action: 0.5
  critical: 0.8
  
batch_size: 20
log_level: INFO
```

Load and use:

```python
import yaml

def load_config(path: str):
    with open(path) as f:
        return yaml.safe_load(f)

config = load_config("config.yaml")

# Use configuration
for source_config in config['sources']['sight']:
    if not source_config['enabled']:
        continue
    
    signals = pm.detect_sight(source=source_config['name'])
    # ... process signals
```

## Operational Best Practices

### 1. Start Small

Begin with a single source and sense:

```python
# Start with one sense, one source
signals = pm.detect_sight(source="test-feed")
```

### 2. Test Your Pipeline

Always test with known data first:

```python
# Use test/mock sources
test_signals = pm.detect_sight(source="test-data")
assert len(test_signals) > 0, "No test signals detected"
```

### 3. Monitor Performance

Track processing times and signal volumes:

```python
metrics = {
    'total_signals': 0,
    'high_priority': 0,
    'actions_executed': 0,
}
```

### 4. Implement Circuit Breakers

Prevent runaway processing:

```python
MAX_SIGNALS = 1000
signals = pm.detect_sight(source="feed")
if len(signals) > MAX_SIGNALS:
    logger.warning(f"Signal count {len(signals)} exceeds limit {MAX_SIGNALS}")
    signals = signals[:MAX_SIGNALS]
```

### 5. Use Dry-Run Mode

Test without executing actions:

```python
def dry_run_pipeline(pm: PluginManager, source: str):
    signals = pm.detect_sight(source=source)
    scored = [pm.score_signal(s)[0] for s in signals]
    
    print(f"Would action {len([s for s in scored if s.score >= 0.5])} signals")
    # Don't actually execute actions
```

## Next Steps

1. Review the [How to Create Plugins](how-to-create-plugins.md) guide
2. Check out [examples/](../examples/) for complete operator scripts
3. Read the [Sense Isolation FAQ](sense-isolation-faq.md)
4. Join [Discussions](https://github.com/SaltProphet/Reaper/discussions) for operator tips

## Troubleshooting

### No Signals Detected

- Verify source parameter is correct
- Check plugin is registered: `pm.list_plugins()`
- Test plugin in isolation

### Low Scores

- Review scoring logic in your scorer plugin
- Check signal data quality
- Adjust scoring thresholds

### Action Failures

- Check action plugin error messages
- Verify external dependencies (APIs, databases)
- Test actions with mock data first

## Future Features

The following features are planned for future releases:

- **CLI Interface**: Command-line console with interactive prompts
- **Web Dashboard**: Browser-based monitoring and control
- **Real-time Streaming**: Continuous signal processing
- **Pipeline Visualization**: Visual pipeline flow monitoring
- **Alert System**: Automated notifications for critical signals
- **Historical Analytics**: Signal trend analysis over time

Stay tuned to the [Roadmap](../Roadmap) for updates!
