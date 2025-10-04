# Repository Guidelines

This guide keeps contributions consistent across the multi-agent research platform. Read it before opening a pull request so new work slots cleanly into the existing orchestration pipeline.

## Project Structure & Module Organization
- `main.py` boots the demo workflow and wires agents via the A2A protocol.
- `agents/` holds orchestrator, domain, and fact-checking agents; each subfolder contains the agent implementation and its README.
- `tools/` defines discovery, execution, and concrete tools (web search, document parsing, statistical analysis).
- `a2a_protocol.py` and `llm_interface.py` provide shared messaging and Gemini LLM access.
- `config/` contains runtime presets; `tests/` mirrors the agent/tool split with `unit/` and `integration/` suites.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` sets up an isolated environment.
- `pip install google-generativeai` installs the primary external dependency; add any extras to project documentation.
- `python main.py --query "Analyze the impact of AI on healthcare"` runs the orchestrated demo.
- `pytest` executes the full suite with verbose, fail-fast settings from `pytest.ini`.
- `pytest -m "unit"` or `pytest -m "integration"` targets a specific layer; pair with `-k agent_name` to narrow a run during debugging.

## Coding Style & Naming Conventions
Use Python 3.7+ with 4-space indentation, module-level `snake_case`, class `PascalCase`, and constant `UPPER_CASE`. Annotate public methods with type hints where practical, keep docstrings focused on behavior, and prefer explicit imports over wildcard patterns. Mirror existing logging patterns when adding agent interactions.

## Testing Guidelines
Add tests alongside code under `tests/unit` or `tests/integration` and respect the discovery rules defined in `pytest.ini`. Mark long-running cases with `@pytest.mark.slow` so contributors can exclude them via `-m "not slow"`. When extending orchestrator flows, assert both tool selection and message routing. Regenerate coverage reports with `pytest --cov=.` when available and leave `htmlcov/` out of version control.

## Commit & Pull Request Guidelines
Follow the current history: concise, sentence-case subjects that summarize the change (e.g., `Improve test coverage for multi-agent system`). Reference related issues in the body, describe agent or tool impacts, and call out new configuration flags. PRs should list verification steps, note any mocked Gemini calls, and include screenshots or transcripts when UI or messaging output changes.

## Environment & Secrets
Set `GOOGLE_API_KEY` (and optionally `GEMINI_MODEL`) in your shell before running against the real Gemini service. Never commit keys; prefer `.env` files kept outside the repo and document fallback defaults in the PR description.
