# Phase 2 Copilot Prompts: Pipeline Completion ("Beta")

**Status**: 🎯 READY TO START  
**Copy-Paste Ready Prompts for GitHub Copilot**

---

## Overview

Phase 2 transforms REAPER from stub-based prototype to production-ready pipeline with real-world plugins. Break down work using these copy-paste prompts.

**Reference Documents:**
- [PHASE_2_PLAN.md](PHASE_2_PLAN.md) - Detailed roadmap
- [PHASE_2_QUICK_REF.md](PHASE_2_QUICK_REF.md) - Templates and examples

---

## Milestone 1: Sense Module Completion (Weeks 1-2)

### Prompt 2.1.1: Enhance Sight Module Documentation

```
@workspace Enhance the Sight module with comprehensive documentation and examples.

Context:
- Sight module in pipeline/sight.py currently has stub implementation
- Need to document visual detection use cases
- Need real-world examples for contributors

Task:
Update `pipeline/sight.py` and create examples:
1. Add comprehensive docstrings explaining visual detection
2. Document use cases: image analysis, UI monitoring, screenshot analysis
3. Create example_sight_image_analyzer.py showing image-based detection
4. Create example_sight_screenshot.py showing screenshot-based detection
5. Update inline comments with detailed explanations

Requirements:
- Keep stub functional (don't break existing tests)
- Add Examples section to docstring
- Include code examples in docstring
- Create 2 real-world example files in examples/ directory
- Examples must follow REAPER conventions (no hard-coding sources)
- Include error handling in examples

Success Criteria:
- [ ] Sight module fully documented with use cases
- [ ] 2 example implementations created
- [ ] Examples run without errors
- [ ] Docstrings include code snippets
- [ ] Tests still pass: pytest tests/test_pipeline_stubs.py::test_sight
```

---

### Prompt 2.1.2: Enhance Hearing Module Documentation

```
@workspace Enhance the Hearing module with comprehensive documentation and examples.

Context:
- Hearing module handles audio/text detection
- Current stub needs real-world examples
- Common use: chat logs, transcripts, text parsing

Task:
Update `pipeline/hearing.py` and create examples:
1. Add comprehensive docstrings for audio/text detection
2. Document use cases: chat logs, sentiment analysis, keyword detection
3. Create example_hearing_text_parser.py for text parsing
4. Create example_hearing_keyword_detector.py for keyword detection
5. Update inline comments

Requirements:
- Keep stub functional
- Document text and audio detection patterns
- Examples must handle various text formats
- Include sentiment analysis concepts
- Follow REAPER conventions (no hard-coding)

Success Criteria:
- [ ] Hearing module fully documented
- [ ] 2 example implementations created
- [ ] Use cases clearly explained
- [ ] Examples demonstrate text processing
- [ ] Tests pass: pytest tests/test_pipeline_stubs.py::test_hearing
```

---

### Prompt 2.1.3: Enhance Touch Module Documentation

```
@workspace Enhance the Touch module with comprehensive documentation and examples.

Context:
- Touch module handles interaction detection
- Focus: API calls, webhooks, user events
- Need examples for web applications

Task:
Update `pipeline/touch.py` and create examples:
1. Add docstrings for interaction detection
2. Document use cases: webhook listeners, form submissions, API monitoring
3. Create example_touch_webhook.py for webhook handling
4. Create example_touch_api_monitor.py for API call detection
5. Include interaction pattern explanations

Requirements:
- Explain difference between Touch and other senses
- Show webhook payload handling
- Demonstrate API call monitoring
- Include async patterns if relevant
- Follow plugin architecture

Success Criteria:
- [ ] Touch module comprehensively documented
- [ ] 2 interaction examples created
- [ ] Webhook and API patterns shown
- [ ] Docstrings explain interaction detection
- [ ] Tests pass: pytest tests/test_pipeline_stubs.py::test_touch
```

---

### Prompt 2.1.4: Enhance Taste Module Documentation

