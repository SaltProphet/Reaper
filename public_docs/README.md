# REAPER Documentation

Welcome to the REAPER documentation! This directory contains comprehensive guides for understanding, using, and contributing to REAPER.

## 📚 Documentation Index

### Getting Started
- **[Getting Started Guide](getting-started.md)** - Your first steps with REAPER

### Core Concepts
- **[Architect's Curse](architects-curse.md)** - Philosophy of functional autonomy and architectural vision
- **[Sense Isolation FAQ](sense-isolation-faq.md)** - Understanding sense boundaries and separation of concerns

### Developer Guides
- **[How to Create Plugins](how-to-create-plugins.md)** - Complete guide to plugin development
- **[Operator Console Walkthrough](operator-console-walkthrough.md)** - Operating the REAPER pipeline

## 🎯 Quick Links

### For New Contributors
1. Start with [Getting Started Guide](getting-started.md)
2. Read the [Architect's Curse](architects-curse.md) for philosophical context
3. Follow [How to Create Plugins](how-to-create-plugins.md) to build your first plugin

### For Plugin Developers
1. Review [Sense Isolation FAQ](sense-isolation-faq.md) for boundary rules
2. Check [How to Create Plugins](how-to-create-plugins.md) for patterns
3. Browse [examples/](../examples/) for reference implementations

### For Operators
1. Read [Operator Console Walkthrough](operator-console-walkthrough.md)
2. Review [examples/](../examples/) for operational scripts
3. Check [Getting Started Guide](getting-started.md) for installation

## 🏗️ Architecture Overview

REAPER is a plugin-driven signal processing pipeline inspired by biological systems:

```
┌─────────────┐
│   SENSES    │  Detect signals from environment
├─────────────┤
│   Sight     │  Visual detection
│   Hearing   │  Text/audio detection  
│   Touch     │  Interaction detection
│   Taste     │  Quality detection
│   Smell     │  Pattern detection
└─────────────┘
       ↓
┌─────────────┐
│   SCORING   │  Evaluate signal priority
└─────────────┘
       ↓
┌─────────────┐
│   ACTIONS   │  Execute responses
└─────────────┘
```

### Key Principles

1. **Plugin-Driven**: All functionality via [Pluggy](https://pluggy.readthedocs.io/) plugins
2. **Type-Safe**: Data validation with [Pydantic v2](https://docs.pydantic.dev/latest/)
3. **No Hard-Coding**: Sources are always parameterized
4. **Separation of Concerns**: Never mix detection, scoring, and action
5. **Extensible**: Add plugins without modifying core

## 📖 Document Summaries

### Architect's Curse
Explores the philosophy behind REAPER's architecture—functional autonomy, worldview embodiment, and boundary enforcement. Essential reading for understanding *why* REAPER is designed the way it is.

**Key Topics:**
- Functional autonomy principles
- The biological worldview metaphor
- Boundary enforcement (sense, scoring, action)
- Plugin contracts and guarantees
- Architectural embodiment vs. documentation

### Sense Isolation FAQ
Answers common questions about sense boundaries and separation of concerns. Practical guide with do's and don'ts.

**Key Topics:**
- What is sense isolation?
- Which sense to use for different data types
- Common anti-patterns and how to avoid them
- Multi-sense plugins (when and how)
- Configuration vs. hard-coding

### How to Create Plugins
Complete technical guide for plugin development, from basics to advanced patterns.

**Key Topics:**
- Plugin types (detection, scoring, action)
- Step-by-step plugin creation
- Hook specifications reference
- Best practices and patterns
- Common integrations (API, files, etc.)
- Testing your plugins

### Operator Console Walkthrough
Practical guide for running and operating REAPER pipelines in production or development.

**Key Topics:**
- Console initialization
- Basic operations (detect, score, act)
- Complete pipeline examples
- Multi-source monitoring
- Batch processing
- Error handling and logging
- Performance monitoring
- Configuration management

### Getting Started Guide
Quickstart guide for installing REAPER, running examples, and creating your first plugin.

**Key Topics:**
- Installation steps
- Running the example
- Creating your first plugin
- Testing your plugin
- Next steps and resources

## 🤝 Contributing to Documentation

Found an error? Have a suggestion? Want to add a guide?

1. Open an [Issue](https://github.com/SaltProphet/Reaper/issues/new?template=documentation.md)
2. Submit a [Pull Request](https://github.com/SaltProphet/Reaper/pulls)
3. Discuss in [GitHub Discussions](https://github.com/SaltProphet/Reaper/discussions)

### Documentation Standards

- Use clear, concise language
- Include code examples for technical concepts
- Add visual diagrams where helpful
- Cross-reference related documents
- Keep the biological metaphor consistent
- Test all code examples before committing

## 📬 Getting Help

- **Questions?** → [GitHub Discussions](https://github.com/SaltProphet/Reaper/discussions)
- **Bugs?** → [Issue Tracker](https://github.com/SaltProphet/Reaper/issues)
- **Ideas?** → [Discussions - Ideas](https://github.com/SaltProphet/Reaper/discussions/categories/ideas)

## 🗺️ Documentation Roadmap

Planned additions:
- [ ] API Reference (auto-generated from docstrings)
- [ ] Advanced Plugin Patterns
- [ ] Performance Tuning Guide
- [ ] Security Best Practices
- [ ] Deployment Guide (Docker, K8s, etc.)
- [ ] Troubleshooting Guide
- [ ] Video Tutorials
- [ ] Plugin Marketplace Catalog

See the main [Roadmap](../ROADMAP.md) for overall project direction.

---

**Happy building! 🏗️**
