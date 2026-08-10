# Prototype Fit — Capstone Brief Compliance

How SolarScan Verify's benchmark prototype maps to the capstone brief
requirements, with evidence paths. Written 2026-08-10.

---

## What the brief requires

> "At least one prototype that compares model performance on the same task:
> the same inputs run against several models, with judged results. This is
> the Project 1 method, applied to your capstone slice."
> "The prototype does not need to be the whole system. It needs to be real,
> tested, and honest about what it shows."

## Our prototype: the 30-image benchmark evaluation

| Brief requirement | Our prototype | Evidence |
|---|---|---|
| **Same inputs** | 30 rooftop images (19 test + 11 valid) from a CC-licensed public drone dataset; every model saw the identical images with the identical system prompt and temperature 0 | `data/benchmark-v1/labeling/subset-30.json`, `scripts/evaluate_benchmark.py` (single SYSTEM_PROMPT, `--subset`) |
| **Several models** | 4 models, 2 closed + 2 open-weights: GPT-5.5 (closed), Gemini 3.5 Flash-Lite (closed, cost baseline), Kimi K3 (open-weights, 2.8T), Gemma 4 26B (open-weights, Apache-2.0) | `docs/benchmark-results.md` §Models |
| **Judged results** | Ground truth locked by 3-labeler majority vote (14 solar / 16 no_solar / 0 uncertain); PRD §6 scorecard on all 30 cases | `data/benchmark-v1/ground-truth.json`, `docs/benchmark-results.md` §Scorecard |
| **Real** | 120 model calls executed; results in `data/benchmark-v1/results/*.json` (gitignored, reproducible via scripts) | `scripts/fetch_benchmark.py`, `scripts/evaluate_benchmark.py` |
| **Tested** | Pipeline verified end-to-end; image integrity SHA-256-checked; ad-hoc verification scripts on every change | `scripts/verify_image_integrity.py`, commit history |
| **Honest** | No model meets the PRD §6 target (best 83% vs 90% target); escalation recall now n/a (no ground-truth ties) — reported as-is | `docs/benchmark-results.md` §Findings |

## Project 1 method, applied

> "a fixed set of cases scored against an answer key you write first"

| P1 element | Our version |
|---|---|
| Fixed set of cases | 30 images (subset-30.json) — fixed before evaluation |
| Answer key written first | Human labels written before model runs; ground truth from 5 labelers |
| One baseline run | Gemini 3.5 Flash-Lite = cost baseline (cheapest closed model) |
| Two evaluations from baseline | **Quality**: clear-case accuracy (target ≥90%) · **Cost**: $/correct (Gemini $0.003, GPT-5.5 $0.013, Gemma $0.002) |
| At least one open-weights + one closed model | ✅ Kimi K3 + Gemma (open) vs GPT-5.5 + Gemini (closed) |
| P1 used six cases | We used 30 — a superset |

## Baseline → harder case testing

> "your testing: the baseline case and how it performed, then a harder case
> and how that performed"

Split the 30 roofs by 4-model agreement:
- **Baseline case** (12 roofs, all models agree): every model 83% (10/12)
- **Harder case** (18 roofs, models disagree): GPT-5.5 83%, Gemini 67%,
  Kimi 56%, Gemma 33%

Source: computed from `results/*.json` + `ground-truth.json`; shown in
`presentation/index.html` slide 5.

## Failed and promising approaches

> "one approach that failed, documented" and "one approach that looks
> potentially good, with the evidence so far"

- **Failed:** bare-prompt classification with Gemini 2.5 defaults (404 for
  new accounts, malformed JSON, 429 rate limits) — see
  `docs/build-log-session5-draft.md` and presentation slide 7.
- **Promising:** structured PRD §3 output contract + human escalation —
  all 4 models produced parseable JSON across 120 calls; escalation path
  catches the 60% of roofs where models disagree. See presentation slide 8.

## What the prototype does NOT yet show

- Escalation recall is not measurable (0 ground-truth uncertain cases after
  the 3rd labeler resolved all ties) — needs a future calibration set of
  genuinely ambiguous roofs.
- No NYC-specific field imagery yet (public dataset only, per data boundary).
- No live context signals (footprints/permits) fused into classification —
  multi-source corroboration designed and data sources validated
  (`docs/multisource-verification.md`), not benchmarked.

These are honest limitations, not omissions — the brief asks the prototype
to be honest about what it shows.

## Bottom line

The benchmark prototype satisfies the capstone brief: same inputs, several
models (including open-weights), judged results against a pre-written answer
key, a baseline and a harder case, and documented failed + promising paths —
all reproducible from `scripts/` and summarized in `docs/benchmark-results.md`.
