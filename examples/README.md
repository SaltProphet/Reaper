# REAPER Examples

This directory contains examples, sample configurations, and reference implementations to help you get started with REAPER.

## Contents

- **[simple_pipeline.py](#simple_pipelinepy)** - Basic pipeline example
- **[multi_source_monitor.py](#multi_source_monitorpy)** - Monitor multiple sources
- **[custom_plugin_example.py](#custom_plugin_examplepy)** - Create a custom plugin
- **[mission_configs/](#mission-configs)** - Sample mission configurations
- **[sample_signals/](#sample-signals)** - Sample signal data for testing

## Running Examples

```bash
# Run from the repository root
python examples/simple_pipeline.py
python examples/multi_source_monitor.py
python examples/custom_plugin_example.py
```

## simple_pipeline.py

Basic pipeline demonstrating the three core phases: detection, scoring, and action.

**What it demonstrates:**
- Plugin registration
- Signal detection
- Scoring signals
- Executing actions
- Basic error handling

## multi_source_monitor.py

Monitor multiple sources across different senses simultaneously.

**What it demonstrates:**
- Multiple source monitoring
- Multi-sense detection
- Source prioritization
- Batch signal processing

## multi_source_monitor.py

Monitor multiple sources across different senses simultaneously.

**What it demonstrates:**
- Multiple source monitoring
- Multi-sense detection
- Source prioritization
- Batch signal processing

## custom_plugin_example.py

Complete example of creating and using a custom plugin.

**What it demonstrates:**
- Plugin development
- Hook implementation
- Configuration handling
- Testing your plugin

## Mission Configs

Sample mission configurations for different use cases:

- **reddit_monitor.yaml** - Monitor Reddit for signals
- **github_issues.yaml** - Track GitHub issues
- **log_analyzer.yaml** - Analyze application logs

## Sample Signals

Pre-built signal datasets for testing:

- **visual_signals.json** - Sample Sight signals
- **text_signals.json** - Sample Hearing signals
- **interaction_signals.json** - Sample Touch signals
- **quality_signals.json** - Sample Taste signals
- **pattern_signals.json** - Sample Smell signals

## Using Samples in Your Code

```python
import json
from reaper.models import Signal

# Load sample signals
with open('examples/sample_signals/text_signals.json') as f:
    sample_data = json.load(f)

# Use in your plugin for testing
signals = [Signal(**data) for data in sample_data]
```

## Contributing Examples

Have a useful example? Submit it via a [Pull Request](../CONTRIBUTING.md)!

Examples should:
- Be self-contained and runnable
- Include clear comments
- Demonstrate a specific pattern or use case
- Follow REAPER's architectural principles
- Include sample data if needed

## Next Steps

- Review the [Getting Started Guide](../public_docs/getting-started.md)
- Read [How to Create Plugins](../public_docs/how-to-create-plugins.md)
- Explore [Operator Console Walkthrough](../public_docs/operator-console-walkthrough.md)
- Check the [Plugin Marketplace](https://github.com/SaltProphet/Reaper/issues?q=label%3Aplugin)
