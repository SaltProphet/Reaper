# Phase 4 Copilot Prompts: Quality, Automation, Community

**Status**: 📅 PLANNED  
**Copy-Paste Ready Prompts for GitHub Copilot**

---

## Overview

Phase 4 prepares REAPER for v1.0 release with comprehensive testing, automation, community growth, and production hardening.

**Prerequisites**: Phase 3 complete (Ouroboros Protocol and operator console functional)

---

## Section 1: Test Harness Expansion

### Prompt 4.1.1: Create Comprehensive Unit Test Suite

```
@workspace Expand unit test coverage to 98%+ across entire codebase.

Context:
- Current coverage at 95%+, need to reach 98%
- Cover all edge cases and error paths
- Add property-based testing

Task:
Enhance test suite:
1. Identify untested code paths
2. Add tests for all edge cases
3. Add property-based tests (Hypothesis)
4. Add mutation testing (mutmut)
5. Fix any flaky tests

Requirements:
- Coverage ≥ 98% on all modules
- Property-based tests for data models
- Mutation testing score ≥ 90%
- Zero flaky tests
- All error paths tested
- Timeout tests for long operations

Success Criteria:
- [ ] Coverage reaches 98%+
- [ ] Property-based tests added
- [ ] Mutation testing passing
- [ ] No flaky tests remain
- [ ] Tests run in < 60 seconds
- [ ] Coverage report generated
```

---

### Prompt 4.1.2: Create Integration Test Suite

```
@workspace Build comprehensive integration test suite for all components.

Context:
- Need thorough integration testing
- Test all component interactions
- Include failure scenarios

Task:
Create `tests/integration/` directory with:
1. test_plugin_integration.py - Plugin interactions
2. test_pipeline_integration.py - End-to-end flows
3. test_feedback_integration.py - Feedback loop
4. test_console_integration.py - Console operations
5. test_external_integration.py - External APIs (mocked)

Requirements:
- Test all plugin combinations
- Test pipeline under load
- Test feedback → learning loop
- Test console commands
- Mock external APIs (Reddit, Discord, etc.)
- Include failure injection tests

Success Criteria:
- [ ] 50+ integration tests created
- [ ] All component interactions tested
- [ ] Failure scenarios covered
- [ ] External APIs mocked
- [ ] Tests pass consistently
- [ ] Documentation with diagrams
```

---

### Prompt 4.1.3: Create End-to-End Test Suite

```
@workspace Build end-to-end test suite simulating real usage.

Context:
- Need full system tests
- Simulate real user workflows
- Test production scenarios

Task:
Create `tests/e2e/` directory with:
1. test_new_user_workflow.py - Setup and first run
2. test_operator_workflow.py - Daily operations
3. test_plugin_development.py - Developer experience
4. test_production_scenarios.py - Real-world cases
5. test_disaster_recovery.py - Failure recovery

Requirements:
- Simulate complete user journeys
- Use real plugins and data
- Test installation and setup
- Test daily operations
- Test disaster recovery
- Include performance tests

Success Criteria:
- [ ] 20+ end-to-end tests created
- [ ] User workflows validated
- [ ] Production scenarios tested
- [ ] Recovery tested
- [ ] All tests pass
- [ ] Execution time < 5 minutes
```

---

### Prompt 4.1.4: Add Performance Regression Tests

```
@workspace Create performance regression test suite.

Context:
- Need to catch performance degradation
- Automated benchmarking in CI
- Track performance over time

Task:
Create `tests/performance/` directory with:
1. test_detection_performance.py - Detection throughput
2. test_scoring_performance.py - Scoring speed
3. test_action_performance.py - Action execution
4. test_memory_performance.py - Memory usage
5. test_startup_performance.py - Startup time

Requirements:
- Benchmark against baselines
- Run in CI/CD pipeline
- Track performance history
- Alert on regressions (> 10% slower)
- Test with varying data sizes
- Memory profiling

Success Criteria:
- [ ] Performance tests created
- [ ] Baselines established
- [ ] CI integration functional
- [ ] Regression detection works
- [ ] Performance history tracked
- [ ] Alerts configured
```

---

## Section 2: Plugin API Hardening

### Prompt 4.2.1: Version and Stabilize Plugin API