```
@workspace Enhance the Taste module with comprehensive documentation and examples.

Context:
- Taste module for quality/sampling detection
- Focus: data validation, health checks, sampling
- Less intuitive than other senses - needs clear examples

Task:
Update `pipeline/taste.py` and create examples:
1. Add docstrings explaining quality/sampling detection
2. Document use cases: data quality checks, sample rate monitoring, health checks
3. Create example_taste_data_validator.py for data quality
4. Create example_taste_health_check.py for system health monitoring
5. Explain "taste" metaphor clearly

Requirements:
- Make the "taste" metaphor clear and understandable
- Show data quality validation patterns
- Demonstrate sampling strategies
- Include health check patterns
- Provide threshold examples

Success Criteria:
- [ ] Taste module clearly documented
- [ ] "Taste" metaphor explained well
- [ ] 2 quality/sampling examples created
- [ ] Use cases make sense to new users
- [ ] Tests pass: pytest tests/test_pipeline_stubs.py::test_taste
```

---

### Prompt 2.1.5: Enhance Smell Module Documentation

```
@workspace Enhance the Smell module with comprehensive documentation and examples.

Context:
- Smell module for pattern/anomaly detection
- Most advanced sense - needs clear guidance
- Focus: trends, patterns, anomalies

Task:
Update `pipeline/smell.py` and create examples:
1. Add docstrings for pattern/anomaly detection
2. Document use cases: trend analysis, outlier detection, pattern matching
3. Create example_smell_pattern_matcher.py for pattern detection
4. Create example_smell_anomaly_detector.py for anomaly detection
5. Include statistical concepts where relevant

Requirements:
- Explain "smell" metaphor (detecting something's off)
- Show pattern matching algorithms
- Demonstrate anomaly detection techniques
- Include time-series concepts if relevant
- Provide threshold and tolerance examples

Success Criteria:
- [ ] Smell module comprehensively documented
- [ ] "Smell" metaphor clear and intuitive
- [ ] 2 pattern/anomaly examples created
- [ ] Statistical concepts explained simply
- [ ] Tests pass: pytest tests/test_pipeline_stubs.py::test_smell
```

---

### Prompt 2.1.6: Create Integration Tests for Each Sense

```
@workspace Create integration tests for complete sense → scoring → action flows.

Context:
- Need end-to-end tests for each sense
- Tests should validate entire pipeline
- Must demonstrate real-world usage

Task:
Create `tests/test_sense_integration.py` with tests:
1. test_sight_to_action_pipeline() - sight → scoring → action
2. test_hearing_to_action_pipeline() - hearing → scoring → action
3. test_touch_to_action_pipeline() - touch → scoring → action
4. test_taste_to_action_pipeline() - taste → scoring → action
5. test_smell_to_action_pipeline() - smell → scoring → action

Requirements:
- Each test uses appropriate sense plugin
- Include scoring step with threshold
- Execute action on high-score signals
- Verify signal flow through pipeline
- Test error handling at each stage
- Use realistic test data

Success Criteria:
- [ ] 5 integration tests created (one per sense)
- [ ] Each test covers detection → scoring → action
- [ ] All tests pass: pytest tests/test_sense_integration.py -v
- [ ] Tests demonstrate proper plugin usage
- [ ] Error handling verified
```

---

## Milestone 2: Plugin Library Expansion (Weeks 3-4)

### Prompt 2.2.1: Create Reddit Ingestor Plugin

```
@workspace Create a Reddit ingestor plugin for monitoring subreddits.

Context:
- Need real-world plugin example for sight detection
- Reddit is common source for problem signals
- Must handle API rate limits and authentication

Task:
Create `plugins/reddit_ingestor.py`:
1. Class RedditIngestor implementing reaper_sight_detect hook
2. Monitor subreddit for posts/comments with friction keywords
3. Parse Reddit API responses into Signal objects
4. Handle rate limiting gracefully
5. Support API key configuration (not hard-coded!)

Requirements:
- Use PRAW library for Reddit API
- Implement @hookimpl decorator
- Take source parameter (subreddit name)
- Parse title, body, comments for signals
- Include metadata: upvotes, author, timestamp
- Handle API errors gracefully
- Respect rate limits
- API key via environment variable

Success Criteria:
- [ ] Plugin implements reaper_sight_detect correctly
- [ ] Can monitor any subreddit (passed as source)
- [ ] Parses posts into Signal objects
- [ ] Handles rate limits and errors
- [ ] Tests created: tests/test_reddit_ingestor.py
- [ ] Documentation includes setup instructions
```

---

### Prompt 2.2.2: Create Discord Ingestor Plugin

