# ukfi-analytics

![CI](https://github.com/arunask09/ukfi-analytics/actions/workflows/ci.yml/badge.svg)

A UK fixed-income pricing and risk analytics library — gilts, SONIA/OIS swaps, the Long Gilt
future, and single-name/index CDS — built incrementally and in public, `v0.1` through `v1.0`.

## Why this exists

The end goal is a curve-to-report pipeline you could hand to an experienced rates quant and have
them fail to find a number that isn't traceable to an input, a convention, and a test. Each
milestone below lands in this repo as it's built, rather than arriving all at once at the end.

## Data & methodology

**Public data only, QuantLib as the sole benchmark.**

- Yield curves — [Bank of England](https://www.bankofengland.co.uk/statistics/yield-curves)
  published SONIA OIS, nominal and real gilt curves. Scriptable, fetched incrementally.
- Gilt reference data — UK DMO, downloaded manually (their bot protection is intentionally not
  bypassed) and cached locally; never committed, since DMO's terms carry no open licence.
- CDS spreads and swaption volatility surfaces are **not** freely available. Where used, they are
  **synthesised and labelled clearly** — never presented as real market data.
- No data, code, configuration, or convention from any employer or production system, at any
  point in this project.

## Roadmap

| Milestone | Dates | Release | Delivers |
|---|---|---|---|
| **M0 — Conventions engine** *(current)* | Sep–Dec 2026 | `v0.1` | Repo skeleton, `daycount.py`, `calendar.py`, schedule generation, QuantLib parity table |
| M1 — Bond analytics + point-in-time store | Jan–Apr 2027 | `v0.2` | Clean/dirty pricing, YTM, spread measures, a bitemporal store with look-ahead impossible by construction |
| M2 — Curve diagnostics lab ★ | Apr–Jun 2027 | — | Interpolation-artefact study, PCA of the gilt curve, the Sept 2022 LDI crisis from public history |
| M3 — Multi-curve bootstrapper + Jacobian risk ★★ | Jun–Sep 2027 | `v0.5` | SONIA discount + projection curves, global calibration, analytic dPV/dQuote risk |
| M4 — Pricing & P&L explain ★★ | Sep–Nov 2027 | `v0.6` | Bond/swap/future/CDS risk, P&L explain (carry + roll + curve + spread + residual) |
| M5 — Production release ★★ | Nov–Dec 2027 (+reserve) | `v1.0` | FastAPI service, CLI, Docker, parallel batch risk, DuckDB/Polars, ADR log, incident runbook |

★★ = the milestones a rates quant-dev interview is actually won on. ★ = showable along the way.
Volatility/derivatives models (SABR, Hull–White) and portfolio VaR/FRTB are deferred to 2028 —
dropped for hours, not importance.

Full milestone detail, the weekly build/maths/DSA cadence, and the reading list behind this
roadmap: **[docs/PLAN.md](docs/PLAN.md)**.

## Current status (14 Sep 2026)

- [x] Repo skeleton — `uv`, `ruff`, `mypy` (strict), `pytest`, CI green
- [ ] `daycount.py` — ACT/365F, ACT/ACT-ICMA, 30/360, business/252
- [ ] `calendar.py` — UK/BoE holidays, business-day arithmetic
- [ ] QuantLib parity table
- [ ] Property tests (Hypothesis) over conventions

## Success criteria for v1.0

1. CI green on `main`, golden-value regression suite included.
2. QuantLib parity wherever an equivalent exists — a committed diff table, not a claim.
3. Invariants hold: calibration inputs re-price to ~zero, analytic risk agrees with bumped risk,
   look-ahead is impossible by construction.
4. `docker compose up` on a clean machine reproduces a full curve-to-report run.
5. The coverage audit passes at a whiteboard, without notes.

## Running it

```bash
uv sync --dev
make lint
make test
```

## License

MIT — see [LICENSE](LICENSE).
