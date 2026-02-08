# The Architect's Curse

## A Philosophy of Functional Autonomy

> "The architect who designs a cathedral doesn't micromanage each stone's placement. Instead, they establish principles, boundaries, and patterns—then trust the builders to embody the vision."

## The Curse

Every architect faces the same curse: **the gap between vision and execution**.

You see the elegant system in your mind—modular, extensible, beautifully abstracted. But then reality hits: tight deadlines, unclear requirements, the temptation to "just hard-code it for now." Before you know it, the cathedral becomes a shack patched together with duct tape.

REAPER exists to fight this curse.

## Functional Autonomy

**Functional autonomy** means each component:
- Knows its **single responsibility** and nothing more
- Operates **independently** without relying on implementation details of other components  
- Respects **boundaries** and never crosses into another component's domain
- Embodies a **worldview** through its interface, not its internals

### The Worldview

In REAPER, the worldview is biological:
- **Senses** detect signals from the environment (Sight, Hearing, Touch, Taste, Smell)
- **Scoring** evaluates signal significance
- **Actions** respond to high-priority signals

This isn't just a metaphor—it's an architectural constraint that prevents the mixing of concerns.

### Why Worldview Matters

A strong worldview acts as an **immune system** against architectural decay:

❌ **Without Worldview:**
```python
class DataProcessor:
    def process(self, data):
        # Detects, scores, and acts - all in one!
        signals = self.detect(data)
        for s in signals:
            score = self.score(s)
            if score > 0.8:
                self.alert(s)
```

