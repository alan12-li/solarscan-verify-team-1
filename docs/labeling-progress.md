# Labeling Progress — Benchmark v1

**Status:** 3 of 5 teammates labeled (Yongpeng, Victor, Praewa)
**Date:** 2026-08-10
**Rule:** majority vote among labelers; a tie becomes `uncertain`
(PRD §5 fail-toward-escalation).

## Coverage

| Labeler | GitHub | Images | Status |
|---|---|---|---|
| Yongpeng | alan12-li | 30/30 | ✅ merged |
| Victor | vchan5526 | 30/30 | ✅ merged |
| Praewa | pointpraewa | 30/30 | ✅ merged (PR #1) |
| Kenji | ktannady22 | — | ⏳ invitation accepted, not yet labeled |
| Tanapat | tanapreuk | — | ⏳ awaiting invite accept |

## Agreement (3 labelers, majority vote)

- **All 30 cases have a majority label — 14 solar / 16 no_solar / 0 uncertain**
- No ties (every case had a 2:1 or 3:0 majority)

### Pairwise agreement

| Pair | Agreement |
|---|---|
| Praewa ↔ Yongpeng | 27/30 |
| Praewa ↔ Victor | 24/30 |
| Yongpeng ↔ Victor | 25/30 |
| All three agree | 23/30 |

### The 5 earlier disagreements — resolved 2:1 by Praewa's labels

| Case ID | Yongpeng | Victor | Praewa | Majority |
|---|---|---|---|---|
| sv-0013 | no_solar | uncertain | no_solar | **no_solar** |
| sv-0017 | solar | uncertain | solar | **solar** |
| sv-0018 | solar | no_solar | no_solar | **no_solar** (opposite calls settled) |
| sv-0133 | no_solar | uncertain | no_solar | **no_solar** |
| sv-0134 | no_solar | uncertain | no_solar | **no_solar** |

sv-0018 was the hardest image (opposite human calls); Praewa's vote settled
it as no_solar.

## Consequence for scoring

With 0 ground-truth `uncertain` cases, **escalation recall is no longer
measurable** on this set. The PRD §6 accuracy scorecard is now computed on
all 30 cases (see `docs/benchmark-results.md`). The escalation-recall
question needs a future calibration set of genuinely ambiguous roofs.

## Files

- `data/benchmark-v1/labels/alan12-li.json` — Yongpeng's labels
- `data/benchmark-v1/labels/vchan5526.json` — Victor's labels
- `data/benchmark-v1/labels/pointpraewa.json` — Praewa's labels
- `data/benchmark-v1/ground-truth.json` — merged majority-vote ground truth
- Labeling tool: `data/benchmark-v1/labeling/label-standalone.html`
