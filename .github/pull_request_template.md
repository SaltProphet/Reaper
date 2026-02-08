## Description

<!-- Provide a brief description of your changes -->

## Type of Change

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 🔌 New plugin (adds a new detection/scoring/action plugin)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🔧 Configuration change
- [ ] ♻️ Refactoring (no functional changes)
- [ ] 🧪 Test improvement
- [ ] 🎨 Style/formatting update

## Changes Made

<!-- List the specific changes in bullet points -->

- 
- 
- 

## Related Issues

<!-- Link related issues using #issue_number -->

Closes #
Related to #

## Testing

<!-- How have you tested these changes? -->

- [ ] All existing tests pass (`pytest`)
- [ ] Added new tests for changes
- [ ] Manual testing performed
- [ ] Linting passes (`ruff check .`)
- [ ] Formatting is correct (`ruff format .`)

### Test Results

```bash
# Paste pytest output here
```

## Plugin-Specific Checklist (if applicable)

- [ ] Uses `@hookimpl` decorator from Pluggy
- [ ] No hard-coded sources (source parameter used)
- [ ] Follows separation of concerns (no mixing roles)
- [ ] Uses Pydantic models for data validation
- [ ] Includes comprehensive docstrings
- [ ] Added tests for plugin functionality
- [ ] Updated example_runner.py if needed

## Code Quality Checklist

- [ ] Code follows project style guidelines (see `.github/copilot-instructions.md`)
- [ ] Self-review of code completed
- [ ] Comments added for complex or non-obvious code
- [ ] Documentation updated (README, docstrings)
- [ ] No new warnings introduced
- [ ] Type hints included for all functions/methods
- [ ] Error handling implemented where appropriate

## Breaking Changes

<!-- If this is a breaking change, describe the impact and migration path -->

## Screenshots (if applicable)

<!-- Add screenshots for UI changes or visual improvements -->

## Additional Context

<!-- Add any other context about the pull request here -->

## Checklist Before Requesting Review

- [ ] Code is ready for review
- [ ] All CI checks pass
- [ ] Documentation is complete
- [ ] Ready to merge (all comments addressed)

---

**For Reviewers:**
- Please review the code for correctness, style, and adherence to REAPER principles
- Check that plugins don't hard-code sources and follow separation of concerns
- Verify test coverage is adequate
- Ensure Pydantic models are used correctly
