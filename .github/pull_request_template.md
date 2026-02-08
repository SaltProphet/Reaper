## Description

<!-- Provide a brief description of the changes in this PR -->

## Type of Change

<!-- Mark the relevant option with an "x" -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Plugin addition or modification
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test addition or modification

## Changes Made

<!-- List the specific changes made in this PR -->

- 
- 
- 

## Sense Isolation Checklist

<!-- Verify sense boundaries are respected -->

- [ ] Detection plugins only detect signals (no scoring or actions)
- [ ] Scoring plugins only score signals (no detection or actions)
- [ ] Action plugins only execute actions (no detection or scoring)
- [ ] No mixing of sense types within a single detection method
- [ ] All sources are parameterized (no hard-coded sources)

## Plugin Contract Checklist

<!-- For plugin changes only -->

- [ ] Uses proper `@hookimpl` decorator
- [ ] Follows hook specification signatures
- [ ] Uses Pydantic models for all data (Signal, ScoredSignal, ActionResult)
- [ ] Handles errors gracefully (returns empty lists, not exceptions)
- [ ] Plugin is independently testable
- [ ] Configuration is passed via constructor, not hard-coded

## Documentation Checklist

- [ ] Code includes docstrings for public methods
- [ ] README updated (if needed)
- [ ] Documentation in `public_docs/` updated (if needed)
- [ ] Examples updated or added (if needed)
- [ ] CHANGELOG updated (if applicable)

## Testing

<!-- Describe the tests you've added or run -->

- [ ] Existing tests pass (`pytest`)
- [ ] New tests added for new functionality
- [ ] Manual testing performed
- [ ] Edge cases considered and tested

**Test results:**
```
# Paste relevant test output here
```

## Code Quality

- [ ] Code follows project style guidelines
- [ ] Linter passes (`ruff check .`)
- [ ] Type hints added where appropriate
- [ ] No unnecessary code duplication
- [ ] Error handling is comprehensive

## Related Issues

<!-- Link related issues using #issue_number -->

Closes #
Related to #

## Additional Context

<!-- Add any additional context, screenshots, or notes for reviewers -->

## Reviewer Notes

<!-- Anything specific you want reviewers to focus on? -->

---

## For Maintainers

- [ ] Changes align with project roadmap
- [ ] Breaking changes documented
- [ ] Security implications considered
- [ ] Performance impact assessed
