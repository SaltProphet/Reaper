# Phase 3: Learning & Operator Experience

**Timeline**: TBD (Post Phase 2 completion)  
**Status**: Planning  
**Goal**: Add self-improvement capabilities, operator tools, and advanced signal processing

---

## Overview

Phase 3 introduces the "learning" capabilities of REAPER through the Ouroboros Protocol (self-improving filters), advanced signal processing, and operator tooling for real-world deployment.

### Key Deliverables

1. **Ouroboros Protocol** - Self-improving filters based on PCI/feedback
2. **Pattern Detection** - Enhanced Smell sense for trend/anomaly detection
3. **PCI/ROI Scoring** - Enhanced Taste sense for quality assessment
4. **Alert/Export Actions** - Production-ready Action plugins
5. **Operator Console** - CLI or web UI for signal monitoring
6. **Realtime/Batch Processing** - Dual-mode signal handling

---

## Task 1: Implement Ouroboros Protocol

### Context
The Ouroboros Protocol enables REAPER to learn from operator feedback and automatically adjust signal filtering thresholds. This creates a self-improving system that gets better over time.

### AI-Ready Prompt

```
Implement the Ouroboros Protocol for REAPER's self-improving signal filtering system.

Requirements:
1. Create a FeedbackLoop class in reaper/ouroboros.py that:
   - Tracks signal outcomes (true positive, false positive, false negative)
   - Calculates precision, recall, and F1 score over time
   - Adjusts scoring thresholds based on feedback
   - Persists feedback data to disk (JSON or SQLite)

2. Add feedback methods to ScoredSignal model:
   - mark_true_positive()
   - mark_false_positive()
   - mark_false_negative()
   - get_feedback_stats()

3. Create FeedbackPlugin that implements reaper_action_execute to:
   - Store feedback when operators mark signals
   - Update the FeedbackLoop with new data
   - Trigger threshold recalculation periodically

4. Add configuration in pyproject.toml:
   - feedback_storage_path
   - min_samples_before_adjustment (default: 100)
   - adjustment_frequency (default: daily)

5. Write comprehensive tests in tests/test_ouroboros.py:
   - Test feedback recording
   - Test threshold adjustment logic
   - Test persistence and loading
   - Test with mock operator feedback scenarios

Follow REAPER conventions:
- Use Pydantic v2 models for all data structures
- Follow plugin-driven architecture
- Use proper hookimpl decorators
- Include docstrings with Args/Returns sections
- Maintain 95%+ test coverage
```

### Acceptance Criteria
- [ ] FeedbackLoop class tracks outcomes and adjusts thresholds
- [ ] ScoredSignal model has feedback methods
- [ ] FeedbackPlugin properly stores and processes feedback
- [ ] Configuration options in pyproject.toml
- [ ] 95%+ test coverage
- [ ] All tests pass
- [ ] Ruff linting passes

---

## Task 2: Enhanced Pattern Detection (Smell Sense)

### Context
The Smell sense detects patterns, trends, and anomalies in signal streams. Phase 3 enhances this with statistical analysis and machine learning capabilities.

### AI-Ready Prompt

```
Enhance the Smell sense with advanced pattern and trend detection capabilities.

Requirements:
1. Create TrendDetector class in pipeline/smell_advanced.py:
   - Detect signal frequency spikes (>2σ from rolling mean)
   - Identify recurring patterns (hourly, daily, weekly cycles)
   - Compute correlation between signal types
   - Use sliding window analysis (configurable window size)

2. Create AnomalyDetector class in pipeline/smell_advanced.py:
   - Implement isolation forest or simple statistical outlier detection
   - Flag signals that deviate significantly from historical patterns
   - Consider multiple features: score, frequency, content similarity

3. Create SmellAdvancedPlugin implementing reaper_smell_detect:
   - Buffer recent signals for analysis (last N signals or time window)
   - Run TrendDetector and AnomalyDetector on buffer
   - Generate new Signals when patterns/anomalies detected
   - Include analysis results in signal.raw_data

4. Add models in reaper/models.py:
   - TrendSignal (extends Signal, adds trend_type, confidence, window_data)
   - AnomalySignal (extends Signal, adds anomaly_score, expected_range)

5. Write comprehensive tests in tests/test_smell_advanced.py:
   - Test spike detection with synthetic data
   - Test pattern recognition with periodic signals
   - Test anomaly detection with outliers
   - Test buffering and sliding window logic

Follow REAPER conventions:
- Use SenseType.SMELL for all generated signals
- Never hard-code sources, use the source parameter
- Use Pydantic v2 models with validation
- Include comprehensive docstrings
- Achieve 95%+ test coverage
```

