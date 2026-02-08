## Description

<!-- Provide a brief description of the changes in this PR -->

## Related Issue

<!-- Link to the related issue(s) if applicable -->
Closes #

## Type of Change

<!-- Mark the relevant option with an "x" -->

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Plugin contribution (new detection, scoring, or action plugin)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Test improvement

## Component

<!-- Mark all that apply with an "x" -->

- [ ] Core (models, plugin_manager, hookspecs)
- [ ] Pipeline (sight, hearing, touch, taste, smell)
- [ ] Action
- [ ] Scoring
- [ ] Tests
- [ ] Documentation
- [ ] CI/CD

## Changes Made

<!-- Describe the changes in detail -->

## Testing

<!-- Describe how you tested your changes -->

- [ ] Tests pass locally (`pytest -v --cov=reaper --cov=pipeline`)
- [ ] New tests added for new functionality
- [ ] Code follows linting rules (Ruff)

## Compliance Checklist

<!-- Ensure your changes follow REAPER guidelines -->

- [ ] Follows plugin-driven architecture principles
- [ ] Uses Pydantic v2 models for data validation
- [ ] Does NOT hard-code data sources
- [ ] Maintains separation of concerns (doesn't mix pipeline roles)
- [ ] Includes appropriate documentation/docstrings
- [ ] No breaking changes to existing plugins (or clearly documented if unavoidable)
- [ ] CI/CD workflows have explicit permissions blocks (if modified)

## Documentation

- [ ] README updated (if needed)
- [ ] Docstrings/comments added or updated
- [ ] Roadmap updated (if this relates to a roadmap phase)
- [ ] CONTRIBUTING.md updated (if adding new contributor guidelines)

## Additional Context

<!-- Add any other context about the PR here -->

## Screenshots (if applicable)

<!-- Add screenshots for UI changes or visual improvements -->

---

<!-- 
For Copilot: This PR should align with REAPER's core principles.
Check .github/copilot-instructions.md for code conventions.
-->
