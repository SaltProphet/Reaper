# Phase 2 Quick Reference

**Quick-start guide for Phase 2 contributors**

---

## 🎯 Phase 2 Goals

**Beta Release: Pipeline Completion**
- Real-world plugins (not just stubs)
- End-to-end integration tests
- Community engagement (Discussions, Projects)
- Plugin ecosystem expansion

---

## 📋 Current Status

### Completed (Phase 1)
- ✅ Core architecture (Pluggy plugins, Pydantic models)
- ✅ 5-sense pipeline stubs (sight, hearing, touch, taste, smell, action)
- ✅ 136 tests, 96% coverage
- ✅ Developer tooling (Codespaces, Copilot instructions)

### In Progress (Phase 2)
- 🔄 Real-world plugin development
- 🔄 Integration test suite
- 🔄 Community engagement setup
- 🔄 Plugin documentation automation

---

## 🔌 Plugin Development Cheat Sheet

### Detection Plugin Template
```python
import pluggy
from reaper.models import Signal, SenseType

hookimpl = pluggy.HookimplMarker("reaper")

class MyDetectionPlugin:
    """Detects signals from [source type]."""
    
    @hookimpl
    def reaper_[sense]_detect(self, source: str):
        """
        Detect signals from source.
        
        Args:
            source: Source identifier (never hard-code!)
        
        Returns:
            List[Signal]: Detected signals
        """
        # Your detection logic here
        return [
            Signal(
                sense_type=SenseType.[SENSE],
                source=source,  # Always use parameter!
                raw_data={"key": "value"},
                metadata={"optional": "data"}
            )
        ]
```

**Replace `[sense]` with**: sight, hearing, touch, taste, smell  
**Replace `[SENSE]` with**: SIGHT, HEARING, TOUCH, TASTE, SMELL

---

### Scoring Plugin Template
```python
import pluggy
from reaper.models import Signal, ScoredSignal

hookimpl = pluggy.HookimplMarker("reaper")

class MyScoringPlugin:
    """Scores signals based on [criteria]."""
    
    @hookimpl
    def reaper_score_signal(self, signal: Signal):
        """
        Score a signal.
        
        Args:
            signal: Signal to score
        
        Returns:
            ScoredSignal: Signal with score (0.0-1.0)
        """
        # Your scoring logic here
        raw_score = self._calculate_score(signal)
        
        # Ensure score is in valid range
        score = max(0.0, min(1.0, raw_score))
        
        return ScoredSignal(
            signal=signal,
            score=score,
            analysis={"method": "custom", "factors": []},
            tags=["custom-scorer"]
        )
    
    def _calculate_score(self, signal: Signal) -> float:
        # Implementation
        return 0.75
```

---

### Action Plugin Template
```python
import pluggy
from reaper.models import ScoredSignal, ActionResult

hookimpl = pluggy.HookimplMarker("reaper")

class MyActionPlugin:
    """Executes [action type] on scored signals."""
    
    @hookimpl
    def reaper_action_execute(self, scored_signal: ScoredSignal):
        """
        Execute action on scored signal.
        
        Args:
            scored_signal: Signal to act upon
        
        Returns:
            ActionResult: Result of action
        """
        try:
            # Your action logic here
            result = self._perform_action(scored_signal)
            
            return ActionResult(
                signal=scored_signal,
                action_type="my-action",
                success=True,
                result_data={"status": "completed", "details": result}
            )
        except Exception as e:
            return ActionResult(
                signal=scored_signal,
                action_type="my-action",
                success=False,
                result_data={},
                error=str(e)
            )
    
    def _perform_action(self, scored_signal: ScoredSignal) -> dict:
        # Implementation
        return {"action": "done"}
```

---

## 🧪 Testing Cheat Sheet

