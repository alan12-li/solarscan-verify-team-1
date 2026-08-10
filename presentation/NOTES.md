# Presentation Notes — Session 6 (Aug 11, 2026)

**Deck:** `presentation/index.html` (11 slides — cover + 10 content,
real-NYC-roofs version; self-contained; open in a browser, F11 for fullscreen)
**Time:** 10 minutes + Q&A. Target ~45–60 seconds per slide.
**Team roles (5 speakers):**
| Slides | Speaker | Section |
|---|---|---|
| Cover–1 | **Yongpeng** (opens) | Title · Problem — 6 real NYC roofs |
| 2–3 | **Victor** | Prototype pipeline · Evaluation design |
| 4–5 | **Praewa** | Model vs human · The two mistakes |
| 6–7 | **Kenji** | Multi-source verification · Surprising facts |
| 8–9 | **Tanapat** | What failed → works · **Live demo** |
| 10 | **Yongpeng** | **Live demo (hands-on)** |
| 11 | **Tanapat** (closes) | Recommendation |

Yongpeng opens (Cover–1) and Tanapat closes (11); demo is hands-on —
the person at the machine runs it (usually Yongpeng, who built it).
Rehearse once as a group before class. If someone is absent, the person
next in the table covers their slides.

> **Agent lookup:** each teammate can ask their agent "Which slides am I
> presenting?" — the agent reads `presentation/SPEAKER-ASSIGNMENTS.md` and
> answers from the table.

> Decision owner: **Yongpeng** (repo owner, benchmark lead). If a slide's
> number is challenged, cite the evidence path listed under it.

---

## Cover · Title (20s) — Yongpeng
- One line: "SolarScan Verify — a verification layer for Con Edison's
  rooftop solar scanner, with a live multi-model prototype."
- Name the team + the brief (Solar Scanner Optimization).

## Slide 1 · Problem — 6 real NYC roofs (60s) — Yongpeng
- Six real Manhattan roofs from **public NYC orthoimagery** (~0.5 m/px),
  shown as a grid: solar = 511 W 182nd St 2024 (permit Completed 2022);
  no_solar = 1086291, 1086435; hard = 1086408 (human uncertain — only
  Kimi agreed), 1086361 (GPT-5.5 said solar ✗), 511 W 182nd 2018
  (pre-install vs 2024).
- Two costly errors: Error A false "solar" → field visit to a bare roof
  (truck + team wasted); Error B false "no solar" → missed generation.
- Today every ambiguous roof = manual review by a person; our slice is the
  verification step, not a new scanner.
- *Evidence:* `docs/nyc-human-validation.md`.

## Slide 2 · The prototype we actually built (60s) — key slide — Victor
- Walk the pipeline: image + optional context → **4 models in parallel**
  (temp 0, same prompt) → each returns {label, confidence, escalate} →
  decision rule (agree & conf ≥ .6 accept; else human review) →
  **corroboration** (public permit + footprint checks, branch tested 20/20)
  → analyst decides.
- Emphasize: the agent **recommends, a person decides**; escalate is never
  auto-accepted (PRD §5, §8).
- *Evidence:* `scripts/demo_server.py`, `scripts/test_corroboration.py`.

## Slide 3 · Evaluation: 6 real NYC roofs (45s) — Victor
- 6 real roofs, **1 human labeler** (labeled before seeing model calls),
  4 models, public records cross-check.
- One address has a **Completed solar permit (2022)** — known positive case.
- Same roof imaged **2018 and 2024** — tests imagery-date sensitivity.
- 24 model calls, all parseable JSON.
- *Evidence:* `docs/nyc-human-validation.md`.

## Slide 4 · Model vs human on real roofs (60s) — key slide — Praewa
- Table: 6 roofs × human × 4 models.
- **Kimi K3 6/6** (100%) · Gemini 5/6 · Gemma 5/6 · GPT-5.5 4/6.
- Kimi was the **only** model to say "uncertain" where the human did
  (1086408) — open-weights honesty.
- GPT-5.5's one miss was the **costly direction** (false "solar").
- *Evidence:* `docs/nyc-human-validation.md`.

## Slide 5 · What the two mistakes tell us (45s) — Praewa
- **GPT-5.5 on 1086361:** human no_solar, GPT-5.5 said solar at conf 0.76 —
  **above the 0.6 accept threshold** → the rule would have passed a false
  positive (truck to a bare roof).
- **Kimi on 1086408:** human uncertain, Kimi uncertain 0.45 — doubt maps to
  human doubt → exactly what an escalation layer wants.
- Lesson: a single confident call is not enough — corroboration + human
  review on split/low-confidence cases.

## Slide 6 · Multi-source verification works (45s) — Kenji
- Pipeline: NYC Building Footprints (BBL) → ortho tile (public, CC BY 4.0)
  → 4 models → **LL24 permit cross-check by address**.
- Branch logic tested **20/20** (10 scenarios × 2 models).
- **Time matters:** 511 W 182nd St is no_solar in 2018 (pre-install) and
  solar in 2024 — imagery date must match the question.
- *Evidence:* `docs/multisource-verification.md`.