```
@workspace Version and stabilize the plugin API for v1.0.

Context:
- Plugin API must be stable for v1.0
- Need versioning strategy
- Backward compatibility important

Task:
Create `reaper/api_version.py` and update docs:
1. Define API version (1.0)
2. Document all public APIs
3. Mark deprecated methods
4. Add version checking
5. Create migration guide

Requirements:
- Semantic versioning (MAJOR.MINOR.PATCH)
- Public API clearly documented
- Deprecation warnings for old APIs
- Version compatibility checking
- Migration guide for breaking changes
- API stability guarantees

Success Criteria:
- [ ] API versioned as 1.0
- [ ] All public APIs documented
- [ ] Deprecation strategy defined
- [ ] Version checking implemented
- [ ] Migration guide complete
- [ ] Stability guarantees published
```

---

### Prompt 4.2.2: Create Plugin Developer Guide

```
@workspace Write comprehensive plugin developer guide.

Context:
- Need thorough guide for plugin authors
- Cover all plugin types
- Include advanced topics

Task:
Create `public_docs/plugin_development_guide.md`:
1. Getting started with plugins
2. Plugin types and when to use each
3. Hook specifications reference
4. Testing plugins
5. Publishing plugins
6. Troubleshooting guide
7. Advanced patterns

Requirements:
- Complete working examples
- Cover all 5 sense types + scoring + action
- Testing best practices
- Performance optimization tips
- Error handling patterns
- Real-world case studies
- Troubleshooting common issues

Success Criteria:
- [ ] Comprehensive guide written
- [ ] All plugin types covered
- [ ] Working examples included
- [ ] Advanced topics explained
- [ ] Troubleshooting section complete
- [ ] Peer reviewed
```

---

### Prompt 4.2.3: Create Plugin Testing Framework

```
@workspace Build plugin testing framework and utilities.

Context:
- Plugin authors need testing tools
- Standardize plugin testing
- Make testing easy

Task:
Create `reaper/plugin_testing.py`:
1. PluginTestCase base class
2. Fixtures for common test data
3. Mock utilities for external APIs
4. Performance testing helpers
5. Assertion helpers

Requirements:
- Base class with common assertions
- Mock generators for signals
- Mock external APIs (Reddit, etc.)
- Performance benchmarking helpers
- Assertion: signal format, score range, etc.
- Documentation with examples

Success Criteria:
- [ ] Plugin testing framework created
- [ ] Base classes and fixtures available
- [ ] Mock utilities functional
- [ ] Performance helpers working
- [ ] Tests: tests/test_plugin_testing.py
- [ ] Examples for each plugin type
```

---

## Section 3: Advanced Automation

### Prompt 4.3.1: Implement Spark Changelog Generation

```
@workspace Setup GitHub Spark for automatic changelog generation.

Context:
- Need automated changelog creation
- Extract from commit messages and PRs
- Format for releases

Task:
Create Spark workflow for changelogs:
1. Configure Spark to monitor commits
2. Extract changelog items from commits
3. Group by category (Added, Changed, Fixed)
4. Generate markdown changelog
5. Update CHANGELOG.md automatically

Requirements:
- Parse conventional commit messages
- Extract from PR descriptions
- Group by type: feat, fix, docs, etc.
- Generate markdown format
- Link to commits and PRs
- Run on release tags

Success Criteria:
- [ ] Spark workflow configured
- [ ] Changelog generated automatically
- [ ] Format is readable
- [ ] Links to commits/PRs work
- [ ] Runs on tag creation
- [ ] Documentation with examples
```

---

### Prompt 4.3.2: Implement Spark Documentation Generator

```
@workspace Setup Spark for automatic documentation updates.

Context:
- Keep documentation in sync with code
- Auto-generate API docs
- Update examples automatically

Task:
Create Spark workflow for docs:
1. Extract docstrings from code
2. Generate API reference
3. Update code examples
4. Verify links in documentation
5. Deploy to GitHub Pages

Requirements:
- Extract from all public APIs
- Generate markdown or HTML
- Keep examples up-to-date
- Check for broken links
- Deploy automatically
- Version docs with releases

Success Criteria:
- [ ] Spark workflow configured
- [ ] API docs auto-generated
- [ ] Examples updated
- [ ] Links verified
- [ ] Deployment automatic
- [ ] Versioned correctly
```

---

### Prompt 4.3.3: Implement Copilot-Powered PR Reviews

