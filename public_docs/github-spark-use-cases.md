# GitHub Spark Use Cases for REAPER

This document outlines potential ways GitHub Spark can accelerate development and operations for REAPER and the apps that can be created to support those workflows. Each use case includes a suggested Spark app concept and a starter prompt you can use to generate it.

## 1) Plugin Scaffolder

**Use case**
Create new detection, scoring, or action plugins quickly with correct hook names and Pydantic models.

**Spark app concept**
A form-driven generator that outputs a plugin module plus a minimal test stub.

**Prompt**
```
Build a single-page app that generates REAPER plugins.
- Inputs: plugin name, sense type (sight/hearing/touch/taste/smell), role (detect/score/action), source parameter name, optional metadata keys.
- Output: Python code with pluggy hook implementation using correct hook names (reaper_*), Pydantic models, and docstrings.
- Enforce: detection returns List[Signal], scoring returns ScoredSignal with score clamped 0.0-1.0, action returns ActionResult.
- Include a copy button and a small test stub snippet.
- Keep layout clean and keyboard-friendly.
```

## 2) Mission Config Builder

**Use case**
Create and validate mission configs for multi-source monitoring without hand-writing YAML.

**Spark app concept**
A YAML builder with inline validation and sample preview.

**Prompt**
```
Create a web app that builds REAPER mission YAML files.
- Sections: sources, schedule, scoring thresholds, action routing, output targets.
- Provide live YAML preview and validation messages.
- Include example presets for GitHub issues, log analyzer, and reddit monitor.
- Export as .yaml and show a copy-to-clipboard button.
```

## 3) Signal Simulator

**Use case**
Generate test signals to validate pipelines and scoring plugins.

**Spark app concept**
A simulator UI that outputs JSON arrays matching Signal schema.

**Prompt**
```
Make a signal simulator for REAPER.
- Let users choose sense type and generate N signals.
- Allow editing source, timestamp, raw_data, and metadata fields.
- Validate against the Signal schema and show errors.
- Export as JSON compatible with sample_signals inputs.
```

## 4) Score Tuning Sandbox

**Use case**
Experiment with scoring rules and observe how scores change on real or simulated signals.

**Spark app concept**
An interactive scoring editor with sliders and rule previews.

**Prompt**
```
Build a scoring sandbox for REAPER.
- Upload or paste Signal JSON.
- Provide a scoring rule editor (weights, thresholds, tags).
- Show computed score per signal and flag scores outside 0.0-1.0.
- Export derived ScoredSignal JSON.
```

## 5) Action Routing Planner

**Use case**
Define which actions trigger for which tags or score ranges.

**Spark app concept**
A rule matrix editor that outputs configuration for action execution.

**Prompt**
```
Create an action routing planner for REAPER.
- Inputs: action types, score ranges, tag filters.
- Visual rule table with add/remove rows.
- Export a JSON/YAML mapping.
- Include a test mode that runs sample ScoredSignals through the rules and shows matches.
```

## 6) Plugin Compliance Checker

**Use case**
Verify that plugins follow the exact hook names and return types.

**Spark app concept**
Paste-in code analyzer with lint-like feedback.

**Prompt**
```
Build a REAPER plugin compliance checker.
- Users paste Python plugin code.
- Detect hook names and validate exact spelling.
- Check for @hookimpl usage and return type hints.
- Warn if source is hard-coded or if hooks mix roles.
- Provide a clear checklist of pass/fail items.
```

## 7) Operator Console Prototype

**Use case**
Prototype dashboards for operators without full backend integration.

**Spark app concept**
A front-end mock console that renders pipeline activity with sample data.

**Prompt**
```
Create a REAPER operator console prototype.
- Show panels for each sense with recent signals.
- Provide filters by sense, source, and score.
- Include a timeline view and a details drawer.
- Use mock data but keep the schema compatible with Signal and ScoredSignal.
```

## 8) Incident Narrative Builder

**Use case**
Generate incident summaries from scored signals and actions for reporting.

**Spark app concept**
A narrative composer that turns selected signals into a report.

**Prompt**
```
Build an incident narrative builder for REAPER.
- Inputs: ScoredSignal JSON and ActionResult JSON.
- Output: a structured report with timeline, key signals, scores, and actions taken.
- Allow export to Markdown and PDF.
```

## 9) Pipeline Coverage Explorer

**Use case**
Understand which sources and senses are covered by plugins and tests.

**Spark app concept**
A coverage map UI with plugin and test inventory.

**Prompt**
```
Create a REAPER pipeline coverage explorer.
- Inputs: list of plugins and tests (manual entry or paste).
- Visualize coverage by sense and role.
- Highlight gaps and suggest missing tests.
- Export a coverage summary Markdown.
```

## 10) Performance Benchmark Viewer

**Use case**
View and compare benchmark runs to track regressions.

**Spark app concept**
A simple charting UI for performance logs.

**Prompt**
```
Build a benchmark viewer for REAPER.
- Paste benchmark output or upload JSON/CSV.
- Plot latency and throughput trends.
- Compare multiple runs and flag regressions.
- Export charts as PNG and summary as Markdown.
```

## 11) Documentation Quickstart Generator

**Use case**
Generate tailored onboarding steps for different plugin types.

**Spark app concept**
A doc generator that produces a quickstart section.

**Prompt**
```
Create a REAPER quickstart generator.
- Select plugin type (detect/score/action) and sense.
- Output a short setup guide, example code, and testing steps.
- Keep code compatible with pluggy and Pydantic v2.
```

## 12) Multi-Source Monitor Builder

**Use case**
Design a monitoring app that consolidates multiple sources into the pipeline.

**Spark app concept**
A wizard that builds a configuration and monitoring UI.

**Prompt**
```
Build a multi-source monitor builder for REAPER.
- Step 1: define sources and sense mapping.
- Step 2: set scoring thresholds and routing.
- Step 3: generate a configuration file and a minimal dashboard view.
- Provide copy/export for both.
```

---

## Suggested Next Steps

- Decide which 2-3 Spark apps to prototype first based on current roadmap priorities.
- Add links to the chosen prompts in public docs or README for easy discovery.
