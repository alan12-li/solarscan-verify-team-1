# Presentation Notes — Session 6 (Aug 11, 2026)

**Deck:** `presentation/index.html` (12 slides, self-contained; open in a
browser, F11 for fullscreen)
**Time:** 10 minutes + Q&A. Target ~45 seconds per slide.
**Team roles (5 speakers):**
| Slides | Speaker | Section |
|---|---|---|
| 1–3 | **Yongpeng** (opens) | Title · Problem · Approach |
| 4–6 | **Victor** | Agent system · Multi-source NYC · Results |
| 7–9 | **Praewa** | Error breakdown · Human validation · Easy vs hard |
| 10–11 | **Kenji** | Surprising facts · What failed |
| 12–13 | **Tanapat** (closes) | Promising · Recommendation |

Yongpeng opens (1–3) and Tanapat closes (12–13); each of the four middle
speakers owns ~2 minutes. Rehearse once as a group before class. If someone
is absent, the person next in the table covers their slides.

> **Agent lookup:** after cloning the repo, each teammate can ask their agent
> "Which slides am I presenting?" — the agent reads
> `presentation/SPEAKER-ASSIGNMENTS.md` and answers from the table.

> Decision owner: **Yongpeng** (repo owner, benchmark lead). If a slide's
> number is challenged, cite the evidence path listed under it.

---

## Slide 1 · Title (30s)
- One line: "SolarScan Verify — a verification layer for Con Edison's
  rooftop solar scanner, with a multi-model prototype."
- Say the team names + the brief (Solar Scanner Optimization).

## Slide 2 · Problem (45s)
- The scanner is right on simple roofs and wrong on complex NYC roofs
  (HVAC, skylights, shadows, obstructions).
- Two costly errors: false solar (field trip to a bare roof) and false
  no-solar (missed generation).
- We chose **one slice**: the low-confidence verification step, not a new
  scanner.
- **Ideation (30s):** we asked the models themselves to map the four briefs,
  ranked by where an agent adds most value, and landed on the verification
  bottleneck because it is measurable and bounded.
- *Evidence:* `docs/con-edison-questions.md` (we asked Con Edison which
  error costs more).

## Slide 3 · Approach (45s)
- Same inputs → several models → structured output → fail toward a person.
- Benchmark: 30 public drone images, ground truth = 5 labelers majority.
- *Evidence:* `data/benchmark-v1/ground-truth.json`.

## Slide 4 · Prototype agent system (60s) — key slide
- Walk the pipeline top to bottom: image → agent → 4 models → decision rule
  → corroboration (public records, branch tested 20/20) → human.
- Emphasize: the agent **recommends, a person decides**; escalate is never
  auto-accepted (PRD §5, §8).
- Corroboration branch: `scripts/test_corroboration.py` — 10 scenarios × 2
  models = 20/20 rule-following; lesson = rules must be unambiguous.
- *Evidence:* `scripts/evaluate_benchmark.py`, `opencode.json` (team-agent).

## Slide 5 · Results (60s) — key slide
- Say it plainly: **no model met our 90% target.** That is the finding, not
  a failure of effort.
- GPT-5.5 83%, Gemini 73%, Kimi 67%, Gemma 53%. All below 90%.
- Also: only 40% of roofs get all-4-model agreement.
- *Evidence:* `docs/benchmark-results.md` §Scorecard.

## Slide 6 · Error breakdown (45s)
- Most errors are `no_solar → uncertain` (models hedge too much) — safe
  direction, recoverable by escalation.
- Dangerous: `no_solar → solar` (3×: Gemini 1, Kimi 2) — sends field teams
  to empty roofs; this is the class the verification layer must catch.
- Confidence signal: correct answers averaged 0.78–0.96 confidence, wrong
  answers 0.39–0.47 — low confidence is a usable escalation trigger.
- *Evidence:* computed from `data/benchmark-v1/results/*.json`.

## Slide 7 · Human validation (45s)
- Models vs our 5 labelers: GPT-5.5 matches humans 83%, Gemini 73%,
  Kimi 67%, Gemma 53%.
- 4 hardest images (≥3 models disagree with humans): sv-0003, sv-0013,
  sv-0015, sv-0137 — on roofs humans found hard, models were confident
  anyway. That is exactly why escalation is the product.

