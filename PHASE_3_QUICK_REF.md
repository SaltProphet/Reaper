# Phase 3 Quick Reference Guide

**Copy-paste ready prompts for GitHub Copilot**

This document provides quick-access prompts for each Phase 3 task. Simply copy the prompt and paste it to your AI coding assistant.

---

## 🔄 Ouroboros Protocol

### Basic Feedback Loop

```
Create reaper/ouroboros.py with a FeedbackLoop class that tracks signal outcomes (TP/FP/FN), calculates precision/recall/F1, and adjusts scoring thresholds. Use Pydantic models, persist to JSON, include comprehensive tests.
```

### Feedback Methods for ScoredSignal

```
Add feedback tracking methods to ScoredSignal in reaper/models.py:
- mark_true_positive() 
- mark_false_positive()
- mark_false_negative()
- get_feedback_stats()
Store feedback in signal metadata, use UTC timestamps.
```

### Feedback Plugin

```
Create pipeline/feedback.py with FeedbackPlugin that implements reaper_action_execute. Store operator feedback, update FeedbackLoop, handle threshold recalculation. Return ActionResult with success status.
```

---

## 👃 Enhanced Smell Sense (Pattern Detection)

### Trend Detector

```
Create TrendDetector class in pipeline/smell_advanced.py that detects signal frequency spikes (>2σ), identifies recurring patterns (hourly/daily/weekly), and computes correlations using sliding window analysis. Include comprehensive docstrings.
```

### Anomaly Detector

```
Create AnomalyDetector class in pipeline/smell_advanced.py using isolation forest or statistical outlier detection. Flag signals that deviate significantly from historical patterns considering score, frequency, and content similarity.
```

### Advanced Smell Plugin

```
Create SmellAdvancedPlugin in pipeline/smell_advanced.py implementing reaper_smell_detect. Buffer recent signals, run TrendDetector and AnomalyDetector, generate Signals with SenseType.SMELL when patterns found. Include analysis in raw_data.
```

---

## 👅 Enhanced Taste Sense (PCI/ROI Scoring)

### PCI Calculator

```
Create PCICalculator class in pipeline/taste_advanced.py that calculates Problem-Complexity Index (0.0-1.0) based on metadata richness, cross-references, and historical resolution difficulty. Return score with explanation.
```

### ROI Calculator

```
Create ROICalculator class in pipeline/taste_advanced.py that calculates ROI score (0.0-1.0) using formula: ROI = (impact * success_rate) / effort. Infer impact from signal type, get effort from PCI, use feedback for success_rate.
```

### Advanced Taste Plugin

```
Create TasteAdvancedPlugin in pipeline/taste_advanced.py implementing reaper_score_signal. Calculate both PCI and ROI, combine with weighted average (configurable), include detailed analysis in scored_signal.analysis, add tags like ["high-roi", "low-effort"].
```

---

## 🔔 Alert and Export Actions

### Alert Plugin

```
Create AlertPlugin in pipeline/action_alert.py implementing reaper_action_execute. Support console, email (SMTP), webhook (POST), and Slack alerts. Include signal details, score, analysis. Handle failures with retry logic. Return ActionResult.
```

### Export Plugin

```
Create ExportPlugin in pipeline/action_export.py implementing reaper_action_execute. Support JSON file, CSV, and SQLite exports. Include metadata: timestamp, sense_type, score, tags. Configurable export directory and mode. Return ActionResult.
```

### Alert/Export Configuration

```
Add AlertConfig and ExportConfig Pydantic models to reaper/models.py. AlertConfig has email_settings, webhook_urls, channels. ExportConfig has format, directory, mode, database_path. Add validation for required fields.
```

---

## 💻 Operator Console (CLI)

### Basic CLI Structure

```
Create reaper/console.py with Click or Typer CLI app. Main commands: monitor (live signal stream), feedback (mark TP/FP/FN), stats (pipeline metrics), plugins (list registered), config (show settings). Add entry point in pyproject.toml.
```

### Monitor Command

```
Implement monitor command in reaper/console.py that displays real-time signal stream using Rich library. Show table with timestamp, sense_type, source, score, tags. Color-code by score: red <0.3, yellow 0.3-0.7, green >0.7. Support filtering.
```

