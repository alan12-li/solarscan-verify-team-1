# Labeling Progress — Benchmark v1

**Status:** 2 of 5 teammates labeled (Yongpeng, Victor)
**Date:** 2026-08-08
**Next step:** Kenji (invitation accepted) is the third labeler — his labels
will adjudicate the 5 disagreements below.

## Coverage

| Labeler | GitHub | Images | Status |
|---|---|---|---|
| Yongpeng | alan12-li | 30/30 | ✅ merged |
| Victor | vchan5526 | 30/30 | ✅ merged |
| Kenji | ktannady22 | — | ⏳ in progress |
| Tanapat | tanapreuk | — | ⏳ awaiting invite accept |
| Praewa | pointpraewa | — | ⏳ awaiting invite accept |

Per the labeling rule, every image needs **≥2 agreeing labelers**;
disagreements become `uncertain` (fail toward escalation, PRD §5).

## Agreement (2 labelers)

- **Agreed: 25 / 30 (83%)**
- **Disagreed: 5 / 30** → pending third labeler / resolved as `uncertain`

### Agreed cases (25) — provisional ground truth

| Label | Case IDs |
|---|---|
| `solar` (13) | sv-0003, sv-0004, sv-0005, sv-0006, sv-0007, sv-0008, sv-0009, sv-0010, sv-0012, sv-0139, sv-0140, sv-0141, sv-0142 |
| `no_solar` (12) | sv-0001, sv-0002, sv-0011, sv-0014, sv-0015, sv-0016, sv-0019, sv-0132, sv-0135, sv-0136, sv-0137, sv-0138 |

### Disagreements (5) — need a third labeler

| Case ID | Yongpeng | Victor | Note |
|---|---|---|---|
| sv-0013 | no_solar | uncertain | |
| sv-0017 | solar | uncertain | |
| sv-0018 | solar | **no_solar** | opposite calls — genuinely hard image |
| sv-0133 | no_solar | uncertain | |
| sv-0134 | no_solar | uncertain | |

sv-0018 is the most interesting disagreement: two labelers made opposite
calls, which is exactly the kind of ambiguous rooftop the verification layer
is built for.

## Early model scoring (provisional, 25 agreed cases only)

Using the 25 two-labeler-agreed cases as provisional ground truth:

| Model | Correct / 25 | Accuracy | Escalated (uncertain) |
|---|---|---|---|
| GPT-5.5 | 21 / 25 | 84% | 4 |
| Gemini 3.5-flash-lite | 20 / 25 | 80% | 5 |
| Kimi K3 | 19 / 25 | 76% | 6 |

PRD §6 target on clear cases: **≥90%** accuracy, escalation recall **1.0**.
The full scorecard is not final until all 30 cases have ≥2 agreeing labels
(the 5 disagreements are excluded here) and the complete label set is locked.

Note: this is a preliminary reading — the 5 disagreement cases are excluded
because they have no agreed ground truth yet.

## Files

- `data/benchmark-v1/labels/alan12-li.json` — Yongpeng's labels (merged)
- `data/benchmark-v1/labels/vchan5526.json` — Victor's labels (merged)
- Labeling tool: `data/benchmark-v1/labeling/label-standalone.html`
- Image integrity: `scripts/verify_image_integrity.py` (PASS before labeling)
