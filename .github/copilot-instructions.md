# GitHub Copilot Instructions for REAPER

## Project Context

REAPER is a **modular, plugin-driven pipeline system** for detecting, scoring, and acting on "problem friction" signals. It follows a biological 5-sense architecture.

## Core Principles

### 1. Plugin Architecture
- **Always use Pluggy**: All functionality must be implemented as Pluggy plugins
- **Never hard-code sources**: Sources must always be passed as parameters
- **Use hookimpl decorator**: `@pluggy.HookimplMarker("reaper")` for all plugin methods
- **Separation of concerns**: Keep detection, scoring, and action separate

### 2. Data Models
- **Use Pydantic v2**: All data structures must use Pydantic models
- **Strict validation**: Enable strict mode for type safety
- **Type hints required**: Always include type hints (Python 3.11+)
- **Core models**:
  - `Signal`: Base signal with sense_type, source, raw_data
  - `ScoredSignal`: Signal with score (0.0-1.0), analysis, tags
  - `ActionResult`: Action execution result with success status

### 3. Code Style
- **Linter**: Ruff (E, F, I, N, W rules)
- **Line length**: 100 characters maximum
- **Import organization**: Standard library → Third party → Local
- **Naming conventions**:
  - Classes: PascalCase
  - Functions/methods: snake_case
  - Constants: UPPER_SNAKE_CASE

## Plugin Implementation Patterns

### Detection Plugin Template
```python
import pluggy
from reaper.models import Signal, SenseType

hookimpl = pluggy.HookimplMarker("reaper")

class MyDetectionPlugin:
    @hookimpl
    def reaper_<sense>_detect(self, source: str) -> list[Signal]:
        # source is NEVER hard-coded
        # Return list of Signal objects
        return [
            Signal(
                sense_type=SenseType.<SENSE>,
                source=source,
                raw_data={"key": "value"}
            )
        ]
```

### Scoring Plugin Template
```python
import pluggy
from reaper.models import Signal, ScoredSignal

hookimpl = pluggy.HookimplMarker("reaper")

class MyScoringPlugin:
    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        # Calculate score (must be 0.0 to 1.0)
        score = self._calculate_score(signal)
        
        return ScoredSignal(
            signal=signal,
            score=score,
            analysis={"method": "description"},
            tags=["tag1", "tag2"]
        )
```

### Action Plugin Template
```python
import pluggy
from reaper.models import ScoredSignal, ActionResult

hookimpl = pluggy.HookimplMarker("reaper")

class MyActionPlugin:
    @hookimpl
    def reaper_execute_action(self, signal: ScoredSignal) -> ActionResult:
        # Execute action based on scored signal
        success = self._execute(signal)
        
        return ActionResult(
            signal=signal,
            success=success,
            action_type="action_name",
            metadata={"details": "info"}
        )
```

## Testing Patterns

### Test Structure
```python
import pytest
from reaper.models import Signal, SenseType

def test_plugin_functionality():
    # Arrange
    plugin = MyPlugin()
    
    # Act
    result = plugin.method()
    
    # Assert
    assert isinstance(result, ExpectedType)
    assert result.field == expected_value
```

### Test Coverage Requirements
- All new plugins must have tests
- Aim for >80% coverage
- Test both success and failure cases
- Test edge cases and validation

## Common Mistakes to Avoid

1. ❌ **Hard-coding sources**
   ```python
   # WRONG
   def reaper_sight_detect(self, source: str):
       return detect_from("hardcoded-source")
   
   # CORRECT
   def reaper_sight_detect(self, source: str):
       return detect_from(source)
   ```

2. ❌ **Mixing pipeline roles**
   ```python
   # WRONG - detection plugin doing scoring
   def reaper_sight_detect(self, source: str):
       signals = self._detect(source)
       scored = self._score(signals)  # Don't do this!
       return signals
   
   # CORRECT - keep separate
   def reaper_sight_detect(self, source: str):
       return self._detect(source)
   ```

3. ❌ **Missing type hints**
   ```python
   # WRONG
   def process_signal(signal):
       return signal.score
   
   # CORRECT
   def process_signal(signal: Signal) -> float:
       return signal.score
   ```

4. ❌ **Not using Pydantic models**
   ```python
   # WRONG
   def create_signal():
       return {"sense_type": "sight", "source": "test"}
   
   # CORRECT
   def create_signal() -> Signal:
       return Signal(
           sense_type=SenseType.SIGHT,
           source="test",
           raw_data={}
       )
   ```

## Sense Types Reference

- **SIGHT**: Visual detection (UI, displays, dashboards)
- **HEARING**: Audio/textual detection (logs, messages, notifications)
- **TOUCH**: Interaction detection (user actions, clicks, API calls)
- **TASTE**: Quality/sampling detection (metrics, samples, probes)
- **SMELL**: Pattern/anomaly detection (trends, outliers, alerts)

## Hookspec Reference

Available hooks defined in `reaper/hookspecs.py`:
- `reaper_sight_detect(source: str) -> list[Signal]`
- `reaper_hearing_detect(source: str) -> list[Signal]`
- `reaper_touch_detect(source: str) -> list[Signal]`
- `reaper_taste_detect(source: str) -> list[Signal]`
- `reaper_smell_detect(source: str) -> list[Signal]`
- `reaper_score_signal(signal: Signal) -> ScoredSignal`
- `reaper_execute_action(signal: ScoredSignal) -> ActionResult`

## Development Workflow

1. **Create plugin** following templates above
2. **Add tests** in `tests/` directory
3. **Run linter**: `ruff check .`
4. **Run tests**: `pytest`
5. **Verify coverage**: `pytest --cov=reaper --cov=pipeline`
6. **Update documentation** if adding new features

## Example Use Cases

When generating code, consider these example scenarios:
- **GitHub Issues**: Detect issues with labels, score by priority, create notifications
- **Slack Messages**: Listen for keywords, score by sentiment, post responses
- **API Metrics**: Sample endpoint performance, score by latency, trigger alerts
- **Log Patterns**: Detect error patterns, score by frequency, create tickets
- **User Interactions**: Track clicks/actions, score by engagement, update dashboards

## Questions?

- Check `README.md` for architecture overview
- Review `example_runner.py` for complete pipeline example
- See `tests/` for testing patterns
- Refer to `reaper/models.py` for data model definitions