```
@workspace Create a Discord ingestor plugin for monitoring channels.

Context:
- Discord is popular communication platform
- Need hearing detection example
- Must handle webhooks or bot API

Task:
Create `plugins/discord_ingestor.py`:
1. Class DiscordIngestor implementing reaper_hearing_detect hook
2. Monitor Discord channels via webhook or bot
3. Parse messages for support requests and bug reports
4. Extract text and metadata into Signal objects
5. Handle Discord API patterns

Requirements:
- Use discord.py library
- Implement @hookimpl decorator
- Take source parameter (channel ID or webhook URL)
- Parse message content, reactions, attachments
- Include metadata: author, timestamp, reactions
- Support both webhook and bot patterns
- Handle connection errors

Success Criteria:
- [ ] Plugin implements reaper_hearing_detect correctly
- [ ] Can monitor any channel (passed as source)
- [ ] Parses messages into Signal objects
- [ ] Handles Discord API properly
- [ ] Tests created: tests/test_discord_ingestor.py
- [ ] Setup guide for webhook/bot configuration
```

---

### Prompt 2.2.3: Create RSS Ingestor Plugin

```
@workspace Create an RSS feed ingestor plugin for monitoring feeds.

Context:
- RSS/Atom feeds are common data sources
- Need hearing detection example
- Simple protocol, good learning example

Task:
Create `plugins/rss_ingestor.py`:
1. Class RSSIngestor implementing reaper_hearing_detect hook
2. Parse RSS/Atom feeds for updates
3. Extract items into Signal objects
4. Support multiple feed formats
5. Handle feed parsing errors

Requirements:
- Use feedparser library
- Implement @hookimpl decorator
- Take source parameter (feed URL)
- Parse title, description, content
- Include metadata: published date, author, categories
- Support RSS 2.0 and Atom formats
- Handle malformed feeds gracefully

Success Criteria:
- [ ] Plugin implements reaper_hearing_detect correctly
- [ ] Can parse any feed URL (passed as source)
- [ ] Handles RSS and Atom formats
- [ ] Extracts rich metadata
- [ ] Tests created: tests/test_rss_ingestor.py
- [ ] Examples with popular feeds (e.g., Hacker News)
```

---

### Prompt 2.2.4: Create Keyword Scorer Plugin

```
@workspace Create a keyword-based scoring plugin.

Context:
- Need scoring example beyond stub
- Keyword matching is fundamental scoring technique
- Should support weighted keywords

Task:
Create `plugins/keyword_scorer.py`:
1. Class KeywordScorer implementing reaper_score_signal hook
2. Score signals based on keyword presence
3. Support weighted keywords (importance)
4. Calculate score based on matches
5. Include matched keywords in analysis

Requirements:
- Implement @hookimpl decorator
- Take Signal, return ScoredSignal
- Support keyword configuration (dict with weights)
- Score formula: (sum of weights for matched keywords) / (total possible)
- Normalize score to 0.0-1.0 range
- Include matched keywords in analysis dict
- Support regex patterns for keywords

Success Criteria:
- [ ] Plugin implements reaper_score_signal correctly
- [ ] Scores based on keyword matches
- [ ] Weighted keywords supported
- [ ] Score always in 0.0-1.0 range
- [ ] Tests created: tests/test_keyword_scorer.py
- [ ] Configuration example provided
```

---

### Prompt 2.2.5: Create Sentiment Scorer Plugin

```
@workspace Create a sentiment analysis scoring plugin.

Context:
- Sentiment is important signal indicator
- Can use ML model or rule-based approach
- Negative sentiment often indicates problems

Task:
Create `plugins/sentiment_scorer.py`:
1. Class SentimentScorer implementing reaper_score_signal hook
2. Analyze text sentiment (positive/negative/neutral)
3. Score based on sentiment intensity
4. Include sentiment metrics in analysis
5. Support both ML and rule-based approaches

Requirements:
- Implement @hookimpl decorator
- Take Signal, return ScoredSignal
- Extract text from raw_data
- Calculate sentiment score
- Higher score for more negative sentiment (indicates problems)
- Include sentiment breakdown in analysis
- Optional: use TextBlob or VADER for sentiment

Success Criteria:
- [ ] Plugin implements reaper_score_signal correctly
- [ ] Analyzes sentiment from signal text
- [ ] Negative sentiment = higher score
- [ ] Score in 0.0-1.0 range
- [ ] Tests created: tests/test_sentiment_scorer.py
- [ ] Works without ML dependencies (rule-based fallback)
```

