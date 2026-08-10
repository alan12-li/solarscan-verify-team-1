# Value for Con Edison — What This Project Improves

**Date:** 2026-08-10
**Purpose:** One-page answer to "what does SolarScan Verify actually improve
for Con Edison?" — for the Session 6 demo, build log, and clinic follow-ups.
Every number below is backed by files in this repo.

---

## TL;DR

We do not replace Con Edison's scanner. We built and **measured** a
verification layer for the ambiguous roofs, and we found something Con
Edison should know: **today's models are over-confident on exactly the roofs
humans hesitate over.** The project hands Con Edison a tested prototype, a
quantified risk map, and an executable next step — not a promise.

---

## 1. What we improved (prototype, measured)

| Today (per our clinic questions) | With the verification layer (measured) |
|---|---|
| Ambiguous roofs → manual review of imagery + records | 4 models screen each roof → structured output (label / confidence / reason / escalate) |
| Every ambiguous case costs human time | Agreement cases auto-pass (12/30 roofs all 4 models agree; 83% correct there) |
| Human reviews without a second opinion | Every decision carries confidence + a reason — explainable, auditable |

**Measured evidence** (all reproducible in this repo):
- 30-image benchmark, 5-labeler majority ground truth
  (`data/benchmark-v1/ground-truth.json`, `docs/labeling-progress.md`)
- 4-model scorecard: GPT-5.5 83%, Gemini 73%, Kimi K3 67%, Gemma 53%
  (`docs/benchmark-results.md`)
- Cost per correct clear-case: $0.003 (Gemini) / $0.013 (GPT-5.5) / $0.002
  (Gemma) — cents per roof, not a blocker
- Pipeline: `scripts/evaluate_benchmark.py` → `build_ground_truth.py` →
  `analyze_results.py`

## 2. What we found they should know (the strategic value)

**The risk is not cost — it is confident wrong answers on hard roofs.**

1. **No model meets the PRD §6 target (best 83% vs 90%).** The "clear" cases
   in thermal imagery are harder than expected, or the prompt needs tuning.
2. **Hard roofs punish models unevenly:** on the 12 roofs where all models
   agree, everyone hits 83%; on the 18 roofs where models disagree, GPT-5.5
   holds 83% but Gemma collapses to 33% (`presentation/index.html` slide 8).
3. **Models are confident where humans hesitate:** e.g. sv-0133 — two
   labelers said no_solar, Kimi K3 confidently said solar. On the 5 roofs
   that first split our labelers, models output confident calls anyway
   (slide 9).
4. **Escalation recall is not yet measurable** — no ground-truth ties after
   5 labelers; a calibration set of genuinely ambiguous roofs is needed.

**Bottom line for Con Edison:** adding today's models to the scanner
without a verification layer would reproduce these confident-wrong answers
at scale. The verification layer — with humans on every escalated case — is
the control that catches them.

## 3. What we propose next (executable roadmap)

- **Recommendation (four-choice brief):** revise the escalation behavior
  (prompt / threshold), then a **limited test on 100 roofs** — not stop, not
  deploy as-is (`presentation/index.html` slide 12).
- **Multi-source corroboration** (`docs/multisource-verification.md`):
  public NYC records — solar PV permits (LL24, dataset `cfz5-6fvh`) and
  building footprints (`5zhs-2jue`) — cross-check the model's call and catch
  confident wrong answers. Data sources validated live; decision branch
  tested **20/20** with models (`scripts/test_corroboration.py`); full
  image→records pipeline is part of the limited test.
- **What we need from Con Edison** (`docs/con-edison-questions.md`):
  which error costs more, which context data is shareable, and how results
  should return to their review tooling.

## 4. Honest scope

We changed no production system. This is the capstone prototype: real,
tested on 30 public roofs, honest about what it does and does not show
(`docs/prototype-fit.md`). No Con Edison data was used; all data is public
(CC drone dataset + NYC Open Data).

---

*One-line version for the demo:* "We don't replace your scanner — we give it
a second pair of eyes that knows when to say 'I'm not sure', and we've
measured exactly where today's models would fail."
