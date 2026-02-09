# GitHub Projects Guide for REAPER

This guide explains how to use GitHub Projects to track REAPER's development across the roadmap phases.

## Project Setup

### Creating a Project Board

1. Navigate to the repository's "Projects" tab
2. Create a new project using the "Board" template
3. Name it according to the roadmap phase (e.g., "Phase 1: Core Architecture")

### Recommended Views

#### Phase Board
- **Columns**: Backlog, In Progress, In Review, Done
- **Fields**: Priority, Component, Roadmap Phase, Assignee
- **Filters**: Group by Component or Priority

#### Timeline View
- Track milestones against the roadmap schedule
- Visualize dependencies between tasks
- Plan sprint cycles aligned with phases

## Workflow Integration

### Linking Issues to Projects

Automatically add issues to projects using labels:
- `phase-1`: Phase 1 - Core Architecture
- `phase-2`: Phase 2 - Pipeline Completion
- `phase-3`: Phase 3 - Learning & Operator Experience
- `phase-4`: Phase 4 - Quality, Automation, Community

### Automation Rules

Set up project automation:
1. **New issues** → Move to "Backlog"
2. **PR opened** → Move to "In Progress"
3. **PR merged** → Move to "Done"
4. **Issue closed** → Move to "Done"

## Roadmap Phase Projects

### Phase 1: Core Architecture (Alpha)
Focus areas:
- 5-sense pipeline scaffolding
- Pluggy-based plugin loader
- First example plugins
- Core documentation

### Phase 2: Pipeline Completion (Beta)
Focus areas:
- Complete all sense stubs
- End-to-end pipeline testing
- Plugin library expansion
- Contributor onboarding

### Phase 3: Learning & Operator Experience
Focus areas:
- Ouroboros Protocol implementation
- Pattern detection and scoring
- Operator console (CLI/web UI)
- Real-time and batch signal handling

### Phase 4: Quality, Automation, Community
Focus areas:
- Test harness expansion
- Plugin API hardening
- Spark automation integration
- Community building and v1.0 launch

## Project Fields

### Custom Fields

**Priority**
- 🔴 Critical
- 🟠 High
- 🟡 Medium
- 🟢 Low

**Component**
- Core
- Pipeline
- Plugins
- Tests
- Documentation
- CI/CD

**Status**
- 📋 Backlog
- 🏃 In Progress
- 👀 In Review
- ✅ Done
- 🚫 Blocked

**Roadmap Phase**
- Phase 1
- Phase 2
- Phase 3
- Phase 4

## Best Practices

### For Maintainers
- Review and triage new issues weekly
- Update project boards during milestone planning
- Close completed items promptly
- Use milestones to track phase completion

### For Contributors
- Check the active phase project before starting work
- Link your PRs to relevant issues
- Update issue status when you start working
- Comment on blocked items to request help

### For Copilot
- Reference project boards when prioritizing work
- Suggest issues from active phases first
- Note dependencies in project tracking
- Update Roadmap when phases complete

## Integration with Other Tools

### Discussions
Link project milestones to discussion threads for community input on upcoming features.

### Actions (Spark)
Use GitHub Actions to:
- Auto-label issues based on content
- Update project cards when PRs merge
- Generate release notes from completed project items

### Codespaces
Launch Codespaces directly from project items to start development quickly.

## Templates

### Milestone Template
```
## Phase X Milestone: [Name]

**Goal**: [Brief description]

**Success Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Target Date**: YYYY-MM-DD

**Related Issues**: #X, #Y, #Z
```

### Sprint Template
```
## Sprint [Number]: [Dates]

**Focus**: [Primary goal]

**Committed Items**:
- [ ] Issue #X - [Description]
- [ ] Issue #Y - [Description]

**Stretch Goals**:
- [ ] Issue #Z - [Description]
```

## Resources

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [REAPER Roadmap](../ROADMAP.md)
- [Issue Templates](./ISSUE_TEMPLATE/)
