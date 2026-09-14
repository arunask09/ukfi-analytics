# The plan behind the roadmap

This is the full detail behind the milestone table in the [README](../README.md): why the repo
is built this way, the weekly cadence, and what each release actually contains. Source of truth
for status is the README's checklist; this page explains the reasoning.

## Mission

The end goal is a role as a **quant developer on a rates & credit desk** — someone who builds and
maintains the pricing/risk analytics library, not just consumes its output. The route there is a
working library, not a certificate: curves → pricing → risk → P&L explain, for UK gilts,
SONIA/OIS swaps, the Long Gilt future, and single-name & index CDS.

The decision that shapes everything here: **build the capstone from week one**, incrementally, so
each phase of learning lands in this repo as a milestone as it happens, rather than all at once
at the end.

Target firms: multi-asset/fixed-income desks (Jane Street, Citadel/Citadel Securities, DRW, Two
Sigma, HRT-type) where this repo is a direct edge, and market-making shops (Optiver, IMC, SIG,
Akuna-type) where DSA and probability speed matter more than FI depth — see Thread 3, below.

## What v1.0 actually does

The M5 "done when" bar, concretely:

```bash
git clone github.com/arunask09/ukfi-analytics && cd ukfi-analytics
docker compose up
```

That one command, on a clean machine, runs a full cycle:

1. **Ingest a dated snapshot** — async pull of the day's BoE curve data plus a cached DMO gilt
   reference, point-in-time, no look-ahead possible by construction.
2. **Build the curves** — SONIA discount + projection, plus a credit survival curve from
   (synthesised) CDS quotes. Every calibration input re-prices to ~zero, checked automatically.
3. **Price the book** — gilts, SONIA swaps, the Long Gilt future, single-name/index CDS, one
   swaption if 2028's vol work lands early. Risk computed both analytically and by
   bump-and-revalue, in parallel, with a measurement of which won.
4. **P&L explain** — carry + roll + curve move + spread move + residual vs. yesterday. A residual
   spike should be traceable to a named cause.
5. **Export** — an Excel risk pack (how a desk actually consumes numbers) plus the same report
   queryable via the API.
6. **Reconcile** — a daily job diffs today's run against the prior one and flags anything outside
   tolerance; an incident runbook is what you follow if it does.

Shipping alongside the running system, not bolted on after: a golden-value regression suite, a
QuantLib benchmark diff table, semantic model versioning, an architecture-decision-record (ADR)
log, and structured logging.

**Not at v1.0:** SABR / Hull–White / Bermudans and portfolio VaR/FRTB — deferred to 2028, dropped
for hours, not importance.

## The three threads, every week

Not sequential blocks — the build, maths, and DSA run together every week (~10 core hours),
because fluency in the latter two is time-under-tension, not intensity.

| Thread | Hours/wk | What |
|---|---|---|
| **The build** | 6.5 | Evenings & weekends, home machine. Implementation, tests, the applied maths the current milestone needs. |
| **Maths** | 2.0 | Strand A (1¼h) — sequenced just ahead of the build: day-count now, linear algebra for M1, stochastic calculus from Apr '27. Strand B (¾h) — Zhou/Crack/Mosteller, interview probability, from month one. |
| **DSA** | 1.5 | 2 timed problems/week, ~15 core patterns, ~130 problems over 15 months. The auto-graded screen that runs before anyone opens the repo — minimum effective dose, spaced not crammed. |

## Two environments

The day splits itself: ~13–18 hrs/week total.

| | When | Hours/wk | Machine | Work that fits |
|---|---|---|---|---|
| **Office** | Mon–Fri downtime | 5–10 | Work machine | FI theory, maths theory, DSA, interview probability — **no repo, no code, no commits** |
| **Home** | Evenings + weekend | 8–10 | Personal machine | The build — implementation, tests, applied maths, commits, PRs |

## Two rules, non-negotiable

**Clean room.** Nothing from work — no data, code, configs, conventions, or benchmarking against
a production system. Public data in, QuantLib as the only oracle. BoE yield curves are scriptable
and verified; DMO gilt data is a manual download, cached locally and never committed (their terms
carry no open licence); CDS spreads and swaption vol are synthesised and labelled loudly.

**Work machine.** The repo never touches company equipment. Most employment contracts claim IP
for anything built on company hardware or time — a finance-adjacent public repo is exactly what
those clauses target. Office hours are reading and paper problems only.

## Reading, bought just-in-time

No stack bought up front — each book lands right before the milestone that needs it.

| When | Book | For |
|---|---|---|
| Now | Tuckman & Serrat, *Fixed Income Securities* 4e | Office reading — the FI book for the whole plan |
| Now | Zhou, *A Practical Guide to Quantitative Finance Interviews* | The probability strand — starts month one because it compounds |
| Now (free) | McKinney, *Python for Data Analysis* 3e | M1/M2 pandas |
| M0 | Ramalho, *Fluent Python* 2e (2022 ed.) | Deep language knowledge — the biggest gap on the shelf |
| M2 (free) | Blitzstein & Hwang, *Introduction to Probability* + Stat 110 | The probability gap, properly |
| M2 → | Baxter & Rennie, *Financial Calculus* | Stochastic calculus for implementers (not Shreve — no numerics) |
| M3 | Henrard, *Interest Rate Modelling in the Multi-Curve Framework* | Precisely the M3 build |
| M3 → | Ballabio, *Implementing QuantLib* | Reading QuantLib internals well enough to land a PR |
| M4 | O'Kane, *Modelling Single-name and Multi-name Credit Derivatives* | Hazard rates, survival curves, CDS |
| Optional | Bhargava, *Grokking Algorithms* (~6 hrs) | The entire DSA reading budget |
| 2028, reference only | Andersen & Piterbarg, *Interest Rate Modeling* (3 vols) · Rebonato | Vol work — expensive, don't buy early |

## Success criteria for v1.0

1. CI green on `main`, golden-value regression suite included.
2. QuantLib parity wherever an equivalent exists — a committed diff table, not a claim.
3. Invariants hold: calibration inputs re-price to ~zero, analytic risk agrees with bumped risk,
   look-ahead is impossible by construction.
4. `docker compose up` on a clean machine reproduces a full curve-to-report run.
5. The coverage audit passes at a whiteboard, without notes.

The honest test: hand the repo to an experienced rates quant and have them fail to find a number
they can't trace back to an input, a convention, and a test.
