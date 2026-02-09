# Quick Start: GitHub Advanced Tools for REAPER

> **Fast-track guide to get productive with GitHub Copilot, Codespaces, and automation in 15 minutes.**

## ⚡ 5-Minute Setup

### Step 1: Enable GitHub Copilot (2 minutes)

1. **Subscribe**: Go to [github.com/settings/copilot](https://github.com/settings/copilot)
2. **Enable**: Click "Enable GitHub Copilot"
3. **Install VS Code Extension**: 
   - Open VS Code Extensions (Ctrl+Shift+X)
   - Search "GitHub Copilot"
   - Install both "GitHub Copilot" and "GitHub Copilot Chat"
   - Sign in when prompted

✅ **Test it**: Open any Python file, type `# Create a function that` and wait for suggestions

### Step 2: Launch Codespace (3 minutes)

1. **Go to repo**: [github.com/SaltProphet/Reaper](https://github.com/SaltProphet/Reaper)
2. **Click**: Code → Codespaces → "Create codespace on main"
3. **Wait**: Environment builds with Python 3.11 and dependencies (~2 min)
4. **Start coding**: Everything is pre-configured!

✅ **Test it**: Run `pytest` in the terminal

### Step 3: Use Copilot for REAPER (5 minutes)

Open Copilot Chat (Ctrl+Shift+I) and try:

```
Create a REAPER plugin that detects high-priority GitHub issues
```

Copilot will generate a plugin following REAPER patterns!

## 🎯 Common Tasks

### Create a New Detection Plugin

**Copilot Chat Prompt:**
```
@workspace Create a new Sight detection plugin called GitHubIssueDetector 
that uses the GitHub API to detect issues with the "bug" label. Follow 
REAPER patterns: use @hookimpl, accept source parameter, return Signal objects.
```

### Write Tests for Your Plugin

**Copilot Chat Command:**
```
/tests for the GitHubIssueDetector class
```

### Debug an Error

**Copilot Chat:**
```
/fix this Pydantic validation error
```

### Understand Existing Code

**Copilot Chat:**
```
/explain the PluginManager class and how it loads plugins
```

## 📋 Pre-Launch Checklist

Before submitting a PR, use this checklist:

```bash
# 1. Lint your code
ruff check .

# 2. Format your code
ruff format .

# 3. Run tests
pytest

# 4. Check coverage
pytest --cov=reaper --cov=pipeline

# 5. Verify plugin loading
python example_runner.py
```

Or use Copilot Chat:
```
@terminal Run linting, formatting, and tests
```

## 🔥 Power User Tips

### 1. Use Copilot Instructions

REAPER includes `.github/copilot-instructions.md` with project-specific guidance. Copilot automatically uses these instructions!

### 2. Context is Everything

Keep these files open for better suggestions:
- `reaper/models.py` (data models)
- `reaper/hookspecs.py` (available hooks)
- Similar plugins from `pipeline/` directory

### 3. Iterate with Comments

Write what you want, let Copilot generate, refine with comments:
```python
# Detect GitHub issues from the API
# Filter for high priority (P0 or P1 labels)
# Return Signal objects with issue details
```

### 4. Use Agents in Copilot Chat

- `@workspace` - Ask about the codebase
- `@terminal` - Get help with commands
- `@test` - Generate tests

Example:
```
@workspace Where should I add a new detection plugin and what patterns should I follow?
```

### 5. Keyboard Shortcuts

- `Tab` - Accept suggestion
- `Alt+]` - Next suggestion
- `Alt+[` - Previous suggestion
- `Ctrl+Shift+I` - Open Copilot Chat
- `Ctrl+Enter` - Trigger inline suggestions

## 🚀 Next Steps

1. **Read Full Guide**: [docs/guides/GITHUB_ADVANCED_TOOLS.md](docs/guides/GITHUB_ADVANCED_TOOLS.md)
2. **Contributing**: [docs/guides/CONTRIBUTING.md](docs/guides/CONTRIBUTING.md)
3. **Architecture**: [README.md](README.md)

## 💡 Example: Build a Complete Plugin in 10 Minutes

### Minute 1-3: Generate Plugin Structure

**Copilot Chat:**
```
Create a REAPER Hearing plugin that detects Slack messages with negative 
sentiment. Use the Slack API, accept channel as source, analyze sentiment, 
and return Signals with sentiment scores in raw_data.
```

### Minute 4-6: Generate Tests

**Copilot Chat:**
```
/tests for SlackSentimentDetector with fixtures for mock Slack responses
```

### Minute 7-8: Run & Debug

```bash
pytest tests/test_slack_sentiment.py -v
```

If errors, use Copilot Chat:
```
/fix [paste error]
```

### Minute 9: Lint & Format

```bash
ruff check --fix . && ruff format .
```

### Minute 10: Commit & Push

```bash
git add .
git commit -m "feat: Add Slack sentiment detection plugin"
git push
```

Open PR using template - done! 🎉

## 🔧 Troubleshooting

### Copilot Not Working
- Check extension is enabled in VS Code
- Sign out and sign in again
- Verify subscription at [github.com/settings/copilot](https://github.com/settings/copilot)

### Codespace Won't Start
- Check usage limits (free tier: 120 hours/month)
- Try creating new Codespace
- Contact GitHub support if persists

### Tests Failing
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -e ".[dev]"

# Run verbose
pytest -v
```

## 📚 Learning Resources

- **Copilot Guide**: [docs.github.com/copilot](https://docs.github.com/en/copilot)
- **Codespaces Guide**: [docs.github.com/codespaces](https://docs.github.com/en/codespaces)
- **REAPER Architecture**: [README.md](README.md)
- **Plugin Development**: [docs/guides/CONTRIBUTING.md](docs/guides/CONTRIBUTING.md)

---

**Questions?** Open a [Discussion](https://github.com/SaltProphet/Reaper/discussions) or ask Copilot Chat:
```
@workspace How do I [your question]?
```

Happy coding! 🎯
