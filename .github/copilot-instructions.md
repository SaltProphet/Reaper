# Copilot Instructions for REAPER

## Project Philosophy

REAPER is a modular, biological pipeline for harvesting "problem friction" signals. The system is plugin-driven, type-safe, and operator-ready.

### Core Principles

1. **Plugin-Driven Architecture**: All functionality via Pluggy plugins - never hard-code sources
2. **Type-Safe Data**: All data structures use Pydantic v2 models with strict validation
3. **Separation of Concerns**: Never mix pipeline roles (detection, scoring, action)
4. **No Hard-Coding**: Sources and implementations are never hard-coded in core
5. **Extensibility First**: Add new plugins without modifying core

## CRITICAL: Correct Hook Names

⚠️ **ALWAYS use these exact hook names** - incorrect names are the #1 source of bugs:

- ✅ `reaper_sight_detect` - Visual detection
- ✅ `reaper_hearing_detect` - Audio/text detection  
- ✅ `reaper_touch_detect` - Interaction detection
- ✅ `reaper_taste_detect` - Quality/sampling detection
- ✅ `reaper_smell_detect` - Pattern/anomaly detection
- ✅ `reaper_score_signal` - Signal scoring
- ✅ `reaper_action_execute` - Action execution (NOT `reaper_execute_action`!)

**Common Error**: Using `reaper_execute_action` instead of `reaper_action_execute`
**Result**: Plugin will not be called - always use `reaper_action_execute`!

## Code Conventions

### Project Structure

```
reaper/
├── models.py           # Pydantic v2 models: Signal, ScoredSignal, ActionResult, SenseType
├── hookspecs.py        # Pluggy hook specifications (HookSpecs class)
├── plugin_manager.py   # PluginManager class for plugin registration
└── __init__.py         # Package exports

pipeline/
├── sight.py      # Reference implementation for visual detection
├── hearing.py    # Reference implementation for audio/text detection
├── touch.py      # Reference implementation for interaction detection
├── taste.py      # Reference implementation for quality/sampling detection
├── smell.py      # Reference implementation for pattern/anomaly detection
├── scoring.py    # Reference implementation for signal scoring
├── action.py     # Reference implementation for action execution
└── __init__.py

tests/
├── test_models.py          # Pydantic model validation tests
├── test_plugin_manager.py  # Plugin registration and detection tests
└── test_pipeline_stubs.py  # Pipeline stub tests
```

### Import Patterns

**Correct imports for plugins:**
```python
import pluggy
from reaper.models import Signal, ScoredSignal, ActionResult, SenseType

hookimpl = pluggy.HookimplMarker("reaper")
```

**Correct imports for using plugins:**
```python
from reaper import PluginManager
from reaper.models import Signal, SenseType
```

### Plugin Development

**MUST use decorator:**
```python
hookimpl = pluggy.HookimplMarker("reaper")

class MyPlugin:
    @hookimpl  # Required!
    def reaper_sight_detect(self, source: str):
        # implementation
```

**MUST NOT hard-code sources:**
```python
# ❌ WRONG - hard-coded source
def reaper_sight_detect(self, source: str):
    return [Signal(source="hardcoded-value")]  # DON'T DO THIS!

# ✅ CORRECT - use source parameter
def reaper_sight_detect(self, source: str):
    return [Signal(source=source)]  # Always use the parameter
```

**MUST keep pipeline roles separate:**
- Detection plugins only detect (return Signal)
- Scoring plugins only score (return ScoredSignal)
- Action plugins only act (return ActionResult)
- Never mix detection + scoring, or scoring + action in one plugin

**MUST follow hookspecs:**
- All hook implementations defined in `reaper/hookspecs.py`
- Check function signatures match exactly
- Return types must match (List[Signal], ScoredSignal, ActionResult)

### Data Validation

