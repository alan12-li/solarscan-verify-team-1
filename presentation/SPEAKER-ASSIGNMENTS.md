# Speaker Assignments — Session 6 (Aug 11, 2026)

This file lets each teammate's agent answer: **"Which slides am I
presenting?"** — the agent reads this table and replies with the speaker's
slides, section, and key points.

Deck: `presentation/index.html` (12 slides). Total time: 10 minutes + Q&A.

## Assignment table

| Slides | Speaker (GitHub) | Section | Key points to cover |
|---|---|---|---|
| 1–3 | **Yongpeng** (alan12-li) | Title · Problem · Approach | What we built · the ambiguous-roof problem · verify-don't-replace, benchmark setup |
| 4–6 | **Victor** (Vchan5526) | Agent system · Multi-source NYC · Results | Pipeline & decision rule · NYC roof pipeline verified (PATH B) · nobody hit 90% (83/73/67/53) |
| 7–9 | **Praewa** (pointpraewa) | Error breakdown · Human validation · Easy vs hard | Error classes, confidence signal · models vs 5-labeler consensus · baseline 83% vs harder 83/67/56/33 |
| 10–11 | **Kenji** (ktannady22) | Surprising facts · What failed | Humans hesitated, models didn't · open-weights honesty · Gemini 2.5 404/JSON/429 failures |
| 12–13 | **Tanapat** (tanapreuk) | Promising · Recommendation | Contract works · escalation path · revise → limited test · risks, close |

## Per-speaker detail (agent lookup answers)

### Yongpeng — slides 1–3
- **1 Title:** SolarScan Verify = verification layer; team; brief.
- **2 Problem:** 2 clear photos vs 2 hard photos; errors A/B; why this
  slice + ideation.
- **3 Approach:** same inputs, 4 models, structured output, fail toward a
  person; benchmark = 30 roofs, 5-labeler ground truth.

### Victor — slides 4–6
- **4 Agent system:** image → agent → 4 models → decision rule → corroboration
  (public records, branch tested 20/20) → human. Real/tested, human in loop.
- **5 Multi-source NYC:** real Manhattan roofs downloaded (public NYC Orthos
  2018, CC BY 4.0) via `fetch_nyc_roofs.py`; model classifies them (no_solar
  conf 0.9). Pipeline verified; accuracy needs labels + addresses (Con Edison
  step).
- **6 Results:** bar chart — GPT-5.5 83%, Gemini 73%, Kimi 67%, Gemma 53%;
  target 90%; nobody made it = finding.

### Praewa — slides 7–9
- **7 Error breakdown:** mostly no_solar→uncertain (24/37, recoverable);
  no_solar→solar ×3 (costly); confidence 0.78–0.96 vs 0.39–0.47.
- **8 Human validation:** hardest roofs sv-0018/sv-0003, per-model judgment
  table — escalation is the product.
- **9 Easy vs hard:** 12 agree-roofs all 83%; 18 disagree-roofs drop to
  83/67/56/33 — harder roof = more human needed.

### Kenji — slides 10–11
- **10 Surprising facts:** 5 disputed roofs → models confident anyway
  (sv-0133: Kimi said solar vs 2 humans no_solar); open-weights honest
  about doubt (Gemma 11/30, Kimi 8/30; Gemma 10× cheaper).
- **11 What failed:** Gemini 2.5 404 for new accounts; malformed JSON;
  429 rate limits; second failure = models over-trust themselves.

### Tanapat — slides 12–13
- **12 What looks promising:** output contract works (120 calls parseable);
  clear cases separable; multi-source branch 20/20; next test = 100 roofs.
- **13 Recommendation:** not stop / not deploy-as-is; revise escalation,
  limited test 100 roofs; cost not blocker ($0.002–0.013); risks incl.
  missing/bad inputs untested; close line.

## Speaker check

- [ ] Clone the repo and open `presentation/index.html`
- [ ] Ask your agent: "Which slides am I presenting? What should I cover?"
- [ ] Rehearse your slides; target ~2 minutes each
