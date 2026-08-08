# SolarScan Verify — Benchmark Results (v1, cross-provider)

**Date:** 2026-08-08
**Benchmark:** 30 rooftop images (19 test + 11 valid from the
`Francesco/solar-panels-taxvb` public drone dataset, CC license)
**Task:** three-way classification — `solar` / `no_solar` / `uncertain`
**PRD link:** `sims/solarscan-verify/PRD.md` §6 (90% clear-case accuracy,
escalation recall 1.0) and §7 (multi-model comparison)

## Models compared (same inputs, same judging rubric)

| Model | Provider | Route |
|---|---|---|
| Gemini 3.5 Flash-Lite | Google | Gemini API |
| GPT-5.5 | OpenAI | OpenRouter |
| Kimi K3 (2.8T, multimodal reasoning) | Moonshot AI | OpenRouter |

All three are vision-capable. Every model saw the identical 30 images with
the identical system prompt (PRD §3 output contract) and temperature 0.
Image integrity between labeling and evaluation was verified by SHA-256
(`scripts/verify_image_integrity.py`).

## Results table

### Label distribution (30 cases)

| Label | Gemini 3.5 Flash-Lite | Kimi K3 | GPT-5.5 |
|---|---|---|---|
| `solar` | 13 | 13 | 13 |
| `no_solar` | 10 | 9 | 12 |
| `uncertain` | 7 | **8** | 5 |

### Escalation (uncertain or confidence < 0.6) — PRD §5 fail-toward-human

| Model | Escalated | Rate |
|---|---|---|
| Gemini 3.5 Flash-Lite | 7 / 30 | 23% |
| Kimi K3 | **12 / 30** | **40%** |
| GPT-5.5 | 5 / 30 | 17% |

### Mean confidence by label

| Label | Gemini 3.5 Flash-Lite | Kimi K3 | GPT-5.5 |
|---|---|---|---|
| `solar` | **0.96** | 0.89 | 0.89 |
| `no_solar` | **0.95** | 0.61 | 0.78 |
| `uncertain` | 0.34 | 0.42 | 0.40 |

### Cross-model agreement

- Cases all 3 models answered: **30 / 30**
- All 3 models agree on the label: **17 / 30 (57%)**
- The 13 disagreements (43%) are exactly the cases where human ground truth
  is needed to judge which model is right.

### Difficulty factors reported (top 5, non-enum values flagged)

| Model | Top factors |
|---|---|
| Gemini 3.5 Flash-Lite | image_quality (22), none (7), unusual_layout (2), shading (2) |
| Kimi K3 | image_quality (20), unusual_layout (15), orientation (8), obstruction (7) |
| GPT-5.5 | image_quality (20), unusual_layout (9), none (7), obstruction (5) |

All models used only the PRD-enumerated difficulty factors (no out-of-enum
values).

## Cost

| Model | Approx. cost (30 images) |
|---|---|
| Gemini 3.5 Flash-Lite | < $0.05 (free-tier usage) |
| GPT-5.5 | ~ $0.27 |
| Kimi K3 | ~ $0.20 |
| **Total (OpenRouter)** | **$0.53** (limit $5.00) |

## Observations

1. **All three models agree on solar (13/13 each)** — clear solar cases are
   not the hard part of this problem.
2. **Kimi K3 is the most conservative** (40% escalation vs GPT-5.5's 17%) —
   it prefers "uncertain" when evidence is thin, which matches the PRD's
   fail-toward-human design. It is also the least confident on `no_solar`
   (0.61).
3. **Gemini is the most confident overall** (0.96 solar / 0.95 no_solar) but
   the least confident when it says `uncertain` (0.34) — it is either sure or
   very unsure.
4. **57% full agreement** means the benchmark's ambiguous cases are doing
   their job: the 43% disagreement cases are precisely the rooftops a
   verification layer must escalate, and human labels will decide who is
   right.

## Status: ground truth pending

Accuracy on clear cases (PRD §6: ≥90%) and escalation recall (PRD §6: 1.0)
**cannot be scored yet** — the 30 images are not yet human-labeled.
Team labeling is in progress via `data/benchmark-v1/labeling/label-standalone.html`
(see `docs/labeling-task.md`). Once ≥2 labelers agree per image, this table
gains the accuracy / escalation-recall columns.

## Reproducibility

- Fetch images: `python3 scripts/fetch_benchmark.py`
- Evaluate: `python3 scripts/evaluate_benchmark.py --subset`
  (needs `GEMINI_API_KEY` and/or `OPENROUTER_API_KEY` in env)
- Analyze: `python3 scripts/analyze_results.py --subset`
- Integrity: `python3 scripts/verify_image_integrity.py`
- Raw model outputs: `data/benchmark-v1/results/*.json` (gitignored)