```
@workspace Configure Copilot for automated PR code reviews.

Context:
- Automate code review process
- Check conventions automatically
- Provide consistent feedback

Task:
Configure Copilot PR review:
1. Setup GitHub Actions for PR review
2. Configure review criteria
3. Check REAPER conventions
4. Generate review comments
5. Assign reviewers based on changes

Review Checks:
- No hard-coded sources
- Correct hook names
- Type hints present
- Tests included
- Documentation updated
- Performance acceptable
- Security scan passed

Success Criteria:
- [ ] Copilot review configured
- [ ] Reviews are helpful
- [ ] Conventions checked
- [ ] Comments are actionable
- [ ] False positives minimal
- [ ] Human review for complex cases
```

---

### Prompt 4.3.4: Create Issue Triage Automation

```
@workspace Implement automated issue triage with Spark.

Context:
- Need automated issue labeling
- Route issues to right people
- Identify duplicates

Task:
Create Spark workflow for issues:
1. Auto-label based on content
2. Assign to appropriate team/person
3. Detect duplicate issues
4. Add to relevant Projects
5. Generate initial response

Requirements:
- Classify: bug, feature, plugin, docs
- Detect: priority, complexity
- Find duplicates (similarity matching)
- Auto-assign based on area
- Add to project boards
- Welcome message for new contributors

Success Criteria:
- [ ] Auto-labeling works
- [ ] Assignment accurate
- [ ] Duplicates detected
- [ ] Project board updated
- [ ] Welcome messages sent
- [ ] 80%+ accuracy
```

---

## Section 4: Community Growth

### Prompt 4.4.1: Launch Weekly Community Updates

```
@workspace Setup weekly community update system.

Context:
- Regular updates keep community engaged
- Share progress and highlights
- Celebrate contributions

Task:
Create update system:
1. Weekly update template
2. Automated data collection
3. Highlight generation
4. Post to Discussions
5. Newsletter option

Content:
- New plugins released
- Top contributors
- Merged PRs
- Upcoming milestones
- Community highlights

Success Criteria:
- [ ] Update template created
- [ ] Automation configured
- [ ] First update posted
- [ ] Community engaged
- [ ] Feedback positive
```

---

### Prompt 4.4.2: Create Plugin Marketplace Showcase

```
@workspace Build plugin marketplace showcase in Discussions.

Context:
- Highlight community plugins
- Make plugins discoverable
- Encourage plugin development

Task:
Setup marketplace:
1. Create showcase Discussion category
2. Plugin submission template
3. Featured plugin rotation
4. Voting system
5. Plugin of the month

Requirements:
- Submission template with metadata
- Screenshots and examples
- Installation instructions
- User ratings/feedback
- Featured rotation (weekly)
- Plugin of the month award

Success Criteria:
- [ ] Marketplace category created
- [ ] Submission template ready
- [ ] First plugins showcased
- [ ] Voting functional
- [ ] Community participating
```

---

### Prompt 4.4.3: Implement Contributor Recognition Program

```
@workspace Create contributor recognition and reward system.

Context:
- Recognize valuable contributions
- Motivate continued participation
- Build strong community

Task:
Create recognition program:
1. Contribution tracking
2. Achievement badges
3. Hall of fame
4. Monthly recognition
5. Special perks for top contributors

Recognition Types:
- First contribution
- 10 PRs merged
- Plugin author
- Documentation hero
- Bug hunter
- Code reviewer

Success Criteria:
- [ ] Recognition system implemented
- [ ] Badges/achievements defined
- [ ] Hall of fame created
- [ ] First recognitions given
- [ ] Community responds positively
```

---

### Prompt 4.4.4: Create Comprehensive Spaces Templates

```
@workspace Build GitHub Spaces templates for collaboration.

Context:
- Need templates for common sessions
- Make collaboration easy
- Document best practices

Task:
Create Spaces templates:
1. Plugin design session
2. Feature discussion
3. Code review session
4. Roadmap planning
5. Community feedback

Requirements:
- Session agendas
- Pre-work instructions
- Facilitation guidelines
- Output templates
- Follow-up tasks

Success Criteria:
- [ ] 5 templates created
- [ ] Documentation complete
- [ ] First sessions held
- [ ] Feedback incorporated
- [ ] Templates refined
```

---

## Section 5: Production Readiness

### Prompt 4.5.1: Conduct Security Audit

