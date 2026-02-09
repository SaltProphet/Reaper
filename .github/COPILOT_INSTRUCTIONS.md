# 🧬 Reaper Project: Copilot & Agent Instructions

**Repo:** SaltProphet/Reaper  
**Purpose:** Modular, plugin-driven, Python pipeline for detecting and solving "problem friction" — built for extensibility, type-safety, and actionable solutions.

---

## 🚦 Vision: What is Reaper For?

> **Reaper is not just eyes and alarms—it's hands and brains.**
>
> **Mission:**  
> Reaper exists to find, score, and solve real problems—harvesting friction (inefficiencies, bugs, pain points) and always driving toward concrete, actionable remediation.

Every pipeline must move through:  
**Detection _→_ Scoring _→_ Solution/Action**  
- **Detection** plugins describe and contextualize problems.
- **Scoring** plugins rank/prioritize detected signals by impact.
- **Action** plugins provide or trigger *real, helpful solutions* (code fix, remediation, notification…).

---

## 🤖 Copilot's Role & Focus

**Copilot is your modular code architect and writing assistant:**

### DO:
- Write or extend strictly modular, single-purpose plugins (detect, score, or act).
- Use **Pluggy** for all plugin hooks (no hard-coding sources/logic).
- Use **Pydantic v2** for type-safe, validated data models.
- Adhere to strict separation of pipeline stages (no role-mixing).
- Generate full test coverage for every plugin, model, and expected pipeline path.
- Draft clear docstrings and user-oriented documentation.
- When suggesting action plugins, focus on *real solutions* (automated remediations, actionable suggestions, or operational tasks).
- Ensure the pipeline output always delivers operator/user-relevant results (not just logs or errors).
- Suggest tangible next steps: "How can this solution be made more automatic, safe, or impactful?"

### DON'T:
- ❌ **Do not** hard-code sources, scoring logic, or action targets in the core.
- ❌ **Do not** invent, rename, or misspell any plugin hook names.
- ❌ **Do not** mix detection, scoring, and action logic; each plugin = one and only one role.
- ❌ **Do not** bypass, ignore, or duplicate strictly typed Pydantic models.
- ❌ **Do not** suggest orchestration, agent, app, CLI, or UI code here.
- ❌ **Do not** add dependencies or complexity outside this modular, biological, friction-sensing theme.
- ❌ **Do not** let the pipeline "end" at detection: every pipeline must produce actionable solution outputs.
- ❌ **Do not** write "action" plugins that just log, report, or restate issues with no attempt to solve.

---

## 🔬 Critical Hook Names

You **must only use** the following, spelled exactly:
```
reaper_sight_detect
reaper_hearing_detect
reaper_touch_detect
reaper_taste_detect
reaper_smell_detect
reaper_score_signal
reaper_action_execute
```

---

## Agent/App Roles vs. Copilot's Role

| Role      | Should Do…                               | Should NOT Do…                               |
|-----------|------------------------------------------|----------------------------------------------|
| Copilot   | Write plugins and Pydantic models;       | App/agent orchestration, IO, or end-user UI  |
|           | Generate tests and docs;                 | Hard-code, role-mix, or add external deps    |
|           | Refactor for modularity/extensibility    | Write general/unfocused or off-theme code    |
| Agent/App | Orchestrate, chain, and run plugins;     | Alter plugin API/design, write core plugins  |
|           | Provide operator interface, pipeline IO  | Tangle detection, scoring, and action roles  |

- **Copilot:** Keeps the repo core pure, modular, and solution-focused.
- **Agents/Apps:** Use plugins to build real-world workflows, user interfaces, and orchestration _outside_ the core.

---

## 🧬 Architectural Philosophy — The Reaper Way

1. **Everything is a plugin. No logic hard-coded in the core.**
2. **One plugin, one role:** detection, scoring, or action—never combined.
3. **All models are strict Pydantic v2, with complete validation.**
4. **Extensibility:** New plugins can be added without altering the core.
5. **Every pipeline finds friction and strives to resolve it, not just report it.**

---

## ✍️ Example: Detection, Scoring, and Action Plugins

```python
import pluggy
from reaper.models import Signal, ScoredSignal, ActionResult, SenseType

hookimpl = pluggy.HookimplMarker("reaper")

# Detection plugin
class QueryDetector:
    @hookimpl
    def reaper_hearing_detect(self, source: str):
        """Detects slow DB queries from a given source."""
        return [Signal(sense_type=SenseType.HEARING, source=source, details="Slow query found")]

# Scoring plugin
class QueryScorer:
    @hookimpl
    def reaper_score_signal(self, signal: Signal):
        """Scores signal severity by duration/impact."""
        # Custom scoring logic...
        return ScoredSignal(signal=signal, score=0.8, analysis={"duration_ms": 1200})

# Action plugin
class QueryOptimizer:
    @hookimpl
    def reaper_action_execute(self, scored_signal: ScoredSignal):
        """Attempts to optimize or notifies about bad query."""
        # Fix query or notify dev; always actionable/remediation
        return ActionResult(scored_signal=scored_signal, result="Index suggestion sent to developer")
```

---

## 🧪 Example: Test (must always show an actual solution path)

```python
def test_query_pipeline_solves_problem():
    detector = QueryDetector()
    scorer = QueryScorer()
    optimizer = QueryOptimizer()
    signals = detector.reaper_hearing_detect("db_source")
    for signal in signals:
        scored = scorer.reaper_score_signal(signal)
        action = optimizer.reaper_action_execute(scored)
        assert "suggestion" in action.result or "fixed" in action.result
```

---

## 📚 For All Contributors & Copilot

- **Always drive plugins and pipeline examples to actionable solutions.**
- **Check this file, README, and CONTRIBUTING for updated best practices and new hooks/models.**
- **Document everything as if for a new contributor.**

#### If ever in doubt:  
"Build the modular pieces, never the whole machine. Never stop at problem discovery—always carry to solution."  

---
