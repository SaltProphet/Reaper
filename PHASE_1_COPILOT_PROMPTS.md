# Phase 1 Copilot Prompts: Core Architecture ("Alpha")

**Status**: ✅ COMPLETE  
**Copy-Paste Ready Prompts for GitHub Copilot**

---

## Overview

Phase 1 establishes the foundational architecture for REAPER. All tasks in this phase are **COMPLETE**, but these prompts are preserved for reference and for understanding the system's design principles.

---

## Prompt 1.1: Scaffold 5-Sense Pipeline

```
@workspace Create the 5-sense pipeline architecture for REAPER.

Context:
- REAPER uses a biological metaphor with 5 senses for signal detection
- Each sense represents a different detection capability
- All senses use the same plugin architecture via Pluggy

Task:
Create stub implementations in the `pipeline/` directory for:
1. sight.py - Visual detection plugin
2. hearing.py - Audio/text detection plugin
3. touch.py - Interaction detection plugin
4. taste.py - Quality/sampling detection plugin
5. smell.py - Pattern/anomaly detection plugin
6. action.py - Action execution plugin
7. scoring.py - Signal scoring plugin

Requirements:
- Each plugin must use @hookimpl decorator from pluggy
- Each plugin must implement the appropriate hook from reaper/hookspecs.py
- Detection plugins return List[Signal]
- Scoring plugin returns ScoredSignal
- Action plugin returns ActionResult
- Never hard-code source parameters
- Include docstrings explaining each sense's purpose

Success Criteria:
- [ ] 7 stub files created in pipeline/ directory
- [ ] Each stub implements correct hook specification
- [ ] All stubs use proper type hints (Pydantic models)
- [ ] Docstrings explain use cases for each sense
- [ ] Tests pass: pytest tests/test_pipeline_stubs.py
```

---

## Prompt 1.2: Define Pydantic Models

```
@workspace Create Pydantic v2 data models for REAPER signals.

Context:
- REAPER needs type-safe data structures for signal flow
- Models must validate data at runtime
- Performance is important (use Pydantic v2, not v1)

Task:
Create models in `reaper/models.py`:
1. SenseType enum (SIGHT, HEARING, TOUCH, TASTE, SMELL, ACTION)
2. Signal model - base signal with validation
3. ScoredSignal model - signal with score (0.0-1.0)
4. ActionResult model - result of action execution

Requirements:
- Use Pydantic v2 (from pydantic import BaseModel)
- Signal must have: sense_type, source, timestamp, raw_data, metadata
- ScoredSignal must have: signal, score, analysis, tags
- ActionResult must have: signal, action_type, success, result_data, error
- Score must be validated to range 0.0-1.0
- Timestamps should auto-generate to UTC
- Include docstrings with field explanations

Success Criteria:
- [ ] All models defined with proper types
- [ ] Score validation enforces 0.0-1.0 range
- [ ] Timestamps auto-generate
- [ ] Tests pass: pytest tests/test_models.py
- [ ] Coverage: 95%+ on reaper/models.py
```

---

## Prompt 1.3: Implement Pluggy Plugin System

```
@workspace Implement the plugin management system using Pluggy.

Context:
- REAPER uses Pluggy for plugin discovery and execution
- Same plugin system used by pytest
- Supports multiple plugins implementing same hook

Task:
Create `reaper/plugin_manager.py` with:
1. PluginManager class
2. Plugin registration methods
3. Hook execution methods for each sense
4. Plugin listing and counting utilities

Requirements:
- Use pluggy.PluginManager with namespace "reaper"
- Provide methods: register_plugin, unregister_plugin, list_plugins, plugin_count
- Provide detection methods: detect_sight, detect_hearing, detect_touch, detect_taste, detect_smell
- Provide score_signal method
- Provide execute_action method
- All hook calls must pass through proper parameters
- Handle multiple plugins implementing same hook

Success Criteria:
- [ ] PluginManager class functional
- [ ] All detection methods work
- [ ] Scoring and action methods work
- [ ] Tests pass: pytest tests/test_plugin_manager.py
- [ ] Coverage: 95%+ on reaper/plugin_manager.py
```

---

## Prompt 1.4: Create Hook Specifications