## Slide 8 · Baseline vs harder (45s)
- Baseline case (12 roofs, all models agree): every model 83%.
- Harder case (18 roofs, models disagree): GPT-5.5 83%, Gemini 67%,
  Kimi 56%, Gemma 33%.
- The gap is where the verification layer earns its keep.

## Slide 9 · Surprising fact (45s)
- Human labelers hesitated on 5 roofs; models were confident anyway.
- Open-weights models are more honest about doubt (Gemma most uncertain,
  11/30) and the cheapest (10× less than GPT-5.5).

## Slide 10 · What failed (45s)
- Bare-prompt + Gemini 2.5 defaults: 404 for new accounts, malformed JSON,
  rate limits. Documented in build log.
- Second failure: models over-trust themselves — the scorecard caught it.
- *Evidence:* `docs/build-log-session5-draft.md`.

## Slide 11 · What looks promising (45s)
- Structured PRD §3 contract worked: 120 calls, all parseable JSON.
- Escalation path catches the 60% of roofs where models disagree.
- Next test: calibration set of genuinely ambiguous roofs, tune escalation
  recall toward 1.0.

## Slide 12 · Recommendation (60s) — close strong
- **Revise the escalation behavior, then run a limited test (100 roofs).**
- Add multi-source corroboration (public NYC permits + footprints) to catch
  confident wrong answers — data validated, path designed
  (`docs/multisource-verification.md`).
- Explicitly NOT stop, NOT deploy as-is.
- Cost is not the blocker: $0.002–$0.013 per correct roof.
- Risks: recall stays low (rubber stamp), escalation explodes (no savings),
  imagery domain shift (needs NYC calibration), **and missing/bad-input
  abstain behavior is defined in PRD §5 but untested — it is part of the
  limited test.**
- Close: "The scanner stays; the ambiguous roofs get a second, explainable,
  human-escalated look."

---

## Q&A preparation

Likely questions and honest answers:

- **"Why is accuracy below 90%?"** Thermal/oblique imagery is harder than
  stock photos; our prompt is a first cut. That is why we recommend a
  revision + limited test, not deployment.
- **"Which model would you use?"** GPT-5.5 for accuracy now; Gemma for
  cost-sensitive bulk with human escalation; revisit after prompt tuning.
- **"Is escalation recall measurable?"** Not on this set (no ground-truth
  ties after 5 labelers). It is the first thing the limited test measures.
- **"What data did you use?"** Public CC drone dataset + NYC Open Data.
  No Con Edison data — we will ask what is shareable.
- **"You claim multi-source verification — did you actually test it
  end-to-end?"** Honest answer: **the capability works, the end-to-end
  test is blocked by data, not by the prototype.**
  - What works (verified): context injection into classification
    (`--context`); the model demonstrably uses context (sv-0003 went from
    uncertain 0.45 → no_solar 0.85); NYC permit lookup API is live and
    returns records by address; the decision branch follows rules 20/20.
  - Why we could not score it end-to-end: our 30 benchmark images are
    **anonymous** — no address, no parcel ID — so we cannot join them to
    real NYC records. No join key = no real-data score.
  - Analogy: we built and bench-tested every part of the engine
    (injection, lookup, rules) but the test chassis has no VIN — we cannot
    register it against the real records until Con Edison shares N roofs
    with parcel IDs. That is the first step of the 100-roof limited test.
  - The synthetic context demo is clearly marked as synthetic
    (`data/benchmark-v1/context/*.json`) — mechanism proof, not accuracy.

## Before class checklist

- [ ] Download `presentation/index.html`; open offline (venue network is not
      guaranteed)
- [ ] Assign speakers per the role table above (Yongpeng 1–3, Victor 4–6,
      Praewa 7–8, Kenji 9–10, Tanapat 11–12)
- [ ] Each speaker confirms their slides via agent: "Which slides am I
      presenting?" (reads `presentation/SPEAKER-ASSIGNMENTS.md`)
- [ ] Rehearse once; time each section
- [ ] Have `docs/team-links.md` handy for follow-up links
- [ ] Print the 3 questions to Con Edison (`docs/con-edison-questions.md`)
