# Contributing to REAPER

Thank you for your interest in contributing to REAPER! We welcome contributions from everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Architectural Principles](#architectural-principles)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## Code of Conduct

Be respectful, inclusive, and constructive. We're building something together.

## Getting Started

1. **Read the Documentation**
   - [Getting Started Guide](public_docs/getting-started.md)
   - [Architect's Curse](public_docs/architects-curse.md) - Philosophy and principles
   - [Sense Isolation FAQ](public_docs/sense-isolation-faq.md) - Boundary rules

2. **Explore the Codebase**
   - Browse `reaper/` for core framework
   - Check `pipeline/` for reference implementations
   - Review `tests/` for testing patterns
   - Look at `examples/` for real-world usage

3. **Pick an Issue**
   - Browse [open issues](https://github.com/SaltProphet/Reaper/issues)
   - Look for `good-first-issue` label
   - Comment on the issue to claim it

## How to Contribute

### Types of Contributions

1. **Code Contributions**
   - Bug fixes
   - New features
   - Performance improvements
   - Test coverage

2. **Plugin Contributions**
   - New sense plugins
   - Scoring algorithms
   - Action handlers
   - Submit via [Plugin Submission](https://github.com/SaltProphet/Reaper/issues/new?template=plugin_submission.yml)

3. **Documentation**
   - Fix typos or errors
   - Add examples
   - Improve explanations
   - Create tutorials

4. **Community Support**
   - Answer questions in Discussions
   - Review pull requests
   - Share your use cases
   - Report bugs

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- pip

### Setup Steps

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/Reaper.git
cd Reaper

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests to ensure everything works
pytest

# Run linter
ruff check .
```

## Contribution Guidelines

### Core Principles (Must Follow)

1. **Sense Isolation**
   - Never mix detection, scoring, and action
   - Each sense handles only its specific signal type
   - See [Sense Isolation FAQ](public_docs/sense-isolation-faq.md)

2. **No Hard-Coding**
   - Always parameterize sources
   - Use constructor parameters for configuration
   - Never hard-code URLs, paths, or credentials

3. **Type Safety**
   - Use Pydantic models for all data structures
   - Add type hints to all functions
   - Validate data at boundaries

4. **Plugin Pattern**
   - Use `@hookimpl` decorator
   - Follow hook specifications in `reaper/hookspecs.py`
   - Make plugins independently testable

### Code Style

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Check code
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

**Style Guidelines:**
- Line length: 100 characters
- Use descriptive variable names
- Add docstrings to public methods
- Include type hints
- Follow PEP 8

### Testing Requirements

All code changes must include tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=reaper --cov=pipeline

# Run specific test file
pytest tests/test_models.py
```

**Testing Guidelines:**
- Write unit tests for new functions
- Test edge cases and error conditions
- Use descriptive test names
- Keep tests isolated and independent
- Mock external dependencies

### Documentation Requirements

- Add docstrings to all public methods
- Update relevant documentation in `public_docs/`
- Include usage examples for new features
- Update README if adding major features

## Architectural Principles

Before contributing, understand these core principles:

### 1. Functional Autonomy

Each component should:
- Have a single, well-defined responsibility
- Operate independently
- Not depend on implementation details of other components
- Be swappable without breaking the system

### 2. The Biological Worldview

REAPER's architecture mirrors biological systems:
- **Senses** detect signals (like eyes, ears, etc.)
- **Scoring** evaluates importance (like a brain)
- **Actions** respond to signals (like muscles)

This isn't just a metaphor—it's an architectural constraint.

### 3. Plugin-First Design

Everything extends through plugins:
- Core framework stays minimal
- Plugins add functionality
- No hard-coded implementations
- Clean hook specifications

### 4. Separation of Concerns

**Detection** → **Scoring** → **Action**

Never mix these phases:
- ❌ Don't score in detection
- ❌ Don't act in scoring
- ❌ Don't detect in actions

See [Sense Isolation FAQ](public_docs/sense-isolation-faq.md) for details.

## Pull Request Process

### Before Submitting

1. **Test Your Changes**
   ```bash
   pytest
   ruff check .
   ```

2. **Update Documentation**
   - Add docstrings
   - Update relevant docs
   - Add examples if needed

3. **Follow Commit Guidelines**
   - Use clear, descriptive commit messages
   - Reference issue numbers: `Fixes #123`
   - Keep commits atomic and focused

### Submitting a PR

1. **Create a Branch**
   ```bash
   git checkout -b feature/my-feature
   # or
   git checkout -b fix/my-bugfix
   ```

2. **Make Your Changes**
   - Write code
   - Add tests
   - Update docs

3. **Push and Open PR**
   ```bash
   git push origin feature/my-feature
   ```
   Then open a PR on GitHub

4. **Fill Out PR Template**
   - Describe your changes
   - Complete all checklists
   - Link related issues
   - Add screenshots if UI changes

### PR Review Process

- Maintainers will review your PR
- Address feedback promptly
- Keep discussions constructive
- Be patient—reviews take time

### Checklist for PRs

- [ ] Tests pass
- [ ] Linter passes
- [ ] Documentation updated
- [ ] Sense isolation respected
- [ ] No hard-coded sources
- [ ] Pydantic models used
- [ ] Type hints added
- [ ] Docstrings included

## Community

### Communication Channels

- **GitHub Discussions**: Questions, ideas, architecture discussions
- **Issues**: Bug reports, feature requests
- **Pull Requests**: Code contributions

### Getting Help

- Check [documentation](public_docs/)
- Search [existing issues](https://github.com/SaltProphet/Reaper/issues)
- Ask in [Discussions](https://github.com/SaltProphet/Reaper/discussions)
- Review [examples](examples/)

### Becoming a Contributor

We appreciate all contributions! Here's how to get more involved:

1. **Start Small**: Fix a typo, improve docs, add a test
2. **Contribute Regularly**: Small, consistent contributions are valued
3. **Help Others**: Answer questions, review PRs
4. **Share Knowledge**: Write blog posts, create tutorials
5. **Maintain a Plugin**: Build and maintain a plugin

### Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes
- Community showcases
- Special thanks in major releases

## Plugin Development

### Creating a Plugin

See [How to Create Plugins](public_docs/how-to-create-plugins.md) for a comprehensive guide.

### Submitting a Plugin

1. Develop your plugin in a separate repository
2. Follow REAPER's plugin contract
3. Add tests and documentation
4. Submit via [Plugin Submission template](https://github.com/SaltProphet/Reaper/issues/new?template=plugin_submission.yml)

### Plugin Guidelines

- Use `@hookimpl` decorator
- Follow sense isolation rules
- Parameterize all configuration
- Use Pydantic models
- Handle errors gracefully
- Include comprehensive tests
- Document usage clearly

## Questions?

- 📚 Check the [documentation](public_docs/)
- 💬 Ask in [Discussions](https://github.com/SaltProphet/Reaper/discussions)
- 🐛 Report bugs via [Issues](https://github.com/SaltProphet/Reaper/issues)
- 📧 Contact maintainers (see repository)

---

**Thank you for contributing to REAPER! Together, we're building a robust, principled signal processing framework.** 🚀
