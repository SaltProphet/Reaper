# Branch Protection Rules

## Required for `main` branch

Configure at: Settings → Branches → Add rule

### Protection Rules

```yaml
Branch name pattern: main

☑ Require pull request before merging
  ☑ Require approvals: 1
  ☑ Dismiss stale approvals when new commits are pushed
  ☑ Require review from Code Owners

☑ Require status checks to pass before merging
  ☑ Require branches to be up to date before merging
  Required checks:
    - Quality Gate
    - Test (Python 3.11)
    - Test (Python 3.12)

☑ Require conversation resolution before merging

☑ Require signed commits

☑ Require linear history

☑ Do not allow bypassing the above settings
  (Even admins must follow the rules)

☐ Allow force pushes (DISABLED)
☐ Allow deletions (DISABLED)
```

### Rationale

These settings enforce:
- No direct pushes to main (PR required)
- All quality gates must pass
- Owner review required for core files
- Linear history (no merge commits)
- Signed commits for auditability

**This is a milspec operation. No exceptions.**