---

### Prompt 2.2.6: Create Urgency Scorer Plugin

```
@workspace Create an urgency-based scoring plugin.

Context:
- Some signals are more urgent than others
- Need multi-factor urgency calculation
- Consider keywords, time, source

Task:
Create `plugins/urgency_scorer.py`:
1. Class UrgencyScorer implementing reaper_score_signal hook
2. Calculate urgency based on multiple factors
3. Consider: keywords, recency, source reliability
4. Apply time decay for old signals
5. Include urgency breakdown in analysis

Requirements:
- Implement @hookimpl decorator
- Take Signal, return ScoredSignal
- Multi-factor scoring: keywords, time, source
- Time decay: older signals = lower urgency
- Configurable urgency keywords and weights
- Combine factors into final score (0.0-1.0)

Success Criteria:
- [ ] Plugin implements reaper_score_signal correctly
- [ ] Multi-factor urgency calculation
- [ ] Time decay implemented
- [ ] Score in 0.0-1.0 range
- [ ] Tests created: tests/test_urgency_scorer.py
- [ ] Configuration examples provided
```

---

### Prompt 2.2.7: Create Notification Action Plugin

```
@workspace Create a notification action plugin for Slack/Discord/Email.

Context:
- Need action plugin example
- Notifications are common action type
- Support multiple notification channels

Task:
Create `plugins/notification_action.py`:
1. Class NotificationAction implementing reaper_action_execute hook
2. Send notifications via Slack, Discord, or Email
3. Format message with signal context
4. Handle rate limiting
5. Return ActionResult with success status

Requirements:
- Implement @hookimpl decorator
- Take ScoredSignal, return ActionResult
- Support multiple channels (configured)
- Template-based message formatting
- Include signal details in notification
- Rate limiting to prevent spam
- Handle API errors gracefully

Success Criteria:
- [ ] Plugin implements reaper_action_execute correctly
- [ ] Sends notifications to configured channel
- [ ] Message includes signal context
- [ ] Rate limiting prevents spam
- [ ] Tests created: tests/test_notification_action.py (use mocks)
- [ ] Setup guide for each notification type
```

---

### Prompt 2.2.8: Create Ticket Action Plugin

```
@workspace Create a ticket creation action plugin for GitHub/Jira.

Context:
- Automatic ticket creation for high-priority signals
- Need action plugin for issue trackers
- Should auto-populate ticket with signal data

Task:
Create `plugins/ticket_action.py`:
1. Class TicketAction implementing reaper_action_execute hook
2. Create tickets in GitHub Issues or Jira
3. Auto-assign based on signal metadata
4. Include signal context in ticket
5. Return ActionResult with ticket URL

Requirements:
- Implement @hookimpl decorator
- Take ScoredSignal, return ActionResult
- Support GitHub Issues and Jira
- Template-based ticket description
- Include signal details, score, analysis
- Auto-assign via configuration
- Return ticket URL in result_data

Success Criteria:
- [ ] Plugin implements reaper_action_execute correctly
- [ ] Creates tickets in configured tracker
- [ ] Ticket includes full signal context
- [ ] Returns ticket URL
- [ ] Tests created: tests/test_ticket_action.py (use mocks)
- [ ] Setup guide for GitHub and Jira
```

---

### Prompt 2.2.9: Create Webhook Action Plugin

```
@workspace Create a webhook action plugin for POSTing signal data.

Context:
- Webhooks allow integration with external systems
- Need generic action plugin example
- Should handle retries and failures

Task:
Create `plugins/webhook_action.py`:
1. Class WebhookAction implementing reaper_action_execute hook
2. POST signal data to configured webhook URL
3. Support custom payload formatting
4. Implement retry logic for failures
5. Return ActionResult with response status

Requirements:
- Implement @hookimpl decorator
- Take ScoredSignal, return ActionResult
- POST to webhook URL (from configuration)
- Configurable payload format (JSON)
- Retry logic: exponential backoff
- Timeout handling
- Include response in result_data

Success Criteria:
- [ ] Plugin implements reaper_action_execute correctly
- [ ] POSTs to any webhook URL
- [ ] Retry logic handles failures
- [ ] Response included in result
- [ ] Tests created: tests/test_webhook_action.py (use mocks)
- [ ] Payload format examples provided
```