```
@workspace Perform comprehensive security audit for v1.0.

Context:
- Production requires security hardening
- Identify and fix vulnerabilities
- Document security practices

Task:
Conduct security audit:
1. Run security scanners (Bandit, Safety)
2. Review authentication/authorization
3. Check input validation
4. Audit dependencies
5. Penetration testing
6. Document security measures

Security Checklist:
- [ ] No hardcoded secrets
- [ ] Input validation everywhere
- [ ] SQL injection prevention
- [ ] XSS prevention (if web UI)
- [ ] Rate limiting
- [ ] HTTPS enforced
- [ ] Secure dependencies

Success Criteria:
- [ ] Security audit complete
- [ ] All high/critical issues fixed
- [ ] Medium issues documented
- [ ] Security guide written
- [ ] Scanning automated in CI
```

---

### Prompt 4.5.2: Implement Performance Tuning

```
@workspace Optimize REAPER performance for production.

Context:
- Production requires optimal performance
- Identify and fix bottlenecks
- Achieve performance targets

Task:
Performance optimization:
1. Profile critical paths
2. Optimize hot spots
3. Implement caching
4. Database optimization
5. Concurrent processing
6. Memory optimization

Targets:
- Detection: 1000+ signals/sec
- Scoring: 5000+ signals/sec
- Action: 100+ actions/sec
- Memory: < 200MB for 10k signals
- Startup: < 3 seconds

Success Criteria:
- [ ] Profiling complete
- [ ] Bottlenecks identified
- [ ] Optimizations implemented
- [ ] Targets achieved
- [ ] Benchmarks passing
- [ ] Memory usage acceptable
```

---

### Prompt 4.5.3: Create Production Deployment Guide

```
@workspace Write comprehensive production deployment guide.

Context:
- Need guide for production deployment
- Cover different environments
- Include monitoring and troubleshooting

Task:
Create `public_docs/production_deployment.md`:
1. System requirements
2. Installation steps
3. Configuration guide
4. Monitoring setup
5. Backup and recovery
6. Troubleshooting
7. Security hardening
8. Scaling strategies

Requirements:
- Cover: Docker, Kubernetes, bare metal
- Environment configuration
- Database setup (if applicable)
- Monitoring with Prometheus/Grafana
- Log aggregation
- Backup procedures
- Disaster recovery
- Performance tuning

Success Criteria:
- [ ] Deployment guide complete
- [ ] All environments covered
- [ ] Monitoring guide included
- [ ] Troubleshooting section comprehensive
- [ ] Tested on production-like environment
```

---

### Prompt 4.5.4: Create Operations Runbook

```
@workspace Create operations runbook for production REAPER.

Context:
- Operators need troubleshooting guide
- Document common issues
- Provide resolution steps

Task:
Create `public_docs/operations_runbook.md`:
1. Common issues and solutions
2. Monitoring and alerts
3. Performance troubleshooting
4. Incident response
5. Maintenance procedures
6. Emergency contacts

Runbook Sections:
- High CPU usage
- Memory leaks
- Plugin failures
- Database issues
- Network problems
- Performance degradation
- Data corruption

Success Criteria:
- [ ] Runbook complete
- [ ] Common issues documented
- [ ] Resolution steps clear
- [ ] Tested on real issues
- [ ] Team trained
```

---

## Section 6: v1.0 Release Preparation

### Prompt 4.6.1: Create Release Checklist

```
@workspace Create comprehensive v1.0 release checklist.

Context:
- Major release needs thorough verification
- All aspects must be verified
- Community ready for v1.0

Task:
Create release checklist:
1. Code quality checks
2. Documentation verification
3. Security audit results
4. Performance benchmarks
5. Community readiness
6. Marketing materials

Checklist:
- [ ] All tests passing (unit, integration, e2e)
- [ ] Coverage ≥ 98%
- [ ] Security audit complete
- [ ] Performance targets met
- [ ] Documentation complete
- [ ] Migration guide ready
- [ ] Release notes written
- [ ] Community notified
- [ ] Marketing materials ready

Success Criteria:
- [ ] Checklist complete
- [ ] All items verified
- [ ] Sign-off from team
- [ ] Ready for release
```

---

### Prompt 4.6.2: Write v1.0 Release Notes

```
@workspace Create comprehensive v1.0 release notes.

Context:
- First major release
- Highlight all features
- Thank contributors

Task:
Create release notes:
1. Feature highlights
2. Complete changelog
3. Breaking changes
4. Migration guide
5. Known issues
6. Contributor acknowledgments

Structure:
## REAPER v1.0 - Production Ready

### Highlights
- 9+ production plugins
- Ouroboros Protocol (self-learning)
- Operator console (CLI + Web)
- 98%+ test coverage
- Production deployment guide

### What's New
(List all Phase 3 & 4 additions)

### Breaking Changes
(List any API changes)

### Migration Guide
(Steps to upgrade from v0.2.0)

### Known Issues
(Document any known limitations)

### Contributors
(Thank all contributors)

Success Criteria:
- [ ] Release notes complete
- [ ] All features documented
- [ ] Migration guide clear
- [ ] Contributors acknowledged
- [ ] Reviewed and approved
```

