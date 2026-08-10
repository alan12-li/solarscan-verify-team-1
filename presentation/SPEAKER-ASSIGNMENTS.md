# Speaker Assignments — Session 6 (Aug 11, 2026)

This file lets each teammate's agent answer: **"Which slides am I
presenting?"** — the agent reads this table and replies with the speaker's
slides, section, and key points.

Deck: `presentation/index.html` (11 slides — cover + 10 content,
real-NYC-roofs version; live at
https://alan12-li.github.io/solarscan-verify-team-1/presentation/).
Total time: 10 minutes + Q&A.

## Assignment table

| Slides | Speaker (GitHub) | Section | Key points to cover |
|---|---|---|---|
| Cover–1 | **Yongpeng** (alan12-li) | Title · Problem — 6 real NYC roofs | Team names + brief · Errors A/B · every ambiguous roof is manual review today · the 6-roof grid (511 W 182nd 2024 solar, 1086291/1086435 no_solar, 1086408/1086361/511-2018 hard) |
| 2–3 | **Victor** (Vchan5526) | Prototype · Evaluation | Pipeline: image+context → 4 models → decision rule → corroboration → human · 24 real calls, parseable JSON · eval design: 1 human labeler, permit-positive case, 2018 vs 2024 |
| 4–5 | **Praewa** (pointpraewa) | Model vs human · The two mistakes | Human-labeler story · Kimi 6/6, Gemini/Gemma 5/6, GPT-5.5 4/6 · GPT-5.5 false "solar" at 0.76 (above 0.6 threshold) · Kimi's uncertain maps to the human's |
| 6–7 | **Kenji** (ktannady22) | Multi-source verification · Surprising facts | Footprints → orthos → models → permit cross-check · 20/20 branch · 2018 vs 2024 date sensitivity · humans hesitated, only Kimi agreed · open-weights honest about doubt |
| 8–9 | **Tanapat** (tanapreuk) | What failed → works · Live demo intro | Bare-prompt + confident-wrong failures · structured contract 24/24 · doubt signal works · hand off to the machine operator for the live demo |
| 10 | **Yongpeng** (alan12-li) | **Live demo (hands-on)** | Open capstone demo link (any machine) or local server (this laptop) · address mode 511 W 182nd St → ACCEPT + permit · photo mode hard roof → ESCALATE · see NOTES.md Slide 9–10 for links & flow |
| 11 | **Tanapat** (tanapreuk) | Recommendation (closes) | Revise decision rule → 100-roof limited test · not stop / not deploy as-is · risks (permit coverage, imagery date, 1 labeler) · missing/bad-input abstain untested · close line |

Hand-off order: Yongpeng → Victor → Praewa → Kenji → Tanapat → (demo: Yongpeng) → Tanapat closes.

## Per-speaker detail (agent lookup answers)

### Yongpeng — Cover–1 (opens) + slide 10 (live demo)
- **Cover:** "SolarScan Verify — a verification layer for Con Edison's
  rooftop solar scanner, with a live multi-model prototype." Name team + brief.
- **1 Problem:** 6 real Manhattan roofs from public NYC orthoimagery
  (~0.5 m/px): solar = 511 W 182nd St 2024 (permit Completed 2022);
  no_solar = 1086291, 1086435; hard = 1086408 (human uncertain — only
  Kimi agreed), 1086361 (GPT-5.5 said solar ✗), 511 W 182nd 2018
  (pre-install vs 2024). Error A: false "solar" → field visit to a bare
  roof (truck + team wasted). Error B: false "no solar" → missed
  generation. Today every ambiguous roof = manual review.
- **10 Live demo:** two links on the slide:
  - Capstone (any machine): https://alan12-li.github.io/solarscan-verify-team-1/presentation/demo.html
    — paste OpenRouter key → LIVE mode (real calls); no key → DEMO MODE
    (pre-recorded real results).
  - Local (this laptop): http://127.0.0.1:8765 — `python3 scripts/demo_server.py`.
  - Flow: address `511 W 182nd St` → ACCEPT solar + permit 8/15/2022;
    photo hard roof → ESCALATE. 45s each, 90s total.

### Victor — slides 2–3
- **2 Prototype:** image + context → 4 models in parallel (temp 0, same
  prompt) → {label, confidence, escalate} → decision rule (agree & conf
  ≥ .6 accept; else human review) → corroboration (public records, branch
  20/20) → analyst decides. Agent recommends, a person decides.
- **3 Evaluation:** 6 real roofs, 1 human labeler (labeled before seeing
  model calls), 4 models, permit-positive case, 2018 vs 2024 imagery-date
  test, 24 calls parseable JSON.

### Praewa — slides 4–5
- **4 Model vs human:** table 6 roofs × 4 models; Kimi 6/6, Gemini 5/6,
  Gemma 5/6, GPT-5.5 4/6; Kimi only model to say uncertain where human did
  (1086408).
- **5 Two mistakes:** GPT-5.5 false "solar" 0.76 on 1086361 (above 0.6
  threshold → rule would pass a false positive); Kimi uncertain 0.45 on
  1086408 maps to human doubt → escalation is the product.

### Kenji — slides 6–7
- **6 Multi-source:** footprints → ortho tile (CC BY 4.0) → 4 models →
  LL24 permit by address; branch 20/20; time matters (511 W 182nd 2018
  no_solar vs 2024 solar).
- **7 Surprising:** humans hesitated, only Kimi agreed; open-weights honest
  about doubt; Kimi/Gemma cheaper than GPT-5.5.

### Tanapat — slides 8–9 + 11 (closes)
- **8 What failed → works:** failed = bare-prompt + confident-wrong
  (GPT-5.5 false solar, real data); works = structured contract 24/24,
  doubt signal, multi-source 20/20, real NYC pipeline.
- **9 Intro demo:** "we built a live prototype you can try — the next slide
  is hands-on; our operator will run it." Hand off to Yongpeng.
- **11 Recommendation:** revise decision rule → 100-roof limited test with
  Con Edison parcels; not stop / not deploy as-is; risks (permit coverage,
  imagery date, 1 labeler not consensus); missing/bad-input abstain
  untested; close: "The scanner stays; the ambiguous roofs get a second,
  explainable, human-escalated look. Try it yourself on the demo."
