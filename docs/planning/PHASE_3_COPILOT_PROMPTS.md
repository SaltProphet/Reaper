# Phase 3 Copilot Prompts: Learning & Operator Experience

**Status**: 📅 PLANNED  
**Copy-Paste Ready Prompts for GitHub Copilot**

---

## Overview

Phase 3 focuses on self-improving systems, advanced analytics, and operator tooling. The Ouroboros Protocol enables REAPER to learn from feedback and improve its signal detection over time.

**Prerequisites**: Phase 2 complete (v0.2.0 released)

---

## Section 1: Ouroboros Protocol

### Prompt 3.1.1: Design Feedback Collection System

```
@workspace Design and implement the feedback collection system for signal quality.

Context:
- Ouroboros Protocol: self-improving filters based on feedback
- Need to collect feedback on signal quality (true/false positives)
- Feedback drives filter improvements

Task:
Create `reaper/feedback.py`:
1. FeedbackCollector class for storing signal feedback
2. Methods: record_feedback(signal_id, quality, reason)
3. Storage: SQLite database or JSON file
4. Query methods: get_feedback_for_signal, get_feedback_stats
5. Integration with Signal model

Requirements:
- Feedback types: true_positive, false_positive, false_negative, irrelevant
- Store: signal_id, feedback_type, timestamp, user, reason
- Support bulk feedback operations
- Provide statistics: accuracy, precision, recall
- Thread-safe for concurrent access

Success Criteria:
- [ ] FeedbackCollector class implemented
- [ ] Feedback stored persistently
- [ ] Query methods functional
- [ ] Statistics calculated correctly
- [ ] Tests: tests/test_feedback.py
- [ ] Documentation with examples
```

---

### Prompt 3.1.2: Implement Pattern Learning Module

```
@workspace Create pattern learning module that improves from feedback.

Context:
- Use feedback to identify patterns in true/false positives
- Learn which keywords, sources, patterns indicate quality signals
- Update detection filters automatically

Task:
Create `reaper/pattern_learner.py`:
1. PatternLearner class that analyzes feedback
2. Identify common patterns in true/false positives
3. Generate improved filter rules
4. Apply learned patterns to future detection
5. Track learning effectiveness over time

Requirements:
- Analyze feedback to find patterns
- Use statistical methods or simple ML
- Generate new keyword weights
- Update scorer configurations
- Track: accuracy before/after learning
- Periodic retraining based on new feedback

Success Criteria:
- [ ] PatternLearner analyzes feedback
- [ ] Learns from true/false positives
- [ ] Generates improved filters
- [ ] Accuracy improves over time
- [ ] Tests: tests/test_pattern_learner.py
- [ ] Performance metrics tracked
```

---

### Prompt 3.1.3: Create Adaptive Scoring System

```
@workspace Implement adaptive scoring that improves from feedback.

Context:
- Scoring should adapt based on feedback
- Keyword weights adjusted based on accuracy
- Thresholds optimized over time

Task:
Create `reaper/adaptive_scorer.py`:
1. AdaptiveScorer class implementing reaper_score_signal
2. Load learned patterns from PatternLearner
3. Adjust scoring based on feedback
4. Update weights periodically
5. A/B test new scoring models

Requirements:
- Integrate with FeedbackCollector
- Adjust keyword weights based on accuracy
- Optimize score thresholds
- Support A/B testing of scoring models
- Track performance metrics per model
- Gradual rollout of improvements

Success Criteria:
- [ ] AdaptiveScorer implemented
- [ ] Integrates with feedback system
- [ ] Weights adjust automatically
- [ ] A/B testing supported
- [ ] Tests: tests/test_adaptive_scorer.py
- [ ] Metrics show improvement
```

---

## Section 2: Advanced Pattern Detection

### Prompt 3.2.1: Implement Smell - Trend Detection

```
@workspace Enhance Smell plugin with time-series trend detection.

Context:
- Smell sense should detect trends over time
- Identify increasing/decreasing patterns
- Alert on unusual trends

Task:
Create `plugins/trend_detector.py`:
1. TrendDetector class implementing reaper_smell_detect
2. Analyze signal history for trends
3. Detect: upward trends, downward trends, spikes
4. Calculate trend strength and confidence
5. Generate signals for significant trends

Requirements:
- Store signal history (time-series database or in-memory)
- Calculate moving averages
- Detect slope changes
- Identify anomalous spikes
- Configurable trend thresholds
- Include trend metadata in signals

Success Criteria:
- [ ] TrendDetector implemented
- [ ] Detects upward/downward trends
- [ ] Identifies spikes and anomalies
- [ ] Confidence scores provided
- [ ] Tests: tests/test_trend_detector.py
- [ ] Examples with synthetic data
```

