# REAPER Copilot Prompts - Master Index

**🤖 Copy-Paste Ready Prompts for GitHub Copilot**

This index provides quick access to all phase-specific Copilot prompts for REAPER development. Each prompt is designed to be copy-pasted directly into GitHub Copilot for AI-assisted development.

---

## 📋 Quick Navigation

| Phase | Status | Document | Focus Area |
|-------|--------|----------|------------|
| **Phase 1** | ✅ Complete | [Phase 1 Prompts](PHASE_1_COPILOT_PROMPTS.md) | Core Architecture ("Alpha") |
| **Phase 2** | 🎯 Ready | [Phase 2 Prompts](PHASE_2_COPILOT_PROMPTS.md) | Pipeline Completion ("Beta") |
| **Phase 3** | 📅 Planned | [Phase 3 Prompts](PHASE_3_COPILOT_PROMPTS.md) | Learning & Operator Experience |
| **Phase 4** | 📅 Planned | [Phase 4 Prompts](PHASE_4_COPILOT_PROMPTS.md) | Quality, Automation, Community |

---

## 🎯 Phase 1: Core Architecture (✅ Complete)

**Status**: Complete (v0.1.0)  
**Document**: [PHASE_1_COPILOT_PROMPTS.md](PHASE_1_COPILOT_PROMPTS.md)

### What Was Built
- 5-sense pipeline architecture (Sight, Hearing, Touch, Taste, Smell, Action)
- Pydantic v2 data models (Signal, ScoredSignal, ActionResult)
- Pluggy plugin system with hook specifications
- Comprehensive test suite (136 tests, 96% coverage)
- Developer experience tools (Ruff, pre-commit, CI/CD)
- Documentation and GitHub collaboration tools

### Key Prompts (10 total)
1. Scaffold 5-sense pipeline
2. Define Pydantic models
3. Implement plugin system
4. Create hook specifications
5. Create example runner
6. Write comprehensive tests
7. Setup developer tools
8. Create Copilot instructions
9. Write documentation
10. Setup GitHub collaboration

### Use This Phase For
- Understanding REAPER architecture
- Learning plugin development patterns
- Setting up new projects with similar structure
- Reference for core conventions

---

## 🚀 Phase 2: Pipeline Completion (🎯 Ready to Start)

**Status**: Ready to Start (Target: v0.2.0)  
**Document**: [PHASE_2_COPILOT_PROMPTS.md](PHASE_2_COPILOT_PROMPTS.md)

### What Will Be Built
- Enhanced documentation for all sense modules
- 9+ real-world plugins (Reddit, Discord, RSS, etc.)
- 10+ integration tests (end-to-end pipeline)
- Performance benchmarks
- Community engagement (Discussions, Projects)
- Plugin documentation automation

### Key Milestones (6 total, 26 prompts)
1. **Sense Module Completion** (6 prompts) - Weeks 1-2
2. **Plugin Library Expansion** (9 prompts) - Weeks 3-4
3. **Integration & Testing** (3 prompts) - Week 5
4. **Community & Documentation** (4 prompts) - Week 6
5. **Quality Assurance** (3 prompts) - Week 7
6. **Phase 2 Release** (3 prompts) - Week 8

### Use This Phase For
- Building real-world plugins
- Creating integration tests
- Setting up community infrastructure
- Learning plugin development at scale

---

## 🧠 Phase 3: Learning & Operator Experience (📅 Planned)

**Status**: Planned (Target: v0.3.0)  
**Document**: [PHASE_3_COPILOT_PROMPTS.md](PHASE_3_COPILOT_PROMPTS.md)

### What Will Be Built
- Ouroboros Protocol (self-improving filters)
- Advanced pattern detection (trends, patterns, ROI)
- Operator console (CLI and Web)
- Real-time stream processing
- Alert system
- State management

### Key Sections (6 total, 19 prompts)
1. **Ouroboros Protocol** (3 prompts) - Feedback and learning
2. **Advanced Pattern Detection** (3 prompts) - Trends, patterns, PCI/ROI
3. **Operator Console** (3 prompts) - CLI, web dashboard, alerts
4. **Real-time Processing** (3 prompts) - Streaming, batch, state
5. **Collaboration & Automation** (3 prompts) - Design sessions, PR automation
6. **Advanced Topics** (2 prompts) - Plugin dependencies, marketplace