---

## Milestone 3: Integration & Testing (Week 5)

### Prompt 2.3.1: Create Mock Data Generator

```
@workspace Create a mock data generator for integration testing.

Context:
- Integration tests need realistic test data
- Should generate data for all sense types
- Support batch generation for performance tests

Task:
Create `tests/mock_data_generator.py`:
1. Functions to generate realistic signals for each sense
2. Support for batch generation
3. Include edge cases (empty, malformed, large)
4. Configurable signal characteristics
5. Utility for performance testing

Requirements:
- Functions: generate_sight_signal, generate_hearing_signal, etc.
- generate_batch_signals(sense_type, count)
- Include edge cases: empty raw_data, missing fields, huge payloads
- Realistic content: text, numbers, timestamps
- Configurable noise and variety

Success Criteria:
- [ ] Generator creates realistic signals
- [ ] Supports all 5 sense types
- [ ] Batch generation works
- [ ] Edge cases included
- [ ] Tests created: tests/test_mock_data_generator.py
- [ ] Documentation with examples
```

---

### Prompt 2.3.2: Create End-to-End Pipeline Tests

```
@workspace Create comprehensive end-to-end pipeline tests.

Context:
- Need tests covering complete pipeline flow
- Test all 5 senses through to action
- Verify signal flow and transformations

Task:
Create `tests/test_e2e_pipeline.py`:
1. test_full_pipeline_all_senses() - All 5 senses → scoring → action
2. test_multi_source_detection() - Sight + hearing simultaneously
3. test_pipeline_with_failing_plugin() - Error handling
4. test_high_volume_processing() - Performance with many signals
5. test_plugin_hot_swap() - Add/remove plugins at runtime

Requirements:
- Use real plugin implementations (from Milestone 2)
- Verify signal transformations at each stage
- Test concurrent detection from multiple senses
- Verify error handling doesn't crash pipeline
- Performance test: 1000+ signals
- Hot-swap test: add/remove plugins dynamically

Success Criteria:
- [ ] 5 end-to-end tests created
- [ ] All tests pass with real plugins
- [ ] Coverage of error scenarios
- [ ] Performance benchmarks established
- [ ] Hot-swap functionality verified
- [ ] Tests run in < 30 seconds
```

---

### Prompt 2.3.3: Create Performance Benchmarks

```
@workspace Create performance benchmarks for REAPER pipeline.

Context:
- Need baseline performance metrics
- Identify bottlenecks
- Track performance over time

Task:
Create `benchmarks/benchmark_pipeline.py`:
1. Benchmark signal detection (signals per second)
2. Benchmark scoring throughput
3. Benchmark action execution
4. Benchmark end-to-end pipeline
5. Generate performance report

Requirements:
- Use pytest-benchmark or timeit
- Test with varying signal counts: 10, 100, 1000, 10000
- Measure: throughput, latency, memory usage
- Compare different plugin implementations
- Generate markdown report with results
- Include in CI/CD for regression tracking

Success Criteria:
- [ ] Benchmark suite created
- [ ] Covers detection, scoring, action
- [ ] Tests multiple signal volumes
- [ ] Results documented in report
- [ ] Baseline metrics established
- [ ] CI integration ready
```

---

## Milestone 4: Community & Documentation (Week 6)

### Prompt 2.4.1: Launch GitHub Discussions

```
@workspace Setup GitHub Discussions for REAPER community.

Context:
- Need community forum for Q&A and ideation
- Discussions organized by categories
- Should encourage plugin sharing

Task:
Setup on GitHub and create initial content:
1. Enable Discussions on repository
2. Create categories: Q&A, Ideas, Plugin Marketplace
3. Create welcome discussion post
4. Create "How to Create Your First Plugin" tutorial
5. Create "Plugin Showcase" discussion

Requirements:
Discussion Categories:
- Q&A - Support questions
- Ideas - Feature requests and discussions
- Plugin Marketplace - Share custom plugins
- Show and Tell - Showcase implementations

Initial Posts:
- Welcome post with guidelines
- Plugin tutorial linking to docs
- Showcase post for voting on favorite plugins

Success Criteria:
- [ ] Discussions enabled on GitHub
- [ ] 3 categories created
- [ ] 3+ initial discussion posts
- [ ] Templates for plugin submissions
- [ ] Community guidelines posted
```

