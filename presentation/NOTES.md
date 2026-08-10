# Presentation Notes — Session 6 (Aug 11, 2026)

**Deck:** `presentation/index.html` (12 slides — cover + 11 content,
real-NYC-roofs version; live at
https://alan12-li.github.io/solarscan-verify-team-1/presentation/)
**Time:** 10 minutes + Q&A. Target ~45–60 seconds per slide.
**Team roles (5 speakers):**
| Slides | Speaker | Section |
|---|---|---|
| Cover–1 | **Yongpeng** (opens) | Title · Problem — 6 real NYC roofs |
| 2–3 | **Victor** | Prototype pipeline · Evaluation design |
| 4–5 | **Praewa** | Model vs human · The two mistakes |
| 6–7 | **Kenji** | Multi-source verification · Surprising facts |
| 8–10 | **Tanapat** | Model economics · What failed → works · Live demo intro |
| 11 | **Yongpeng** (hands-on) | 🖥️ Live demo |
| 12 | **Tanapat** (closes) | Recommendation |

Yongpeng opens (Cover–1) and Tanapat closes (12). The demo is hands-on —
the person at the machine runs it (usually Yongpeng, who built it). If
someone is absent, the person next in the table covers their slides.

> **Agent lookup:** each teammate can ask their agent "Which slides am I
> presenting?" — the agent reads `presentation/SPEAKER-ASSIGNMENTS.md` and
> answers from the table.

> Decision owner: **Yongpeng** (repo owner, benchmark lead). If a slide's
> number is challenged, cite the evidence path listed under it.

---

## Cover · Title (20s) — Yongpeng

**Say something like:** "Good morning — we're SolarScan Verify. Our brief
was Con Edison's Solar Scanner Optimization, and we built a verification
layer for the roofs the scanner gets wrong. And we brought a live demo."

- Name the team; keep it to one breath.

## Slide 1 · Problem — 6 real NYC roofs (60s) — Yongpeng

**Say something like:** "These are six real roofs in Manhattan, straight
from public NYC orthoimagery. Two of them are easy — this one has solar,
this one doesn't. A scanner handles those. The hard ones are the problem:
this roof made a human genuinely hesitate, and this one split our models —
one of them confidently said 'solar' on a roof with no panels."

- Grid: solar = 511 W 182nd St 2024 (permit Completed 2022); no_solar =
  1086291, 1086435; hard = 1086408 (human uncertain — only Kimi agreed),
  1086361 (GPT-5.5 said solar ✗), 511 W 182nd 2018 (pre-install vs 2024).
- Two costly errors: Error A false "solar" → a truck and a field team show
  up at a bare roof. Error B false "no solar" → generation we never see.
- Today every ambiguous roof means a person reviews it by hand — that's
  where we aimed.
- *Evidence:* `docs/nyc-human-validation.md`; images from NYC Orthos (public).

## Slide 2 · The prototype we actually built (60s) — key slide — Victor

**Say something like:** "Here's what we actually built. A roof image goes
in, four models look at it in parallel — Gemini, GPT-5.5, and two
open-weights, Kimi K3 and Gemma. Same prompt, temperature zero, so it's a
fair comparison. Each one returns a label, a confidence, and whether it
wants to escalate. Then a decision rule: if they agree and confidence is
decent, accept; otherwise a human reviews. And we cross-check public
records — permits and building footprints — before anyone signs off.
The agent recommends, a person decides."

- Pipeline: image + optional context → 4 models in parallel (temp 0, same
  prompt) → {label, confidence, escalate} → decision rule (agree & conf
  ≥ .6 accept; else human review) → corroboration (branch tested 20/20) →
  analyst decides.
- Emphasize: **real & tested** — 24 model calls on 6 real NYC roofs, all
  parseable JSON; escalated cases are never auto-accepted.
- *Evidence:* `scripts/evaluate_benchmark.py`, `scripts/test_corroboration.py`.

## Slide 3 · Evaluation: 6 real NYC roofs (45s) — Victor

**Say something like:** "Six real roofs, one human labeler — labels written
before the models ever saw the images, so there's no peeking. And we
deliberately built in two tricky features: one address has a completed
solar permit, so we know it's a real positive; and we imaged the same roof
in 2018 and 2024, so we can test whether imagery date matters."

- Design: 1 human labeler labels solar/no_solar/uncertain **before seeing
  model calls**; 4 models; public records (LL24 permits + Building
  Footprints).
- Deliberate features: permit-positive case (2022); same roof 2018 vs 2024.
- *Evidence:* `docs/nyc-human-validation.md`.

## Slide 4 · Model vs human on real roofs (60s) — key slide — Praewa

**Say something like:** "Here's the table that tells the whole story.
Against the human, Kimi got 6 out of 6. Gemini and Gemma 5. GPT-5.5 got 4 —
and its one miss was the expensive kind: it called 'solar' at 0.76 on a
roof with no panels. Meanwhile on the roof where the human was genuinely
unsure, Kimi was the only model that also said 'I'm not sure.' That's
exactly the honesty an escalation layer needs."

- Agreement: Kimi 6/6, Gemini 5/6, Gemma 5/6, GPT-5.5 4/6.
- Kimi honest about doubt: only model that said "uncertain" where the human
  did (1086408). GPT-5.5 false positive: "solar" at 0.76 on 1086361.
- *Evidence:* `docs/nyc-human-validation.md`.

## Slide 5 · What the two mistakes tell us (45s) — Praewa

**Say something like:** "These two mistakes are worth a closer look. On
1086361, GPT-5.5 said solar at 0.76 — and our accept threshold was 0.6, so
the rule as written would have passed a false positive. A truck shows up at
a bare roof. And on 1086408, Kimi's uncertainty matched the human's — the
other three models were confident and wrong. So the lesson is: a single
confident call is not enough. You need corroboration and a human on the
split cases."

- GPT-5.5 on 1086361: human no_solar, GPT-5.5 solar at 0.76 — 0.76 > 0.6
  threshold → the rule would have passed a false positive.
- Kimi on 1086408: human uncertain, Kimi uncertain at 0.45 — doubt maps to
  human doubt → exactly the escalation behavior the layer wants.

## Slide 6 · Multi-source verification works (45s) — Kenji

**Say something like:** "We didn't stop at the image. Building footprints
give us the roof's geometry, the orthoimagery gives us the roof itself,
four models classify it, and then we check the public solar permit record
for that address. The decision branch follows the rules 20 out of 20 times.
And here's a finding we didn't expect: imagery date matters. The same roof
reads 'no solar' in 2018 and 'solar' in 2024 — because it was installed in
between. If your imagery is older than your question, you'll miss it."

- Pipeline: footprints (BBL) → ortho tile (CC BY 4.0) → 4 models → LL24
  permit cross-check by address.
- Branch logic 20/20; time matters (511 W 182nd 2018 no_solar vs 2024
  solar); context injection works.
- *Evidence:* `docs/multisource-verification.md`, `scripts/test_corroboration.py`.

## Slide 7 · Surprising facts (45s) — Kenji

**Say something like:** "Two things surprised us. First: on the roof where
humans hesitated, only one model hesitated with us — the other three were
confidently wrong. Second: it's the open-weights models that are honest
about doubt. Kimi matched the human on all six roofs, including the hard
one — and Kimi and Gemma cost a fraction of GPT-5.5. The closed models were
more confident, and more wrong."

- Humans hesitated — only one model agreed (1086408).
- Open-weights honest about doubt: Kimi 6/6, Gemma 5/6; closed models more
  confident and more wrong; Kimi/Gemma far cheaper.

## Slide 8 · What failed → what works (45s) — Tanapat

**Say something like:** "We tried some things that failed, and we're not
hiding them. Bare prompts gave us inconsistent output and no confidence
signal. And we saw a model confidently call 'solar' on a bare roof — that's
the costly error, on real data, not in theory. What works: a structured
output contract — 24 calls, all parseable. Clear cases separate cleanly.
And the doubt signal works — Kimi's uncertainty matched the human's. That's
the foundation we'd build on."

- Failed: bare-prompt (no confidence); confident-wrong (GPT-5.5 0.76).
- Works: structured contract 24/24; clear cases separable; doubt signal
  (Kimi ↔ human); multi-source 20/20; real NYC pipeline.

## Slide 9 · Model economics — real cost per roof (45s) — Tanapat

**Say something like:** "You might be thinking — four models on every roof,
isn't that expensive? Let's show you the actual bills. We ran the same
rooftop image through all four models and looked at what OpenRouter charged
us. Look at these bars. Gemma — the open-weight one — six hundredths of a
cent. Gemini, under half a cent. Kimi, the other open model, about
two-tenths of a cent. And GPT-5.5 at the end — two point six tenths of a
cent. That bar is forty-four times the first one. But here's the thing:
the whole panel — all four models, one roof — costs about half a cent. Run
a hundred roofs through all four models and you're at fifty cents. One
unnecessary truck visit costs more than that — the field team, the
vehicle, the afternoon. So cost was never our bottleneck. The bottleneck
is a model confidently saying 'solar' on a roof with no panels. And the
nicest part? The cheapest models here — Kimi and Gemma — are the ones
that were honest about doubt. Kimi matched the human on all six real
roofs. So when we design the system, we optimize for accuracy and honest
uncertainty — not for the price tag."

- Measured (2026-08-10, OpenRouter, same image 511 W 182nd 2024, temp 0):
  Gemma $0.000059 · Gemini $0.00044 · Kimi $0.00191 · GPT-5.5 $0.00260 per image.
- 4 models × 1 roof ≈ $0.005; 100 roofs × 4 models ≈ $0.50.
- Open-weights ~44× cheaper than GPT-5.5 AND Kimi matched the human 6/6.
- Cost is not the blocker — accuracy + honest doubt is.
- *Evidence:* `docs/model-cost-measurement.md` (method + full table).

**Pacing:** point at each bar as you name it; pause after "forty-four
times" — that's the visual punchline. End on "honest uncertainty, not the
price tag" and transition: "So what actually failed, and what worked?"

## Slide 10 · Live demo intro (20s) — Tanapat

**Say something like:** "All of that is a live prototype — and you can try
it yourself. The next slide is hands-on; our operator will run it for you."

- Short hand-off; don't steal the demo's thunder.

## Slide 11 · 🖥️ Live demo (90s) — hands-on (machine operator: Yongpeng)

**Say something like:** "Here it is. Two ways to open it: the Local demo on
this laptop — one click, keys already loaded, real calls. Or the Capstone
demo — that's the same page on GitHub Pages, so it works on any machine,
even the professor's; paste an OpenRouter key for live calls, or it runs
pre-recorded results with no key at all. Let's do an address first."

Two links on the slide:
- **💻 Local demo (this laptop):** http://127.0.0.1:8765
- **🌐 Capstone demo (any machine):**
  https://alan12-li.github.io/solarscan-verify-team-1/presentation/demo.html

Flow (45s each):
1. **Address mode:** type `511 W 182nd St` → geocode → 2024 ortho → 4 models
   say solar (0.97–1.0) → permit Completed 8/15/2022 → **ACCEPT "record
   agrees"**.
2. **Photo mode:** drop a hard roof (e.g. 1086361) → models split
   (GPT-5.5 solar 0.76 vs 3× no_solar) → **ESCALATE** → "truck to a bare
   roof" recommendation.

Fallback if the network is down: the slide itself carries the pipeline
diagram; tell the story from the deck.

## Slide 12 · Recommendation (60s) — close strong — Tanapat

**Say something like:** "So where does this leave Con Edison? Not 'stop' —
the pipeline works end to end on real New York roofs. Not 'deploy as-is' —
one model confidently produced the expensive error. Our recommendation:
revise the decision rule, then run a 100-roof limited test with real parcel
IDs, so we can join permits at scale. And if we do nothing, the costly
error class is already in the scanner — verification is the mitigation, not
the cost. The scanner stays; the ambiguous roofs get a second, explainable,
human-escalated look. And you can try it — the demo is one click away."

- Revise decision rule → 100-roof limited test (Con Edison parcels → permit
  join at scale).
- Not "stop"; not "deploy as-is". If we do nothing: costly error class
  already in the scanner.
- Risks: permit coverage incomplete; imagery-date mismatch; one labeler
  isn't a consensus.
- Missing/bad-input abstain behavior (PRD §5) untested — part of the test.
- Ask Con Edison: N roofs with parcel IDs; which context is shareable
  (footprints, permits, historical imagery); calibration set of genuinely
  ambiguous roofs.
- *Evidence:* `docs/value-for-conedison.md`, `docs/con-edison-questions.md`.

---

## Q&A preparation

Likely questions and honest answers:

- **"Why only 6 roofs?"** It's a real-data validation set from public NYC
  orthoimagery with one human labeler — deliberately small and honest. The
  100-roof limited test with Con Edison parcels scales it.
- **"Which model would you use?"** Kimi matched the human 6/6 including the
  uncertain case and is far cheaper; GPT-5.5 is strong on clear cases but
  produced the costly false positive. Revisit after revising the decision
  rule.
- **"Is one human labeler enough?"** No — that's a stated limitation. The
  ground rule is ≥2 agreeing labelers; the limited test adds more humans.
- **"What data did you use?"** Public NYC orthoimagery (CC BY 4.0), NYC
  Building Footprints, LL24 solar permits. No Con Edison data — we will ask
  what is shareable.
- **"Did you test multi-source end-to-end?"** The capability is verified
  piecewise: context injection works, the permit lookup API is live, the
  decision branch follows rules 20/20. Scoring it end-to-end needs parcel
  IDs to join roofs to real records — that's the first step of the
  100-roof test.
- **"The 2018 vs 2024 roof?"** 511 W 182nd St — no_solar in 2018
  (pre-install), solar in 2024, permit Completed 2022. Imagery date must
  match the question being asked.
- **"The demo says DEMO MODE — is it real?"** DEMO MODE is pre-recorded
  results from our real runs (2026-08-10). Paste an OpenRouter key → LIVE
  MODE runs real calls on any address or photo you type.

## Before class checklist

- [ ] Download `presentation/index.html`; open offline (venue network is not
      guaranteed)
- [ ] **Demo links ready:** bookmark both — local
      (http://127.0.0.1:8765, start `python3 scripts/demo_server.py`) and
      capstone (https://alan12-li.github.io/solarscan-verify-team-1/presentation/demo.html)
- [ ] If using the professor's machine: open the capstone demo link, have
      your OpenRouter key ready to paste (never leave it saved on their machine)
- [ ] Assign speakers per the role table above (Yongpeng Cover–1 + demo,
      Victor 2–3, Praewa 4–5, Kenji 6–7, Tanapat 8–10 + 12)
- [ ] Each speaker confirms their slides via agent: "Which slides am I
      presenting?" (reads `presentation/SPEAKER-ASSIGNMENTS.md`)
- [ ] Rehearse once; time each section (demo = 90s max)
- [ ] Have `docs/team-links.md` handy for follow-up links
- [ ] Print the questions to Con Edison (`docs/con-edison-questions.md`)