### Use This Phase For
- Implementing self-learning systems
- Building operator interfaces
- Real-time data processing
- Advanced plugin features

---

## 🎖️ Phase 4: Quality, Automation, Community (📅 Planned)

**Status**: Planned (Target: v1.0.0)  
**Document**: [PHASE_4_COPILOT_PROMPTS.md](PHASE_4_COPILOT_PROMPTS.md)

### What Will Be Built
- 98%+ test coverage (unit, integration, e2e)
- Advanced automation (Spark, Copilot reviews)
- Community growth programs
- Production hardening (security, performance)
- v1.0 release preparation

### Key Sections (6 total, 24 prompts)
1. **Test Harness Expansion** (4 prompts) - Unit, integration, e2e, performance
2. **Plugin API Hardening** (3 prompts) - Versioning, guides, testing framework
3. **Advanced Automation** (4 prompts) - Spark, Copilot, issue triage
4. **Community Growth** (4 prompts) - Updates, marketplace, recognition, templates
5. **Production Readiness** (4 prompts) - Security, performance, deployment, operations
6. **v1.0 Release** (4 prompts) - Checklist, notes, marketing, execution

### Use This Phase For
- Preparing for production
- Building automation pipelines
- Community management
- Major release processes

---

## 📖 How to Use These Prompts

### For GitHub Copilot Chat

1. **Open GitHub Copilot Chat** in your IDE (VS Code, etc.)
2. **Navigate to the relevant phase document**
3. **Copy the entire prompt** (including the markdown code block)
4. **Paste into Copilot Chat** with `@workspace` prefix
5. **Review and execute** the generated code

### Example Workflow

```
Step 1: Choose your task
→ Look at Phase 2, Milestone 1, Prompt 2.1.1

Step 2: Copy the prompt
→ Copy everything in the code block

Step 3: Paste into Copilot
→ Open Copilot Chat
→ Type @workspace and paste the prompt

Step 4: Review the output
→ Copilot generates code, docs, or configuration
→ Review for correctness and conventions

Step 5: Test and iterate
→ Run tests: pytest -v
→ Fix any issues
→ Move to next prompt
```

### Tips for Best Results

✅ **DO:**
- Use `@workspace` prefix for context
- Read the prompt before pasting (understand requirements)
- Review generated code for REAPER conventions
- Run tests immediately after implementation
- Iterate if first attempt isn't perfect

❌ **DON'T:**
- Skip the context sections (Copilot needs context)
- Paste multiple prompts at once (work incrementally)
- Skip testing (verify each step)
- Ignore success criteria (use them as checklist)
- Hard-code values (always use parameters!)

---

## 🔍 Finding the Right Prompt

### By Development Stage

**Just Starting?**
- Use Phase 1 prompts to understand architecture
- Read [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md)
- Run `example_runner.py` to see it work

**Building Plugins?**
- Phase 2, Milestone 2 has 9 plugin examples
- Use [PHASE_2_QUICK_REF.md](PHASE_2_QUICK_REF.md) for templates
- Check `.github/copilot-instructions.md` for conventions

**Adding Advanced Features?**
- Phase 3 has learning, streaming, and console prompts
- Start with Section 1 (Ouroboros Protocol)
- Check Phase 3 prerequisites

**Preparing for Production?**
- Phase 4 has testing, security, and deployment prompts
- Start with Section 1 (Test Harness)
- Follow the v1.0 release checklist

### By Task Type

| Task Type | Relevant Prompts |
|-----------|-----------------|
| **New Plugin** | Phase 2, Milestone 2 (2.2.1 - 2.2.9) |
| **Testing** | Phase 1 (1.6), Phase 2 Milestone 3, Phase 4 Section 1 |
| **Documentation** | Phase 1 (1.9), Phase 2 Milestone 4, Phase 4 Section 2 |
| **Performance** | Phase 2 (2.3.3), Phase 4 (4.5.2) |
| **Security** | Phase 4 (4.5.1) |
| **Automation** | Phase 4 Section 3 |
| **Community** | Phase 2 Milestone 4, Phase 4 Section 4 |

### By Technology

