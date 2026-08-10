# Labeling Progress — Benchmark v1

**Status:** ✅ **5 of 5 teammates labeled**
**Date:** 2026-08-10
**Rule:** majority vote among labelers; a tie becomes `uncertain`
(PRD §5 fail-toward-escalation).

## Coverage

| Labeler | GitHub | Images | Status |
|---|---|---|---|
| Yongpeng | alan12-li | 30/30 | ✅ merged |
| Victor | vchan5526 | 30/30 | ✅ merged |
| Praewa | pointpraewa | 30/30 | ✅ merged (PR #1) |
| Kenji | ktannady22 | 30/30 | ✅ merged |
| Tanapat | tanapreuk | 30/30 | ✅ merged (PR #2) |

**All 5 teammates have committed through their own agent** (capstone
requirement: "each of you makes one commit through your own agent").

## Agreement (5 labelers, majority vote)

- **All 30 cases have a clear majority — 14 solar / 16 no_solar / 0 uncertain**
- **20 cases unanimous (5:0), 10 cases majority (4:1 or 3:2)**
- No ties (every case had ≥3 agreeing labelers)

### Pairwise agreement (high: 22–29 of 30)

| Pair | Agreement |
|---|---|
| Yongpeng ↔ Tanapat | 29/30 |
| Praewa ↔ Tanapat | 28/30 |
| Praewa ↔ Kenji | 27/30 |
| Praewa ↔ Yongpeng | 27/30 |
| Kenji ↔ Tanapat | 26/30 |
| Tanapat ↔ Victor | 26/30 |
| Yongpeng ↔ Kenji | 25/30 |
| Yongpeng ↔ Victor | 25/30 |
| Kenji ↔ Praewa | 27/30 |
| Kenji ↔ Victor | 22/30 |

### Majority details (10 non-unanimous cases)

| Case ID | Majority | Votes |
|---|---|---|
| sv-0003 | solar (4:1) | solar×4, no_solar×1 |
| sv-0013 | no_solar (4:1) | no_solar×4, uncertain×1 |
| sv-0014 | no_solar (3:1:1) | no_solar×3, solar×1, uncertain×1 — most split |
| sv-0015 | no_solar (3:2) | no_solar×3, uncertain×2 |
| sv-0017 | solar (4:1) | solar×4, uncertain×1 |
| sv-0018 | no_solar (4:1) | no_solar×4, solar×1 — earlier opposite calls settled |
| sv-0133 | no_solar (4:1) | no_solar×4, uncertain×1 |
| sv-0134 | no_solar (4:1) | no_solar×4, uncertain×1 |
| sv-0140 | solar (4:1) | solar×4, no_solar×1 |

## Stability note

The 5-labeler majority distribution (14 solar / 16 no_solar / 0 uncertain)
is **identical** to the earlier 3-labeler majority — the benchmark's
ground truth is robust to adding more labelers, and the model scorecard
(83 / 73 / 67 / 53) is unchanged.

## Files

- `data/benchmark-v1/labels/alan12-li.json` · `vchan5526.json` ·
  `pointpraewa.json` · `ktannady22.json` · `tanapreuk.json`
- `data/benchmark-v1/ground-truth.json` — merged 5-labeler majority ground truth
- Labeling tool: `data/benchmark-v1/labeling/label-standalone.html`
