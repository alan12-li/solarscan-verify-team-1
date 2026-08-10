# Presentation Notes — Session 6 (Aug 11, 2026)

**Deck:** `presentation/index.html` (9 slides — real-NYC-roofs version,
self-contained; open in a browser, F11 for fullscreen)
**Time:** 10 minutes + Q&A. Target ~45–60 seconds per slide.
**Team roles (5 speakers):**
| Slides | Speaker | Section |
|---|---|---|
| 1 | **Yongpeng** (opens) | Problem — 6 real NYC roofs |
| 2–3 | **Victor** | Prototype pipeline · Evaluation design |
| 4–5 | **Praewa** | Model vs human · The two mistakes |
| 6–7 | **Kenji** | Multi-source verification · Surprising facts |
| 8–9 | **Tanapat** (closes) | What failed → works · Recommendation |

Yongpeng opens (slide 1) and Tanapat closes (8–9); each of the four middle
speakers owns ~2 minutes. Rehearse once as a group before class. If someone
is absent, the person next in the table covers their slides.

> **Agent lookup:** each teammate can ask their agent "Which slides am I
> presenting?" — the agent reads `presentation/SPEAKER-ASSIGNMENTS.md` and
> answers from the table.

> Decision owner: **Yongpeng** (repo owner, benchmark lead). If a slide's
> number is challenged, cite the evidence path listed under it.

---

## Slide 1 · Problem — 6 real NYC roofs (60s) — Yongpeng
- Six real Manhattan roofs from **public NYC orthoimagery** (~0.5 m/px),
  shown as a grid: solar = 511 W 182nd St 2024 (permit Completed 2022);
  no_solar = 1086291, 1086435; hard = 1086408 (human uncertain — only Kimi
  agreed), 1086361 (GPT-5.5 said solar ✗), 511 W 182nd 2018 (pre-install vs
  2024).
- Two costly errors: Error A false "solar" → field visit to a bare roof
  (truck + team wasted); Error B false "no solar" → missed generation.
- Today every ambiguous roof = manual review by a person; our slice is the
  verification step, not a new scanner.
- *Evidence:* `docs/nyc-human-validation.md`; images from NYC Orthos (public).

## Slide 2 · Prototype we actually built (60s) — key slide — Victor
- Walk the pipeline top to bottom: roof image + optional context (footprint,
  permit) → 4 models in parallel (Gemini 3.5 Flash-Lite, GPT-5.5, Kimi K3
  open-weights, Gemma 4-26B open-weights), temperature 0, same prompt → each
  returns {label, confidence, escalate} → decision rule: agree & conf ≥ 0.6 →
  accept; disagree / low conf / record conflict → human review →
  corroboration (public permit + footprint checks, branch tested 20/20) →
  analyst decides.
- Emphasize: **real & tested** — 24 model calls on 6 real NYC roofs, all
  parseable JSON; reproducible (`scripts/fetch_nyc_roofs.py` → evaluate →
  compare with human labels); escalated cases are never auto-accepted.
- *Evidence:* `scripts/evaluate_benchmark.py`, `scripts/test_corroboration.py`,
  `opencode.json` (team-agent).

## Slide 3 · Evaluation: 6 real NYC roofs (45s) — Victor
- Design: 1 human labeler (Praewa) labels solar/no_solar/uncertain **before
  seeing model calls**; 4 models; public records (LL24 permits + Building
  Footprints).
- Two deliberate features: one address has a Completed solar permit (2022) =
  known positive case; same roof imaged 2018 and 2024 = imagery-date
  sensitivity. Same prompt, temperature 0, structured JSON output.
- *Evidence:* `docs/nyc-human-validation.md`.

## Slide 4 · Model vs human on real roofs (60s) — key slide — Praewa
- Read the table roof by roof: agreement with the human = Kimi 6/6,
  Gemini 5/6, Gemma 5/6, GPT-5.5 4/6.
- Kimi is honest about doubt: the only model that said "uncertain" where the
  human did (1086408). GPT-5.5 false positive: "solar" at 0.76 on a bare roof
  (1086361) — the costly error class.
- *Evidence:* `docs/nyc-human-validation.md`.

## Slide 5 · What the two mistakes tell us (45s) — Praewa
- GPT-5.5 on 1086361: human no_solar, GPT-5.5 solar at 0.76, 3 other models
  no_solar → Error A would send a truck to a bare roof; 0.76 > 0.6 accept
  threshold → the rule as written would have passed it.
- Kimi on 1086408: human uncertain, Kimi uncertain at 0.45; Gemini/GPT-5.5/
  Gemma all no_solar at high confidence → Kimi's doubt maps to the human's —
  exactly the escalation behavior the layer wants (doubt → human review).

