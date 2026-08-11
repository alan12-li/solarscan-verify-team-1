# NYC Human Validation (2026-08-10)

## Setup
- **6 real Manhattan roofs** from public NYC orthoimagery (~0.5 m/px), labeled by Yongpeng (alan12-li) on 2026-08-10.
- **Second labeler added 2026-08-11:** Praewa (pointpraewa) — **6/6 unanimous** with Yongpeng (majority decision reached, no third labeler needed).
- Roofs: 1086291, 1086361, 1086408, 1086435, 511 W 182nd St (2024), 511 W 182nd St (2018).
- 511 W 182nd St has a **Completed LL24 solar permit (2022)** — the 2024 vs 2018 pair tests imagery-date sensitivity.

## Labels (2 labelers, unanimous)

| Roof | Yongpeng | Praewa | Consensus |
|---|---|---|---|
| 1086291 | no_solar | no_solar | no_solar |
| 1086361 | no_solar | no_solar | no_solar |
| 1086408 | uncertain | uncertain | uncertain |
| 1086435 | no_solar | no_solar | no_solar |
| 511 W 182nd (2024) | solar | solar | solar |
| 511 W 182nd (2018) | no_solar | no_solar | no_solar |

Source: `data/nyc-validation/labels/pointpraewa.json` (exported from `data/nyc-validation/label-nyc.html`).

## Results

| Roof | Human | Gemini | GPT-5.5 | Kimi K3 | Gemma |
|---|---|---|---|---|---|
| 1086291 | no_solar | no_solar .95 | no_solar .87 | no_solar .78 | no_solar .95 |
| 1086361 | no_solar | no_solar .95 | **solar .76** | no_solar .68 | no_solar .95 |
| 1086408 | **uncertain** | no_solar .95 | no_solar .74 | **uncertain .45** | no_solar .90 |
| 1086435 | no_solar | no_solar .95 | no_solar .82 | no_solar .55 | no_solar .90 |
| 511 W 182nd (2024) | solar | solar .99 | solar .98 | solar .97 | solar 1.0 |
| 511 W 182nd (2018) | no_solar | no_solar .95 | no_solar .91 | no_solar .72 | no_solar .95 |

## Human-model agreement (6 roofs)

| Model | Agreement |
|---|---|
| **Kimi K3** | **6/6 (100%)** |
| Gemini | 5/6 (83%) |
| Gemma | 5/6 (83%) |
| GPT-5.5 | 4/6 (67%) |

## Findings

1. **Kimi K3 was the only model that said `uncertain` where the human said uncertain (r3)** — the open-weights honesty pattern from the 30-roof benchmark reproduced on real NYC data.
2. **GPT-5.5 false-positived `solar` on r2** (a no-solar roof) at conf 0.76 — the costly error class.
3. **Imagery date matters**: 511 W 182nd St is no_solar in 2018 (pre-install) and solar in 2024 (post-install), matching the permit. All 4 models got both right, and the permit predicted the 2024 result.
4. Honest scope: 2 labelers (unanimous 6/6 — majority rule satisfied), 6 roofs (not 30), real NYC data but no ground truth beyond this labeling session.

```json
{
  "date": "2026-08-10",
  "labeler": "Yongpeng (alan12-li)",
  "scope": "6 real Manhattan roofs, NYC orthoimagery (~0.5 m/px)",
  "ground_truth": {
    "r1_1086291": "no_solar",
    "r2_1086361": "no_solar",
    "r3_1086408": "uncertain",
    "r4_1086435": "no_solar",
    "r5_511W182nd_2024": "solar",
    "r6_511W182nd_2018": "no_solar"
  },
  "models": {
    "Gemini": {
      "r1": "no_solar .95",
      "r2": "no_solar .95",
      "r3": "no_solar .95",
      "r4": "no_solar .95",
      "r5": "solar .99",
      "r6": "no_solar .95"
    },
    "GPT-5.5": {
      "r1": "no_solar .87",
      "r2": "solar .76",
      "r3": "no_solar .74",
      "r4": "no_solar .82",
      "r5": "solar .98",
      "r6": "no_solar .91"
    },
    "Kimi K3": {
      "r1": "no_solar .78",
      "r2": "no_solar .68",
      "r3": "uncertain .45",
      "r4": "no_solar .55",
      "r5": "solar .97",
      "r6": "no_solar .72"
    },
    "Gemma": {
      "r1": "no_solar .95",
      "r2": "no_solar .95",
      "r3": "no_solar .90",
      "r4": "no_solar .90",
      "r5": "solar 1.0",
      "r6": "no_solar .95"
    }
  },
  "agreement_with_human": {
    "Kimi K3": "6/6 (100%)",
    "Gemini": "5/6 (83%)",
    "Gemma": "5/6 (83%)",
    "GPT-5.5": "4/6 (67%)"
  },
  "note": "New human validation on REAL NYC roofs (replaces anonymous-set validation on the deck). Kimi K3 was the only model to say 'uncertain' where the human said uncertain (r3); open-weights honesty pattern from the 30-roof benchmark reproduced on real data. GPT-5.5 false-positive 'solar' on r2."
}
```