```
@workspace Define Pluggy hook specifications for REAPER plugins.

Context:
- Hook specifications define the contract for plugins
- Each hook has specific signature and return type
- Plugins implement these hooks to add functionality

Task:
Create `reaper/hookspecs.py` with HookSpecs class containing:
1. reaper_sight_detect(source: str) -> List[Signal]
2. reaper_hearing_detect(source: str) -> List[Signal]
3. reaper_touch_detect(source: str) -> List[Signal]
4. reaper_taste_detect(source: str) -> List[Signal]
5. reaper_smell_detect(source: str) -> List[Signal]
6. reaper_score_signal(signal: Signal) -> ScoredSignal
7. reaper_action_execute(scored_signal: ScoredSignal) -> ActionResult

Requirements:
- Use @hookspec decorator from pluggy
- Include complete type hints
- Include docstrings explaining each hook
- Mark hooks as firstresult=False (allow multiple implementations)
- Note: reaper_action_execute NOT reaper_execute_action (common mistake)

Success Criteria:
- [ ] All 7 hooks defined
- [ ] Type hints match model definitions
- [ ] Docstrings explain parameters and return values
- [ ] Tests validate hook signatures: pytest tests/test_hookspecs.py
```

---

## Prompt 1.5: Create Example Runner

```
@workspace Create an example demonstrating the complete REAPER pipeline.

Context:
- Need working example showing all components together
- Should demonstrate detection → scoring → action flow
- Must be runnable by new contributors

Task:
Create `example_runner.py` that:
1. Imports PluginManager and all stub plugins
2. Registers all plugins
3. Detects signals from each sense
4. Scores detected signals
5. Executes actions on high-score signals
6. Prints results to console

Requirements:
- Use all 5 sense plugins + scoring + action
- Show source parameter usage (never hard-coded)
- Include inline comments explaining each step
- Print clear output showing pipeline flow
- Handle errors gracefully
- Make it educational for new users

Success Criteria:
- [ ] File runs without errors: python example_runner.py
- [ ] Output shows all pipeline stages
- [ ] Inline comments explain architecture
- [ ] Demonstrates proper plugin usage
- [ ] Can be used as template for real implementations
```

---

## Prompt 1.6: Write Comprehensive Tests

```
@workspace Create comprehensive test suite for REAPER core components.

Context:
- Need 95%+ test coverage for production readiness
- Tests must cover happy paths and edge cases
- Use pytest for all testing

Task:
Create test files in `tests/` directory:
1. test_models.py - Pydantic model validation tests
2. test_plugin_manager.py - Plugin registration and execution tests
3. test_pipeline_stubs.py - Stub plugin implementation tests
4. test_hookspecs.py - Hook specification validation tests
5. test_edge_cases.py - Edge case and error handling tests
6. test_parametrized.py - Parametrized tests for variations

Requirements:
- Use pytest fixtures for test setup
- Test validation errors (invalid scores, missing fields)
- Test plugin registration/unregistration
- Test multiple plugins on same hook
- Test error handling in plugins
- Use parametrize for testing variations
- Aim for 95%+ coverage

Success Criteria:
- [ ] All tests pass: pytest -v
- [ ] Coverage reaches 95%+: pytest --cov=reaper --cov=pipeline
- [ ] Edge cases covered
- [ ] Parametrized tests for variations
- [ ] No flaky tests
```

---

## Prompt 1.7: Setup Developer Experience Tools

```
@workspace Configure developer experience tools for REAPER.

Context:
- Need consistent code quality across contributors
- Automate formatting and linting
- Make contribution process smooth

Task:
Configure these files:
1. pyproject.toml - Project metadata, dependencies, Ruff config
2. .pre-commit-config.yaml - Pre-commit hooks
3. .github/workflows/ci.yml - CI/CD pipeline
4. .gitignore - Ignore build artifacts and dependencies

Requirements:
Ruff Configuration:
- Line length: 100
- Target: Python 3.11+
- Rules: E, F, I, N, W
- Per-file ignore: reaper/hookspecs.py:N805

Pre-commit Hooks:
- Ruff format (on commit)
- Ruff check (on commit)
- Pytest (on push)

CI/CD:
- Test on Python 3.11 and 3.12
- Run Ruff formatting check
- Run Ruff linting
- Run pytest with coverage
- Fail on coverage < 95%

Success Criteria:
- [ ] Ruff configured and working: ruff format . && ruff check .
- [ ] Pre-commit hooks installed: pre-commit install
- [ ] CI pipeline functional (check GitHub Actions)
- [ ] All checks pass locally
```

---

## Prompt 1.8: Create Copilot Instructions

