# SolarScan Verify — Team Guide

Everything a teammate needs to get set up, contribute, and label.

**Repo:** https://github.com/alan12-li/solarscan-verify-team-1 (private)
**Capstone:** Con Edison · Solar Scanner Optimization
**Team:** Yongpeng Li (alan12-li) · Praewa Udomlertsakul (pointpraewa) ·
Kenji Tannady (ktannady22) · Tanapat Boontuam (tanapreuk) · Victor Chan (Vchan5526)

---

## 1. First-time setup (one time, ~10 min)

1. **Accept the GitHub invite** — check your GitHub notifications
   (bell icon, top-right) or open the invitation link sent in chat.
2. **Clone the repo** (or use GitHub Desktop):
   ```bash
   git clone https://github.com/alan12-li/solarscan-verify-team-1.git
   cd solarscan-verify-team-1
   ```
3. **Connect your own OpenRouter key** in OpenCode:
   - Start OpenCode from the repo root (it auto-loads `opencode.json`)
   - `/connect` → **OpenRouter** → paste **your own** key
     (get one at [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys);
     the team recommended setup is $5 credit + $5 limit, name it `stern-course-agent`)
   - `/models` → confirm `openrouter/google/gemini-3.5-flash-lite`
4. **Never** paste a key into chat, a file, or a commit. Each teammate uses
   their own key. If you think a key leaked, say so immediately.

## 2. Where we are now (Session 6 ready)

Labeling is **complete** — all 5 teammates labeled the 30-image set; ground
truth is locked (majority vote) and the final deck is NYC-data based.

1. **Final deck:** `presentation/index.html` (10 slides, self-contained;
   open in any browser, works offline once downloaded).
2. **Results to review:** `docs/benchmark-results.md`,
   `docs/nyc-human-validation.md` (6 real NYC roofs, model vs human).
3. **Live:** https://alan12-li.github.io/solarscan-verify-team-1/presentation/

## 3. What's already in the repo

| Path | What it is |
|---|---|
| `opencode.json` | Team agent config (no keys; model, permissions, prompts) |
| `data/benchmark-v1/manifest.json` | All 161 candidate images, registered |
| `data/benchmark-v1/labeling/subset-30.json` | The 30-case benchmark subset metadata |
| `data/benchmark-v1/labels/*.json` | 5 teammates' labels (all complete) |
| `data/benchmark-v1/results/*.json` | Raw model outputs (gitignored, local) |
| `docs/benchmark-results.md` | Cross-provider comparison table |
| `docs/nyc-human-validation.md` | Model vs human on 6 real NYC roofs |
| `docs/prototype-fit.md` | Capstone brief compliance mapping (evidence paths) |
| `docs/multisource-verification.md` | Multi-source corroboration design (public NYC records) |
| `docs/value-for-conedison.md` | What the project improves for Con Edison (one-page) |
| `docs/labeling-progress.md` | Labeling status and disagreement resolution |
| `docs/con-edison-questions.md` | Our 3 questions for the Con Edison clinic |
| `docs/labeling-task.md` | Labeling instructions (historical — task complete) |
| `docs/reference/chartwise/` | Yongpeng's Project 2 PRD as a format reference |
| `scripts/` | Fetch, evaluate, analyze, verify, labeling-tool scripts |

## 4. Reproduce or extend the evaluation

```bash
# 1. (re)download the 161 images (12 MB) — images stay out of Git
python3 scripts/fetch_benchmark.py

# 2. verify labeling images == evaluation images (byte-identical)
python3 scripts/verify_image_integrity.py

# 3. run the 3 models on the 30-case subset (needs keys in env)
export GEMINI_API_KEY=<your-key-here>   # from aistudio.google.com
export OPENROUTER_API_KEY=<your-key-here>  # from openrouter.ai/settings/keys
python3 scripts/evaluate_benchmark.py --subset --resume

# 4. produce the comparison table
python3 scripts/analyze_results.py --subset
```

Models compared (same 30 images, same prompt, temperature 0):
`google/gemini-3.5-flash-lite` · `openai/gpt-5.5` · `moonshotai/kimi-k3`

## 5. Rules (from the PRD and course)

- **Data boundary:** public/synthetic data only. No Con Edison operational
  data, no customer info, no credentials, no `.env`, no raw media in Git.
- **Human review:** `uncertain`/low-confidence results are never auto-accepted;
  a person decides.
- **Git:** work on a branch (`work/<handle>/<task>`), show diffs, ask before
  pushing. `opencode.json` makes push an explicit approval step.
- **Ground truth rule:** each image needs ≥2 agreeing labelers; disagreements
  become `uncertain` (fail toward escalation).

## 6. Links

- Repo: https://github.com/alan12-li/solarscan-verify-team-1 (**PUBLIC — treat
  every push as public; no keys, no personal data, no Con Edison data**)
- Live presentation: https://alan12-li.github.io/solarscan-verify-team-1/presentation/
- NYC human validation: `docs/nyc-human-validation.md`
- Benchmark results: `docs/benchmark-results.md`
- Prototype-fit (brief compliance): `docs/prototype-fit.md`
- Labeling progress: `docs/labeling-progress.md`
- PRD (course repo): `sims/solarscan-verify/PRD.md` in
  clg236/applied-generative-ai-course-students

## 7. Live demo system (Session 6)

A local demo of the prototype: upload a roof photo **or** enter a NYC
address; 4 models classify in parallel, the decision rule fires, and
public NYC records cross-check the result.

```bash
# terminal 1: start the server (reads keys from env — never commit keys)
cd solarscan-verify-team-1
export GEMINI_API_KEY="$(cat ~/.gemini_api_key)"
export OPENROUTER_API_KEY="$(cat ~/.openrouter_api_key)"
python3 scripts/demo_server.py        # -> http://127.0.0.1:8765

# terminal 2 / browser: open the UI
open http://127.0.0.1:8765
```

- **Address mode** demo case: `511 W 182nd St` → 4 models say solar, permit
  Completed 8/15/2022 found → ACCEPT with record agreement.
- **Photo mode** demo case: upload any rooftop image (local files only,
  nothing leaves your machine except the API calls to the model providers).
- Files: `scripts/demo_server.py` (stdlib only, no pip installs),
  `presentation/demo.html` (UI). Keys are read from env only.

## 8. Why GitHub links show source code, and how to view HTML

GitHub deliberately does **not** render `.html` files in the browser
(security: HTML can run scripts on the github.com domain). `github.com/.../blob/...`
and `raw.githubusercontent.com/...` both show the source text.

Our repo is **public** with GitHub Pages enabled, so the presentation is
live at <https://alan12-li.github.io/solarscan-verify-team-1/presentation/>.
For a local copy, the reliable options:

| Option | How | Use for |
|---|---|---|
| **Download & double-click** (recommended) | Open the blob link → **Download raw file** → double-click the downloaded `.html` | Everything; works offline, no network needed |
| **Local server** (team review on same network) | In the repo root run `python3 -m http.server 8000`, then open `http://localhost:8000/presentation/index.html` | Previewing the presentation together |

**Presentation day:** download `presentation/index.html` ahead of time and
open it in a browser in fullscreen (F11) — do not depend on the venue's
network.