---

### Prompt 2.4.2: Create GitHub Projects Board

```
@workspace Create GitHub Projects board for Phase 2 tracking.

Context:
- Need transparent progress tracking
- Projects board shows Phase 2 status
- Community can see what's being worked on

Task:
Create and configure Projects board:
1. Create "Phase 2: Pipeline Completion" project
2. Setup columns: Backlog, In Progress, Review, Done
3. Add all Phase 2 issues/tasks
4. Configure automation (issue → project)
5. Setup milestone tracking

Requirements:
Columns:
- Backlog - Not started
- In Progress - Being worked on
- Review - Needs review
- Done - Completed

Automation:
- New issues auto-added to Backlog
- PRs linked to issues
- Closed issues move to Done

Content:
- Add issue for each Milestone 2 plugin
- Add issue for integration tests
- Add issue for documentation tasks

Success Criteria:
- [ ] Projects board created and public
- [ ] All Phase 2 tasks as cards
- [ ] Automation configured
- [ ] Visual progress tracking working
- [ ] Milestone completion visible
```

---

### Prompt 2.4.3: Create Plugin Documentation Generator

```
@workspace Create automated plugin documentation generator.

Context:
- Need to auto-generate docs from plugin code
- Extract docstrings and type hints
- Generate markdown docs automatically

Task:
Create `scripts/generate_plugin_docs.py`:
1. Scan plugins directory for plugin files
2. Extract docstrings, type hints, examples
3. Generate markdown documentation
4. Include usage examples
5. Cross-reference with API docs

Requirements:
- Parse Python files for plugin classes
- Extract class and method docstrings
- Include type hints in docs
- Generate usage examples from docstrings
- Create one markdown file per plugin
- Output to public_docs/plugins/
- Run as part of CI/CD

Success Criteria:
- [ ] Script generates plugin docs
- [ ] Markdown output is readable
- [ ] Usage examples included
- [ ] Type hints documented
- [ ] CI integration: docs auto-update
- [ ] Tests: tests/test_doc_generator.py
```

---

### Prompt 2.4.4: Update Copilot Instructions

```
@workspace Update Copilot instructions with Phase 2 learnings.

Context:
- Phase 2 revealed new patterns and pitfalls
- Need to update .github/copilot-instructions.md
- Include real plugin examples

Task:
Update `.github/copilot-instructions.md`:
1. Add Phase 2 plugin examples (Reddit, Discord, RSS)
2. Document new common errors discovered
3. Add integration testing patterns
4. Include performance optimization tips
5. Update quick reference with Phase 2 patterns

Requirements:
New Sections:
- Real-world plugin patterns (from Milestone 2)
- Integration testing examples
- Performance best practices
- Multi-plugin coordination

Updates:
- Common errors: Add Phase 2 specific issues
- Quick reference: Add plugin templates
- Examples: Use actual Phase 2 plugins

Success Criteria:
- [ ] Copilot instructions updated
- [ ] Phase 2 plugins referenced
- [ ] New patterns documented
- [ ] Performance tips included
- [ ] Examples from real code
```

---

## Milestone 5: Quality Assurance (Week 7)

### Prompt 2.5.1: Run Full Test Suite

```
@workspace Run complete test suite and verify all quality gates.

Context:
- Phase 2 completion requires all tests passing
- Need 95%+ coverage maintained
- All quality gates must pass

Task:
Run and verify:
1. Full pytest suite: pytest -v
2. Coverage report: pytest --cov=reaper --cov=pipeline --cov=plugins
3. Linting: ruff format --check . && ruff check .
4. Security scan: Run CodeQL if available
5. Example runner: python example_runner.py

Requirements:
All Must Pass:
- 136+ tests (more with Phase 2 additions)
- Coverage: 95%+ on all modules
- Ruff formatting: No errors
- Ruff linting: No errors
- CodeQL: 0 vulnerabilities
- Examples: Run without errors

Fix Any Failures:
- Update tests if needed
- Fix coverage gaps
- Address linting issues
- Fix security vulnerabilities

Success Criteria:
- [ ] All tests pass: pytest -v
- [ ] Coverage ≥ 95%: pytest --cov
- [ ] Linting clean: ruff format --check . && ruff check .
- [ ] No security issues
- [ ] Examples run successfully
- [ ] Document results
```