This violates functional autonomy. When detection, scoring, and action are mixed:
- Testing becomes impossible (can't test detection without triggering actions)
- Changes ripple (modify scoring, break detection)
- Reuse is blocked (can't swap detection without rewriting actions)

✅ **With Worldview:**
```python
# Detection: Only senses, never judges or acts
class SightPlugin:
    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        return self.detect_visual(source)

# Scoring: Only judges, never senses or acts  
class Scorer:
    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        return ScoredSignal(signal=signal, score=self.analyze(signal))

# Action: Only acts, never senses or judges
class Action:
    @hookimpl
    def reaper_action_execute(self, scored: ScoredSignal) -> ActionResult:
        return self.alert_if_urgent(scored)
```

Now each component is:
- **Testable** in isolation
- **Swappable** without affecting others
- **Composable** in any configuration
- **Understandable** at a glance

## The Boundaries

Boundaries aren't constraints—they're **liberations**.

When you know your lane, you're free to optimize within it without fear of breaking something elsewhere.

### Sense Boundaries

Each sense has a clear input type:
- **Sight**: Visual/UI data
- **Hearing**: Text/audio data  
- **Touch**: Interaction/event data
- **Taste**: Quality/metric data
- **Smell**: Pattern/trend data

**The Rule:** A sense plugin converts its input type into `Signal` objects. Nothing more, nothing less.

### Scoring Boundaries

Scorers receive `Signal` objects and return `ScoredSignal` objects. They:
- ✅ Analyze signal content
- ✅ Calculate priority scores
- ✅ Add metadata and tags
- ❌ Never fetch new data
- ❌ Never execute actions
- ❌ Never modify the original signal

### Action Boundaries

Actions receive `ScoredSignal` objects and return `ActionResult` objects. They:
- ✅ Execute side effects (alerts, logs, API calls)
- ✅ Handle failures gracefully
- ✅ Return success/failure status
- ❌ Never detect new signals
- ❌ Never re-score signals
- ❌ Never modify scoring logic

## The Plugin Contract

REAPER uses [Pluggy](https://pluggy.readthedocs.io/) to enforce contracts through **hook specifications**.

### Why Contracts Matter

Contracts are promises:
- "If you give me X, I'll return Y"
- "I won't do Z, ever"
- "You can trust my output format"

Without contracts, every integration is a negotiation. With them, plugins Just Work™.

### The Three Guarantees

**1. Interface Stability**
```python
@hookspec
def reaper_sight_detect(self, source: str) -> List[Signal]:
    """This signature will never change."""
```

**2. No Hard-Coding**
```python
# ❌ NEVER
def reaper_sight_detect(self, source: str) -> List[Signal]:
    return fetch_from("https://reddit.com/r/programming")

# ✅ ALWAYS  
def reaper_sight_detect(self, source: str) -> List[Signal]:
    return fetch_from(source)  # source is parameterized
```

**3. Type Safety**
```python
# Pydantic ensures this at runtime
signal = Signal(
    sense_type=SenseType.SIGHT,
    source="my-source",
    raw_data={"content": "..."}
)
# Invalid? Pydantic raises ValidationError immediately
```

## Embodiment: Living the Architecture

The curse isn't broken by **documentation**—it's broken by **embodiment**.

Every contributor must internalize these principles:

### Muscle Memory Questions

Before writing code, ask:
1. **Which boundary am I in?** (Detection / Scoring / Action)
2. **Am I crossing boundaries?** (Mixing concerns)
3. **Am I hard-coding sources?** (Violating parameterization)
4. **Does this match the worldview?** (Is this truly a "sense"?)

### Code Review Mantras

When reviewing PRs:
1. "Can I test this in isolation?"
2. "Can I swap this plugin without breaking others?"
3. "Does this respect the sense boundaries?"
4. "Would a new contributor understand this in 30 seconds?"

### Refactoring Instinct

When you feel the urge to mix concerns:
- **Stop** ✋
- **Identify** the boundary violation
- **Separate** into proper components
- **Reconnect** through the plugin interface

## The Reward

When you embody functional autonomy, you unlock:

1. **Velocity**: Changes are surgical, not systemic
2. **Confidence**: Tests cover boundaries, not implementations  
3. **Onboarding**: New devs understand components in minutes
4. **Evolution**: Replace any piece without fear
5. **Joy**: Code that does one thing well is a pleasure to maintain

## The Vision Lives On

REAPER isn't just a pipeline—it's a **statement**:

> "Complex systems can be simple when each part knows its role."

Every plugin you write, every boundary you respect, every hard-coded value you parameterize—these are acts of architectural fidelity.

The curse is real, but so is the cure.

**Build components that embody the vision. Trust the system to compose them.**

---

## Practical Reminders

### For Plugin Authors

- One sense per detection plugin (or clearly separated multi-sense implementations)
- Return signals, don't act on them
- Parameterize everything (sources, thresholds, configs)
- Use Pydantic models for all data structures
- Handle errors gracefully (return empty lists, not exceptions)

### For Integrators

- Register plugins cleanly without modifying core
- Orchestrate pipelines in application layer, not plugins
- Trust plugin boundaries—don't reach into internals
- Test integrations with mock plugins first

### For Reviewers

- Check for sense isolation violations
- Verify no hard-coded sources
- Confirm proper Pydantic model usage
- Look for mixed concerns (detection + scoring, etc.)
- Ask: "Can I understand this in 30 seconds?"

### For Architects

- Maintain the biological metaphor
- Resist feature creep that blurs boundaries
- Document the "why" behind constraints
- Celebrate contributors who embody the principles
- Evolve carefully—some boundaries are sacred

## Further Reading

- [Sense Isolation FAQ](sense-isolation-faq.md) - Deep dive on boundary enforcement
- [How to Create Plugins](how-to-create-plugins.md) - Practical plugin development
- [Operator Console Walkthrough](operator-console-walkthrough.md) - Using the system

## Contributing to the Philosophy

Have insights on functional autonomy? Examples of architectural patterns that work (or don't)? 

Share them in [Discussions](https://github.com/SaltProphet/Reaper/discussions) under the `architecture` or `philosophy` tags.

The vision evolves through collective embodiment.

---

*"The architect's curse isn't that the vision fades—it's that we stop believing it's possible. REAPER proves it is."*