### Feedback Command

```
Implement feedback command in reaper/console.py that accepts signal_id and feedback_type (tp/fp/fn). Validate signal exists, call FeedbackLoop to record, show updated statistics. Handle errors gracefully with user-friendly messages.
```

### Stats Command

```
Implement stats command in reaper/console.py using Rich library. Display: total signals, signals per sense type, average score by sense, feedback statistics. Format as table with colors and proper alignment.
```

---

## ⚙️ Realtime and Batch Processing

### Signal Queue

```
Create SignalQueue class in reaper/queue.py with thread-safe operations: enqueue(), dequeue(), peek(), size(), clear(). Support priority ordering by score or timestamp. Configurable max size with overflow handling (drop oldest or raise error).
```

### Realtime Processor

```
Create RealtimeProcessor in reaper/processor.py that continuously polls SignalQueue, processes signals immediately through detect→score→action pipeline. Run in separate thread. Support start(), stop(), pause(), resume(). Emit events for monitoring.
```

### Batch Processor

```
Create BatchProcessor in reaper/processor.py that collects signals over time window or count threshold. Process batch when triggered or scheduled (cron-like). Support start(), stop(), trigger_now(). Optimize for bulk operations.
```

### Processing Configuration

```
Add ProcessingMode enum (REALTIME/BATCH/HYBRID) to reaper/models.py. Add [tool.reaper.processing] section to pyproject.toml with: mode, queue_max_size, batch_size, batch_interval_seconds. Use Pydantic for validation.
```

---

## 🤖 Collaboration & Automation

### Copilot PR Review Workflow

```
Create .github/workflows/copilot-review.yml that triggers on pull_request. Use GitHub Copilot API for automated code review. Check for: correct hook names, proper Pydantic usage, test coverage, documentation. Post comments on PR. Use permissions: contents: read, pull-requests: write.
```

### Advanced Plugin Guide

```
Create docs/ADVANCED_PLUGINS.md with guide for building advanced plugins. Explain Ouroboros integration, pattern detection, PCI/ROI scoring. Include code examples, troubleshooting section, and links to relevant source files. Use clear, beginner-friendly language.
```

### Operator Guide

```
Create docs/OPERATOR_GUIDE.md explaining how to use the operator console, provide feedback, interpret statistics, and configure REAPER. Include command examples, configuration snippets, and troubleshooting tips. Add screenshots if possible (ASCII art is fine).
```

---

## 🧪 Testing Prompts

### Ouroboros Tests

```
Create tests/test_ouroboros.py with comprehensive tests for FeedbackLoop. Test: feedback recording, threshold adjustment logic, persistence/loading, mock operator scenarios. Use pytest fixtures for common test data. Aim for 95%+ coverage.
```

### Smell Advanced Tests

```
Create tests/test_smell_advanced.py with tests for TrendDetector and AnomalyDetector. Test: spike detection with synthetic data, pattern recognition with periodic signals, anomaly detection with outliers, buffering logic. Use parametrized tests.
```

### Taste Advanced Tests

```
Create tests/test_taste_advanced.py with tests for PCICalculator and ROICalculator. Test: PCI calculation with various signals, ROI with different scenarios, composite scoring, edge cases (missing data, zeros). Use mock feedback data.
```

### Action Tests

```
Create tests/test_action_alert.py and tests/test_action_export.py. Mock external services (SMTP, webhooks, file I/O). Test all alert channels and export formats. Test error handling, retry logic, configuration loading. Use pytest-mock.
```

### Console Tests

```
Create tests/test_console.py using Click.CliRunner. Test each command: monitor (with mock signals), feedback (validation), stats (formatting), plugins (listing), config (display). Test filtering and error cases.
```

### Processor Tests

```
Create tests/test_queue.py and tests/test_processor.py. Test SignalQueue thread safety with concurrent access. Test RealtimeProcessor and BatchProcessor lifecycle. Test mode switching, error recovery, event emission. Use threading/asyncio test utilities.
```

---

## 📋 Configuration Templates

### Ouroboros Configuration

```toml
[tool.reaper.feedback]
storage_path = "data/feedback.json"
min_samples_before_adjustment = 100
adjustment_frequency = "daily"
```