```
@workspace Create comprehensive Copilot instructions for REAPER development.

Context:
- GitHub Copilot needs context about project conventions
- Instructions guide code generation alignment
- Critical for maintaining consistency

Task:
Create `.github/copilot-instructions.md` with:
1. Project philosophy and core principles
2. Correct hook names (with warnings about common mistakes)
3. Code conventions and import patterns
4. Plugin development guidelines
5. Data validation rules (Pydantic models)
6. Testing guidelines
7. Common errors to avoid (with examples)
8. Quick reference card

Requirements:
- Emphasize: NEVER hard-code sources
- Emphasize: Correct hook names (reaper_action_execute NOT reaper_execute_action)
- Include working code examples
- Reference actual files in the codebase
- Provide troubleshooting guidance
- Keep updated as patterns emerge

Success Criteria:
- [ ] File covers all key conventions
- [ ] Examples use actual codebase patterns
- [ ] Common mistakes documented with fixes
- [ ] Hook name warnings prominent
- [ ] Quick reference card for rapid lookup
```

---

## Prompt 1.9: Write Documentation

```
@workspace Create comprehensive documentation for REAPER.

Context:
- New users need clear getting-started guide
- Contributors need contribution guidelines
- Documentation must cover all aspects

Task:
Create/update these files:
1. README.md - Project overview, installation, quick start
2. CONTRIBUTING.md - Contributor guidelines, workflow, standards
3. Roadmap - Development phases and timeline
4. LICENSE - MIT license
5. public_docs/ - Detailed guides

Requirements:
README.md:
- Project description and badges
- Architecture overview (5-sense pipeline)
- Installation instructions
- Quick start example
- Testing instructions
- Project structure
- Contributing section

CONTRIBUTING.md:
- Development setup
- Code quality requirements (Ruff, pytest)
- PR process and templates
- Testing guidelines
- Issue templates

Success Criteria:
- [ ] README complete with working examples
- [ ] CONTRIBUTING covers full workflow
- [ ] All documentation accurate and tested
- [ ] Links work and point to correct files
- [ ] Examples can be copy-pasted and run
```

---

## Prompt 1.10: Setup GitHub Collaboration Tools

```
@workspace Configure GitHub collaboration features for REAPER.

Context:
- Need templates for consistent issue/PR format
- Codespaces for instant contributor onboarding
- Automation for code quality

Task:
Create GitHub configurations:
1. .github/ISSUE_TEMPLATE/ - Bug report, feature request, plugin submission
2. .github/pull_request_template.md - PR template
3. .devcontainer/devcontainer.json - Codespaces configuration
4. .github/workflows/ - CI/CD workflows
5. .github/CODEOWNERS - Code ownership

Requirements:
Issue Templates:
- Bug report with steps to reproduce
- Feature request with use cases
- Plugin submission template

PR Template:
- Description, type of change, testing checklist
- Compliance checklist (no hard-coding, proper types, etc.)

Codespaces:
- Python 3.11+ pre-installed
- Dependencies auto-installed
- Pre-commit hooks configured
- Extensions: Python, Pylance, Ruff

Success Criteria:
- [ ] Issue templates functional on GitHub
- [ ] PR template appears on new PRs
- [ ] Codespaces launches in < 2 minutes
- [ ] All tools pre-configured in Codespaces
```

---

## Phase 1 Verification Checklist

Before moving to Phase 2, verify:

- [ ] All tests pass: `pytest -v`
- [ ] Coverage at 95%+: `pytest --cov=reaper --cov=pipeline`
- [ ] Linting passes: `ruff format --check . && ruff check .`
- [ ] Example runs: `python example_runner.py`
- [ ] Documentation complete and accurate
- [ ] GitHub tools configured (issues, PRs, Codespaces)
- [ ] CI/CD pipeline functional
- [ ] Copilot instructions comprehensive

---

## Notes for AI Coders

**Critical Reminders:**
1. Hook name is `reaper_action_execute` NOT `reaper_execute_action`
2. Never hard-code source parameters - always use function parameter
3. Scores must be 0.0-1.0 range (validated by Pydantic)
4. Always use @hookimpl decorator for plugin methods
5. Return types must match hookspecs: List[Signal], ScoredSignal, ActionResult

**Testing:**
- Run tests after each change: `pytest -v`
- Check coverage: `pytest --cov=reaper --cov=pipeline`
- Run example: `python example_runner.py`

**Formatting:**
- Auto-format: `ruff format .`
- Auto-fix linting: `ruff check --fix .`

---

**Related Documents:**
- [Roadmap](Roadmap) - Full project timeline
- [README.md](README.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributor guide
- [.github/copilot-instructions.md](.github/copilot-instructions.md) - Detailed conventions
