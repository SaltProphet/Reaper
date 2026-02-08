# Sense Isolation FAQ

## What is Sense Isolation?

Sense isolation is a core architectural principle of REAPER. It means that each sense (Sight, Hearing, Touch, Taste, Smell) operates independently and handles only its specific type of signal detection. Similarly, scoring and actions are separate concerns that must never be mixed with detection.

## Why is Sense Isolation Important?

1. **Maintainability**: Changes to one sense don't affect others
2. **Testability**: Each sense can be tested in isolation
3. **Extensibility**: New plugins can be added without modifying existing code
4. **Clarity**: Each component has a single, well-defined responsibility
5. **Plugin Independence**: Plugins can be swapped without breaking the pipeline

## Common Questions

### Q: Can a Sight plugin access Hearing data?

**No.** Each sense plugin should only detect signals of its own type. If you need to correlate data from multiple senses, do this in a separate scoring or action plugin, not in the detection phase.

**❌ Wrong:**
```python
class BadSightPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        # DON'T DO THIS - Sight accessing Hearing data
        hearing_data = self.get_hearing_signals()
        visual_data = self.get_visual_data(source)
        combined = self.merge(hearing_data, visual_data)
        return combined
```

**✅ Correct:**
```python
class GoodSightPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        # Only detect visual signals
        return self.get_visual_data(source)

class CorrelationScorer:
    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        # Correlation happens at scoring, not detection
        score = self.correlate_with_other_senses(signal)
        return ScoredSignal(signal=signal, score=score, ...)
```

### Q: Can I score signals inside a detection plugin?

**No.** Detection plugins should only detect and return raw signals. Scoring is a separate concern handled by scoring plugins.

**❌ Wrong:**
```python
class BadPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        signals = self.fetch_data(source)
        # DON'T DO THIS - Scoring during detection
        for signal in signals:
            signal.priority = self.calculate_priority(signal)
        return signals
```

**✅ Correct:**
```python
class GoodDetectionPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        # Only detect and return raw signals
        return self.fetch_data(source)

class GoodScoringPlugin:
    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        # Scoring happens separately
        score = self.calculate_priority(signal)
        return ScoredSignal(signal=signal, score=score, ...)
```

### Q: Can I execute actions inside a scoring plugin?

**No.** Actions should only be executed by action plugins, never during detection or scoring.

**❌ Wrong:**
```python
class BadScorer:
    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        score = self.calculate_score(signal)
        # DON'T DO THIS - Action during scoring
        if score > 0.8:
            self.send_alert(signal)
        return ScoredSignal(signal=signal, score=score, ...)
```

**✅ Correct:**
```python
class GoodScorer:
    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        # Only score, don't act
        score = self.calculate_score(signal)
        return ScoredSignal(signal=signal, score=score, ...)

class GoodAction:
    @hookimpl
    def reaper_execute_action(self, scored_signal: ScoredSignal) -> ActionResult:
        # Actions happen separately
        if scored_signal.score > 0.8:
            return self.send_alert(scored_signal)
```

### Q: Which sense should I use for my plugin?

Choose based on the **type of input**, not the content:

- **Sight**: Visual data (screenshots, images, UI elements, visual patterns)
- **Hearing**: Text/audio (conversations, transcripts, logs, messages)
- **Touch**: Interactions (clicks, API calls, user actions, events)
- **Taste**: Quality samples (metrics, measurements, quality indicators)
- **Smell**: Patterns (anomalies, trends, correlations, statistical patterns)

**Example Mappings:**

| Data Source | Sense | Why |
|------------|-------|-----|
| Reddit posts (text) | Hearing | Text-based content |
| GitHub issues (text) | Hearing | Text-based content |
| Website screenshots | Sight | Visual data |
| Click analytics | Touch | Interaction data |
| Performance metrics | Taste | Quality sampling |
| Anomaly detection | Smell | Pattern recognition |
| User behavior patterns | Smell | Pattern analysis |
| Discord messages | Hearing | Text-based communication |
| Error logs | Hearing | Text-based data |
| Response time metrics | Taste | Quality measurement |

