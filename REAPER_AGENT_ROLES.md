# REAPER Agent Roles

This document defines specialized agent roles for developing and maintaining REAPER. Each role represents a focused area of expertise and responsibility. Teams can assign roles based on project phase and needs, while solo contributors can adopt multiple roles sequentially.

## Table of Contents

- [Overview](#overview)
- [Role Definitions](#role-definitions)
  - [Plugin Architect](#plugin-architect)
  - [Plugin Implementer](#plugin-implementer)
  - [Data Model Guardian](#data-model-guardian)
  - [Quality Guardian](#quality-guardian)
  - [Documentation Engineer](#documentation-engineer)
  - [Operator Experience Designer](#operator-experience-designer)
- [Role Assignment Guidelines](#role-assignment-guidelines)
- [Cross-Role Collaboration](#cross-role-collaboration)

## Overview

REAPER's plugin-driven architecture requires clear separation of concerns. These roles ensure each aspect of the system receives focused attention while maintaining coherent integration.

**Key Principles:**
- ✅ Each role has clear boundaries and deliverables
- ✅ Roles work together via defined interfaces (APIs, models, specs)
- ✅ Plugin-first: No hard-coding, all functionality via plugins
- ✅ Type-safe: Pydantic models enforce data contracts
- ✅ Testable: Each role produces verifiable outputs

## Role Definitions

### Plugin Architect

**Mission**: Design and maintain the plugin ecosystem architecture, ensuring scalability, hot-swappability, and separation of concerns.

#### Detailed Responsibilities

1. **Define Plugin Interfaces**
   - Design hookspecs for new sense types or pipeline stages
   - Ensure backward compatibility in hook signatures
   - Document plugin contracts and guarantees

2. **Maintain Architecture Integrity**
   - Review PRs for architectural compliance
   - Prevent hard-coding and role mixing
   - Enforce separation between core and plugins

3. **Guide Plugin Developers**
   - Create plugin design patterns and anti-patterns
   - Provide architecture feedback on plugin proposals
   - Maintain plugin ecosystem roadmap

4. **Versioning and Compatibility**
   - Define plugin API versioning strategy
   - Plan deprecation and migration paths
   - Ensure smooth upgrades for plugin authors

#### Tools and Skills

**Required:**
- Expert knowledge of plugin architectures (Pluggy, setuptools entry points)
- Deep understanding of Python type systems
- Experience with API design and versioning
- Familiarity with REAPER core (`reaper/models.py`, `reaper/hookspecs.py`, `reaper/plugin_manager.py`)

**Recommended:**
- Experience with other plugin systems (Jenkins, Pytest, Airflow)
- Knowledge of distributed systems patterns
- Understanding of dependency injection

#### Sample Workflow

```
1. Review new sense type proposal
   ↓
2. Design hookspec with proper typing
   ↓
3. Create reference implementation stub
   ↓
4. Document in hookspecs.py with examples
   ↓
5. Update PluginManager with new methods
   ↓
6. Add integration tests
   ↓
7. Update architecture documentation
```

#### Day in the Life

**Morning**: Review 3 PRs proposing new plugins. One mixes detection and scoring logic - provide feedback on separating concerns. Another hard-codes a source URL - guide toward parameter-based approach.

**Mid-day**: Design hookspec for new "Intuition" sense type requested for Phase 3. Define signature, return types, and document example use cases. Create stub implementation.

**Afternoon**: Pair with Plugin Implementer on complex Reddit API plugin. Discuss whether pagination belongs in the plugin or should be a separate concern. Document decision in architecture notes.

**Evening**: Update plugin versioning strategy document. Plan for v2 hookspec that adds optional context parameter without breaking existing plugins.

#### Deliverables

- [ ] Updated `reaper/hookspecs.py` with new hook specifications
- [ ] Architecture decision records (ADRs) for significant changes
- [ ] Plugin design patterns documentation
- [ ] Compatibility and versioning guidelines
- [ ] Reference implementations for new sense types

---

### Plugin Implementer

**Mission**: Build, test, and maintain concrete plugin implementations that solve real-world signal detection, scoring, and action needs.

#### Detailed Responsibilities

1. **Implement Real-World Plugins**
   - Build plugins for external APIs (Reddit, Discord, GitHub, etc.)
   - Create analyzer plugins for scoring signals
   - Develop action plugins for notifications and integrations

2. **Follow Plugin Standards**
   - Use `@hookimpl` decorator correctly
   - Never hard-code sources - always use parameters
   - Return properly validated Pydantic models
   - Include comprehensive docstrings

3. **Handle External Dependencies**
   - Manage API credentials via environment variables
   - Implement proper error handling and retries
   - Handle rate limiting gracefully
   - Mock external services in tests

4. **Optimize Performance**
   - Use `Signal.create_batch()` for bulk operations
   - Implement caching where appropriate
   - Profile and optimize bottlenecks
   - Document performance characteristics

#### Tools and Skills

**Required:**
- Proficiency in Python 3.11+
- Experience with REST APIs and authentication
- Understanding of async/await patterns
- Knowledge of Pydantic validation
- Familiarity with pytest and mocking

**Recommended:**
- Experience with specific APIs (Reddit, Discord, GitHub, Slack)
- Understanding of rate limiting and backoff strategies
- Knowledge of caching strategies (Redis, in-memory)
- Experience with performance profiling

#### Sample Workflow

```
1. Review plugin requirements from Issue/Discussion
   ↓
2. Set up development environment with API credentials
   ↓
3. Implement plugin following template
   ↓
4. Add unit tests with mocked API responses
   ↓
5. Add integration tests (optional, gated on env var)
   ↓
6. Document API setup in plugin README
   ↓
7. Submit PR with plugin checklist
```

#### Day in the Life

**Morning**: Implement RedditIngestor plugin that detects signals from specified subreddits. Set up PRAW library, configure OAuth, implement `reaper_sight_detect` hook. Use environment variables for credentials.

**Mid-day**: Write 15 unit tests for RedditIngestor. Mock PRAW API responses. Test error conditions (rate limit, network error, invalid credentials). Achieve 98% coverage.

**Afternoon**: Debug DiscordNotifier action plugin that's failing in CI. Issue is hard-coded webhook URL. Refactor to accept webhook as parameter. Update tests and documentation.

**Evening**: Optimize GitHubIssueScorer plugin. Replace individual Signal creation with `create_batch()`. Benchmark shows 35% speedup. Document performance improvements in PR.

#### Deliverables

- [ ] Working plugin implementation with proper hookimpl
- [ ] Unit tests with >95% coverage
- [ ] Plugin-specific README with setup instructions
- [ ] Environment variable documentation
- [ ] Example usage in plugin docstring
- [ ] PR passing all CI checks

---

### Data Model Guardian

**Mission**: Maintain data integrity across the pipeline through rigorous Pydantic model design and validation.

#### Detailed Responsibilities

1. **Design Data Models**
   - Create Pydantic models for new data types
   - Define field constraints and validators
   - Document model relationships and usage

2. **Maintain Model Quality**
   - Review PRs for proper model usage
   - Ensure validation is comprehensive
   - Prevent model drift and inconsistency

3. **Handle Model Evolution**
   - Design backward-compatible model changes
   - Create migration strategies for breaking changes
   - Version models when necessary

4. **Optimize Model Performance**
   - Profile model validation overhead
   - Use appropriate field types (str vs Enum, etc.)
   - Implement efficient batch operations

#### Tools and Skills

**Required:**
- Expert knowledge of Pydantic v2
- Understanding of Python type hints and validation
- Experience with data modeling and schemas
- Knowledge of JSON serialization

**Recommended:**
- Experience with schema evolution patterns
- Understanding of performance profiling
- Knowledge of alternative validation libraries
- Familiarity with OpenAPI/JSON Schema

#### Sample Workflow

```
1. Review request for new data type
   ↓
2. Design Pydantic model with proper fields
   ↓
3. Add field validators and constraints
   ↓
4. Create comprehensive validation tests
   ↓
5. Document model in docstring with examples
   ↓
6. Update related models for consistency
   ↓
7. Add to reaper/__init__.py exports
```

#### Day in the Life

**Morning**: Design new `EnrichedSignal` model for Phase 3. Add fields for historical context, related signals, and metadata aggregation. Define proper types and defaults. Write 20 validation tests.

**Mid-day**: Review PR adding custom validator to ScoredSignal. Validator ensures tags are lowercase. Suggest using Field(pre=True) for automatic normalization. Update tests.

**Afternoon**: Investigate performance issue in Signal creation. Profile shows datetime overhead. Implement and document `create_batch()` method. Benchmark shows 40% speedup for bulk operations.

**Evening**: Plan migration strategy for breaking change to Signal.source field (changing from str to SourceIdentifier model). Write migration guide. Create backward-compatible shim for v1 plugins.

#### Deliverables

- [ ] Well-documented Pydantic models in `reaper/models.py`
- [ ] Comprehensive validation tests
- [ ] Model usage examples in docstrings
- [ ] Performance benchmarks for model operations
- [ ] Migration guides for breaking changes
- [ ] Updated type stubs and exports

---

### Quality Guardian

**Mission**: Ensure code quality, security, and maintainability through comprehensive testing, linting, and security scanning.

#### Detailed Responsibilities

1. **Maintain Test Infrastructure**
   - Ensure >95% code coverage
   - Create test utilities and fixtures
   - Maintain CI/CD pipeline
   - Optimize test execution time

2. **Enforce Code Standards**
   - Configure and maintain Ruff linting
   - Enforce formatting standards
   - Review code for best practices
   - Maintain pre-commit hooks

3. **Security Scanning**
   - Configure and monitor CodeQL
   - Review security alerts
   - Ensure no secrets in code
   - Validate dependency security

4. **Review Code Quality**
   - Review PRs for code smell
   - Identify technical debt
   - Suggest refactoring opportunities
   - Maintain quality metrics

#### Tools and Skills

**Required:**
- Expert knowledge of pytest
- Experience with coverage tools
- Understanding of linting (Ruff, flake8, mypy)
- Security scanning knowledge (CodeQL, Bandit)
- CI/CD experience (GitHub Actions)

**Recommended:**
- Experience with mutation testing
- Knowledge of performance profiling
- Understanding of static analysis
- Familiarity with security best practices

#### Sample Workflow

```
1. Review PR for quality issues
   ↓
2. Run tests with coverage report
   ↓
3. Check linting and formatting
   ↓
4. Review security scanning results
   ↓
5. Provide actionable feedback
   ↓
6. Verify fixes before approval
   ↓
7. Update quality documentation
```

#### Day in the Life

**Morning**: Review 5 PRs. One has 87% coverage - identify missing edge case tests. Another has unused imports - run `ruff check --fix`. Third has hardcoded API key - flag security issue immediately.

**Mid-day**: Investigate flaky test in test_plugin_manager.py. Race condition in plugin registration order. Add explicit ordering or make test order-independent. Fix verified.

**Afternoon**: Configure new CodeQL query for detecting hard-coded sources (forbidden practice). Test on codebase, finds 2 instances in old code. Create issues to refactor.

**Evening**: Optimize CI pipeline. Tests taking 8 minutes. Parallelize test execution, add caching for dependencies. Runtime down to 3 minutes. Document optimization in CI docs.

#### Deliverables

- [ ] Comprehensive test suite with >95% coverage
- [ ] Updated linting and formatting configuration
- [ ] Security scanning reports with zero high-severity issues
- [ ] Code quality metrics and trends
- [ ] CI/CD improvements and optimizations
- [ ] Quality checklist updates

---

### Documentation Engineer

**Mission**: Create and maintain clear, comprehensive documentation that enables contributors and operators to succeed.

#### Detailed Responsibilities

1. **Write User Documentation**
   - Create getting started guides
   - Document installation and setup
   - Write troubleshooting guides
   - Provide usage examples

2. **Write Developer Documentation**
   - Document plugin development process
   - Create API references
   - Write architecture guides
   - Provide code examples

3. **Maintain Documentation Quality**
   - Review PRs for documentation changes
   - Ensure consistency across docs
   - Keep documentation in sync with code
   - Test all documented examples

4. **Organize Documentation**
   - Maintain documentation structure
   - Create navigation and indexes
   - Improve discoverability
   - Archive outdated content

#### Tools and Skills

**Required:**
- Excellent technical writing skills
- Understanding of documentation as code
- Markdown proficiency
- Experience with documentation generators
- Ability to explain complex concepts simply

**Recommended:**
- Experience with MkDocs, Sphinx, or similar
- Knowledge of documentation testing tools
- Understanding of SEO for documentation
- Familiarity with diagramming tools (Mermaid, etc.)

#### Sample Workflow

```
1. Identify documentation gap or update need
   ↓
2. Outline structure and key points
   ↓
3. Write initial draft with examples
   ↓
4. Test all code examples
   ↓
5. Review for clarity and completeness
   ↓
6. Add to appropriate location in docs/
   ↓
7. Update indexes and cross-references
```

#### Day in the Life

**Morning**: Update CONTRIBUTING.md with new role assignment guidelines from this document. Add examples for solo vs team workflows. Create cross-references to REAPER_AGENT_ROLES.md.

**Mid-day**: Write plugin development tutorial. Cover detection, scoring, and action plugins. Include complete working examples. Test examples in clean environment to ensure accuracy.

**Afternoon**: Review 3 plugin submission PRs. One has missing README - provide template and examples. Another has unclear setup instructions - suggest improvements with specific examples.

**Evening**: Reorganize docs/ directory structure. Move planning docs to docs/planning/, guides to docs/guides/. Update all cross-references. Create docs/README.md navigation guide.

#### Deliverables

- [ ] Updated README with clear onboarding
- [ ] Comprehensive guides in docs/guides/
- [ ] API reference documentation
- [ ] Plugin development tutorials
- [ ] Troubleshooting documentation
- [ ] Documentation structure and navigation
- [ ] All code examples tested and working

---

### Operator Experience Designer

**Mission**: Design and improve the operator-facing tools, CLI, and workflows that make REAPER practical and delightful to use.

#### Detailed Responsibilities

1. **Design Operator Workflows**
   - Create intuitive CLI commands
   - Design configuration workflows
   - Plan onboarding experience
   - Optimize common tasks

2. **Build Operator Tools**
   - Implement CLI using Click or Typer
   - Create interactive wizards
   - Build configuration validators
   - Develop diagnostic tools

3. **Improve Usability**
   - Gather operator feedback
   - Identify pain points
   - Design improvements
   - Test with real operators

4. **Documentation for Operators**
   - Write operator guides
   - Create video tutorials
   - Document common scenarios
   - Provide troubleshooting help

#### Tools and Skills

**Required:**
- UX design principles
- CLI design experience (Click, Typer, argparse)
- Understanding of operator workflows
- Empathy for user needs

**Recommended:**
- Experience with TUIs (Rich, Textual)
- Knowledge of configuration management
- Understanding of monitoring and observability
- Familiarity with devops tools

#### Sample Workflow

```
1. Identify operator pain point
   ↓
2. Design improved workflow
   ↓
3. Create mockups or sketches
   ↓
4. Implement CLI command or tool
   ↓
5. Write operator documentation
   ↓
6. Test with real operators
   ↓
7. Iterate based on feedback
```

#### Day in the Life

**Morning**: Design `reaper init` command for project setup. Should create config file, detect available plugins, test connections. Sketch out interactive prompts and validation.

**Mid-day**: Implement onboarding wizard using Rich library. Beautiful terminal UI with progress indicators. Validates API credentials as user enters them. Provides helpful error messages.

**Afternoon**: Review operator feedback on configuration. Common complaint: unclear error when source parameter wrong. Add validation that suggests correct format. Test with 5 common mistakes.

**Evening**: Create video tutorial showing end-to-end setup. Record terminal session with asciinema. Add to docs with written transcript for accessibility.

#### Deliverables

- [ ] Intuitive CLI commands with --help text
- [ ] Interactive configuration wizards
- [ ] Operator-focused documentation
- [ ] Diagnostic and validation tools
- [ ] Video tutorials and screencasts
- [ ] Operator feedback incorporated

---

## Role Assignment Guidelines

### For Solo Contributors

**Recommended Sequence:**

1. **Phase 1: Foundation**
   - Start as **Data Model Guardian** - understand the data structures
   - Then **Plugin Architect** - understand the plugin system
   - Then **Plugin Implementer** - build your first plugin
   - Use **Quality Guardian** mindset throughout

2. **Phase 2: Expansion**
   - Primarily **Plugin Implementer** - create real plugins
   - Occasional **Data Model Guardian** - evolve models as needed
   - Regular **Quality Guardian** - maintain test coverage
   - Regular **Documentation Engineer** - document your plugins

3. **Phase 3: Maturity**
   - Add **Operator Experience Designer** - make it usable
   - Maintain **Quality Guardian** - keep quality high
   - Continue **Documentation Engineer** - comprehensive docs

**Time Allocation Example** (per week):
- 50% Plugin Implementer (building features)
- 20% Quality Guardian (testing, reviewing)
- 15% Documentation Engineer (writing docs)
- 10% Data Model Guardian (evolving models)
- 5% Plugin Architect (planning architecture)

### For Small Teams (2-3 people)

**Recommended Split:**

**Person 1: Architecture & Quality Lead**
- Primary: Plugin Architect (60%)
- Secondary: Quality Guardian (30%)
- Tertiary: Data Model Guardian (10%)

**Person 2: Implementation Lead**
- Primary: Plugin Implementer (70%)
- Secondary: Data Model Guardian (20%)
- Tertiary: Documentation Engineer (10%)

**Person 3: Experience & Documentation Lead**
- Primary: Operator Experience Designer (50%)
- Secondary: Documentation Engineer (40%)
- Tertiary: Quality Guardian (10%)

### For Larger Teams (4+ people)

**Recommended Structure:**

- **1 Plugin Architect** (full-time, senior)
- **2-3 Plugin Implementers** (full-time, mix of experience levels)
- **1 Data Model Guardian** (can be part-time or shared)
- **1 Quality Guardian** (full-time, can rotate among team)
- **1 Documentation Engineer** (can be part-time or shared)
- **1 Operator Experience Designer** (grows in importance over time)

**Team Meeting Cadence:**
- Daily standup (15 min)
- Weekly architecture review (Plugin Architect + senior devs)
- Bi-weekly quality review (Quality Guardian + team)
- Monthly documentation review (Documentation Engineer + stakeholders)

## Cross-Role Collaboration

### Plugin Architect ↔ Plugin Implementer

**Collaboration Points:**
- Review plugin proposals before implementation
- Pair on complex plugins requiring new patterns
- Architect reviews implementation for compliance

**Deliverables:**
- Architecture Decision Records (ADRs)
- Plugin design reviews
- Compliance checklists

### Data Model Guardian ↔ Plugin Implementer

**Collaboration Points:**
- Design models for new plugin data types
- Review model usage in plugin code
- Optimize model performance together

**Deliverables:**
- Model evolution proposals
- Validation test suites
- Performance benchmarks

### Quality Guardian ↔ All Roles

**Collaboration Points:**
- Review all PRs for quality
- Provide testing guidance
- Maintain CI/CD pipeline

**Deliverables:**
- Quality metrics dashboard
- PR review checklists
- CI/CD improvements

### Documentation Engineer ↔ All Roles

**Collaboration Points:**
- Document architectural decisions
- Write guides for new features
- Capture tribal knowledge

**Deliverables:**
- Up-to-date documentation
- Tutorial content
- API references

### Operator Experience Designer ↔ Plugin Implementer

**Collaboration Points:**
- Design operator-facing APIs
- Create intuitive configuration
- Build diagnostic tools

**Deliverables:**
- CLI commands
- Configuration wizards
- Operator guides

---

## Evolving These Roles

These roles are not fixed. As REAPER grows:

1. **Add New Roles**: Create specialized roles for new needs (Security Engineer, Performance Engineer, etc.)
2. **Refine Existing Roles**: Update responsibilities as patterns emerge
3. **Merge or Split Roles**: Adjust based on team size and phase
4. **Document Changes**: Keep this file updated with learnings

**To propose role changes:**
1. Open a Discussion in the "Process & Organization" category
2. Describe the need and proposed changes
3. Gather feedback from team/community
4. Update this document via PR
5. Announce changes in team meetings and release notes

---

## Resources

- [Contributing Guide](CONTRIBUTING.md) - How to contribute to REAPER
- [Code Quality Guide](CODE_QUALITY.md) - Quality standards and practices
- [Documentation Guidelines](docs/README_GUIDELINES.md) - How to write docs
- [Plugin Template](templates/plugin_template.py) - Plugin scaffold
- [Plugin README Template](templates/PLUGIN_README_TEMPLATE.md) - Plugin docs template

---

**Questions about roles?** Ask in [GitHub Discussions - Q&A](https://github.com/SaltProphet/Reaper/discussions/categories/q-and-a)
