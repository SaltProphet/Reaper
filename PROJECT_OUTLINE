# Project Overview

**REAPER** (Universal Problem Engine) — A source-agnostic ETL system for extracting "friction points" from any data source.

**Core Principle:** Treat every input as a generic "Blob" that gets sanitized and classified by the Logic Gatekeeper.

---

## Key Architectural Decisions

### 1. GitHub Copilot Native Integration

**Use Native Agents, Not Just Prompts:**

- Use `@workspace` agent to auto-index entire file tree
- Use `@terminal` agent for immediate test feedback loops
- Keep `.github/[copilot-instructions.md](http://copilot-instructions.md)` as the "North Star" context file

**Why:** Context Space indexing ensures generated code is always aware of existing primitives (e.g., BaseIngestor knows about ReaperSignal without manual pasting)

### 2. Copilot Spark for Prototyping

**Rapid UI Development:**

- Use Spark to prototype "Solution Informant" UI
- Use Spark for "Market Arbitrage Dashboard" sandbox testing
- Test logic in isolated environment before committing to main repo

**Why:** Validate "Solvable Problem" logic without polluting the core Python backend

### 3. Source-Agnostic Design

**Universal Primitive Contract:**

- No hard-coded platforms (no Reddit, Twitter, etc.)
- All inputs are treated as generic "Blobs"
- Logic Gatekeeper sanitizes and classifies

**Why:** Prevents legacy pattern hallucination from old monolithic build

---

## Core Architecture

### The Universal Primitive: ReaperSignal

**File:** `reaper_factory/core/[primitives.py](http://primitives.py)`

**Pydantic v2 Data Contract:**

```python
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Dict, Any

class ReaperSignal(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    raw_payload: str
    sanitized_intent: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('raw_payload')
    def validate_friction_indicators(cls, v):
        # Must contain identifiable friction keywords
        # or indicators of inefficiency
        friction_keywords = [
            'cannot', 'broken', 'slow', 'error', 
            'failed', 'issue', 'problem', 'frustrating'
        ]
        if not any(keyword in v.lower() for keyword in friction_keywords):
            raise ValueError('raw_payload must contain friction indicators')
        return v
```

**Key Fields:**

- `id` — UUID for unique identification
- `timestamp` — UTC timestamp of capture
- `raw_payload` — Unprocessed input string
- `sanitized_intent` — Cleaned/classified text (post-gatekeeper)
- `metadata` — Source-agnostic context dictionary

---

### Plugin Architecture: BaseIngestor

**File:** `reaper_factory/core/base_[ingestor.py](http://ingestor.py)`

**Abstract Base Class Pattern:**

```python
from abc import ABC, abstractmethod
from typing import List
from reaper_factory.core.primitives import ReaperSignal

class BaseIngestor(ABC):
    
    @abstractmethod
    async def harvest(self) -> List[ReaperSignal]:
        """
        Extract friction signals from any data source.
        
        Returns:
            List of ReaperSignal objects
        """
        pass
```

**Design Constraints:**

- **Async-first** — All ingestors must be async
- **Source-agnostic** — No platform-specific logic in base class
- **Pluggable** — Discovered via pluggy plugin system

---

### Orchestration Engine: [main.py](http://main.py)