---

### Prompt 4.6.3: Prepare Marketing Materials

```
@workspace Create marketing materials for v1.0 launch.

Context:
- Need materials to announce v1.0
- Reach wider audience
- Attract new users

Task:
Create marketing materials:
1. Launch blog post
2. Social media posts
3. Demo video
4. Feature tour
5. Use case examples
6. Press release

Materials:
- Blog post highlighting v1.0 features
- Twitter/LinkedIn announcement thread
- YouTube demo video (5-10 minutes)
- Screenshots and GIFs
- Real-world use cases
- Press release for tech sites

Success Criteria:
- [ ] Blog post written
- [ ] Social posts drafted
- [ ] Demo video recorded
- [ ] Screenshots captured
- [ ] Use cases documented
- [ ] Ready for launch day
```

---

### Prompt 4.6.4: Execute v1.0 Release

```
@workspace Execute the v1.0 release process.

Context:
- All preparation complete
- Ready to release v1.0
- Coordinate launch activities

Task:
Execute release:
1. Final verification
2. Create release tag
3. Publish to PyPI
4. Update documentation
5. Announce to community
6. Monitor for issues

Release Steps:
1. Run full test suite
2. Verify all quality gates
3. Create git tag: v1.0.0
4. Build distribution packages
5. Publish to PyPI
6. Create GitHub Release
7. Deploy documentation
8. Post announcement
9. Monitor community channels

Success Criteria:
- [ ] All quality gates passed
- [ ] Release tag created
- [ ] Published to PyPI
- [ ] GitHub Release live
- [ ] Documentation updated
- [ ] Community notified
- [ ] Monitoring active
- [ ] v1.0 SHIPPED! 🎉
```

---

## Phase 4 Verification Checklist

Before v1.0 release:

### Testing
- [ ] Unit tests: 98%+ coverage
- [ ] Integration tests: 50+ tests passing
- [ ] E2E tests: 20+ tests passing
- [ ] Performance tests: All benchmarks met
- [ ] Security audit: Complete, issues resolved

### Documentation
- [ ] API reference: Complete
- [ ] Plugin guide: Comprehensive
- [ ] Deployment guide: Production-ready
- [ ] Operations runbook: Complete
- [ ] Migration guide: Clear

### Automation
- [ ] Changelog: Auto-generated
- [ ] Docs: Auto-updated
- [ ] PR reviews: Automated
- [ ] Issue triage: Working

### Community
- [ ] Weekly updates: Running
- [ ] Plugin marketplace: Active
- [ ] Recognition program: Implemented
- [ ] Spaces templates: Available

### Production
- [ ] Security: Hardened
- [ ] Performance: Optimized
- [ ] Deployment: Tested
- [ ] Monitoring: Configured

### Release
- [ ] Release notes: Written
- [ ] Marketing: Ready
- [ ] Community: Notified
- [ ] v1.0: READY TO SHIP! 🚀

---

## Post-Release Activities

### Immediate (Day 1-7)
- Monitor for critical issues
- Respond to community feedback
- Fix any showstopper bugs
- Update documentation based on feedback

### Short-term (Week 2-4)
- Analyze adoption metrics
- Gather user feedback
- Plan patch releases
- Start Phase 5 planning

### Long-term (Month 2+)
- Community growth initiatives
- Plugin ecosystem expansion
- Performance improvements
- Feature planning

---

## Tips for AI Coders

**Phase 4 Focus:**
- Quality (98%+ coverage, security, performance)
- Automation (CI/CD, docs, reviews)
- Community (recognition, marketplace)
- Production readiness (deployment, operations)

**Quality Standards:**
- All code reviewed
- All tests passing
- Security verified
- Performance validated

**Documentation:**
- Clear and comprehensive
- Examples for everything
- Troubleshooting included
- Production-focused

**Community:**
- Regular communication
- Recognition and rewards
- Make contributing easy
- Celebrate successes

---

**Related Documents:**
- [Roadmap](Roadmap) - Overall timeline
- [PHASE_3_COPILOT_PROMPTS.md](PHASE_3_COPILOT_PROMPTS.md) - Previous phase
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
