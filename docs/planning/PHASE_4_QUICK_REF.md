# Phase 4 Quick Reference Guide

**Copy-paste ready prompts for GitHub Copilot**

This document provides quick-access prompts for each Phase 4 task. Simply copy the prompt and paste it to your AI coding assistant.

---

## 🧪 Expanded Test Harness

### Integration Tests

```
Create tests/integration/test_pipeline_e2e.py with full pipeline tests from signal detection through scoring to action execution. Test all five senses flowing through the complete pipeline. Use pytest fixtures, mock external services, assert on ActionResult.
```

### End-to-End Scenarios

```
Create tests/e2e/scenario_reddit_to_alert.py that simulates: Reddit signal detection → pattern analysis with Smell → PCI/ROI scoring with Taste → alert via webhook. Use real plugin instances, synthetic Reddit data, verify alert sent correctly.
```

### Test Harness Utilities

```
Create tests/harness.py with TestHarness class that sets up complete REAPER environment (PluginManager with all plugins registered), generates synthetic test data (signals, feedback), provides fixtures, cleans up resources. Support parallel test execution.
```

### Performance Tests

```
Create tests/performance/test_throughput.py that measures signals/second processing capacity. Generate 10,000+ test signals, measure realtime and batch processing throughput, compare to baseline, fail if regression >10%. Use pytest-benchmark.
```

### Test Utilities

```
Create tests/utils.py with SignalFactory.generate(count, sense_type, score_range), MockPluginFactory.create_detector(), AssertHelpers.assert_signal_valid(), PerformanceMonitor.track(). Make test writing easier and more consistent.
```

---

## 🔒 Hardened Plugin API

### API Versioning

```
Create reaper/api_version.py with API_VERSION="1.0.0", APIVersion class for compatibility checking, deprecation warning system. Check plugin compatibility on registration, provide clear migration guidance if incompatible.
```

### Plugin Validator

```
Create reaper/plugin_validator.py with PluginAPIValidator class that validates: hook signatures match hookspecs, return types correct, @hookimpl decorator present, no deprecated patterns used. Provide helpful error messages with links to docs.
```

### Plugin Metadata

```
Add metadata to hookimpl decorator: @hookimpl(api_version="1.0", author="name", description="...", tags=["detector", "reddit"]). Validate in PluginManager.register_plugin(), store for marketplace, display in console `reaper plugins`.
```

### API Reference Documentation

```
Create docs/API_REFERENCE.md documenting all hookspecs with: function signature, parameters, return type, example code, common mistakes. Include Signal/ScoredSignal/ActionResult model field reference, validation rules, migration guides for future versions.
```

### Plugin Development Guide

```
Create docs/PLUGIN_DEVELOPMENT.md with step-by-step guide for plugin development. Sections: setup, each sense type explained, testing plugins, deployment, best practices, anti-patterns to avoid, troubleshooting. Include complete working examples.
```

---

## 🤖 Advanced Automation Suite

### Changelog Automation

```
Create .github/workflows/changelog.yml triggered on release. Use conventional commits to group changes by type (feat/fix/docs). Auto-update CHANGELOG.md with PR links, contributor credits. Use GitHub Spark or actions/create-release. Permissions: contents: write.
```

### Documentation Auto-Update

```
Create .github/workflows/docs-update.yml triggered on push to main. Auto-generate API docs from docstrings using pdoc or similar. Update README metrics (test count, coverage %). Rebuild API_REFERENCE.md from hookspecs. Commit and push updates. Permissions: contents: write.
```

### Advanced PR Review

```
Create .github/workflows/pr-review-advanced.yml using GitHub Copilot API. Check for: correct hook names (@hookimpl decorator, reaper_action_execute not reaper_execute_action), proper Pydantic usage, test coverage for new files, docstrings present. Post constructive review comments. Permissions: pull-requests: write.
```

### Issue Triage Automation

```
Create .github/workflows/issue-triage.yml triggered on issues (opened). Auto-label based on content (bug/feature/plugin/docs). Check for duplicates using similarity search. Request missing information if template incomplete. Welcome first-time contributors. Permissions: issues: write.
```

### Release Automation

```
Create .github/workflows/release.yml triggered on tag push (v*.*.*). Build wheel and sdist, publish to PyPI, create GitHub release with auto-generated changelog, update version in pyproject.toml, tag Docker image. Include rollback steps. Permissions: contents: write, packages: write.
```

---

## 👥 Community Infrastructure

### Plugin Marketplace

```
Set up GitHub Discussions category "Plugin Showcase". Create template .github/DISCUSSION_TEMPLATES/plugin-showcase.yml with fields: plugin_name, author, description, repository_url, sense_type, version. Create workflow to auto-link plugins from submissions.
```