### Acceptance Criteria
- [ ] TrendDetector identifies signal patterns and spikes
- [ ] AnomalyDetector flags outliers effectively
- [ ] SmellAdvancedPlugin buffers and analyzes signals
- [ ] New signal models for trends and anomalies
- [ ] 95%+ test coverage
- [ ] All tests pass
- [ ] Ruff linting passes

---

## Task 3: PCI/ROI Scoring (Taste Sense)

### Context
The Taste sense evaluates signal quality through sampling. Phase 3 adds Problem-Complexity Index (PCI) and Return-on-Investment (ROI) scoring to prioritize high-value signals.

### AI-Ready Prompt

```
Enhance the Taste sense with PCI (Problem-Complexity Index) and ROI scoring.

Requirements:
1. Create PCICalculator class in pipeline/taste_advanced.py:
   - Calculate complexity score (0.0-1.0) based on:
     - Signal metadata richness (# of fields, depth)
     - Cross-reference count (mentions in other signals)
     - Historical resolution difficulty (if feedback available)
   - Return PCI score with explanation

2. Create ROICalculator class in pipeline/taste_advanced.py:
   - Calculate ROI score (0.0-1.0) based on:
     - Potential impact (inferred from signal type/content)
     - Estimated effort (from PCI)
     - Historical success rate (from feedback loop)
   - ROI = (impact * success_rate) / effort

3. Create TasteAdvancedPlugin implementing reaper_score_signal:
   - Calculate both PCI and ROI for incoming signals
   - Combine into composite score with weighted average
   - Include detailed analysis in scored_signal.analysis
   - Add tags like ["high-roi", "low-effort", "complex"]

4. Add configuration in pyproject.toml:
   - pci_weight (default: 0.3)
   - roi_weight (default: 0.7)
   - min_score_threshold (default: 0.5)

5. Write comprehensive tests in tests/test_taste_advanced.py:
   - Test PCI calculation with various signal types
   - Test ROI calculation with different scenarios
   - Test composite scoring logic
   - Test edge cases (missing data, zero values)

Follow REAPER conventions:
- Ensure score stays in 0.0-1.0 range
- Use Pydantic validation for all models
- Plugin implements reaper_score_signal hook correctly
- Include docstrings with calculation explanations
- Achieve 95%+ test coverage
```

### Acceptance Criteria
- [ ] PCICalculator computes complexity scores accurately
- [ ] ROICalculator computes ROI with impact/effort/success
- [ ] TasteAdvancedPlugin combines PCI and ROI effectively
- [ ] Configuration options for weighting
- [ ] 95%+ test coverage
- [ ] All tests pass
- [ ] Ruff linting passes

---

## Task 4: Alert and Export Actions

### Context
Production-ready action plugins for alerting operators and exporting signals to external systems.

### AI-Ready Prompt

```
Create production-ready Alert and Export action plugins.

Requirements:
1. Create AlertPlugin in pipeline/action_alert.py:
   - Implement reaper_action_execute hook
   - Support multiple alert channels:
     - Console (print with formatting)
     - Email (via SMTP, configurable)
     - Webhook (POST to configurable URL)
     - Slack (via webhook URL)
   - Include signal details, score, and analysis in alerts
   - Handle failures gracefully (retry logic, fallback)

2. Create ExportPlugin in pipeline/action_export.py:
   - Implement reaper_action_execute hook
   - Support multiple export formats:
     - JSON file (one file per signal or append mode)
     - CSV (with flattened signal data)
     - SQLite database (signals table with JSON columns)
   - Include metadata: timestamp, sense_type, score, tags
   - Configurable export directory

3. Add models in reaper/models.py:
   - AlertConfig (email_settings, webhook_urls, channels)
   - ExportConfig (format, directory, mode, database_path)

4. Add configuration in pyproject.toml:
   - [tool.reaper.alerts] section for alert settings
   - [tool.reaper.exports] section for export settings

5. Write comprehensive tests:
   - tests/test_action_alert.py - Test all alert channels with mocks
   - tests/test_action_export.py - Test all export formats
   - Test error handling and retry logic
   - Test configuration loading

Follow REAPER conventions:
- Use reaper_action_execute (NOT reaper_execute_action!)
- Return ActionResult with success/failure status
- Include error messages in ActionResult.error field
- Use proper exception handling
- Achieve 95%+ test coverage
```