## Slide 6 · Multi-source verification works (45s) — Kenji
- Pipeline: NYC Building Footprints (BBL + centroid) → NYC Orthos tile
  (public, CC BY 4.0) → 4 models classify → cross-check LL24 solar permit by
  address.
- Branch logic: 10 scenarios × 2 models = 20/20 rule-following (conflict →
  escalate). Time matters: 511 W 182nd = no_solar 2018 (pre-install), solar
  2024 — imagery date must match the question. Context injection works.
- *Evidence:* `docs/multisource-verification.md`,
  `scripts/test_corroboration.py`.

## Slide 7 · Surprising facts (45s) — Kenji
- Humans hesitated — only one model agreed (1086408; the other three
  confidently wrong). On 1086361 GPT-5.5 was confidently wrong in the costly
  direction.
- Open-weights models are honest about doubt: Kimi 6/6 incl. the uncertain
  case, Gemma 5/6; closed models more confident and more wrong; Kimi/Gemma
  far cheaper than GPT-5.5.

## Slide 8 · What failed → what works (45s) — Tanapat
- Failed: bare-prompt classification (inconsistent output, no confidence
  signal); confident wrong answers (GPT-5.5 0.76 above the threshold); the
  costly error class is real on real data, not theory.
- Works: structured output contract (24/24 parseable JSON); clear cases
  separable; doubt signal works (Kimi's uncertain matched the human's);
  multi-source branch 20/20; real NYC pipeline (footprints → ortho → model →
  permit).
- *Evidence:* `docs/build-log-session5-draft.md`.

## Slide 9 · Recommendation (60s) — close strong — Tanapat
- **Revise the decision rule, then run a limited test (100 roofs).** Not
  "stop" (pipeline works end-to-end on real NYC roofs); not "deploy as-is"
  (one model produced the costly error). Add corroboration — don't trust a
  single confident call.
- If we do nothing: the costly error class appears in real data —
  verification is the mitigation, not the cost.
- The 100-roof test: Con Edison parcels → real addresses → permit join at
  scale; more labelers, more roofs, harder cases; also test missing/bad-input
  abstain behavior (defined in PRD §5, untested so far).
- Risks: permit coverage incomplete (older/unpermitted systems); imagery-date
  mismatch (2018 vs 2024 example); one labeler isn't a consensus.
- Ask Con Edison: N roofs with parcel IDs; which context is shareable
  (footprints, permits, historical imagery); a calibration set of genuinely
  ambiguous roofs.
- Close: "The scanner stays; the ambiguous roofs get a second, explainable,
  human-escalated look."
- *Evidence:* `docs/value-for-conedison.md`, `docs/con-edison-questions.md`.

---

## Q&A preparation

Likely questions and honest answers:

- **"Why only 6 roofs?"** It is a real-data validation set from public NYC
  orthoimagery with one human labeler — deliberately small and honest. The
  100-roof limited test with Con Edison parcels scales it.
- **"Which model would you use?"** Kimi matched the human 6/6 including the
  uncertain case and is far cheaper; GPT-5.5 is strong on clear cases but
  produced the costly false positive. Revisit after revising the decision
  rule.
- **"Is one human labeler enough?"** No — that is a stated limitation. The
  ground rule is ≥2 agreeing labelers; the limited test adds more humans.
- **"What data did you use?"** Public NYC orthoimagery (CC BY 4.0), NYC
  Building Footprints, LL24 solar permits. No Con Edison data — we will ask
  what is shareable.
- **"Did you test multi-source verification end-to-end?"** The capability is
  verified piecewise: context injection works, the permit lookup API is live,
  the decision branch follows rules 20/20. Scoring it end-to-end needs parcel
  IDs to join roofs to real records — that is the first step of the 100-roof
  test.
- **"The 2018 vs 2024 roof?"** 511 W 182nd St — no_solar in 2018
  (pre-install), solar in 2024, permit Completed 2022. Imagery date must
  match the question being asked.

## Before class checklist

- [ ] Download `presentation/index.html`; open offline (venue network is not
      guaranteed)
- [ ] Assign speakers per the role table above (Yongpeng 1, Victor 2–3,
      Praewa 4–5, Kenji 6–7, Tanapat 8–9)
- [ ] Each speaker confirms their slides via agent: "Which slides am I
      presenting?" (reads `presentation/SPEAKER-ASSIGNMENTS.md`)
- [ ] Rehearse once; time each section (10 minutes total)
- [ ] Have `docs/team-links.md` handy for follow-up links
- [ ] Print the questions to Con Edison (`docs/con-edison-questions.md`)