### Unit Test Template
```python
import pytest
from reaper import PluginManager
from reaper.models import Signal, SenseType
from my_plugin import MyPlugin

def test_my_plugin_detection():
    """Test plugin detects signals correctly."""
    pm = PluginManager()
    pm.register_plugin(MyPlugin(), name="test-plugin")
    
    signals = pm.detect_sight(source="test-source")
    
    assert len(signals) > 0
    assert signals[0].sense_type == SenseType.SIGHT
    assert signals[0].source == "test-source"
    assert "key" in signals[0].raw_data

def test_my_plugin_error_handling():
    """Test plugin handles errors gracefully."""
    pm = PluginManager()
    pm.register_plugin(MyPlugin(), name="test-plugin")
    
    # Test with invalid source
    signals = pm.detect_sight(source="")
    assert signals == []  # Should return empty list, not crash
```

---

### Integration Test Template
```python
import pytest
from reaper import PluginManager
from reaper.models import SenseType
from my_detection_plugin import MyDetectionPlugin
from my_scoring_plugin import MyScoringPlugin
from my_action_plugin import MyActionPlugin

def test_end_to_end_pipeline():
    """Test complete pipeline: detect → score → act."""
    pm = PluginManager()
    
    # Register plugins
    pm.register_plugin(MyDetectionPlugin(), name="detector")
    pm.register_plugin(MyScoringPlugin(), name="scorer")
    pm.register_plugin(MyActionPlugin(), name="actor")
    
    # 1. Detect signals
    signals = pm.detect_sight(source="test-source")
    assert len(signals) > 0
    
    # 2. Score signals
    scored_signals = pm.score_signal(signals[0])
    assert len(scored_signals) > 0
    assert 0.0 <= scored_signals[0].score <= 1.0
    
    # 3. Execute actions
    results = pm.execute_action(scored_signals[0])
    assert len(results) > 0
    assert results[0].success is True
```

---

## 🚀 Development Workflow

### 1. Setup Development Environment
```bash
# Clone repo
git clone https://github.com/SaltProphet/Reaper.git
cd Reaper

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### 2. Create New Plugin
```bash
# Create plugin file
touch my_plugin.py

# Create test file
touch tests/test_my_plugin.py

# Implement plugin (use templates above)
# Add tests (use templates above)
```

### 3. Test Your Plugin
```bash
# Run tests
pytest tests/test_my_plugin.py -v

# Run with coverage
pytest tests/test_my_plugin.py --cov=my_plugin

# Run all tests
pytest -v
```

### 4. Lint Your Code
```bash
# Check formatting
ruff format --check .

# Auto-fix formatting
ruff format .

# Check linting
ruff check .

# Auto-fix linting
ruff check --fix .
```

### 5. Submit Pull Request
```bash
# Create branch
git checkout -b feature/my-plugin

# Commit changes
git add my_plugin.py tests/test_my_plugin.py
git commit -m "Add MyPlugin for [functionality]"

# Push branch
git push origin feature/my-plugin

# Open PR on GitHub
# Follow PR template
```

---

## ⚠️ Common Mistakes to Avoid

### ❌ Hard-Coding Sources
```python
# WRONG
def reaper_sight_detect(self, source: str):
    return [Signal(source="hardcoded")]  # DON'T!

# CORRECT
def reaper_sight_detect(self, source: str):
    return [Signal(source=source)]  # Use parameter
```

---

### ❌ Wrong Hook Name
```python
# WRONG
@hookimpl
def reaper_execute_action(self, scored_signal):  # Wrong name!
    pass

# CORRECT
@hookimpl
def reaper_action_execute(self, scored_signal):  # Correct name
    pass
```

---

### ❌ Missing @hookimpl Decorator
```python
# WRONG
class MyPlugin:
    def reaper_sight_detect(self, source: str):  # Missing decorator!
        pass

# CORRECT
hookimpl = pluggy.HookimplMarker("reaper")

class MyPlugin:
    @hookimpl  # Required!
    def reaper_sight_detect(self, source: str):
        pass
```

---

### ❌ Score Out of Range
```python
# WRONG
return ScoredSignal(signal=signal, score=1.5)  # > 1.0!