### Acceptance Criteria
- [ ] AlertPlugin supports console, email, webhook, Slack
- [ ] ExportPlugin supports JSON, CSV, SQLite formats
- [ ] Configuration models with validation
- [ ] Graceful error handling and retry logic
- [ ] 95%+ test coverage
- [ ] All tests pass
- [ ] Ruff linting passes

---

## Task 5: Operator Console (CLI)

### Context
A command-line interface for operators to monitor signals, provide feedback, and control the pipeline in real-time.

### AI-Ready Prompt

```
Create a CLI operator console for REAPER signal monitoring and control.

Requirements:
1. Create CLI application in reaper/console.py using Click or Typer:
   - Main command: `reaper console` to launch interactive mode
   - Subcommands:
     - `reaper monitor` - Live signal stream display
     - `reaper feedback <signal_id>` - Mark signal as TP/FP/FN
     - `reaper stats` - Show pipeline statistics
     - `reaper plugins` - List registered plugins
     - `reaper config` - Show current configuration

2. Implement MonitorCommand:
   - Display incoming signals in real-time (table format)
   - Color-code by score (red: <0.3, yellow: 0.3-0.7, green: >0.7)
   - Show: timestamp, sense_type, source, score, tags
   - Support filtering by sense_type, source, or score range
   - Use Rich library for beautiful terminal output

3. Implement FeedbackCommand:
   - Accept signal_id and feedback type (tp/fp/fn)
   - Validate signal exists in recent history
   - Call FeedbackLoop to record feedback
   - Show updated statistics after feedback

4. Implement StatsCommand:
   - Display pipeline metrics:
     - Total signals processed
     - Signals per sense type
     - Average score by sense
     - Feedback statistics (if available)
   - Show as formatted table with Rich

5. Add entry point in pyproject.toml:
   - [project.scripts] section: reaper = "reaper.console:cli"

6. Write tests in tests/test_console.py:
   - Test each command with Click.CliRunner
   - Test output formatting
   - Test filtering and edge cases

Follow REAPER conventions:
- Use existing PluginManager for plugin operations
- Read configuration from pyproject.toml
- Include --help documentation for all commands
- Handle errors gracefully with user-friendly messages
- Achieve 90%+ test coverage (UI testing can be challenging)
```

### Acceptance Criteria
- [ ] CLI with monitor, feedback, stats, plugins, config commands
- [ ] Real-time signal display with color-coding
- [ ] Feedback integration with Ouroboros Protocol
- [ ] Beautiful output using Rich library
- [ ] Entry point configured in pyproject.toml
- [ ] 90%+ test coverage
- [ ] All tests pass
- [ ] Ruff linting passes

---

## Task 6: Realtime and Batch Signal Processing

### Context
Support two operational modes: realtime (streaming) and batch (scheduled processing) to handle different use cases.

### AI-Ready Prompt

```
Implement realtime and batch signal processing modes for REAPER.

Requirements:
1. Create ProcessingMode enum in reaper/models.py:
   - REALTIME - Process signals as they arrive
   - BATCH - Collect and process in batches
   - HYBRID - Mix of both based on signal type

2. Create SignalQueue class in reaper/queue.py:
   - Thread-safe queue for incoming signals
   - Support priority ordering (by score or timestamp)
   - Configurable max size with overflow handling
   - Methods: enqueue(), dequeue(), peek(), size(), clear()

3. Create RealtimeProcessor in reaper/processor.py:
   - Continuously poll SignalQueue for new signals
   - Process immediately through pipeline (detect→score→action)
   - Run in separate thread or asyncio task
   - Support start(), stop(), pause(), resume()
   - Emit events for monitoring (signal_processed, error_occurred)

4. Create BatchProcessor in reaper/processor.py:
   - Collect signals over time window or count threshold
   - Process batch through pipeline when triggered
   - Support scheduled execution (cron-like)
   - Optimize for bulk operations (batch scoring)
   - Support start(), stop(), trigger_now()

5. Add configuration in pyproject.toml:
   - [tool.reaper.processing] section:
     - mode (realtime/batch/hybrid)
     - queue_max_size (default: 10000)
     - batch_size (default: 100)
     - batch_interval_seconds (default: 60)

6. Write comprehensive tests:
   - tests/test_queue.py - Test queue operations and thread safety
   - tests/test_processor.py - Test both processor modes
   - Test mode switching and hybrid operation
   - Test error handling and recovery

Follow REAPER conventions:
- Use proper threading/asyncio patterns
- Handle exceptions gracefully
- Log important events
- Use Pydantic for configuration
- Achieve 95%+ test coverage
```