## Slide 7 · Surprising facts (45s) — Kenji
- **Humans hesitated — only one model agreed:** on 1086408 only Kimi said
  uncertain too; the other three were confidently wrong.
- **Open-weights = honest about doubt:** Kimi matched the human 6/6;
  Kimi/Gemma are far cheaper than GPT-5.5.

## Slide 8 · What failed → what works (45s) — Tanapat
- **Failed:** bare-prompt classification (inconsistent, no confidence);
  confident wrong answers (GPT-5.5 false "solar" 0.76 — real data, not
  theory).
- **Works:** structured contract (24 calls parseable); clear cases
  separable; **doubt signal works** (Kimi uncertain ↔ human uncertain);
  multi-source branch 20/20; real NYC pipeline end-to-end.

## Slide 9–10 · 🖥️ Live demo (90s) — hands-on (machine operator: Yongpeng)
Two links, both on this slide:
- **🔗 Capstone demo (any machine, incl. professor's):**
  https://alan12-li.github.io/solarscan-verify-team-1/presentation/demo.html
  — paste your OpenRouter key once → **LIVE mode**: real 4-model calls on
  any address or photo. Without a key it runs **DEMO MODE** (pre-recorded
  real results) so it always works.
- **🔗 Local demo (this laptop, live backend):**
  http://127.0.0.1:8765 — started with
  `python3 scripts/demo_server.py`; uses the machine's keys, no key entry.

Suggested flow (45s each):
1. **Address mode:** type `511 W 182nd St` → geocode → 2024 ortho → 4 models
   say solar (0.97–1.0) → permit Completed 8/15/2022 → **ACCEPT "record
   agrees"**. (If on the professor's machine: open the capstone link, paste
   key, same flow.)
2. **Photo mode:** drop a hard roof (e.g. 1086361) → models split
   (GPT-5.5 solar 0.76 vs 3× no_solar) → **ESCALATE** → "truck to a bare
   roof" recommendation.

Fallback if the network is down: the demo slide itself carries the
pipeline diagram and both demo cases are in the deck's narrative — you can
still tell the story.

## Slide 11 · Recommendation (60s) — close strong — Tanapat
- **Revise the decision rule, then run a 100-roof limited test** (with Con
  Edison parcels → permit join at scale).
- Not "stop" (pipeline works end-to-end); not "deploy as-is" (one model
  confidently produced the costly error).
- What if we do nothing: the costly error class already exists in the
  scanner — verification is the mitigation, not the cost.
- Risks: permit coverage incomplete; imagery-date mismatch; one labeler
  isn't a consensus (need more humans).
- Also test missing/bad inputs (PRD §5 abstain) — untested so far.
- Close: "The scanner stays; the ambiguous roofs get a second, explainable,
  human-escalated look. Try it yourself on the demo."

---

## Q&A preparation

Likely questions and honest answers:

- **"Did you test on real NYC data?"** Yes — 6 real Manhattan roofs from
  public orthoimagery, labeled by a human, 4 models, plus permit
  cross-checks. The live demo runs these calls in front of you.
- **"Which model would you use?"** On real roofs Kimi K3 matched the human
  6/6 and is cheap; GPT-5.5 was accurate but produced the costly false
  "solar" — model choice matters less than the escalation rule + human
  review.
- **"Is escalation recall measurable?"** Not yet — 1 labeler, 6 roofs, no
  true-ambiguous ground truth. It is the first thing the 100-roof limited
  test measures.
- **"What data did you use?"** Public NYC orthoimagery (CC BY 4.0), Building
  Footprints, LL24 solar permits. No Con Edison data — we will ask what is
  shareable.
- **"The demo says DEMO MODE — is it real?"** DEMO MODE is pre-recorded
  results from our real runs (2026-08-10). Paste an OpenRouter key → LIVE
  MODE runs real calls on any address/photo you type.
- **"Why not test 30 anonymous images anymore?"** We replaced the anonymous
  benchmark photos with **real NYC roofs that have addresses** — that is
  what lets us join permits and prove the pipeline on real data.

## Before class checklist

- [ ] Download `presentation/index.html`; open offline (venue network is not
      guaranteed)
- [ ] **Demo links ready:** add both to browser bookmarks —
      capstone: https://alan12-li.github.io/solarscan-verify-team-1/presentation/demo.html
      local: http://127.0.0.1:8765 (start `python3 scripts/demo_server.py` first)
- [ ] If using the professor's machine: open the capstone demo link, have
      your OpenRouter key ready to paste (never leave it saved on their machine)
- [ ] Assign speakers per the role table above (Yongpeng Cover–1 + demo,
      Victor 2–3, Praewa 4–5, Kenji 6–7, Tanapat 8–9 + 11)
- [ ] Each speaker confirms their slides via agent: "Which slides am I
      presenting?" (reads `presentation/SPEAKER-ASSIGNMENTS.md`)
- [ ] Rehearse once; time each section (demo = 90s max)
- [ ] Have `docs/team-links.md` handy for follow-up links
- [ ] Print the 3 questions to Con Edison (`docs/con-edison-questions.md`)