---

### Prompt 3.2.2: Implement Smell - Pattern Matching

```
@workspace Create advanced pattern matching for Smell sense.

Context:
- Smell should recognize recurring patterns
- Temporal patterns (daily cycles, weekly patterns)
- Spatial patterns (related signals from different sources)

Task:
Create `plugins/pattern_matcher.py`:
1. PatternMatcher class implementing reaper_smell_detect
2. Detect recurring temporal patterns
3. Identify related signals (clustering)
4. Find correlation between signals
5. Generate pattern match signals

Requirements:
- Pattern types: temporal, spatial, correlation
- Use time-series analysis for temporal
- Use clustering for spatial (k-means, DBSCAN)
- Calculate correlation coefficients
- Configurable sensitivity thresholds
- Include pattern details in signal metadata

Success Criteria:
- [ ] PatternMatcher implemented
- [ ] Detects temporal patterns
- [ ] Identifies signal clusters
- [ ] Calculates correlations
- [ ] Tests: tests/test_pattern_matcher.py
- [ ] Real-world pattern examples
```

---

### Prompt 3.2.3: Implement Taste - PCI/ROI Scoring

```
@workspace Create Problem-Cost Index (PCI) and ROI scoring for Taste sense.

Context:
- Taste sense evaluates signal quality/value
- PCI: How costly is this problem?
- ROI: What's the value of solving it?

Task:
Create `plugins/pci_roi_scorer.py`:
1. PCIScorer class implementing reaper_score_signal
2. Calculate Problem-Cost Index (impact × urgency × frequency)
3. Calculate estimated ROI of solving
4. Consider factors: users affected, time wasted, revenue impact
5. Include PCI/ROI breakdown in analysis

Requirements:
- PCI formula: impact × urgency × frequency
- ROI formula: (benefit - cost) / cost
- Configurable weight factors
- Estimate users affected, time saved
- Include confidence intervals
- Normalize to 0.0-1.0 score

Success Criteria:
- [ ] PCIScorer implemented
- [ ] PCI calculation accurate
- [ ] ROI estimation reasonable
- [ ] Factors configurable
- [ ] Tests: tests/test_pci_roi_scorer.py
- [ ] Documentation with examples
```

---

## Section 3: Operator Console

### Prompt 3.3.1: Design CLI Console Architecture

```
@workspace Design command-line interface for REAPER operator console.

Context:
- Operators need UI to monitor and control REAPER
- CLI is fastest path to functionality
- Should support common operations

Task:
Create `reaper/console/cli.py`:
1. CLI application using Click or argparse
2. Commands: start, stop, status, config, feedback
3. Real-time signal monitoring
4. Feedback submission interface
5. Configuration management

Requirements:
- Commands:
  - `reaper start` - Start pipeline
  - `reaper stop` - Stop pipeline
  - `reaper status` - Show statistics
  - `reaper feedback <signal-id>` - Submit feedback
  - `reaper config` - View/edit configuration
- Colorized output (use Rich or colorama)
- Real-time updates (use websockets or polling)
- Table display for signals
- Interactive feedback prompts

Success Criteria:
- [ ] CLI application functional
- [ ] All commands working
- [ ] Real-time monitoring works
- [ ] User-friendly interface
- [ ] Tests: tests/test_cli.py
- [ ] Documentation with screenshots
```

---

### Prompt 3.3.2: Create Web-Based Dashboard (Optional)

```
@workspace Create optional web dashboard for REAPER monitoring.

Context:
- Web UI provides richer visualization
- Optional alternative to CLI
- Shows real-time signal flow

Task:
Create `reaper/console/web.py` and frontend:
1. FastAPI backend for API
2. Simple HTML/JS frontend (or React)
3. Real-time signal display (WebSocket)
4. Feedback submission form
5. Statistics dashboard

Requirements:
Backend (FastAPI):
- Endpoints: /signals, /feedback, /stats, /config
- WebSocket for real-time updates
- CORS configured
- API documentation (Swagger)

Frontend:
- Signal list with filtering
- Real-time updates
- Feedback form
- Charts for statistics
- Responsive design

Success Criteria:
- [ ] FastAPI backend functional
- [ ] Frontend displays signals
- [ ] Real-time updates work
- [ ] Feedback submission works
- [ ] Tests: tests/test_web_console.py
- [ ] Deployment guide included
```

---

### Prompt 3.3.3: Implement Alert System