**All models use Pydantic v2:**
```python
from pydantic import BaseModel, Field

class Signal(BaseModel):
    sense_type: SenseType  # Required enum
    source: str            # Required string
    timestamp: datetime    # Auto-generated if not provided
    raw_data: dict         # Optional, defaults to {}
    metadata: dict         # Optional, defaults to {}
```

**Score validation is enforced:**
```python
# ScoredSignal automatically validates score range
scored = ScoredSignal(
    signal=signal,
    score=0.75,  # MUST be between 0.0 and 1.0
    analysis={"method": "custom"},
    tags=["tag1", "tag2"]
)
```

**Common validation errors to avoid:**
- ❌ Score outside 0.0-1.0 range → Will raise ValidationError
- ❌ Missing required fields (sense_type, source) → Will raise ValidationError  
- ❌ Wrong type for sense_type → Must use SenseType enum
- ❌ Passing non-dict for raw_data/metadata → Will raise ValidationError

### Testing

**Test commands:**
```bash
# Run all tests with coverage
pytest -v --cov=reaper --cov=pipeline

# Run specific test file
pytest tests/test_models.py

# Run specific test
pytest tests/test_models.py::test_signal_validation -v
```

**Test file organization:**
- `tests/test_models.py` - Pydantic model tests
- `tests/test_plugin_manager.py` - Plugin registration/management tests
- `tests/test_pipeline_stubs.py` - Pipeline stub implementation tests

**Writing plugin tests:**
```python
import pytest
from reaper.models import Signal, SenseType
from reaper import PluginManager

def test_my_plugin():
    """Test plugin detection."""
    pm = PluginManager()
    pm.register_plugin(MyPlugin(), name="test-plugin")
    
    signals = pm.detect_sight(source="test-source")
    
    assert len(signals) > 0
    assert signals[0].sense_type == SenseType.SIGHT
    assert signals[0].source == "test-source"
```

**Coverage requirements:**
- Maintain 95%+ code coverage
- Test happy paths AND edge cases
- Test Pydantic validation errors
- Mock external dependencies

### Linting

**Linting commands:**
```bash
# Check formatting
ruff format --check .

# Check linting rules
ruff check .

# Auto-fix issues (safe)
ruff check --fix .

# Auto-format code
ruff format .
```