# CORRECT
score = max(0.0, min(1.0, raw_score))  # Clamp to 0.0-1.0
return ScoredSignal(signal=signal, score=score)
```

---

### ❌ Mixing Pipeline Roles
```python
# WRONG - Don't detect AND score in same plugin
@hookimpl
def reaper_sight_detect(self, source: str):
    signal = Signal(...)
    scored = ScoredSignal(signal=signal, score=0.8)  # Don't score here!
    return [scored]  # Wrong type!

# CORRECT - Detection only returns Signals
@hookimpl
def reaper_sight_detect(self, source: str):
    return [Signal(...)]  # Just detect
```

---

## 📚 Resources

### Documentation
- [Phase 2 Plan](PHASE_2_PLAN.md) - Detailed Phase 2 roadmap
- [README](README.md) - Project overview
- [CONTRIBUTING](CONTRIBUTING.md) - Contributor guide
- [Copilot Instructions](.github/copilot-instructions.md) - AI coding guide

### Examples
- [Example Runner](example_runner.py) - Complete pipeline example
- [Pipeline Stubs](pipeline/) - Reference implementations
- [Tests](tests/) - Test examples

### Community
- [GitHub Discussions](https://github.com/SaltProphet/Reaper/discussions) - Q&A, ideas
- [Issues](https://github.com/SaltProphet/Reaper/issues) - Bug reports, features
- [Projects](https://github.com/SaltProphet/Reaper/projects) - Phase 2 tracking

---

## 🎯 Phase 2 Priorities (What to Work On)

### High Priority
1. **Real-World Ingestors**
   - RedditIngestor (monitor subreddits)
   - DiscordIngestor (listen to channels)
   - RSSIngestor (parse feeds)

2. **Scoring Plugins**
   - KeywordScorer (keyword matching)
   - SentimentScorer (sentiment analysis)
   - UrgencyScorer (priority determination)

3. **Action Plugins**
   - NotificationAction (Slack/Discord/Email)
   - TicketAction (GitHub/Jira tickets)
   - WebhookAction (POST to webhooks)

### Medium Priority
4. **Integration Tests**
   - End-to-end pipeline tests
   - Multi-source tests
   - Error handling tests

5. **Documentation**
   - Plugin development guide
   - API reference
   - Troubleshooting guide

### Low Priority
6. **Automation**
   - Plugin docs generator
   - Template generator
   - CI/CD enhancements

---

## 💡 Plugin Ideas (Need Contributors!)

### Ingestors
- GitHub Issues/PRs monitor
- Log file tailer
- Slack message monitor
- Twitter feed monitor
- Email inbox monitor

### Scorers
- ML-based sentiment scorer
- Regex pattern scorer
- Time-based urgency scorer
- Multi-factor scorer

### Actions
- Webhook poster
- File writer
- Database inserter
- API caller
- Email sender

---

## 🎉 Quick Wins (Easy First Contributions)

1. **Add Plugin Example**: Create real-world plugin with tests
2. **Improve Documentation**: Add examples to existing docs
3. **Write Integration Test**: Test end-to-end pipeline flow
4. **Fix Typos**: Improve docs, comments, error messages
5. **Add Discussion Post**: Share plugin ideas, ask questions

---

## 📞 Getting Help

### I have a question
- Check [README](README.md) and [docs](public_docs/)
- Search [Discussions](https://github.com/SaltProphet/Reaper/discussions)
- Ask in Discussions (Q&A category)

### I found a bug
- Check [existing issues](https://github.com/SaltProphet/Reaper/issues)
- Open new issue using [bug template](.github/ISSUE_TEMPLATE/bug_report.yml)

### I want to contribute
- Read [CONTRIBUTING.md](CONTRIBUTING.md)
- Pick issue from [Projects board](https://github.com/SaltProphet/Reaper/projects)
- Ask questions in Discussions

---

**Last Updated**: 2026-02-08  
**Phase 2 Status**: 🚀 STARTING SOON  
**Next Milestone**: Sense Module Completion (Weeks 1-2)