---

### Prompt 2.5.2: Performance Validation

```
@workspace Validate performance meets Phase 2 requirements.

Context:
- Phase 2 requires production-ready performance
- Benchmarks must meet targets
- Identify any bottlenecks

Task:
Run and analyze performance:
1. Run benchmark suite: pytest benchmarks/ -v
2. Analyze results against baselines
3. Identify bottlenecks
4. Optimize critical paths if needed
5. Document final performance metrics

Requirements:
Target Metrics:
- Detection: 100+ signals/second per sense
- Scoring: 1000+ signals/second
- Action: 50+ actions/second
- End-to-end: 50+ signals/second
- Memory: < 100MB for 1000 signals

Analysis:
- Compare against baselines
- Identify slow operations
- Profile if needed
- Optimize critical paths

Success Criteria:
- [ ] Benchmarks run successfully
- [ ] Performance meets targets
- [ ] Bottlenecks identified and documented
- [ ] Critical optimizations completed
- [ ] Final metrics documented
```

---

### Prompt 2.5.3: Code Review All Phase 2 Changes

```
@workspace Perform comprehensive code review of Phase 2 changes.

Context:
- Phase 2 added significant new code
- Need quality review before release
- Verify conventions followed

Task:
Review all Phase 2 additions:
1. Review all new plugin implementations
2. Review integration tests
3. Review documentation updates
4. Check for code smells and anti-patterns
5. Verify REAPER conventions followed

Review Checklist:
- [ ] No hard-coded sources (all use parameters)
- [ ] Proper hook names used (reaper_action_execute)
- [ ] Type hints complete and correct
- [ ] Docstrings comprehensive
- [ ] Error handling robust
- [ ] No security vulnerabilities
- [ ] Tests cover edge cases
- [ ] Documentation accurate

Action Items:
- Create issues for any problems found
- Fix critical issues immediately
- Document tech debt for future phases

Success Criteria:
- [ ] All Phase 2 code reviewed
- [ ] Critical issues fixed
- [ ] Minor issues documented
- [ ] Conventions verified
- [ ] Quality stamp approved
```

---

## Milestone 6: Phase 2 Release (Week 8)

### Prompt 2.6.1: Create Phase 2 Release Notes

```
@workspace Create comprehensive release notes for Phase 2 (v0.2.0).

Context:
- Phase 2 complete, ready to release
- Need changelog documenting all changes
- Should highlight new features and improvements

Task:
Create `CHANGELOG.md` or update existing:
1. Document all new plugins added
2. List integration test additions
3. Highlight documentation improvements
4. Note performance improvements
5. List any breaking changes

Requirements:
Format:
## [0.2.0] - 2026-04-05 - Phase 2: Pipeline Completion

### Added
- 9 real-world plugins (list them)
- 10+ integration tests
- Performance benchmarks
- Plugin documentation generator
- GitHub Discussions and Projects

### Changed
- Enhanced all sense module documentation
- Updated Copilot instructions

### Performance
- Detection: 100+ signals/second
- End-to-end: 50+ signals/second

### Community
- Launched Discussions
- Created Projects board

Success Criteria:
- [ ] CHANGELOG.md complete
- [ ] All additions documented
- [ ] Performance metrics included
- [ ] Breaking changes noted (if any)
- [ ] Community features highlighted
```

---

### Prompt 2.6.2: Tag and Release v0.2.0

```
@workspace Create git tag and GitHub release for Phase 2.

Context:
- Phase 2 complete and verified
- Ready to tag stable release
- Create GitHub release with notes

Task:
Create release:
1. Ensure all changes committed to main/develop
2. Create annotated git tag: v0.2.0
3. Push tag to GitHub
4. Create GitHub Release from tag
5. Include release notes and highlights

Requirements:
Git Tag:
```bash
git tag -a v0.2.0 -m "Phase 2: Pipeline Completion (Beta)

