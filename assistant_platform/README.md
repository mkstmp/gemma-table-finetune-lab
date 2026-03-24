# Assistant Platform V1

A modular, multi-agent consumer assistant platform with deterministic tool execution.

## Quickstart

```bash
cd assistant_platform
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
uvicorn assistant_platform.api.app:app --reload
```

## Implemented in this build
- Full repository skeleton from spec
- Shared schemas and tool registry
- Skill loader + validator
- Entity extraction + hybrid router
- Dialogue, policy, tool executor, orchestrator agents
- Phase 1 tools: time/date, weather (stub provider), reminders, utilities
- API chat endpoint and tests