### Q: Can one plugin implement multiple senses?

**Yes, but be careful.** While technically allowed, each sense implementation must remain isolated:

**✅ Acceptable:**
```python
class MultiSensePlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        # Sight logic - completely independent
        return self._detect_visual(source)
    
    @hookimpl
    def reaper_hearing_detect(self, source: str) -> List[Signal]:
        # Hearing logic - completely independent
        return self._detect_textual(source)
```

**❌ Not Acceptable:**
```python
class BadMultiSensePlugin:
    def __init__(self):
        self.shared_cache = {}  # Sharing state between senses
    
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        self.shared_cache['sight'] = self._detect_visual(source)
        # DON'T DO THIS - Senses shouldn't share mutable state
        return self.shared_cache['sight']
    
    @hookimpl
    def reaper_hearing_detect(self, source: str) -> List[Signal]:
        # DON'T DO THIS - Hearing depends on Sight's state
        if 'sight' in self.shared_cache:
            return self._correlate(self.shared_cache['sight'])
```

### Q: What if I need to share code between senses?

Use shared utility functions or base classes, but keep the sense implementations independent:

**✅ Correct:**
```python
class APIHelper:
    """Shared utility - not a plugin."""
    @staticmethod
    def fetch_from_api(source: str):
        # Common API logic
        pass

class SightPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        data = APIHelper.fetch_from_api(source)
        return self._process_visual(data)

class HearingPlugin:
    @hookimpl
    def reaper_hearing_detect(self, source: str) -> List[Signal]:
        data = APIHelper.fetch_from_api(source)
        return self._process_textual(data)
```

### Q: Can I hard-code a data source in my plugin?

**Never.** Sources must always be passed as parameters. This is critical for reusability and testing.

**❌ Wrong:**
```python
class BadPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        # DON'T DO THIS - Hard-coded source
        data = fetch_from("https://reddit.com/r/programming")
        return [Signal(...)]
```

**✅ Correct:**
```python
class GoodPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        # Use the provided source parameter
        data = fetch_from(source)
        return [Signal(source=source, ...)]
```

### Q: How do I pass configuration to plugins?

Use constructor parameters, not hard-coded values:

**✅ Correct:**
```python
class ConfigurablePlugin:
    def __init__(self, api_key: str, threshold: float = 0.5):
        self.api_key = api_key
        self.threshold = threshold
    
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        data = self._fetch_with_auth(source, self.api_key)
        return self._filter_by_threshold(data, self.threshold)

# Usage
pm = PluginManager()
pm.register_plugin(
    ConfigurablePlugin(api_key="my-key", threshold=0.7),
    name="sight"
)
```

### Q: What about pipeline orchestration?

Pipeline orchestration (deciding when to run which sense, how to route signals, etc.) should be handled by the operator/application layer, not within plugins.

**Responsibilities:**
- **Plugins**: Detect/score/act on signals (pure functions)
- **Plugin Manager**: Register and call plugins
- **Operator/Application**: Orchestrate the pipeline flow

## Checklist for Plugin Developers

Before submitting a plugin, verify:

- [ ] Plugin only implements its designated sense type(s)
- [ ] No hard-coded sources (all sources come from parameters)
- [ ] Detection doesn't include scoring logic
- [ ] Scoring doesn't include action logic
- [ ] Actions don't include detection or scoring logic
- [ ] No shared mutable state between different senses
- [ ] All data uses Pydantic models (Signal, ScoredSignal, ActionResult)
- [ ] Error handling is graceful (return empty lists, not exceptions)
- [ ] Plugin is independently testable

## Related Documentation

- [How to Create Plugins](how-to-create-plugins.md)
- [Architect's Curse](architects-curse.md)
- [Plugin Marketplace](https://github.com/SaltProphet/Reaper/issues)

## Still Have Questions?

Open a [Discussion](https://github.com/SaltProphet/Reaper/discussions) with the `sense-isolation` tag.