```
@workspace Create alerting system for high-priority signals.

Context:
- Operators need immediate alerts for critical signals
- Multiple alert channels (email, Slack, SMS)
- Configurable alert rules

Task:
Create `reaper/alerting.py`:
1. AlertManager class
2. Rule engine for alert conditions
3. Multiple delivery channels
4. Alert deduplication
5. Alert escalation logic

Requirements:
- Alert rules: score > threshold, keyword match, source match
- Channels: email, Slack, Discord, SMS (Twilio)
- Deduplication: same alert within time window
- Escalation: repeat alert if not acknowledged
- Alert history tracking
- Configurable per-plugin

Success Criteria:
- [ ] AlertManager implemented
- [ ] Rule engine functional
- [ ] Multiple channels supported
- [ ] Deduplication works
- [ ] Tests: tests/test_alerting.py
- [ ] Configuration examples
```

---

## Section 4: Real-time Processing

### Prompt 3.4.1: Implement Stream Processing Pipeline

```
@workspace Create stream processing pipeline for real-time signals.

Context:
- Need real-time signal processing (not just batch)
- Use streaming library (asyncio queues or Kafka)
- Low-latency processing

Task:
Create `reaper/streaming.py`:
1. StreamProcessor class for real-time processing
2. Async signal ingestion
3. Pipeline stages: detect → score → action
4. Backpressure handling
5. State management for windows

Requirements:
- Use asyncio for concurrency
- Support high throughput (1000+ signals/sec)
- Windowing: tumbling, sliding, session
- Backpressure: slow down if overwhelmed
- State persistence for fault tolerance
- Metrics: latency, throughput

Success Criteria:
- [ ] StreamProcessor implemented
- [ ] Handles 1000+ signals/sec
- [ ] Windowing functional
- [ ] Backpressure works
- [ ] Tests: tests/test_streaming.py
- [ ] Performance benchmarks
```

---

### Prompt 3.4.2: Add Batch Processing Support

```
@workspace Implement batch processing mode alongside streaming.

Context:
- Need both real-time (streaming) and batch processing
- Batch for historical analysis
- Same plugins work in both modes

Task:
Create `reaper/batch.py`:
1. BatchProcessor class for batch jobs
2. Process historical signals
3. Parallel processing for performance
4. Progress tracking
5. Results aggregation

Requirements:
- Load signals from files or database
- Parallel processing (multiprocessing or Ray)
- Progress bar (tqdm)
- Results: JSON, CSV, database
- Configurable batch size
- Same plugins as streaming mode

Success Criteria:
- [ ] BatchProcessor implemented
- [ ] Processes large datasets
- [ ] Parallel processing works
- [ ] Progress tracking visible
- [ ] Tests: tests/test_batch.py
- [ ] Examples with real data
```

---

### Prompt 3.4.3: Implement State Management

```
@workspace Create state management system for pipeline.

Context:
- Need to track pipeline state
- Persist state for fault tolerance
- Resume processing after restart

Task:
Create `reaper/state.py`:
1. StateManager class for state persistence
2. Track: processed signals, plugin states, feedback
3. Checkpoint and recovery
4. State queries
5. Cleanup old state

Requirements:
- Storage: SQLite or Redis
- Track: signal IDs processed, plugin configurations
- Checkpoint periodically
- Recovery: resume from checkpoint
- Cleanup: delete old state
- Thread-safe operations

Success Criteria:
- [ ] StateManager implemented
- [ ] State persists correctly
- [ ] Recovery works after restart
- [ ] Cleanup functional
- [ ] Tests: tests/test_state.py
- [ ] Performance acceptable
```

---

## Section 5: Collaboration & Automation

### Prompt 3.5.1: Host Operator Console Design Sessions

```
@workspace Organize GitHub Spaces session for operator console design.

Context:
- Need community input on console features
- Collaborative design via GitHub Spaces
- Document decisions

Task:
Plan and execute design session:
1. Create Spaces session agenda
2. Invite key contributors
3. Present console mockups
4. Gather feedback and requirements
5. Document decisions

Agenda:
- Console requirements (operators' needs)
- CLI vs Web tradeoffs
- Alert system design
- Real-time visualization
- Feedback mechanism

Deliverables:
- Session notes document
- Updated console requirements
- UI mockups (if applicable)
- Task breakdown for implementation

Success Criteria:
- [ ] Spaces session completed
- [ ] Community input gathered
- [ ] Requirements documented
- [ ] Mockups created
- [ ] Implementation tasks defined
```

---

### Prompt 3.5.2: Automate PR Reviews with Copilot

```
@workspace Setup automated PR review process using GitHub Copilot.

Context:
- Need consistent code reviews
- Copilot can check conventions automatically
- Human review for complex decisions

Task:
Configure automated reviews:
1. Create PR review checklist workflow
2. Setup Copilot code review action
3. Define review criteria
4. Configure auto-comments
5. Escalation to human reviewers

Review Criteria:
- Code follows conventions (no hard-coding, etc.)
- Tests included and passing
- Documentation updated
- Performance acceptable
- No security issues

Success Criteria:
- [ ] Automated review workflow active
- [ ] Copilot checks conventions
- [ ] Auto-comments helpful
- [ ] Human review for complex cases
- [ ] Process documented
```

