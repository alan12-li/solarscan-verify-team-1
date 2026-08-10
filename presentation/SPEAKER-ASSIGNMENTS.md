# Speaker Assignments — Session 6 (Aug 11, 2026)

This file lets each teammate's agent answer: **"Which slides am I
presenting?"** — the agent reads this table and replies with the speaker's
slides, section, and key points.

Deck: `presentation/index.html` (9 slides — real-NYC-roofs version; live at
https://alan12-li.github.io/solarscan-verify-team-1/presentation/).
Total time: 10 minutes + Q&A.

> Updated 2026-08-10 to match the current 9-slide NYC deck (supersedes the
> previous 13-slide mapping).

## Assignment table

| Slides | Speaker (GitHub) | Section | Key points to cover |
|---|---|---|---|
| 1 | **Yongpeng** (alan12-li) | Problem — 6 real NYC roofs | Errors A/B · every ambiguous roof is manual review today · the 6-roof grid |
| 2–3 | **Victor** (Vchan5526) | Prototype · Evaluation | Pipeline: image+context → 4 models → decision rule → corroboration → human · 24 real calls, parseable JSON · eval design: 1 human labeler, permit-positive case, 2018 vs 2024 |
| 4–5 | **Praewa** (pointpraewa) | Model vs human · The two mistakes | Human-labeler story · Kimi 6/6, Gemini/Gemma 5/6, GPT-5.5 4/6 · GPT-5.5 false "solar" at 0.76 (above 0.6 threshold) · Kimi's uncertain maps to the human's |
| 6–7 | **Kenji** (ktannady22) | Multi-source verification · Surprising facts | Footprints → orthos → models → permit cross-check · 20/20 branch · 2018 vs 2024 date sensitivity · humans hesitated, only Kimi agreed · open-weights honest about doubt |
| 8–9 | **Tanapat** (tanapreuk) | What failed → works · Recommendation | Bare-prompt + confident-wrong failures · structured contract 24/24 · revise decision rule → 100-roof limited test · risks · ask to Con Edison · close |

Hand-off order: Yongpeng → Victor → Praewa → Kenji → Tanapat.

## Per-speaker detail (agent lookup answers)

### Yongpeng — slide 1 (opens)
- 6 real Manhattan roofs from public NYC orthoimagery (~0.5 m/px): solar =
  511 W 182nd St 2024 (permit Completed 2022); no_solar = 1086291, 1086435;
  hard = 1086408 (human uncertain — only Kimi agreed), 1086361 (GPT-5.5 said
  solar ✗), 511 W 182nd 2018 (pre-install vs 2024).
- Error A: false "solar" → field visit to a bare roof (truck + team wasted).
  Error B: false "no solar" → missed generation on a roof that has it.
- Today: every ambiguous roof = manual review by a person.
- Close by naming the team, then hand to Victor.

### Victor — slides 2–3
- Slide 2 (pipeline): roof image + optional context (footprint, permit) →
  4 models in parallel (Gemini 3.5 Flash-Lite, GPT-5.5, Kimi K3 open-weights,
  Gemma 4-26B open-weights), temperature 0, same prompt → each returns
  {label, confidence, escalate} → decision rule: agree & conf ≥ 0.6 → accept;
  disagree / low conf / record conflict → human review → corroboration
  (public permit + footprint checks, branch tested 20/20) → analyst decides.
- Real & tested: 24 model calls on 6 real NYC roofs, all parseable JSON.
  Reproducible: `scripts/fetch_nyc_roofs.py` → evaluate → compare with human
  labels. Escalated cases are never auto-accepted.
- Slide 3 (eval design): 1 human labeler labels solar/no_solar/uncertain
  before seeing model calls; public records (LL24 solar permits + Building
  Footprints); one address has a Completed solar permit (2022) = known
  positive; same roof imaged 2018 and 2024 = imagery-date sensitivity.

### Praewa — slides 4–5
- Slide 4 (table): agreement with the human = Kimi 6/6, Gemini 5/6,
  Gemma 5/6, GPT-5.5 4/6. Kimi honest about doubt (only model saying
  "uncertain" where the human did, 1086408). GPT-5.5 false positive: "solar"
  at 0.76 on a bare roof (1086361) — the costly error class.
- Slide 5 (two mistakes): GPT-5.5 on 1086361 — 3 other models said no_solar;
  0.76 > 0.6 accept threshold → the rule as written would have passed it.
  Kimi on 1086408 — human uncertain, Kimi uncertain at 0.45; others no_solar
  at high confidence → Kimi's doubt maps to the human's → that is the
  escalation behavior the layer wants (doubt → human review).

### Kenji — slides 6–7
- Slide 6: NYC Building Footprints (BBL + centroid) → NYC Orthos tile
  (public, CC BY 4.0) → 4 models classify → cross-check LL24 solar permit by
  address. Branch logic: 10 scenarios × 2 models = 20/20 rule-following
  (conflict → escalate). Time matters: 511 W 182nd = no_solar 2018
  (pre-install), solar 2024 — imagery date must match the question.
  Context injection works (models accept footprint/permit context).
- Slide 7: humans hesitated — only one model agreed (1086408; the other
  three confidently wrong). GPT-5.5 confidently wrong in the costly direction
  (1086361). Open-weights honest about doubt: Kimi 6/6 incl. the uncertain
  case, Gemma 5/6; closed models more confident and more wrong; Kimi/Gemma
  far cheaper.

### Tanapat — slides 8–9 (closes)
- Slide 8: failed = bare-prompt classification (inconsistent output, no
  confidence), confident wrong answers (GPT-5.5 0.76 above threshold), costly
  error class real on real data. Works = structured output contract (24/24
  parseable), clear cases separable, doubt signal works (Kimi's uncertain
  matched the human's), multi-source branch 20/20, real NYC pipeline
  (footprints → ortho → model → permit).
- Slide 9: not "stop" (pipeline works end-to-end on real NYC roofs), not
  "deploy as-is" (one model produced the costly error). Revise the decision
  rule: add corroboration, don't trust a single confident call. If we do
  nothing: the costly error class appears in real data — verification is the
  mitigation, not the cost. Next: 100-roof limited test with Con Edison
  parcels (permit join at scale, more labelers/roofs/harder cases, and test
  missing/bad-input abstain behavior — untested so far). Risks: permit
  coverage incomplete, imagery-date mismatch, one labeler isn't a consensus.
  Ask Con Edison: N roofs with parcel IDs; which context is shareable
  (footprints, permits, historical imagery); a calibration set of genuinely
  ambiguous roofs. Close line: "The scanner stays; the ambiguous roofs get a
  second, explainable, human-escalated look."

## Speaker check

- [ ] Clone the repo and open `presentation/index.html`
- [ ] Ask your agent: "Which slides am I presenting? What should I cover?"
- [ ] Rehearse your slides: Yongpeng ~1.5 min opener · Victor/Praewa/Kenji
      ~2 min each · Tanapat ~2 min close (10 minutes total)
