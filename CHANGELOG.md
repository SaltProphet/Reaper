# Changelog

All notable changes to REAPER will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive repository analysis and recommendations document
- Dependabot configuration for automated dependency updates
- Security policy (SECURITY.md) for vulnerability reporting
- CodeQL security scanning workflow
- Enhanced module exports with __all__ declarations

### Changed
- Improved Copilot instructions with cross-references

## [0.1.0] - 2026-02-09

### Added
- Initial release of REAPER with 5-sense pipeline architecture
- Plugin-driven system using Pluggy framework
- Type-safe data models using Pydantic v2
- Core models: Signal, ScoredSignal, ActionResult, SenseType
- Plugin Manager with full lifecycle support
- Reference implementations for all 5 senses:
  - Sight (visual detection)
  - Hearing (audio/text detection)
  - Touch (interaction detection)
  - Taste (quality/sampling detection)
  - Smell (pattern/anomaly detection)
- Scoring plugin for signal prioritization
- Action plugin for signal response
- 136 comprehensive tests achieving 96% code coverage
- Parametrized tests for efficiency
- Edge case coverage tests
- End-to-end pipeline tests
- Complete documentation suite:
  - README with quick start guide
  - CONTRIBUTING guide for developers
  - Plugin development guide
  - Troubleshooting section
  - Phase planning documents (Phases 1-4)
  - Copilot-ready prompts (79 prompts total)
  - Roadmap with timeline
- CI/CD pipeline:
  - Quality gate enforcement
  - Auto-fix PR workflow
  - Plugin validation
  - Changelog automation
  - Python 3.11 and 3.12 support
- Pre-commit hooks for code quality
- Ruff linting and formatting configuration
- Example runner demonstrating full pipeline

### Documentation
- README.md with badges and comprehensive examples
- QUICKSTART.md for new users
- ROADMAP.md with 4-phase development plan
- docs/ directory organization:
  - planning/ (phase docs, Copilot prompts)
  - guides/ (CONTRIBUTING, advanced tools)
  - archive/ (checkpoints, summaries)
  - performance/ (performance analysis)
- .github/ guides:
  - Projects guide
  - Spaces guide
  - Spark automation guide
  - Branch protection guide
- Copilot instructions (technical + agent roles)

### Infrastructure
- GitHub Actions workflows (CI, quality gate, plugin check, auto-fix, changelog)
- CODEOWNERS file for maintainer assignments
- Issue and PR templates
- Discussion templates
- Dev container configuration

### Performance
- Batch signal creation (30-40% faster than individual creation)
- Efficient plugin detection with itertools
- Minimal memory footprint with only 2 runtime dependencies

### Security
- Explicit GitHub Actions permissions (principle of least privilege)
- No hard-coded secrets or credentials
- Type-safe validation throughout
- Plugin isolation via Pluggy

## Links

[Unreleased]: https://github.com/SaltProphet/Reaper/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/SaltProphet/Reaper/releases/tag/v0.1.0
