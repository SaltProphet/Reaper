# [Plugin Name] Plugin

<!-- 
Replace [Plugin Name] with your plugin name throughout this document.
Replace [plugin-name] with your plugin's module/package name (lowercase, hyphens).
Replace [PLUGIN_NAME] with your plugin's environment variable prefix (UPPERCASE, underscores).
-->

**Brief one-sentence description of what this plugin does.**

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Performance](#performance)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## Overview

Provide a more detailed description (2-3 paragraphs) explaining:
- What problem this plugin solves
- How it fits into the REAPER pipeline
- What external service/API it integrates with (if any)
- Which sense type(s) it implements

**Plugin Type**: Detection | Scoring | Action (choose one or list multiple)

**Sense Type**: Sight | Hearing | Touch | Taste | Smell | Action (choose one or list multiple)

**REAPER Version**: ≥ 0.1.0 (specify minimum required version)

## Features

- ✅ Feature 1: Brief description
- ✅ Feature 2: Brief description
- ✅ Feature 3: Brief description
- ⚠️ Known Limitation 1: Brief description
- ⚠️ Known Limitation 2: Brief description

## Installation

### Prerequisites

**Required:**
- Python 3.11 or higher
- REAPER framework installed (`pip install reaper` or local installation)
- [Any other system requirements]

**Optional:**
- [Optional dependencies for advanced features]

### Install from Source

```bash
# Clone this plugin (if in separate repo)
git clone https://github.com/[your-org]/[plugin-name].git
cd [plugin-name]

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Install Dependencies Only

If plugin is part of REAPER repository:

```bash
# Core dependencies are already installed with REAPER
# Install plugin-specific dependencies if any
pip install [dependency1] [dependency2]
```

## Configuration

### Environment Variables

This plugin requires the following environment variables:

**Required:**

```bash
# API key for authentication with [service]
export [PLUGIN_NAME]_API_KEY="your-api-key-here"
```

**Optional:**

```bash
# Override default API endpoint (default: https://api.example.com)
export [PLUGIN_NAME]_ENDPOINT="https://custom-endpoint.com"

# Override request timeout in seconds (default: 30)
export [PLUGIN_NAME]_TIMEOUT="60"

# Override rate limit in requests per minute (default: 100)
export [PLUGIN_NAME]_RATE_LIMIT="200"

# Enable debug logging (default: false)
export [PLUGIN_NAME]_DEBUG="true"
```

### Getting API Credentials

Step-by-step instructions for obtaining API credentials:

1. **Sign up for [Service]**
   - Visit [service website URL]
   - Create an account or sign in
   - Navigate to API/Developer settings

2. **Generate API Key**
   - [Specific steps for the service]
   - Copy your API key
   - ⚠️ Keep this key secure! Never commit it to version control.

3. **Set Environment Variable**
   ```bash
   export [PLUGIN_NAME]_API_KEY="your-api-key-here"
   ```

4. **Verify Configuration**
   ```bash
   python -c "import os; print('API key is set!' if os.getenv('[PLUGIN_NAME]_API_KEY') else 'API key is missing!')"
   ```

### Configuration File (Optional)

If your plugin supports configuration files:

Create `config.yml` or `.env` file:

```yaml
# config.yml example
plugin_name:
  api_key: ${[PLUGIN_NAME]_API_KEY}
  endpoint: https://api.example.com
  timeout: 30
  rate_limit: 100
  options:
    option1: value1
    option2: value2
```

## Usage

### Basic Usage

```python
from reaper import PluginManager
from [plugin_module] import [PluginClass]

# Initialize plugin manager
pm = PluginManager()

# Register the plugin
plugin = [PluginClass]()
pm.register_plugin(plugin, name="[plugin-name]")

# For detection plugins:
signals = pm.detect_[sense](source="[source-identifier]")
print(f"Detected {len(signals)} signals")

# For scoring plugins:
scored = pm.score_signal(signal)[0]
print(f"Score: {scored.score:.2f}")

# For action plugins:
result = pm.execute_action(scored_signal)[0]
print(f"Action {'succeeded' if result.success else 'failed'}")
```

### Source Identifier Format

The `source` parameter format for this plugin:

**Format**: `[format description]`

**Examples:**
- `"channel-name"` - For [specific use case]
- `"https://example.com/feed"` - For [specific use case]
- `"topic-id:123"` - For [specific use case]

**Validation:**
- Must not be empty
- [Any other validation rules]

## Examples

### Example 1: Basic Detection

```python
"""Detect signals from [source description]."""
from reaper import PluginManager
from [plugin_module] import [PluginClass]

# Setup
pm = PluginManager()
plugin = [PluginClass]()
pm.register_plugin(plugin, name="[plugin-name]")

# Detect signals
signals = pm.detect_[sense](source="example-source")

# Process signals
for signal in signals:
    print(f"Signal from {signal.source}:")
    print(f"  Type: {signal.sense_type}")
    print(f"  Timestamp: {signal.timestamp}")
    print(f"  Data: {signal.raw_data}")
```

**Expected Output:**
```
Signal from example-source:
  Type: SenseType.SIGHT
  Timestamp: 2026-02-09 12:00:00+00:00
  Data: {'item_id': '123', 'title': 'Example Item'}
```

### Example 2: Complete Pipeline

```python
"""Run complete detection → scoring → action pipeline."""
from reaper import PluginManager
from [plugin_module] import [PluginClass]
from pipeline.scoring import ScoringPlugin
from pipeline.action import ActionPlugin

# Setup
pm = PluginManager()
pm.register_plugin([PluginClass](), name="detector")
pm.register_plugin(ScoringPlugin(), name="scorer")
pm.register_plugin(ActionPlugin(), name="actor")

# Run pipeline
signals = pm.detect_[sense](source="example-source")

for signal in signals:
    # Score
    scored = pm.score_signal(signal)[0]
    print(f"Signal scored: {scored.score:.2f}")
    
    # Act on high-score signals
    if scored.score >= 0.7:
        result = pm.execute_action(scored)[0]
        print(f"Action result: {result.success}")
```

### Example 3: Custom Configuration

```python
"""Use custom configuration instead of environment variables."""
from [plugin_module] import [PluginClass], PluginConfig

# Create custom config
config = PluginConfig(
    api_key="your-api-key",
    endpoint="https://custom-endpoint.com",
    timeout=60,
    rate_limit=200,
)

# Initialize plugin with custom config
plugin = [PluginClass](config=config)

# Use as normal
pm = PluginManager()
pm.register_plugin(plugin, name="[plugin-name]")
```

### Example 4: Error Handling

```python
"""Handle errors gracefully."""
import os
from reaper import PluginManager
from [plugin_module] import [PluginClass]

# Check for required environment variables
if not os.getenv("[PLUGIN_NAME]_API_KEY"):
    print("Error: [PLUGIN_NAME]_API_KEY environment variable not set")
    exit(1)

try:
    # Setup
    pm = PluginManager()
    plugin = [PluginClass]()
    pm.register_plugin(plugin, name="[plugin-name]")
    
    # Detect signals
    signals = pm.detect_[sense](source="example-source")
    
except RuntimeError as e:
    print(f"Detection failed: {e}")
    # Handle error (retry, log, alert, etc.)
except Exception as e:
    print(f"Unexpected error: {e}")
    raise
```

## API Reference

### Plugin Class: `[PluginClass]`

Main plugin class implementing REAPER hook specifications.

**Constructor:**
```python
[PluginClass](config: PluginConfig | None = None)
```

**Parameters:**
- `config` (PluginConfig, optional): Plugin configuration. If None, loads from environment variables.

**Raises:**
- `KeyError`: If required environment variables are missing and no config provided
- `ValidationError`: If configuration values are invalid

### Hook Implementations

#### `reaper_[sense]_detect(source: str) -> List[Signal]`

[Hook implementation description]

**Parameters:**
- `source` (str): Source identifier (format: [format description])

**Returns:**
- `List[Signal]`: List of detected signals

**Raises:**
- `RuntimeError`: If detection fails due to API errors
- `ValidationError`: If source format is invalid

**Performance:**
- Typical response time: [X] seconds
- Rate limit: [X] requests per minute
- Recommended batch size: [X] sources per call

### Configuration Class: `PluginConfig`

Configuration model for the plugin.

**Fields:**
- `api_key` (str, required): API key for authentication
- `endpoint` (str, default="https://api.example.com"): API endpoint URL
- `timeout` (int, default=30): Request timeout in seconds (range: 1-300)
- `rate_limit` (int, default=100): Maximum requests per minute (min: 1)

**Methods:**

#### `from_env() -> PluginConfig`

Load configuration from environment variables.

**Returns:**
- `PluginConfig`: Configuration instance

**Raises:**
- `KeyError`: If required environment variables are missing
- `ValidationError`: If configuration values are invalid

### Data Models

#### `PluginSpecificData`

Model for plugin-specific data stored in `Signal.raw_data`.

**Fields:**
- `item_id` (str, required): Unique identifier for the item
- `title` (str, required): Item title
- `metadata` (dict, optional): Additional metadata

## Testing

### Running Tests

```bash
# Run all plugin tests
pytest tests/test_[plugin_name].py

# Run with coverage
pytest tests/test_[plugin_name].py --cov=[plugin_module]

# Run specific test
pytest tests/test_[plugin_name].py::test_function_name -v
```

### Unit Tests

Unit tests mock external API calls and test plugin logic:

```bash
# Run unit tests only (fast)
pytest tests/test_[plugin_name].py -m "not integration"
```

### Integration Tests

Integration tests call real APIs (require valid credentials):

```bash
# Run integration tests (requires API key)
export [PLUGIN_NAME]_API_KEY="your-api-key"
pytest tests/test_[plugin_name].py -m integration
```

**Note:** Integration tests are skipped by default in CI. Set environment variables to enable.

### Test Coverage

Target coverage: **≥95%**

Current coverage: [X]%

```bash
# Generate coverage report
pytest tests/test_[plugin_name].py --cov=[plugin_module] --cov-report=html
open htmlcov/index.html
```

## Troubleshooting

### Common Issues

#### Issue: "KeyError: '[PLUGIN_NAME]_API_KEY'"

**Cause:** Environment variable not set

**Solution:**
```bash
export [PLUGIN_NAME]_API_KEY="your-api-key"
# Or add to your shell profile (~/.bashrc, ~/.zshrc)
```

#### Issue: "RuntimeError: Failed to detect signals"

**Cause:** API request failed (network, authentication, rate limit)

**Solutions:**
1. **Check API credentials:**
   ```bash
   python -c "import os; print(os.getenv('[PLUGIN_NAME]_API_KEY'))"
   ```

2. **Verify API endpoint is reachable:**
   ```bash
   curl [endpoint-url]
   ```

3. **Check rate limits:**
   - Default: [X] requests per minute
   - Increase with `[PLUGIN_NAME]_RATE_LIMIT` env var
   - Or wait and retry

4. **Enable debug logging:**
   ```bash
   export [PLUGIN_NAME]_DEBUG="true"
   python your_script.py
   ```

#### Issue: "ValidationError: score must be between 0.0 and 1.0"

**Cause:** Scoring plugin returned invalid score

**Solution:** This is a plugin bug. Scores should be clamped:
```python
score = max(0.0, min(1.0, raw_score))
```

#### Issue: Plugin not being called

**Causes:**
1. Missing `@hookimpl` decorator
2. Wrong hook name (e.g., `reaper_execute_action` instead of `reaper_action_execute`)
3. Plugin not registered

**Solutions:**
1. Verify decorator:
   ```python
   hookimpl = pluggy.HookimplMarker("reaper")
   
   class MyPlugin:
       @hookimpl  # Must be present!
       def reaper_sight_detect(self, source: str):
           pass
   ```

2. Verify hook name matches hookspec exactly

3. Verify registration:
   ```python
   pm = PluginManager()
   pm.register_plugin(plugin, name="my-plugin")
   print(f"Registered plugins: {len(pm.list_plugins())}")
   ```

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
export [PLUGIN_NAME]_DEBUG="true"
export PYTHONPATH="."
python -m pdb your_script.py
```

Or add logging to your script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

- **Documentation:** [Link to main REAPER docs]
- **Issues:** [Link to issue tracker]
- **Discussions:** [Link to discussions]
- **Discord/Slack:** [Link if available]

When reporting issues, include:
1. Plugin version
2. REAPER version (`python -c "import reaper; print(reaper.__version__)"`)
3. Python version (`python --version`)
4. Error message and full traceback
5. Minimal reproduction script

## Performance

### Benchmarks

Typical performance on standard hardware:

| Operation | Time | Throughput |
|-----------|------|------------|
| Single detection | [X] ms | [X] signals/sec |
| Batch detection (10 sources) | [X] ms | [X] signals/sec |
| Scoring | [X] ms | [X] scores/sec |
| Action execution | [X] ms | [X] actions/sec |

**Measured on:** [Hardware specs, e.g., "AWS t3.medium, Python 3.11"]

### Optimization Tips

1. **Use batch operations when possible:**
   ```python
   # Good: Single call for multiple items
   items = plugin._fetch_from_source(source)
   signals = Signal.create_batch([...])
   
   # Avoid: Multiple individual calls
   for item in items:
       signal = Signal(...)
   ```

2. **Configure appropriate timeouts:**
   ```bash
   # Increase for slow networks
   export [PLUGIN_NAME]_TIMEOUT="60"
   ```

3. **Respect rate limits:**
   - Monitor API rate limit headers
   - Implement backoff strategy
   - Cache results when appropriate

4. **Use connection pooling for multiple requests**

### Rate Limiting

This plugin implements rate limiting to respect API limits:

- Default: [X] requests per minute
- Configure: `export [PLUGIN_NAME]_RATE_LIMIT="200"`
- Algorithm: [Token bucket | Sliding window | etc.]

If you hit rate limits:
1. Reduce request frequency
2. Increase `RATE_LIMIT` if your API plan allows
3. Implement local caching
4. Use batch operations

## Security

### Best Practices

1. **Never hard-code credentials:**
   ```python
   # ❌ BAD
   API_KEY = "sk-1234567890"
   
   # ✅ GOOD
   API_KEY = os.environ["[PLUGIN_NAME]_API_KEY"]
   ```

2. **Never commit secrets to version control:**
   - Use `.env` files (add to `.gitignore`)
   - Use environment variables
   - Use secret management tools (AWS Secrets Manager, HashiCorp Vault)

3. **Validate all inputs:**
   - Plugin validates source format
   - Use Pydantic models for configuration
   - Sanitize data before external API calls

4. **Handle errors securely:**
   ```python
   # ❌ BAD - Exposes API key in error
   raise RuntimeError(f"Failed to call {API_KEY}")
   
   # ✅ GOOD - Generic error message
   raise RuntimeError("API call failed")
   ```

5. **Use HTTPS for all API calls**

6. **Keep dependencies updated:**
   ```bash
   pip install --upgrade [plugin-dependencies]
   ```

### Security Scanning

This plugin is scanned for vulnerabilities:
- **CodeQL**: Security code analysis
- **Dependabot**: Dependency vulnerability scanning
- **Manual Review**: Code review for security issues

Report security vulnerabilities privately to: [security contact]

### Permissions

This plugin requires the following permissions:
- Network access to `[API endpoint]`
- Read access to environment variables
- [Any other permissions]

No filesystem access required (unless using local cache).

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/[your-username]/[plugin-name].git
cd [plugin-name]

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

### Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Add tests for new functionality
4. Run tests: `pytest`
5. Run linting: `ruff check . && ruff format .`
6. Commit: `git commit -m "feat: your feature description"`
7. Push: `git push origin feature/your-feature`
8. Open a Pull Request

### Plugin Checklist

Before submitting:

- [ ] Uses `@hookimpl` decorator
- [ ] Does NOT hard-code sources
- [ ] Uses Pydantic models for data
- [ ] Includes comprehensive docstrings
- [ ] Has unit tests (≥95% coverage)
- [ ] Has integration tests (if applicable)
- [ ] Follows separation of concerns
- [ ] Environment variables documented
- [ ] README updated
- [ ] Examples provided
- [ ] Error handling implemented
- [ ] Security review completed

## License

[Specify license - typically matches REAPER's MIT license]

This plugin is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Changelog

### [Version] - YYYY-MM-DD

**Added:**
- Initial release
- Feature 1
- Feature 2

**Changed:**
- N/A

**Fixed:**
- N/A

**Security:**
- N/A

See [CHANGELOG.md](CHANGELOG.md) for full version history.

---

**Plugin maintained by:** [Your Name/Organization]

**Questions?** Ask in [GitHub Discussions](https://github.com/SaltProphet/Reaper/discussions)