- 9 real-world plugins
- 10+ integration tests
- Performance benchmarks
- Community engagement (Discussions, Projects)
- Full documentation"
```

GitHub Release:
- Title: "v0.2.0 - Phase 2: Pipeline Completion (Beta)"
- Include changelog
- Highlight key features
- Link to documentation
- Installation instructions

Success Criteria:
- [ ] Git tag created: v0.2.0
- [ ] Tag pushed to GitHub
- [ ] GitHub Release published
- [ ] Release notes complete
- [ ] Community notified
```

---

### Prompt 2.6.3: Update Roadmap for Phase 3

```
@workspace Update Roadmap document to mark Phase 2 complete and prepare Phase 3.

Context:
- Phase 2 now complete
- Need to update roadmap status
- Begin Phase 3 planning

Task:
Update `Roadmap` file:
1. Mark Phase 2 as complete (✅)
2. Add completion date to Phase 2
3. Update Phase 2 link to point to release tag
4. Begin Phase 3 section elaboration
5. Update progress tracking section

Requirements:
Phase 2 Section:
```markdown
## Phase 2: Pipeline Completion ("Beta") ✅

**Completed**: April 5, 2026
📋 **[Phase 2 Release](https://github.com/SaltProphet/Reaper/releases/tag/v0.2.0)**

**Delivered:**
- ✅ 9 real-world plugins (3 ingestors, 3 analyzers, 3 actions)
- ✅ 10+ integration tests
- ✅ Performance benchmarks
- ✅ Community engagement (Discussions, Projects)
- ✅ Enhanced documentation
```

Phase 3 Section:
- Elaborate on Ouroboros Protocol
- Detail operator console requirements
- Expand collaboration tasks

Success Criteria:
- [ ] Roadmap updated with Phase 2 completion
- [ ] Phase 3 section elaborated
- [ ] Links to Phase 2 release
- [ ] Progress tracking updated
- [ ] Ready for Phase 3 kickoff
```

---

## Phase 2 Final Verification Checklist

Before marking Phase 2 complete:

### Core Development
- [ ] All 5 sense modules fully documented
- [ ] 2+ examples per sense created
- [ ] 9+ real-world plugins implemented:
  - [ ] RedditIngestor
  - [ ] DiscordIngestor
  - [ ] RSSIngestor
  - [ ] KeywordScorer
  - [ ] SentimentScorer
  - [ ] UrgencyScorer
  - [ ] NotificationAction
  - [ ] TicketAction
  - [ ] WebhookAction
- [ ] 10+ integration tests created
- [ ] Performance benchmarks completed

### Quality Gates
- [ ] All tests pass (136+)
- [ ] Coverage ≥ 95%
- [ ] Ruff linting clean
- [ ] CodeQL: 0 vulnerabilities
- [ ] Code review completed
- [ ] Examples run successfully

### Community & Documentation
- [ ] GitHub Discussions launched
- [ ] GitHub Projects board active
- [ ] Plugin documentation automated
- [ ] Copilot instructions updated
- [ ] Changelog complete

### Release
- [ ] Release notes written
- [ ] Git tag created: v0.2.0
- [ ] GitHub Release published
- [ ] Roadmap updated
- [ ] Community notified

---

## Tips for AI Coders

**Phase 2 Focus:**
- Real-world plugins (not just stubs)
- Integration testing (end-to-end flows)
- Performance optimization
- Community building

**Testing Commands:**
```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_reddit_ingestor.py -v

# Run integration tests only
pytest tests/test_e2e_pipeline.py -v

# Check coverage
pytest --cov=reaper --cov=pipeline --cov=plugins

# Run benchmarks
pytest benchmarks/ -v
```

**Common Pitfalls:**
1. Hard-coding API keys (use environment variables)
2. Not handling rate limits (implement backoff)
3. Missing error handling (APIs fail!)
4. Forgetting to mock external APIs in tests
5. Not testing with realistic data

**Plugin Development:**
- Always use @hookimpl decorator
- Source parameter never hard-coded
- Return correct types (List[Signal], ScoredSignal, ActionResult)
- Handle errors gracefully
- Include comprehensive docstrings

---

**Related Documents:**
- [PHASE_2_PLAN.md](PHASE_2_PLAN.md) - Detailed roadmap
- [PHASE_2_QUICK_REF.md](PHASE_2_QUICK_REF.md) - Templates and examples
- [Roadmap](Roadmap) - Overall project timeline
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributor guidelines
