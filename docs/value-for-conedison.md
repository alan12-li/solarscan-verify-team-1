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
| Every ambiguous case costs human time | Clear cases auto-pass; only disagreements / low confidence / record conflicts go to a person |
| Human reviews without a second opinion | Every decision carries confidence + a reason — explainable, auditable |

**Measured evidence** (all reproducible in this repo):
- 6 real NYC roofs, 1 human labeler, 4 models
  (`docs/nyc-human-validation.md`)
- Model vs human agreement: Kimi K3 6/6, Gemini 5/6, Gemma 5/6, GPT-5.5 4/6
  (GPT-5.5's one miss was a false "solar" — the costly error class)
- Multi-source branch: 20/20 rule-following with public records
  (`docs/multisource-verification.md`)
- Cost per correct call: $0.002–0.013 (Gemini) — cents per roof, not a blocker
- Pipeline: `scripts/fetch_nyc_roofs.py` → `evaluate_benchmark.py` →
  compare with human labels

## 2. What we found they should know (the strategic value)

**The risk is not cost — it is confident wrong answers on hard roofs.**

1. **A single confident call can be dangerously wrong.** On a real Manhattan
   roof (1086361), GPT-5.5 called "solar" at conf 0.76 on a roof a human
   labeled no_solar — a false "solar" would send a field team to a bare
   roof. The other three models all said no_solar (`presentation/index.html`
   slide 6).
2. **Open-weights are honest about doubt:** on the one roof the human was
   genuinely uncertain about (1086408), Kimi K3 was the only model that
   also said uncertain — the doubt signal maps to human doubt (slide 5/8).
3. **Imagery date matters:** 511 W 182nd St has a Completed solar permit
   (2022); the same roof reads no_solar on 2018 imagery and solar on 2024 —
   a verification layer must check imagery date against the question
   (slide 7).
4. **Escalation recall is not yet measurable** — one labeler, 6 roofs; a
   calibration set of genuinely ambiguous roofs is needed.

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