**File:** [`main.py`](http://main.py)

**Async Plugin Manager:**

```python
import asyncio
import pluggy
import structlog
from reaper_factory.core.base_ingestor import BaseIngestor

logger = structlog.get_logger()

class ReaperOrchestrator:
    def __init__(self):
        self.plugin_manager = pluggy.PluginManager("reaper")
        self.plugin_manager.add_hookspecs(BaseIngestor)
        self.plugin_manager.load_setuptools_entrypoints("reaper")
    
    async def run(self):
        # Discover all plugins from reaper_factory/plugins/
        ingestors = self.plugin_manager.hook.get_ingestors()
        
        logger.info("Starting harvest", ingestor_count=len(ingestors))
        
        # Execute all ingestors concurrently
        results = await asyncio.gather(
            *[ingestor.harvest() for ingestor in ingestors],
            return_exceptions=True
        )
        
        # Log results
        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error("Ingestor failed", 
                           ingestor=ingestors[idx].__class__.__name__,
                           error=str(result))
            else:
                logger.info("Harvest complete",
                          ingestor=ingestors[idx].__class__.__name__,
                          signal_count=len(result))
        
        return results

if __name__ == "__main__":
    orchestrator = ReaperOrchestrator()
    asyncio.run(orchestrator.run())
```

**Key Features:**

- **Pluggy plugin system** — Auto-discovers plugins
- **Concurrent execution** — `asyncio.gather` for parallel harvesting
- **Resilient** — `return_exceptions=True` prevents one failure from killing all
- **Structured logging** — `structlog` for production observability

---

## Tech Stack

### Core Dependencies

**Python 3.11+**

- Async/await native patterns
- Type hints and dataclasses

**Data Contracts:**

- **Pydantic v2** — Data validation and serialization
- Validators for friction keyword detection

**Database:**

- **SQLAlchemy 2.0** — Async ORM
- Universal schema for signal storage

**Web Scraping:**

- **Playwright** — Async browser automation
- Handles JavaScript-rendered content

**Plugin System:**

- **pluggy** — Hook-based plugin architecture
- Same system used by pytest

**Logging:**

- **structlog** — Structured, contextual logging
- JSON output for production parsing

**Async Runtime:**

- **asyncio** — Native Python async orchestration
- `gather()` for concurrent execution

---

## Repository Structure

```
REAPER/
├── .github/
│   └── copilot-instructions.md    # North Star context file
├── reaper_factory/
│   ├── core/
│   │   ├── primitives.py          # ReaperSignal definition
│   │   ├── base_ingestor.py       # ABC for all plugins
│   │   └── validator.py           # Logic Gatekeeper
│   ├── plugins/
│   │   ├── __init__.py
│   │   └── [dynamic discovery]    # Plugin ingestors
│   └── __init__.py
├── tests/
│   ├── test_primitives.py
│   ├── test_ingestors.py
│   └── test_orchestrator.py
├── main.py                        # Async orchestrator
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## GitHub Copilot Workflow

### 1. Context Management

**`.github/[copilot-instructions.md](http://copilot-instructions.md)`**

This file is the "North Star" — loaded into every Copilot session:

```markdown
# REAPER Project Context

## Mission
Universal Problem Engine — Extract friction points from ANY data source.

## Core Constraints
- Source-agnostic design (no hard-coded platforms)
- All inputs are "Blobs" sanitized by Logic Gatekeeper
- Async-first architecture
- Plugin-based extensibility

## Primitives
- ReaperSignal: Universal data contract (Pydantic v2)
- BaseIngestor: ABC for all data sources

## Tech Stack
- Python 3.11+
- Pydantic v2, SQLAlchemy 2.0, Playwright, pluggy, structlog
```

### 2. Using Native Agents

**@workspace Agent:**

- Automatically indexes all files
- Code generation is context-aware
- No need to manually paste primitives

**Example:**

```
@workspace Implement a WebIngestor plugin that extends BaseIngestor
and scrapes forum pages for friction signals.
```

**@terminal Agent:**

- Run tests immediately after code generation
- Closed feedback loop: write → test → fix → repeat

**Example:**

```
@terminal Run pytest tests/test_primitives.py -v
```

### 3. Prompt Engineering (The 4 S's)

**Structured:**

- Clear role/persona definition
- Technical specifications in numbered lists

**Specific:**

- Exact file paths
- Explicit library versions (Pydantic v2, not just Pydantic)

**Short:**

- High-density library names
- Directives, not conversational narratives

**Source-referenced:**

- Use `@workspace` to reference existing code
- Use file paths instead of describing code

---

## The "First Move" Prompt

**Use this in GitHub Copilot Chat to bootstrap the repo:**

```
@workspace /new 
Persona: Lead System Architect
Project: REAPER (Universal Problem Engine)
Task: Implement the core ETL orchestration and the 'Universal Primitive' data contract.

Technical Specifications:
1. Define 'reaper_factory/core/primitives.py' using Pydantic v2. Implement the 'ReaperSignal' class with fields: id (UUID), timestamp (UTC), raw_payload (str), sanitized_intent (Optional[str]), and a 'metadata' dictionary. Include a validation method to ensure the 'raw_payload' contains identifiable 'friction' keywords or indicators of inefficiency.

2. Implement 'reaper_factory/core/base_ingestor.py' as an Abstract Base Class (ABC) using the 'abc' module. Define an 'async def harvest()' method that returns a list of 'ReaperSignal' objects.

3. Implement 'main.py' as an asynchronous orchestrator. Use the 'pluggy' library to create a plugin manager. It must:
    - Load all discovered plugins from the 'reaper_factory/plugins/' directory.
    - Execute 'harvest()' concurrently across all loaded ingestors using 'asyncio.gather'.
    - Log results using the 'structlog' library.

4. Logic Constraint: All modules must be source-agnostic. No references to Reddit, specific APIs, or hard-coded platforms. The system must treat every input as a generic 'Blob' to be sanitized by the Logic Gatekeeper.

Format: Provide the file structure and the complete, production-ready code for these three files. Use high-density, asynchronous Python 3.11 patterns.
```

---

## Strategy for Tool Utilization

### Context Control

**Keep `.github/[copilot-instructions.md](http://copilot-instructions.md)` updated:**

- Every Copilot session loads this automatically
- Ensures "Universal" definition is always in context
- No more Reddit-specific hallucinations

### The Sanitization Loop

**Use @terminal for immediate feedback:**

1. @workspace generates Validator logic
2. @terminal runs pytest tests/test_[validator.py](http://validator.py)
3. Review errors
4. @workspace fixes based on test output
5. Repeat until green

### Multi-Repo Access

**Testing against Target Silos:**

- Use IDE's "Add Folder to Workspace" feature
- @workspace can cross-reference Reaper logic against Target data
- No need for manual `git clone` inside repo

---

## Next Steps

1. **Initialize clean repo**
2. **Create `.github/[copilot-instructions.md](http://copilot-instructions.md)`** with North Star context
3. **Run "First Move" prompt** in GitHub Copilot Chat
4. **Use @terminal** to validate generated code
5. **Iterate** with @workspace for plugin development

---

**Key Insight:** This architecture eliminates all platform-specific coupling from the old monolithic build. Every component is now a pluggable, testable unit that operates on the universal ReaperSignal primitive.