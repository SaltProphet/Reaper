# Documentation Guidelines

This document defines standards for writing clear, comprehensive, and maintainable documentation for REAPER. Following these guidelines ensures consistency and helps both contributors and operators succeed.

## Table of Contents

- [Overview](#overview)
- [Documentation Types](#documentation-types)
- [Writing Standards](#writing-standards)
- [Structure Guidelines](#structure-guidelines)
- [Code Examples](#code-examples)
- [Environment Variables](#environment-variables)
- [Troubleshooting Sections](#troubleshooting-sections)
- [Plugin Documentation](#plugin-documentation)
- [Operator Documentation](#operator-documentation)
- [API Documentation](#api-documentation)
- [Maintenance](#maintenance)

## Overview

**Documentation Principles:**
- 📝 **Clarity**: Write for newcomers, not experts
- 🎯 **Actionable**: Provide concrete steps and examples
- ✅ **Tested**: All code examples must work
- 🔗 **Connected**: Link related documentation
- 🔄 **Current**: Keep in sync with code changes

**Target Audiences:**
1. **Plugin Developers**: Creating new plugins
2. **Operators**: Running and configuring REAPER
3. **Contributors**: Improving REAPER core
4. **Integrators**: Embedding REAPER in larger systems

## Documentation Types

### 1. README Files

**Purpose**: Quick overview and getting started

**Required Sections:**
- Title and one-sentence description
- Quick start / Installation
- Basic usage example
- Links to detailed documentation

**Location:**
- Root `README.md`: Project overview
- Plugin `README.md`: Plugin-specific guide
- Directory `README.md`: Section overview

**Example:**
```markdown
# Component Name

One-sentence description.

## Quick Start

\`\`\`bash
# Installation
pip install component

# Basic usage
python -m component
\`\`\`

See [Full Documentation](docs/component.md) for details.
```

### 2. Guides

**Purpose**: Step-by-step tutorials and how-tos

**Location**: `docs/guides/`

**Types:**
- Getting started guides
- Plugin development tutorials
- Configuration guides
- Deployment guides

**Structure:**
```markdown
# Guide Title

## What You'll Learn
- Objective 1
- Objective 2

## Prerequisites
- Required knowledge
- Required setup

## Steps

### Step 1: [Action]
Description and code

### Step 2: [Action]
Description and code

## Next Steps
- Link to related guides
```

### 3. Reference Documentation

**Purpose**: Complete API and configuration reference

**Location**: `docs/reference/` or inline docstrings

**Types:**
- API reference (classes, functions, parameters)
- Configuration reference (env vars, config files)
- Hook specifications
- Data models

### 4. Planning Documents

**Purpose**: Roadmap, architecture decisions, design docs

**Location**: `docs/planning/`

**Types:**
- Phase plans (PHASE_1_PLAN.md, etc.)
- Architecture Decision Records (ADRs)
- RFC-style proposals

## Writing Standards

### Language and Tone

**Style:**
- Active voice: "Create a plugin" not "A plugin is created"
- Present tense: "The plugin returns" not "The plugin will return"
- Second person: "You can configure" not "One can configure"
- Imperative for instructions: "Run the command" not "You should run"

**Clarity:**
- Short sentences (aim for <25 words)
- Simple words (prefer "use" over "utilize")
- Avoid jargon (or explain it)
- Define acronyms on first use

**Examples:**

```markdown
❌ BAD: The utilization of environment variables is recommended for configuration.
✅ GOOD: Use environment variables to configure the plugin.

❌ BAD: In the event that the API returns a 429 status code, retrying should be attempted.
✅ GOOD: If the API returns a 429 status code, retry the request.

❌ BAD: It is possible to leverage the batch creation functionality to improve performance.
✅ GOOD: Use Signal.create_batch() for better performance.
```

### Formatting

**Headers:**
- Use sentence case: "Getting started" not "Getting Started"
- Be descriptive: "Install dependencies" not "Installation"
- Maintain hierarchy: H1 → H2 → H3 (don't skip levels)

**Lists:**
- Use bullets for unordered items
- Use numbers for sequential steps
- Keep items parallel in structure

```markdown
✅ GOOD:
1. Install dependencies
2. Configure environment
3. Run the application

❌ BAD:
1. Dependencies should be installed
2. Configuring your environment
3. You can now run the application
```

**Emphasis:**
- **Bold** for UI elements, commands, important terms
- *Italic* for emphasis (sparingly)
- `Code` for inline code, filenames, variables

**Admonitions:**
```markdown
⚠️ **Warning**: Critical information that could cause data loss
💡 **Tip**: Helpful but non-essential information
📝 **Note**: Additional context or clarification
🔒 **Security**: Security-related information
```

## Structure Guidelines

### Document Template

Every documentation file should follow this structure:

```markdown
# Document Title

Brief description (1-2 sentences) of what this document covers.

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)

## Section 1

Content...

### Subsection 1.1

Content...

## Section 2

Content...

---

**Questions?** Ask in [GitHub Discussions](link)
```

### Section Order

**For Guides:**
1. Overview/Introduction
2. Prerequisites
3. Step-by-step instructions
4. Verification/Testing
5. Troubleshooting
6. Next steps
7. Related resources

**For Reference:**
1. Overview
2. Quick reference (table/summary)
3. Detailed sections
4. Examples
5. See also

### Link Conventions

**Internal Links:**
```markdown
- Relative paths: [Guide](../guides/CONTRIBUTING.md)
- Anchors: [Section](#section-name)
- Root-relative: [README](/README.md)
```

**External Links:**
```markdown
- Full URL: [Pydantic](https://docs.pydantic.dev/)
- Open in new tab: Use standard markdown (browser handles it)
```

**Link Text:**
- Descriptive: "See the [plugin development guide](link)"
- Not: "Click [here](link) for the guide"

## Code Examples

### Requirements

**Every code example must:**
1. ✅ Be complete and runnable
2. ✅ Include necessary imports
3. ✅ Show expected output (when relevant)
4. ✅ Be tested (manually or automated)
5. ✅ Follow REAPER coding standards

### Example Structure

````markdown
### Example: [Descriptive Title]

Brief description of what this example demonstrates.

```python
# Complete, runnable code
from reaper import PluginManager
from plugin import MyPlugin

pm = PluginManager()
pm.register_plugin(MyPlugin(), name="example")

signals = pm.detect_sight(source="test")
print(f"Detected {len(signals)} signals")
```

**Expected Output:**
```
Detected 2 signals
```

**Explanation:**
1. Import required modules
2. Initialize plugin manager
3. Register the plugin
4. Call detection method
````

### Code Block Languages

Use appropriate language identifiers:

```markdown
- Python: ```python
- Bash: ```bash
- YAML: ```yaml
- JSON: ```json
- Text output: ```text or just ```
- No language: ```
```

### Highlighting Important Lines

````markdown
```python
from reaper import PluginManager

# This is the important part!
pm.register_plugin(MyPlugin(), name="example")  # ← Note the name parameter

signals = pm.detect_sight(source="test")
```
````

## Environment Variables

### Documentation Format

Every environment variable should be documented with:

**Required Information:**
- Variable name
- Description
- Required vs Optional
- Default value (if any)
- Valid values/format
- Example

**Template:**

```markdown
### `PLUGIN_NAME_API_KEY`

**Required**: Yes | No

**Description**: API key for authenticating with [service].

**Format**: String, 32 alphanumeric characters

**Example**:
\`\`\`bash
export PLUGIN_NAME_API_KEY="abc123xyz789def456ghi012jkl345mn"
\`\`\`

**How to obtain**: See [Authentication Guide](link)
```

### Environment Variable Naming

**Convention**: `[PLUGIN_NAME]_[VARIABLE_NAME]`

**Examples:**
- `REDDIT_INGESTOR_API_KEY`
- `DISCORD_NOTIFIER_WEBHOOK_URL`
- `GITHUB_ANALYZER_TOKEN`

**Guidelines:**
- All uppercase
- Underscore separators
- Plugin prefix to avoid conflicts
- Descriptive but concise

### .env.example

Always provide `.env.example` with:
- All required variables
- All optional variables
- Placeholder values (never real secrets)
- Comments explaining each variable

```bash
# Required: API key for Reddit access
# Get from: https://www.reddit.com/prefs/apps
REDDIT_INGESTOR_API_KEY="your-api-key-here"

# Optional: Custom API endpoint (default: https://oauth.reddit.com)
# REDDIT_INGESTOR_ENDPOINT="https://custom-endpoint.com"

# Optional: Request timeout in seconds (default: 30)
# REDDIT_INGESTOR_TIMEOUT="60"
```

## Troubleshooting Sections

### Structure

Every troubleshooting section should follow this pattern:

```markdown
## Troubleshooting

### Common Issues

#### Issue: [Error Message or Problem]

**Symptoms**: What the user observes

**Cause**: Why this happens

**Solution**:
1. Step 1 to resolve
2. Step 2 to resolve
3. Verification step

**Alternative Solutions** (if applicable):
- Alternative approach 1
- Alternative approach 2

**Related Issues**: [Link to similar issues]
```

### Example

```markdown
#### Issue: "RuntimeError: Failed to detect signals"

**Symptoms**: Plugin raises RuntimeError when calling detect method

**Cause**: API request failed (network error, authentication, rate limit)

**Solution**:
1. **Verify API credentials**:
   \`\`\`bash
   python -c "import os; print(os.getenv('MY_PLUGIN_API_KEY'))"
   \`\`\`

2. **Test API endpoint manually**:
   \`\`\`bash
   curl -H "Authorization: Bearer $MY_PLUGIN_API_KEY" https://api.example.com/test
   \`\`\`

3. **Check rate limits**: Wait 60 seconds and retry

**Alternative Solutions**:
- Increase timeout: `export MY_PLUGIN_TIMEOUT="60"`
- Use different endpoint: `export MY_PLUGIN_ENDPOINT="https://alt-endpoint.com"`

**Related Issues**: [#123 - Rate limiting improvements](#)
```

### Debug Mode

Document how to enable debug/verbose logging:

```markdown
### Enable Debug Logging

For detailed troubleshooting output:

\`\`\`bash
# Method 1: Environment variable
export MY_PLUGIN_DEBUG="true"
python your_script.py

# Method 2: Logging configuration
import logging
logging.basicConfig(level=logging.DEBUG)
\`\`\`

Debug logs include:
- API request/response details
- Plugin registration events
- Signal creation steps
- Error stack traces
```

## Plugin Documentation

### Plugin README Requirements

Every plugin must have a `README.md` with these sections:

1. **Title and Description**: What does this plugin do?
2. **Features**: Bullet list of capabilities and limitations
3. **Installation**: Dependencies and setup steps
4. **Configuration**: Environment variables and config files
5. **Usage**: Basic and advanced examples
6. **API Reference**: Classes, methods, parameters
7. **Testing**: How to run tests
8. **Troubleshooting**: Common issues and solutions
9. **Contributing**: How to contribute
10. **License**: License information

**Use the template**: `templates/PLUGIN_README_TEMPLATE.md`

### Plugin Docstrings

Every plugin class and method needs docstrings:

```python
class MyPlugin:
    """
    [One-line description of plugin].
    
    [Longer description with more details about what it does,
    when to use it, and any important considerations.]
    
    Implements: reaper_[hook_name] hook
    
    Environment Variables:
        PLUGIN_NAME_API_KEY: Required API key for authentication
        PLUGIN_NAME_ENDPOINT: Optional API endpoint override
    
    Example:
        >>> plugin = MyPlugin()
        >>> pm = PluginManager()
        >>> pm.register_plugin(plugin, name="my-plugin")
        >>> signals = pm.detect_sight(source="example")
    """
    
    def __init__(self, config: PluginConfig | None = None):
        """
        Initialize the plugin.
        
        Args:
            config: Optional plugin configuration. If None, loads from
                   environment variables.
        
        Raises:
            KeyError: If required environment variables are missing
            ValidationError: If configuration is invalid
        """
        pass
    
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        """
        Detect visual signals from the specified source.
        
        Args:
            source: Source identifier (format: [describe format]).
                   Examples: "channel-123", "https://example.com/feed"
        
        Returns:
            List of Signal objects detected from the source.
            Empty list if no signals detected.
        
        Raises:
            RuntimeError: If detection fails due to API errors
            ValidationError: If source format is invalid
        
        Performance:
            Typical: 100-500ms per source
            Rate limit: 60 requests/minute
        """
        pass
```

### Plugin Examples

Provide at least 3 examples:

1. **Basic Usage**: Simplest possible use case
2. **Full Pipeline**: Detection → Scoring → Action
3. **Error Handling**: How to handle failures gracefully

See `templates/PLUGIN_README_TEMPLATE.md` for complete examples.

## Operator Documentation

### Operator Guides

**Focus**: Practical "how to get things done" guides

**Structure:**
1. **Goal**: What will be accomplished
2. **Prerequisites**: What's needed before starting
3. **Steps**: Numbered, sequential instructions
4. **Verification**: How to confirm success
5. **Troubleshooting**: What to do if it doesn't work

**Example:**

```markdown
# Deploy REAPER with Docker

This guide shows you how to deploy REAPER in a Docker container.

## Goal

By the end of this guide, you'll have:
- REAPER running in Docker
- Plugins configured with environment variables
- Logs accessible for monitoring

## Prerequisites

- Docker installed (version 20.10+)
- Basic familiarity with Docker commands
- REAPER configuration prepared

## Steps

### 1. Create Dockerfile

Create a file named `Dockerfile`:

\`\`\`dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["python", "example_runner.py"]
\`\`\`

### 2. Build Docker image

\`\`\`bash
docker build -t reaper:latest .
\`\`\`

[Continue with remaining steps...]
```

### Configuration Documentation

**Format**: Reference table + detailed explanations

```markdown
## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PLUGIN_API_KEY` | Yes | - | API authentication key |
| `PLUGIN_ENDPOINT` | No | `https://api.example.com` | API endpoint URL |
| `PLUGIN_TIMEOUT` | No | `30` | Request timeout (seconds) |

### Detailed Configuration

#### `PLUGIN_API_KEY`

[Detailed explanation, how to obtain, format requirements, security notes]

#### `PLUGIN_ENDPOINT`

[Detailed explanation, when to override, valid formats]
```

## API Documentation

### Function Documentation

Use this format for all public functions:

```python
def function_name(param1: Type1, param2: Type2 = default) -> ReturnType:
    """
    One-line summary of what the function does.
    
    More detailed explanation if needed. Can span multiple lines
    and include important details about behavior, side effects, etc.
    
    Args:
        param1: Description of param1. Include format, constraints,
               and examples if helpful.
        param2: Description of param2. Note that this is optional
               (has a default value).
    
    Returns:
        Description of return value. Include type information and
        any important details about the returned data structure.
    
    Raises:
        ExceptionType1: When this exception is raised
        ExceptionType2: When this exception is raised
    
    Example:
        >>> result = function_name("input", param2=42)
        >>> print(result)
        expected output
    
    Note:
        Any additional important information, warnings, or
        performance considerations.
    """
    pass
```

### Class Documentation

```python
class ClassName:
    """
    One-line summary of what the class does.
    
    Detailed description of the class purpose, when to use it,
    and any important considerations.
    
    Attributes:
        attr1: Description of public attribute
        attr2: Description of public attribute
    
    Example:
        >>> obj = ClassName(param="value")
        >>> result = obj.method()
    """
    
    def __init__(self, param: Type):
        """
        Initialize the class.
        
        Args:
            param: Description
        
        Raises:
            ExceptionType: When this happens
        """
        pass
```

## Maintenance

### Keeping Documentation Current

**When to Update Documentation:**
- ✅ Anytime code behavior changes
- ✅ When adding new features
- ✅ When fixing bugs that affect usage
- ✅ When environment variables change
- ✅ When configuration changes
- ✅ When API signatures change

**Documentation Review Checklist:**
- [ ] All code examples still work
- [ ] Environment variables are current
- [ ] Links are not broken
- [ ] Screenshots match current UI
- [ ] Version numbers are correct
- [ ] Troubleshooting section covers recent issues

### Documentation in PRs

**Requirements:**
- All PRs with user-facing changes must update documentation
- Documentation changes should be in the same PR as code changes
- PR description should highlight documentation changes

**PR Review Checklist:**
- [ ] README updated (if applicable)
- [ ] Inline docstrings updated
- [ ] Examples updated
- [ ] Environment variables documented
- [ ] Troubleshooting updated (if new error cases)

### Testing Documentation

**Manual Testing:**
1. Copy code examples into fresh environment
2. Run all commands as documented
3. Verify output matches documentation
4. Test troubleshooting solutions

**Automated Testing:**
```bash
# Test code examples (if tooling available)
pytest --doctest-modules

# Check links
# (Use link checker tool)
```

### Documentation TODOs

Mark incomplete documentation:

```markdown
<!-- TODO: Add examples for advanced usage -->
<!-- TODO: Document performance benchmarks -->
<!-- FIXME: Update to reflect new API in v2.0 -->
```

Track documentation TODOs in issues with `docs` label.

## Resources

### Templates

- [Plugin README Template](../templates/PLUGIN_README_TEMPLATE.md)
- [Plugin Code Template](../templates/plugin_template.py)

### Style Guides

- [Google Style Guide](https://developers.google.com/style) - General technical writing
- [Microsoft Style Guide](https://docs.microsoft.com/en-us/style-guide/) - Reference
- [Write the Docs](https://www.writethedocs.org/) - Community resources

### Tools

- **Markdown Linters**: markdownlint, remark-lint
- **Link Checkers**: markdown-link-check
- **Spell Checkers**: codespell, aspell
- **Documentation Generators**: MkDocs, Sphinx

## Questions?

Ask in [GitHub Discussions - Documentation](https://github.com/SaltProphet/Reaper/discussions/categories/documentation)

---

**Remember**: Good documentation is as important as good code. Take the time to write it well!