### Alert Configuration

```toml
[tool.reaper.alerts]
enabled_channels = ["console", "webhook"]
webhook_url = "https://hooks.example.com/reaper"
smtp_host = "smtp.gmail.com"
smtp_port = 587
smtp_user = "alerts@example.com"
```

### Export Configuration

```toml
[tool.reaper.exports]
format = "json"
directory = "data/exports"
mode = "append"
database_path = "data/signals.db"
```

### Processing Configuration

```toml
[tool.reaper.processing]
mode = "realtime"
queue_max_size = 10000
batch_size = 100
batch_interval_seconds = 60
```

---

## 🎯 One-Line Quick Commands

**Run all Phase 3 tests:**
```bash
pytest tests/test_ouroboros.py tests/test_smell_advanced.py tests/test_taste_advanced.py tests/test_action_*.py tests/test_console.py tests/test_queue.py tests/test_processor.py -v --cov
```

**Check Phase 3 files linting:**
```bash
ruff check reaper/ouroboros.py reaper/console.py reaper/queue.py reaper/processor.py pipeline/smell_advanced.py pipeline/taste_advanced.py pipeline/action_alert.py pipeline/action_export.py
```

**Format Phase 3 files:**
```bash
ruff format reaper/ouroboros.py reaper/console.py reaper/queue.py reaper/processor.py pipeline/*.py
```

**Run console in dev mode:**
```bash
python -m reaper.console monitor --filter score:>0.5
```

---

## 🔍 Debugging Tips

### Test Feedback Loop
```python
from reaper.ouroboros import FeedbackLoop

loop = FeedbackLoop()
loop.record_feedback(signal_id="test-123", outcome="true_positive")
stats = loop.get_stats()
print(f"Precision: {stats['precision']:.2f}")
```

### Test Pattern Detection
```python
from pipeline.smell_advanced import TrendDetector

detector = TrendDetector(window_size=100)
spike_detected = detector.detect_spike(signal_stream)
print(f"Spike detected: {spike_detected}")
```

### Test Console Commands
```python
from click.testing import CliRunner
from reaper.console import cli

runner = CliRunner()
result = runner.invoke(cli, ['stats'])
assert result.exit_code == 0
print(result.output)
```

---

## 📚 Reference Links

- **Roadmap**: See `Roadmap` file, Phase 3 section (lines 38-51)
- **Copilot Instructions**: `.github/copilot-instructions.md`
- **Contributing Guide**: `CONTRIBUTING.md`
- **Main README**: `README.md`
- **Phase 3 Full Plan**: `PHASE_3_PLAN.md`

---

## ✅ Phase 3 Completion Checklist

Copy this checklist to track progress:

```markdown
## Phase 3 Progress

### Core Development
- [ ] Ouroboros Protocol implemented
- [ ] Enhanced Smell sense (pattern detection)
- [ ] Enhanced Taste sense (PCI/ROI scoring)
- [ ] Alert plugin (console, email, webhook, Slack)
- [ ] Export plugin (JSON, CSV, SQLite)
- [ ] Operator console CLI
- [ ] Realtime processor
- [ ] Batch processor

### Testing
- [ ] test_ouroboros.py (95%+ coverage)
- [ ] test_smell_advanced.py (95%+ coverage)
- [ ] test_taste_advanced.py (95%+ coverage)
- [ ] test_action_alert.py (95%+ coverage)
- [ ] test_action_export.py (95%+ coverage)
- [ ] test_console.py (90%+ coverage)
- [ ] test_queue.py (95%+ coverage)
- [ ] test_processor.py (95%+ coverage)

### Documentation
- [ ] docs/ADVANCED_PLUGINS.md created
- [ ] docs/OPERATOR_GUIDE.md created
- [ ] CONTRIBUTING.md updated
- [ ] All docstrings complete

### Quality Gates
- [ ] All tests pass
- [ ] 95%+ overall coverage
- [ ] Ruff linting passes
- [ ] CodeQL security scan passes
- [ ] Code review complete
```

---

**Need help?** Paste any prompt above into GitHub Copilot or Claude and start building! 🚀