**Ruff configuration:**
- Line length: 100 characters
- Target: Python 3.11+
- Rules: E (errors), F (pyflakes), I (isort), N (naming), W (warnings)
- Exception: `reaper/hookspecs.py` ignores N805 (hooks don't use self)

**Common linting issues:**
- Unused imports → Will fail CI
- Formatting issues → Will fail CI  
- Line length > 100 → Will fail CI
- Import order issues → Will fail CI

**Pre-commit hooks:**
- Ruff runs on commit (exits if fixes needed)
- Pytest runs on push (exits on first failure)

### CI/CD Security
- GitHub Actions workflows must have explicit permissions block
- Use `permissions: contents: read` at workflow and job level
- Follow principle of least privilege

## Pipeline Architecture

The 5-sense pipeline represents distinct stages:

1. **Sight** (`pipeline/sight.py`) - Visual detection of signals
2. **Hearing** (`pipeline/hearing.py`) - Audio/textual detection of signals
3. **Touch** (`pipeline/touch.py`) - Physical/interaction detection of signals
4. **Taste** (`pipeline/taste.py`) - Quality/sampling detection of signals
5. **Smell** (`pipeline/smell.py`) - Pattern/anomaly detection of signals
6. **Action** (`pipeline/action.py`) - Execute actions on scored signals

Each sense is isolated and fully documented in `/pipeline/`.

**Hook specifications for each sense:**
```python
# Detection hooks - all take source: str, return List[Signal]
reaper_sight_detect(source: str) -> List[Signal]
reaper_hearing_detect(source: str) -> List[Signal]
reaper_touch_detect(source: str) -> List[Signal]
reaper_taste_detect(source: str) -> List[Signal]
reaper_smell_detect(source: str) -> List[Signal]

# Scoring hook - takes Signal, returns ScoredSignal
reaper_score_signal(signal: Signal) -> ScoredSignal

# Action hook - takes ScoredSignal, returns ActionResult
reaper_action_execute(scored_signal: ScoredSignal) -> ActionResult
```

## Common Errors to Avoid

### ❌ Error 1: Wrong Action Hook Name
```python
# WRONG - This will NOT be called!
@hookimpl
def reaper_execute_action(self, scored_signal):
    pass

# CORRECT - Use this exact name
@hookimpl
def reaper_action_execute(self, scored_signal):
    pass
```

### ❌ Error 2: Hard-Coding Sources
```python
# WRONG - Never hard-code sources
@hookimpl
def reaper_sight_detect(self, source: str):
    return [Signal(source="my-camera")]  # DON'T DO THIS

# CORRECT - Always use source parameter
@hookimpl
def reaper_sight_detect(self, source: str):
    return [Signal(source=source)]  # Use the parameter
```

### ❌ Error 3: Mixing Pipeline Roles
```python
# WRONG - Don't detect AND score in same plugin
@hookimpl
def reaper_sight_detect(self, source: str):
    signal = Signal(...)
    # Don't score here!
    scored = ScoredSignal(signal=signal, score=0.8)
    return [scored]  # Wrong return type!

# CORRECT - Detection only returns Signals
@hookimpl
def reaper_sight_detect(self, source: str):
    return [Signal(...)]  # Just detect
```

### ❌ Error 4: Score Out of Range
```python
# WRONG - Score must be 0.0-1.0
scored = ScoredSignal(
    signal=signal,
    score=1.5  # ValidationError!
)

# CORRECT - Clamp score to valid range
scored = ScoredSignal(
    signal=signal,
    score=max(0.0, min(1.0, raw_score))
)
```

### ❌ Error 5: Missing HookImpl Decorator
```python
# WRONG - Plugin won't be registered
class MyPlugin:
    def reaper_sight_detect(self, source: str):  # Missing decorator!
        return [Signal(...)]

# CORRECT - Always use @hookimpl
hookimpl = pluggy.HookimplMarker("reaper")

class MyPlugin:
    @hookimpl  # Required!
    def reaper_sight_detect(self, source: str):
        return [Signal(...)]
```

### ❌ Error 6: Wrong Return Type
```python
# WRONG - Detection must return List[Signal]
@hookimpl
def reaper_sight_detect(self, source: str):
    return Signal(...)  # Should be list!

# CORRECT - Always return list
@hookimpl
def reaper_sight_detect(self, source: str):
    return [Signal(...)]  # List of signals
```

### ❌ Error 7: Modifying Core Files
```python
# WRONG - Don't modify core files
# Modifying reaper/models.py, reaper/hookspecs.py, reaper/plugin_manager.py

# CORRECT - Extend via plugins
# Create new plugin file, register with PluginManager
```

## Contributing Guidelines

### Before Writing Code

1. **Check hookspecs first**: Always review `reaper/hookspecs.py` for exact signatures
2. **Respect plugin architecture**: Don't modify core files (`reaper/*`)
3. **Use existing patterns**: Look at `pipeline/*` for reference implementations
4. **Check tests**: See `tests/*` for testing patterns

### When Suggesting Code Changes

**DO:**
- ✅ Create new plugin files for functionality
- ✅ Use Pydantic models for all data
- ✅ Include docstrings with Args/Returns
- ✅ Add tests for new functionality
- ✅ Follow separation of concerns
- ✅ Use source parameters (never hard-code)
- ✅ Return correct types (List[Signal], ScoredSignal, ActionResult)

**DON'T:**
- ❌ Modify core files (`reaper/models.py`, `reaper/hookspecs.py`, `reaper/plugin_manager.py`)
- ❌ Hard-code data sources
- ❌ Mix pipeline roles (detect + score, score + act)
- ❌ Skip Pydantic validation
- ❌ Use wrong hook names
- ❌ Return wrong types

### Code Review Checklist

Before suggesting code, verify:
- [ ] Correct hook name used (check hookspecs.py)
- [ ] `@hookimpl` decorator present
- [ ] Source parameter used (not hard-coded)
- [ ] Correct return type (List[Signal], ScoredSignal, ActionResult)
- [ ] Score in 0.0-1.0 range (if applicable)
- [ ] Pydantic models used
- [ ] Docstrings included
- [ ] Tests included (if new functionality)
- [ ] No core file modifications
- [ ] Follows separation of concerns

## Common Patterns

### Plugin Registration Pattern

**Standard registration:**
```python
from reaper import PluginManager
from pipeline.sight import SightPlugin

# Create manager
pm = PluginManager()

# Register plugin with name
pm.register_plugin(SightPlugin(), name="sight")

# Unregister if needed
pm.unregister_plugin(plugin_instance)

# Check registered plugins
plugins = pm.list_plugins()  # Returns tuple of (plugin, name) pairs
count = pm.plugin_count()    # Returns count
```

### Creating a Detection Plugin

**Complete example from actual codebase:**
```python
import pluggy
from reaper.models import Signal, SenseType

hookimpl = pluggy.HookimplMarker("reaper")

class SightPlugin:
    """Visual detection plugin - reference implementation."""
    
    @hookimpl
    def reaper_sight_detect(self, source: str):
        """
        Detect visual signals from source.
        
        Args:
            source: Source identifier (e.g., "camera-1", "image-url")
        
        Returns:
            List[Signal]: Detected signals with sense_type=SIGHT
        """
        # Your detection logic here
        return [
            Signal(
                sense_type=SenseType.SIGHT,
                source=source,  # Never hard-code!
                raw_data={"detected": "visual data", "confidence": 0.85}
            )
        ]
```

**Batch signal creation for performance:**
```python
# Efficient: Create multiple signals with shared timestamp
signals = Signal.create_batch(
    signals_data=[
        {"sense_type": SenseType.SIGHT, "source": "cam1", "raw_data": {...}},
        {"sense_type": SenseType.SIGHT, "source": "cam2", "raw_data": {...}},
    ]
)
# ~30-40% faster than creating signals individually
```

### Creating a Scoring Plugin

**Complete example from actual codebase:**
```python
import pluggy
from reaper.models import Signal, ScoredSignal

hookimpl = pluggy.HookimplMarker("reaper")

class ScoringPlugin:
    """Signal scoring plugin - reference implementation."""
    
    @hookimpl
    def reaper_score_signal(self, signal: Signal):
        """
        Score a signal based on criteria.
        
        Args:
            signal: Signal to score
        
        Returns:
            ScoredSignal: Signal with score (0.0-1.0) and analysis
        """
        # Your scoring logic here
        score = self._calculate_score(signal)
        
        return ScoredSignal(
            signal=signal,
            score=max(0.0, min(1.0, score)),  # Ensure 0.0-1.0 range
            analysis={"method": "custom", "factors": ["f1", "f2"]},
            tags=["scored", "custom-method"]
        )
    
    def _calculate_score(self, signal: Signal) -> float:
        """Calculate score from signal data."""
        # Implementation
        return 0.75
```

### Creating an Action Plugin

**Complete example from actual codebase:**
```python
import pluggy
from reaper.models import ScoredSignal, ActionResult

hookimpl = pluggy.HookimplMarker("reaper")

class ActionPlugin:
    """Action execution plugin - reference implementation."""
    
    @hookimpl
    def reaper_action_execute(self, scored_signal: ScoredSignal):  # NOTE: reaper_action_execute, NOT reaper_execute_action!
        """
        Execute action on scored signal.
        
        Args:
            scored_signal: Scored signal to act upon
        
        Returns:
            ActionResult: Result of action execution
        """
        try:
            # Your action logic here
            result = self._perform_action(scored_signal)
            
            return ActionResult(
                signal=scored_signal,
                action_type="notification",
                success=True,
                result_data={"status": "sent", "details": result}
            )
        except Exception as e:
            return ActionResult(
                signal=scored_signal,
                action_type="notification",
                success=False,
                result_data={},
                error=str(e)
            )
    
    def _perform_action(self, scored_signal: ScoredSignal) -> dict:
        """Perform the actual action."""
        # Implementation
        return {"action": "completed"}
```

### Using Plugins in Pipeline

**Complete pipeline example:**
```python
from reaper import PluginManager
from pipeline.sight import SightPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.action import ActionPlugin

# Initialize
pm = PluginManager()

# Register all plugins
pm.register_plugin(SightPlugin(), name="sight")
pm.register_plugin(ScoringPlugin(), name="scoring")
pm.register_plugin(ActionPlugin(), name="action")

# Run pipeline
# 1. Detect signals
signals = pm.detect_sight(source="camera-feed-1")

# 2. Score signals
for signal in signals:
    scored_signals = pm.score_signal(signal)
    
    # 3. Execute actions on high-score signals
    for scored in scored_signals:
        if scored.score > 0.7:
            results = pm.execute_action(scored)
            for result in results:
                print(f"Action {result.action_type}: {'✓' if result.success else '✗'}")
```

## Automation Opportunities

- **Documentation**: Use GitHub Spark to auto-generate changelogs from commits
- **PR Reviews**: Leverage Copilot for code review automation
- **Plugin Testing**: Automate plugin validation against hookspecs
- **Roadmap Updates**: Keep roadmap in sync with completed milestones

## Resources

- [README.md](../../README.md) - Project overview and quick start
- [Roadmap](../../Roadmap) - Development phases and timeline
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Contributor guidelines
- Issues/Projects - Track progress and next actions

## Quick Reference Card

### Essential Imports
```python
import pluggy
from reaper import PluginManager
from reaper.models import Signal, ScoredSignal, ActionResult, SenseType

hookimpl = pluggy.HookimplMarker("reaper")
```

### Hook Names (MEMORIZE THESE!)
```python
reaper_sight_detect      # Visual detection
reaper_hearing_detect    # Audio/text detection
reaper_touch_detect      # Interaction detection
reaper_taste_detect      # Quality/sampling detection
reaper_smell_detect      # Pattern/anomaly detection
reaper_score_signal      # Signal scoring
reaper_action_execute    # Action execution (NOT reaper_execute_action!)
```

### Model Field Reference

**Signal:**
- `sense_type: SenseType` (required) - Use enum: SIGHT, HEARING, TOUCH, TASTE, SMELL, ACTION
- `source: str` (required) - Never hard-code, use parameter
- `timestamp: datetime` (auto) - Auto-generated UTC timestamp
- `raw_data: dict` (optional) - Raw signal data
- `metadata: dict` (optional) - Additional metadata

**ScoredSignal:**
- `signal: Signal` (required) - Original signal
- `score: float` (required) - Must be 0.0-1.0
- `analysis: dict` (optional) - Analysis results
- `tags: list[str]` (optional) - Classification tags

**ActionResult:**
- `signal: ScoredSignal` (required) - Signal acted upon
- `action_type: str` (required) - Type of action
- `success: bool` (required) - Success/failure flag
- `result_data: dict` (optional) - Result details
- `error: str` (optional) - Error message if failed

### Testing Commands
```bash
pytest -v --cov=reaper --cov=pipeline    # Full test with coverage
pytest tests/test_models.py              # Test specific file
ruff format . && ruff check .            # Format and lint
```

### Common Fix Commands
```bash
ruff check --fix .      # Auto-fix linting issues
ruff format .           # Auto-format code
```