### Acceptance Criteria
- [ ] ProcessingMode enum with REALTIME/BATCH/HYBRID
- [ ] Thread-safe SignalQueue implementation
- [ ] RealtimeProcessor with lifecycle management
- [ ] BatchProcessor with scheduling support
- [ ] Configuration options for both modes
- [ ] 95%+ test coverage
- [ ] All tests pass
- [ ] Ruff linting passes

---

## Collaboration & Automation Tasks

### Task 7: Automate PR Reviews with Copilot

**AI-Ready Prompt:**
```
Set up automated PR review workflow using GitHub Copilot.

Requirements:
1. Create .github/workflows/copilot-review.yml:
   - Trigger on pull_request (opened, synchronize)
   - Use GitHub Copilot API or Actions for code review
   - Check for:
     - Correct hook names (common error patterns)
     - Proper Pydantic usage
     - Test coverage for new code
     - Documentation updates
   - Post review comments on PR

2. Add review checklist template in .github/COPILOT_REVIEW_TEMPLATE.md
3. Document in CONTRIBUTING.md under "Automated Reviews" section

Follow conventions:
- Use permissions: contents: read, pull-requests: write
- Include helpful, constructive feedback
- Link to relevant documentation
```

### Task 8: Expand Contributor Guides

**AI-Ready Prompt:**
```
Create advanced contributor guides for Phase 3 features.

Requirements:
1. Create docs/ADVANCED_PLUGINS.md:
   - Guide for building advanced plugins (Ouroboros, Smell, Taste)
   - Explain feedback loop integration
   - Show pattern detection examples
   - Include troubleshooting section

2. Update CONTRIBUTING.md:
   - Add section on self-improving systems
   - Explain PCI/ROI scoring concepts
   - Link to advanced guides

3. Create docs/OPERATOR_GUIDE.md:
   - How to use the console
   - How to provide feedback
   - How to interpret statistics
   - Configuration examples

Follow conventions:
- Use clear, beginner-friendly language
- Include code examples
- Add diagrams if helpful (ASCII art is fine)
```

---

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Mock external dependencies
- Aim for 95%+ coverage per file

### Integration Tests
- Test Ouroboros Protocol with FeedbackPlugin
- Test advanced Smell/Taste plugins with PluginManager
- Test console commands end-to-end
- Test realtime/batch processing workflows

### Performance Tests
- Test SignalQueue under load (1000+ signals/sec)
- Benchmark batch vs realtime processing
- Measure Ouroboros Protocol overhead

---

## Quality Gates

All Phase 3 deliverables must pass:
- [ ] `pytest -v --cov=reaper --cov=pipeline` (95%+ coverage)
- [ ] `ruff format --check .`
- [ ] `ruff check .`
- [ ] Code review (manual or automated)
- [ ] Security scan (CodeQL)
- [ ] Documentation complete

---

## Timeline Estimate

- **Week 1-2**: Ouroboros Protocol + tests
- **Week 3-4**: Enhanced Smell and Taste plugins
- **Week 5-6**: Alert/Export actions + operator console
- **Week 7-8**: Realtime/batch processing + integration
- **Week 9-10**: Collaboration tools + documentation
- **Week 11-12**: Testing, refinement, launch

**Total**: ~12 weeks

---

## Success Criteria

Phase 3 is complete when:
1. ✅ Ouroboros Protocol learns from feedback and adjusts thresholds
2. ✅ Advanced pattern detection identifies trends and anomalies
3. ✅ PCI/ROI scoring prioritizes high-value signals
4. ✅ Production-ready alert and export actions deployed
5. ✅ Operator console provides real-time monitoring
6. ✅ Both realtime and batch processing modes work reliably
7. ✅ All tests pass with 95%+ coverage
8. ✅ Documentation updated and comprehensive
9. ✅ Collaboration tools enhanced for Phase 4

---

## Next Steps

After Phase 3 completion:
- Begin Phase 4 planning
- Gather community feedback on operator console
- Identify areas for optimization
- Plan v1.0 feature freeze
