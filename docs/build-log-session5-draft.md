# Session 5 Build Log — Draft (Yongpeng)

> Draft prepared before Session 5 from real work done on 2026-08-08.
> The in-class log is written in the last 20 minutes of Session 5; this is the
> material to draw from, not a replacement for the in-room writing.
> Evidence links: see "Evidence" section at the bottom.

---

## 1. What did I try today?

Built the benchmark and evaluation pipeline for SolarScan Verify:
- Assembled a 30-image benchmark subset (19 test + 11 valid) from the
  CC-licensed `Francesco/solar-panels-taxvb` drone dataset, with NYC Open
  Data context sources documented.
- Ran three vision models — **Gemini 3.5 Flash-Lite** (Gemini API),
  **GPT-5.5** and **Kimi K3** (via OpenRouter) — on the same 30 images with
  the same prompt, temperature 0.
- Locked ground truth from two labelers (mine + Victor's), 5 disagreements
  resolved to `uncertain` per the labeling rule.
- Generated the PRD §6 scorecard.

## 2. What surprised me or failed?

**The headline finding: no model met the PRD §6 targets.**

| Model | Clear-case accuracy (≥90% target) | Escalation recall (1.0 target) |
|---|---|---|
| GPT-5.5 | 84% (21/25) | 20% (1/5) |
| Gemini 3.5 Flash-Lite | 80% (20/25) | 40% (2/5) |
| Kimi K3 | 76% (19/25) | 40% (2/5) |

What surprised me most was **escalation recall**: of the 5 ground-truth
`uncertain` cases, the best models caught only 2. The models are *too
confident* on exactly the rooftops that need a human — which is the core
problem SolarScan Verify exists to solve. A confident wrong answer on an
ambiguous roof is worse than an honest "uncertain", and that is what the
benchmark exposed.

## 3. What will I do differently next?

- **Prompt tuning for escalation**: the current system prompt says
  "escalate when uncertain or confidence < 0.6" but models still under-escalate.
  Next test: force the confidence threshold behavior (see "Next test" below).
- **Don't commit raw images**: caught `.gitignore` gap — `data/**/images/`
  was needed to keep 161 downloaded images out of Git. Fixed and verified.
- **Rate limits are the enemy**: free-tier 429s cost ~25 min of retries.
  Next time: batch API calls with longer delays from the start.

---

## The correction (Session 5 required element)

| What the agent did | What I expected | What I changed |
|---|---|---|
| The evaluation script first used Gemini 2.5 Flash models | They would classify the images | New accounts get 404 on 2.5 ("no longer available to new users") — switched to Gemini 3.5 Flash-Lite + GPT-5.5 + Kimi K3 |
| One model returned multiple JSON objects in one response | Clean single JSON per image | Added robust JSON extraction (fence stripping + last-object fallback) — zero parse errors after fix |
| 429 rate limits after ~40 calls | Free tier would handle 300 calls | Added exponential-backoff retry (15→120s), `--resume` (skip done), `--delay` control |
| Images were not gitignored | `.gitignore`'s `data/raw/` covered everything | Added `data/benchmark-v1/images/` + `data/**/images/`; verified 161 files stay untracked |

## Which check caught it

- **Data boundary** caught: the `.gitignore` gap (images about to be committed).
- **Failure path** caught: 404 on 2.5 models; malformed JSON from one model;
  429 rate limiting.
- **Critical path** caught: escalation recall below target — the scorecard
  check itself is what revealed the models over-trust themselves.
- **Recovery** exercised: `--resume` let us keep 100 successful results and
  only re-run failures.

## One defined next test

**First thing I will check about anything the agent builds from our PRD:**
does raising the escalation behavior actually move escalation recall toward
1.0 on the 5 ground-truth `uncertain` cases — e.g. re-prompting with
"when in doubt, output `uncertain`" and re-scoring the same 30 images, or
tuning the confidence threshold. If recall stays at 40%, the prompt/contract
is the problem; if it rises, the fix is prompt-side, not model-side.

---

## Post-session additions (2026-08-10, before Session 6)

Work done after the Session 5 draft, listed so the final build log reflects
the whole arc:

### Multi-source verification — beyond the image alone

The 30-case benchmark's core finding was that models are confident on the
roofs humans hesitate over. To catch those confident-wrong answers, we
designed a **corroboration branch** using public records — this is the PRD
§3 "optional context" made concrete:

- **Validated two public NYC data sources (live API queries):**
  - Solar PV permits (LL24, dataset `cfz5-6fvh`) — address → permit status,
    installation date. Direct evidence a roof has solar.
  - Building footprints (dataset `5zhs-2jue`) — roof height, feature code,
    footprint geometry.
- **Tested the decision branch with real models**
  (`scripts/test_corroboration.py`): 10 synthetic {hypothesis, permit}
  scenarios × 2 models = **20/20 rule-following** (GPT-5.5 and Gemini
  3.5 Flash-Lite both 10/10).
- **Finding:** rule-following requires *unambiguous* rules. Iterating the
  prompt — separating "lookup OK, zero records" from "lookup unavailable",
  and making the confidence threshold literal (< 0.8) — took both models
  from ~88–94% to 100%. Same lesson as the main classification:
  **prompt quality is the system.**
- **Honest scope:** the branch logic is tested; the full image→records
  pipeline is not (the 30 benchmark images have no addresses to join).
  That end-to-end test is part of the proposed 100-roof limited test.
- Docs: `docs/multisource-verification.md`, `docs/value-for-conedison.md`.

### Other post-session updates (same day)

- **5-labeler ground truth locked** — all five teammates labeled 30/30 via
  their own agents (Kenji, Tanapat added after the draft); majority vote
  gives 14 solar / 16 no_solar / 0 uncertain, matching the earlier 3-labeler
  result (scorecard unchanged, robust to labeler count).
- **Presentation expanded to 12 slides** with real roof photos, error
  breakdown, human-validation table, and the multi-source branch.

## Evidence

- PRD: `sims/solarscan-verify/PRD.md` in clg236/... (merged PR #26)
- Benchmark results + scorecard: `docs/benchmark-results.md`
- Labeling progress + disagreements: `docs/labeling-progress.md`
- Ground truth: `data/benchmark-v1/ground-truth.json`
- Raw model outputs: `data/benchmark-v1/results/*.json` (gitignored, local)
- Scripts: `scripts/{fetch_benchmark,evaluate_benchmark,analyze_results,
  build_ground_truth,verify_image_integrity,test_corroboration}.py`
- Multi-source verification + value: `docs/multisource-verification.md`,
  `docs/value-for-conedison.md`
- Repo: https://github.com/alan12-li/solarscan-verify-team-1

## AI use disclosure

- Tools: OpenCode/Hermes agent (DeepSeek V4 Flash as assistant model),
  Google Gemini API, OpenRouter (GPT-5.5, Kimi K3).
- Where output helped: pipeline design, retry/backoff logic, robust JSON
  parsing, the labeling tool.
- Where my judgment changed/rejected it: I rejected the first evaluation
  setup (2.5 models — wrong for new accounts), and I chose to treat the
  "no model meets target" result as the finding rather than tuning numbers
  to look better. A confident wrong answer is the finding — write it down
  before fixing it.
