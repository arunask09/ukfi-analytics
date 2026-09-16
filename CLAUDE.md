# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Install deps: `uv sync --dev`
- Lint: `make lint` (`uv run ruff check .` then `uv run mypy src` — mypy runs in strict mode)
- Format: `make fmt` (`uv run ruff format .`)
- Test: `make test` (`uv run pytest`)
- Single test: `uv run pytest tests/test_smoke.py::test_package_imports` (or `-k <name>`)
- CI (`.github/workflows/ci.yml`) runs the same three checks in order: ruff check, mypy src, pytest — keep local runs matching that order before pushing.

## Architecture

The repo is at milestone **M0 (conventions engine, `v0.1`)** — `src/ukfi_analytics/` is still a
skeleton (`__init__.py` with a placeholder `main()`, wired as the `ukfi-analytics` console script
in `pyproject.toml`). Real modules land incrementally, one milestone at a time; check the
checklist in README.md before assuming a component (curve bootstrapper, pricing engine, risk
calc, etc.) already exists.

**Milestone roadmap** (full rationale in `docs/PLAN.md`, live status in README.md's checklist):
M0 conventions engine (`daycount.py`, `calendar.py`, schedule generation) → M1 bond analytics +
a bitemporal SQL point-in-time store (raw window functions/as-of joins, not an ORM) → M2 curve
diagnostics → M3 multi-curve bootstrap + Jacobian risk → M4 pricing & P&L explain → M5 production
release (FastAPI service, CLI, Docker). Vol models (SABR/Hull-White) and portfolio VaR/FRTB are
deliberately deferred past `v1.0`.

**Data & methodology constraint — applies to any code added here:**
- Public data only: Bank of England published yield curves (scriptable/fetched incrementally),
  UK DMO gilt reference data (manual download, cached locally, **never committed** — no open
  licence).
- QuantLib is the sole pricing/risk oracle — new pricing or curve logic should be checked against
  it, with parity differences tracked as a committed diff table, not left implicit.
- CDS spreads and swaption vols aren't freely available — when needed, synthesise them and label
  them loudly as synthetic; never present them as real market data.
- No data, code, config, or convention from any employer or production system may enter this
  repo, at any point.

**Top-level `scratch_*.py` files** (`scratch_tour.py`, `scratch_unexplained_pnl.py`) are hands-on
exercises from the author's mentorship curriculum, not part of the shipped package. They contain
intentional `TODO`s for the author to complete — don't silently "fix" or finish them unless
explicitly asked to.