---

### Prompt 3.5.3: Use Spark for Test Analysis

```
@workspace Integrate GitHub Spark for test result analysis.

Context:
- Spark can analyze test failures
- Provide diagnostics and suggestions
- Speed up debugging

Task:
Setup Spark integration:
1. Configure Spark for test result parsing
2. Analyze failure patterns
3. Generate diagnostic reports
4. Suggest fixes for common failures
5. Track flaky tests

Requirements:
- Parse pytest output
- Identify failure patterns
- Generate markdown reports
- Suggest likely causes
- Track test reliability over time

Success Criteria:
- [ ] Spark analyzes test results
- [ ] Diagnostic reports generated
- [ ] Suggestions actionable
- [ ] Flaky tests identified
- [ ] Documentation with examples
```

---

## Section 6: Advanced Topics

### Prompt 3.6.1: Create Plugin Dependency System

```
@workspace Implement plugin dependency and ordering system.

Context:
- Some plugins depend on others
- Need deterministic execution order
- Support plugin chains

Task:
Create `reaper/plugin_deps.py`:
1. Plugin dependency declaration
2. Topological sort for execution order
3. Circular dependency detection
4. Plugin isolation (failures don't cascade)
5. Dependency injection

Requirements:
- Plugins declare: requires, provides
- Execution order via topological sort
- Detect circular dependencies
- Isolate plugin failures
- Dependency injection for plugin needs

Success Criteria:
- [ ] Dependency system implemented
- [ ] Execution order correct
- [ ] Circular deps detected
- [ ] Failures isolated
- [ ] Tests: tests/test_plugin_deps.py
- [ ] Examples with dependent plugins
```

---

### Prompt 3.6.2: Implement Plugin Marketplace

```
@workspace Create plugin marketplace for sharing community plugins.

Context:
- Community creates custom plugins
- Need discovery and installation mechanism
- Plugin registry

Task:
Create plugin marketplace:
1. Plugin registry structure (GitHub repo or API)
2. Plugin metadata format
3. Installation CLI command
4. Version management
5. Security scanning

Requirements:
Plugin Metadata:
- Name, description, author, version
- Dependencies, requirements
- Installation instructions
- Tests and documentation

CLI Commands:
- `reaper plugin search <keyword>`
- `reaper plugin install <name>`
- `reaper plugin list`
- `reaper plugin update <name>`

Security:
- Verify plugin signatures
- Scan for vulnerabilities
- User confirmation before install

Success Criteria:
- [ ] Plugin registry established
- [ ] Installation system works
- [ ] Version management functional
- [ ] Security scanning implemented
- [ ] Tests: tests/test_plugin_marketplace.py
- [ ] User guide published
```

---

## Phase 3 Verification Checklist

Before marking Phase 3 complete:

### Ouroboros Protocol
- [ ] Feedback collection system functional
- [ ] Pattern learning improves accuracy
- [ ] Adaptive scoring implemented
- [ ] Learning metrics positive

### Advanced Detection
- [ ] Trend detection in Smell plugin
- [ ] Pattern matching implemented
- [ ] PCI/ROI scoring functional
- [ ] All tests passing

### Operator Console
- [ ] CLI console functional
- [ ] Web dashboard (if implemented)
- [ ] Alert system working
- [ ] Real-time monitoring active

### Processing Modes
- [ ] Stream processing implemented
- [ ] Batch processing functional
- [ ] State management working
- [ ] Performance benchmarks met

### Collaboration
- [ ] Design sessions completed
- [ ] PR automation active
- [ ] Test analysis working
- [ ] Community engaged

---

## Tips for AI Coders

**Phase 3 Focus:**
- Self-improving systems (learning from feedback)
- Real-time processing (streaming)
- Operator tooling (console, alerts)
- Advanced analytics (trends, patterns, ROI)

**Key Technologies:**
- Asyncio for streaming
- SQLite/Redis for state
- FastAPI for web console
- Click for CLI
- Statistical libraries for learning

**Testing Strategies:**
- Mock feedback data
- Synthetic time-series for trends
- Load testing for streaming
- UI testing for console

**Common Challenges:**
- State persistence complexity
- Real-time performance
- Learning algorithm tuning
- UI/UX design

---

**Related Documents:**
- [Roadmap](Roadmap) - Overall timeline
- [PHASE_2_COPILOT_PROMPTS.md](PHASE_2_COPILOT_PROMPTS.md) - Previous phase
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