### Contributor Recognition

```
Create .github/CONTRIBUTORS.md that auto-updates with contributor list. Track code commits, PR reviews, issue responses, documentation. Assign badges (🥉 bronze 5+ contributions, 🥈 silver 20+, 🥇 gold 50+). Update weekly via GitHub Action. Highlight in README.
```

### GitHub Projects Board

```
Create GitHub Projects board "REAPER v1.0" with Kanban view (Backlog/In Progress/Review/Done). Add timeline view showing milestones. Configure automation: auto-add issues/PRs, auto-move on status change. Make public for transparency. Link from README.
```

### Plugin Submission Workflow

```
Create .github/workflows/plugin-submission.yml triggered when discussion created in Plugin Showcase. Validate plugin: check repository exists, clone and run tests, verify API compatibility, check documentation present. Auto-approve and showcase if passing, notify author of issues if failing.
```

### Community Metrics Dashboard

```
Create public_docs/community.html static page showing: contributor count, plugin count, issue/PR stats over time, activity graphs, top contributors list. Use GitHub API to fetch data, generate HTML with Chart.js for graphs. Regenerate weekly via GitHub Action.
```

---

## 🚀 v1.0 Preparation

### Security Scanning

```
Add security scanning to CI: Bandit (Python security issues), Safety (dependency vulnerabilities), pip-audit (supply chain). Create .github/workflows/security.yml running on every PR. Fail if critical/high issues found. Generate security report as artifact.
```

### Security Hardening

```
Review and harden REAPER security: validate all user inputs (console, config), sanitize webhook URLs, secure file permissions on exports, add rate limiting to external calls, ensure no sensitive data logged. Create tests/security/ with injection, traversal, validation tests.
```

### Security Documentation

```
Create docs/SECURITY.md with: supported versions table, vulnerability reporting process (security@...), security best practices for plugin authors, update schedule. Create SECURITY_CHANGELOG.md documenting fixes. Link from README.
```

### Performance Profiling

```
Profile REAPER with cProfile on typical workload (1000 signals through full pipeline). Identify bottlenecks. Optimize: cache plugin lookups, batch database operations, reduce object allocations. Benchmark before/after. Document in docs/PERFORMANCE.md.
```

### Performance Monitoring

```
Create reaper/monitoring.py with Metrics class tracking: signals/sec, memory usage, plugin execution times. Expose Prometheus format at /metrics endpoint (if web server) or via `reaper metrics` command. Add --monitor flag to console for live stats.
```

### Performance Benchmarks

```
Create benchmarks/benchmark_v1.py comparing performance vs Phase 1/2/3. Benchmark: throughput (signals/sec), latency (p50, p95, p99), memory usage (peak, average). Set regression thresholds in CI: fail if throughput drops >10% or memory increases >20%.
```

### Documentation Polish

```
Review and polish all documentation: README.md (add demo GIF, improve quick start), API_REFERENCE.md (proofread, add examples), PLUGIN_DEVELOPMENT.md (ensure clarity), CONTRIBUTING.md (update for v1.0), OPERATOR_GUIDE.md (screenshots/diagrams). Fix typos, improve formatting.
```

### Launch Materials

```
Create launch materials: announcement blog post (what/why/how of REAPER), demo video script (3-5 min YouTube video), social media posts (Twitter, LinkedIn, Reddit /r/Python), presentation slides (for conferences), FAQ document (common questions). Store in public_docs/launch/.
```

### PyPI Package Preparation

```
Update pyproject.toml with complete metadata: long_description from README, classifiers (Development Status :: 5 - Production/Stable, Intended Audience :: Developers, Topic :: Software Development), keywords, project_urls (Documentation, Source, Issues). Test build: `python -m build`. Test install in fresh venv.
```

### Project Website

```
Create GitHub Pages site in docs/ with: index.html (landing page explaining REAPER), plugins.html (plugin gallery), community.html (contributor page), documentation links, getting started guide. Use simple static HTML/CSS or Jekyll theme. Configure GitHub Pages in repo settings.
```

### Onboarding Experience

```
Create `reaper init` command in reaper/console.py that: creates config directory (~/.reaper/), runs interactive configuration wizard (ask about processing mode, alert preferences), installs sample plugins, generates example config file, prints next steps with docs links. Test on fresh system.
```

### Migration Guide

```
Create docs/MIGRATION_TO_V1.md for users of pre-release versions. Document: breaking changes (API changes, config format changes), deprecated features (with alternatives), step-by-step migration instructions, automated migration script (if complex), where to get help. Include before/after code examples.
```

---

## 📊 Testing Quick Commands

