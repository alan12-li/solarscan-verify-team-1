# Speaker Assignments — Session 6 (Aug 11, 2026)

This file lets each teammate's agent answer: **"Which slides am I
presenting?"** — the agent reads this table and replies with the speaker's
slides, section, and key points.

Deck: `presentation/index.html` (12 slides — cover + 11 content,
real-NYC-roofs version; live at
https://alan12-li.github.io/solarscan-verify-team-1/presentation/).
Total time: 10 minutes + Q&A.

Full word-for-word delivery lines are in `presentation/NOTES.md` (each
slide has a "Say something like" script). This file is the lookup table.

## Assignment table

| Slides | Speaker (GitHub) | Section | Key points to cover |
|---|---|---|---|
| 1–3 | **Yongpeng** (alan12-li) | Cover · Problem — 6 real NYC roofs · Prototype | Team + brief · 6 real Manhattan roofs (solar: 511 W 182nd 2024; no_solar: 1086291/1086435; hard: 1086408/1086361/511-2018) · Error A truck to bare roof · Error B missed generation · today = manual review · pipeline: image → 4 models → rule → corroboration 20/20 → analyst decides |
| 4–5 | **Victor** (Vchan5526) | Evaluation design · Model vs human | 24 real calls parseable · 2 human labelers (unanimous 6/6), permit-positive case, 2018 vs 2024 · Kimi 6/6, Gemini/Gemma 5/6, GPT-5.5 4/6 · GPT-5.5 false "solar" 0.76 (above 0.6) · Kimi uncertain 0.45 ↔ human uncertain — escalation is the product |
| 6–7 | **Praewa** (pointpraewa) | The two mistakes · Multi-source verification | GPT-5.5 0.76 > 0.6 threshold → rule would pass a false positive · Kimi doubt ↔ human doubt · footprints → orthos → models → permit cross-check · 20/20 branch · 2018 vs 2024 date sensitivity |
| 8–9 | **Kenji** (ktannady22) | Surprising facts · Model economics | humans hesitated, only Kimi agreed · open-weights honest about doubt, cheaper · measured per-image cost (Gemma $0.000059 / Gemini $0.00044 / Kimi $0.00191 / GPT-5.5 $0.00260) · 100 roofs ≈ $0.50 |
| 10–12 | **Tanapat** (tanapreuk) | What failed → works · Live demo · Recommendation (closes) | bare-prompt + confident-wrong failures · structured contract 24/24 · demo: two links (Local = Alan's Mac / Capstone = any machine) · address 511 W 182nd St → ACCEPT + permit · photo hard roof → ESCALATE · revise rule → 100-roof test · not stop / not deploy as-is · close: "scanner stays, ambiguous roofs get a second look — try the demo" |

Hand-off order: Yongpeng (1–3) → Victor (4–5) → Praewa (6–7) → Kenji (8–9)
→ Tanapat (10–12, incl. live demo + close).

## Per-speaker detail (agent lookup answers)

### Yongpeng — slides 1–3 (opens)
- **Cover:** "We're SolarScan Verify. Brief: Con Edison's Solar Scanner
  Optimization. We built a verification layer for the roofs the scanner
  gets wrong — and we brought a live demo." Name team, one breath.
- **1 Problem:** 6 real Manhattan roofs from public NYC orthoimagery
  (~0.5 m/px): solar = 511 W 182nd St 2024 (permit Completed 2022);
  no_solar = 1086291, 1086435; hard = 1086408 (human uncertain — only
  Kimi agreed), 1086361 (GPT-5.5 said solar ✗), 511 W 182nd 2018
  (pre-install vs 2024). Error A: false "solar" → truck at a bare roof.
  Error B: false "no solar" → missed generation. Today = manual review.
- **2 Prototype:** input = roof image **or** NYC address (address → fetch
  from public orthoimagery) + optional context (footprint, permit) → 4
  models in parallel (Gemini, GPT-5.5, Kimi K3, Gemma; temp 0, same
  prompt) → {label, confidence, escalate} → decision rule (agree & conf
  ≥ .6 accept; else human review) → corroboration (public records, branch
  20/20) → analyst decides. Agent recommends, a person decides.

### Victor — slides 4–5
- **4 Evaluation:** 6 real roofs, 2 human labelers, unanimous 6/6 (labels
  before model
  calls), 4 models, permit-positive case, 2018 vs 2024 imagery-date test;
  24 real calls, all parseable JSON.
- **5 Model vs human:** table 6 roofs × 4 models; Kimi 6/6, Gemini 5/6,
  Gemma 5/6, GPT-5.5 4/6; Kimi only model to say uncertain where human did
  (1086408); GPT-5.5 false "solar" 0.76 on 1086361.

### Praewa — slides 6–7
- **6 Two mistakes:** GPT-5.5 0.76 > 0.6 threshold → rule would pass a
  false positive (truck to bare roof); Kimi uncertain 0.45 ↔ human
  uncertain → escalation is the product.
- **7 Multi-source:** footprints → ortho tile (CC BY 4.0) → 4 models →
  LL24 permit by address; branch 20/20; time matters (511 W 182nd 2018
  no_solar vs 2024 solar); context injection works.

### Kenji — slides 8–9
- **8 Surprising:** humans hesitated, only Kimi agreed (1086408); other
  three confidently wrong; open-weights honest about doubt (Kimi 6/6,
  Gemma 5/6); Kimi/Gemma far cheaper than GPT-5.5.
- **9 Model economics:** measured per-image cost (OpenRouter, same image,
  2026-08-10): Gemma $0.000059 · Gemini $0.00044 · Kimi $0.00191 ·
  GPT-5.5 $0.00260 (44× Gemma). 4 models × 1 roof ≈ $0.005; 100 roofs × 4
  models ≈ $0.50. Cost is not the blocker — accuracy + honest doubt is.
  Open-weights cheaper AND Kimi 6/6 on real roofs.

### Tanapat — slides 10–12 (closes)
- **10 What failed → works:** failed = bare-prompt (no confidence) +
  confident-wrong (GPT-5.5 0.76, real data); works = structured contract
  24/24, doubt signal (Kimi ↔ human), multi-source 20/20, real NYC
  pipeline.
- **11 Live demo (hands-on):** two links on the slide — Local
  (http://127.0.0.1:8765, `python3 scripts/demo_server.py`, Alan's Mac)
  and Capstone (https://alan12-li.github.io/solarscan-verify-team-1/presentation/demo.html).
  Flow: address `511 W 182nd St` → ACCEPT solar + permit 8/15/2022; photo
  hard roof → ESCALATE. 45s each, 90s total. If the network is down, tell
  the story from the deck.
- **12 Recommendation:** revise decision rule → 100-roof limited test with
  Con Edison parcels; not stop / not deploy as-is; risks (permit coverage,
  imagery date, 2 labelers is a small panel); missing/bad-input abstain
  untested; close: "The scanner stays; the ambiguous roofs get a second,
  explainable, human-escalated look. And the demo is one click away."