| Technology | Relevant Prompts |
|------------|-----------------|
| **Pydantic** | Phase 1 (1.2) |
| **Pluggy** | Phase 1 (1.3, 1.4) |
| **Pytest** | Phase 1 (1.6), Phase 4 Section 1 |
| **FastAPI** | Phase 3 (3.3.2) |
| **Asyncio** | Phase 3 (3.4.1, 3.4.2) |
| **ML/Learning** | Phase 3 Section 1 |
| **CLI** | Phase 3 (3.3.1) |

---

## 📚 Related Documentation

### Core Documentation
- [README.md](README.md) - Project overview and quick start
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributor guidelines
- [Roadmap](Roadmap) - Full project roadmap
- [.github/copilot-instructions.md](.github/copilot-instructions.md) - Copilot conventions

### Phase Planning
- [PHASE_2_PLAN.md](PHASE_2_PLAN.md) - Detailed Phase 2 roadmap
- [PHASE_2_QUICK_REF.md](PHASE_2_QUICK_REF.md) - Phase 2 quick reference

### API Documentation
- [public_docs/](public_docs/) - User guides and API docs
- [reaper/models.py](reaper/models.py) - Data models
- [reaper/hookspecs.py](reaper/hookspecs.py) - Plugin hooks

---

## ✅ Quality Checklist

Before considering any prompt "complete":

### Code Quality
- [ ] All tests pass: `pytest -v`
- [ ] Coverage adequate: `pytest --cov=reaper --cov=pipeline`
- [ ] Linting clean: `ruff format --check . && ruff check .`
- [ ] Type hints complete
- [ ] Docstrings comprehensive

### REAPER Conventions
- [ ] No hard-coded sources (always use parameters)
- [ ] Correct hook names (reaper_action_execute, not reaper_execute_action)
- [ ] Proper return types (List[Signal], ScoredSignal, ActionResult)
- [ ] @hookimpl decorator present
- [ ] Error handling robust

### Documentation
- [ ] Code documented (docstrings)
- [ ] Examples provided
- [ ] README updated (if needed)
- [ ] Changes documented

### Testing
- [ ] Unit tests written
- [ ] Tests pass locally
- [ ] Edge cases covered
- [ ] Mocks used for external dependencies

---

## 🆘 Getting Help

### Prompt Not Working?
1. Check prerequisites (previous phases complete?)
2. Verify context (is `@workspace` included?)
3. Review success criteria (what's missing?)
4. Check [.github/copilot-instructions.md](.github/copilot-instructions.md)
5. Ask in [Discussions](https://github.com/SaltProphet/Reaper/discussions)

### Need Clarification?
1. Read the detailed phase plan (PHASE_X_PLAN.md)
2. Check examples in `examples/` directory
3. Review stub implementations in `pipeline/`
4. Look at existing tests in `tests/`
5. Ask in Discussions

### Found a Bug?
1. Use [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml)
2. Include: prompt used, expected vs actual, error messages
3. Link to generated code (if applicable)

### Want to Improve Prompts?
1. Submit PR with improvements
2. Follow [CONTRIBUTING.md](CONTRIBUTING.md)
3. Explain why the change helps
4. Include example of improved output

---

## 📊 Progress Tracking

### Phase Completion Status

```
Phase 1: ████████████████████ 100% (✅ Complete - v0.1.0)
Phase 2: ░░░░░░░░░░░░░░░░░░░░   0% (🎯 Ready to Start)
Phase 3: ░░░░░░░░░░░░░░░░░░░░   0% (📅 Planned)
Phase 4: ░░░░░░░░░░░░░░░░░░░░   0% (📅 Planned)
```

### Current Milestone
**Phase 2, Milestone 1**: Sense Module Completion (Weeks 1-2)

### Next Actions
1. Start Phase 2, Prompt 2.1.1 (Enhance Sight Module)
2. Follow Phase 2 timeline in [PHASE_2_PLAN.md](PHASE_2_PLAN.md)
3. Track progress in [GitHub Projects](https://github.com/SaltProphet/Reaper/projects)

---

## 🎉 Success Stories

As phases complete, successful prompts and their outcomes will be documented here to help future developers.

---

**Last Updated**: 2026-02-09  
**Total Prompts**: 79 across 4 phases  
**Maintained By**: REAPER Community

---

**Happy Coding! 🚀**

*Remember: These prompts are designed to guide, not dictate. Use your judgment, follow REAPER conventions, and always test your code!*