**Run integration tests:**
```bash
pytest tests/integration/ -v --cov
```

**Run e2e tests:**
```bash
pytest tests/e2e/ -v --cov -m e2e
```

**Run performance tests:**
```bash
pytest tests/performance/ -v --benchmark-only
```

**Run security tests:**
```bash
pytest tests/security/ -v
bandit -r reaper/ pipeline/
safety check
```

**Run all Phase 4 tests:**
```bash
pytest tests/integration/ tests/e2e/ tests/performance/ tests/security/ -v --cov --benchmark-skip
```

---

## 🔍 Quality Assurance Commands

**Check coverage:**
```bash
pytest --cov=reaper --cov=pipeline --cov-report=html
open htmlcov/index.html
```

**Profile performance:**
```bash
python -m cProfile -o profile.stats example_runner.py
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(20)"
```

**Check memory usage:**
```bash
python -m memory_profiler example_runner.py
```

**Run security scans:**
```bash
bandit -r reaper/ pipeline/ -f json -o bandit-report.json
safety check --json
pip-audit
```

**Validate package build:**
```bash
python -m build
twine check dist/*
```

---

## 🎯 v1.0 Launch Commands

**Create release tag:**
```bash
git tag -a v1.0.0 -m "REAPER v1.0.0 - Production Release"
git push origin v1.0.0
```

**Build and publish to PyPI:**
```bash
python -m build
twine upload dist/*
```

**Deploy documentation:**
```bash
cd docs/
bundle exec jekyll build
git add -A
git commit -m "Deploy docs for v1.0.0"
git push origin gh-pages
```

**Verify installation:**
```bash
python -m venv test_env
source test_env/bin/activate
pip install reaper
reaper --version
reaper init
```

---

## 📚 Documentation Templates

### Security Issue Template

```markdown
## Security Vulnerability Report

**Affected Version**: 
**Severity**: [Critical/High/Medium/Low]
**Component**: 

### Description
<!-- Detailed description of the vulnerability -->

### Steps to Reproduce
1. 
2. 
3. 

### Impact
<!-- What could an attacker do? -->

### Suggested Fix
<!-- If you have ideas for fixing it -->
```

### Plugin Showcase Template

```yaml
name: Plugin Showcase
description: Submit your REAPER plugin to the marketplace
title: "[PLUGIN] "
labels: ["plugin", "showcase"]
body:
  - type: input
    id: plugin_name
    attributes:
      label: Plugin Name
      placeholder: "RedditDetector"
    validations:
      required: true
  - type: input
    id: repository
    attributes:
      label: Repository URL
      placeholder: "https://github.com/user/reaper-reddit"
    validations:
      required: true
  - type: dropdown
    id: sense_type
    attributes:
      label: Sense Type
      options:
        - Sight
        - Hearing
        - Touch
        - Taste
        - Smell
        - Action
        - Scoring
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Description
      placeholder: "Detects signals from Reddit posts and comments..."
    validations:
      required: true
```

---

## 🎉 Community Engagement Prompts

### Weekly Update

```
Generate GitHub Discussions post summarizing this week's activity:
- New contributors: [count and names]
- Merged PRs: [list with titles and authors]
- New plugins: [names and descriptions]
- Open issues needing help: [critical ones]
- Next week's focus: [Phase 4 milestone]

Use friendly, encouraging tone. Thank contributors by name. Include links to PRs/issues.
```

### Contributor Spotlight

```
Write contributor spotlight for README.md highlighting @username:
- Contributions made (PRs, reviews, issues)
- Impact on project (what problem solved)
- Quote from contributor (if available)
- Badge earned (bronze/silver/gold)
- Link to profile

Keep to 3-4 sentences, positive and genuine.
```

### Release Announcement

```
Write REAPER v1.0.0 release announcement for:
- GitHub Discussions (detailed)
- Twitter (concise, 280 chars)
- LinkedIn (professional)
- Reddit /r/Python (technical, with examples)

Highlight: 5 sense architecture, plugin ecosystem, self-improving via Ouroboros, production-ready, 95%+ test coverage. Include getting started link.
```

---

## 🛠️ Utility Scripts

### Generate API Docs

```python
# scripts/generate_api_docs.py
import inspect
from reaper.hookspecs import HookSpecs

with open("docs/API_REFERENCE.md", "w") as f:
    f.write("# REAPER API Reference\n\n")
    for name, method in inspect.getmembers(HookSpecs, predicate=inspect.isfunction):
        if name.startswith("reaper_"):
            sig = inspect.signature(method)
            f.write(f"## {name}\n\n")
            f.write(f"```python\n{name}{sig}\n```\n\n")
            f.write(f"{inspect.getdoc(method)}\n\n")
```

### Update Metrics

```python
# scripts/update_metrics.py
import subprocess

# Get test count
result = subprocess.run(["pytest", "--collect-only", "-q"], capture_output=True, text=True)
test_count = result.stdout.count("test_")

# Get coverage
result = subprocess.run(["pytest", "--cov", "--cov-report=term"], capture_output=True, text=True)
coverage = result.stdout.split("TOTAL")[1].split()[1]

# Update README
with open("README.md", "r") as f:
    content = f.read()
content = content.replace("<!-- TEST_COUNT -->", str(test_count))
content = content.replace("<!-- COVERAGE -->", coverage)
with open("README.md", "w") as f:
    f.write(content)
```

---

## ✅ Phase 4 Completion Checklist

Copy this checklist to track progress:

```markdown
## Phase 4 Progress

### Testing
- [ ] Integration tests (50+ tests)
- [ ] End-to-end scenarios (5+ scenarios)
- [ ] Performance tests with baselines
- [ ] Security tests (input validation, injection, etc.)
- [ ] Test harness and utilities
- [ ] 95%+ overall coverage

### API Hardening
- [ ] API versioning system
- [ ] Plugin validator
- [ ] Plugin metadata system
- [ ] docs/API_REFERENCE.md
- [ ] docs/PLUGIN_DEVELOPMENT.md
- [ ] Backward compatibility layer

### Automation
- [ ] Changelog automation
- [ ] Documentation auto-update
- [ ] Advanced PR review
- [ ] Issue triage automation
- [ ] Release automation
- [ ] Community engagement automation

### Community
- [ ] Plugin marketplace in Discussions
- [ ] Contributor recognition program
- [ ] GitHub Projects board
- [ ] Community metrics dashboard
- [ ] Plugin submission workflow
- [ ] 5+ community plugins showcased

### v1.0 Preparation
- [ ] Security scan clean (0 critical/high)
- [ ] docs/SECURITY.md complete
- [ ] Performance profiling done
- [ ] Optimizations implemented
- [ ] docs/PERFORMANCE.md complete
- [ ] All documentation polished
- [ ] Launch materials ready
- [ ] PyPI package tested
- [ ] Project website live
- [ ] Onboarding experience smooth
- [ ] Migration guide complete

### Launch
- [ ] Beta testing complete (2+ weeks)
- [ ] Known issues documented
- [ ] Announcement posts ready
- [ ] Demo video published
- [ ] v1.0.0 tagged and released
- [ ] PyPI package published
- [ ] Community notified
- [ ] Support channels ready
```

---

## 🎓 Learning Resources

### For Contributors

```
Recommended reading before Phase 4 contribution:
1. CONTRIBUTING.md - Contribution process
2. docs/PLUGIN_DEVELOPMENT.md - How to build plugins
3. docs/API_REFERENCE.md - Complete API documentation
4. tests/integration/ - Integration test examples
5. .github/copilot-instructions.md - Coding conventions
```

### For Maintainers

```
Phase 4 maintainer checklist:
1. Review PRs using automated tools + manual review
2. Respond to issues within 48 hours
3. Update CONTRIBUTORS.md weekly
4. Post weekly community updates
5. Monitor security scans and address issues ASAP
6. Keep documentation in sync with code
7. Plan and execute v1.0 launch activities
```

---

## 🚨 Troubleshooting

### Common Phase 4 Issues

**Integration tests failing:**
```bash
# Check if plugins registered correctly
pytest tests/integration/test_plugin_interactions.py -v -s

# Verify test environment
python -c "from reaper import PluginManager; pm = PluginManager(); print(pm.list_plugins())"
```

**Performance regression:**
```bash
# Run benchmark comparison
pytest tests/performance/ --benchmark-compare

# Profile specific function
python -m cProfile -s cumulative -m pytest tests/performance/test_throughput.py
```

**Security scan failures:**
```bash
# Get detailed Bandit report
bandit -r reaper/ pipeline/ -f txt -o bandit-report.txt
cat bandit-report.txt

# Check dependency vulnerabilities
safety check --full-report
```

**Documentation build fails:**
```bash
# Check for syntax errors
python -m docutils docs/API_REFERENCE.md

# Rebuild API docs
python scripts/generate_api_docs.py
```

---

## 📞 Getting Help

- **Issues**: https://github.com/SaltProphet/Reaper/issues
- **Discussions**: https://github.com/SaltProphet/Reaper/discussions
- **Security**: See docs/SECURITY.md for vulnerability reporting
- **Contributing**: See CONTRIBUTING.md for contribution guidelines

---

**Ready to ship v1.0? Let's do this! 🚀**
