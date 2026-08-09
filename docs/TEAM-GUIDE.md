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

## 2. Your task right now: label 30 images (~15 min)

This is the team's current bottleneck — the ground truth that lets us score
the three AI models.

1. Open **`data/benchmark-v1/labeling/label-standalone.html`**
   (double-click; it works in any browser, no install. All 30 images are
   embedded in the file, so nothing else is needed).
2. Type your **GitHub handle** in the box at the top.
3. For each image choose one of:
   - **Solar** — panels clearly visible
   - **No solar** — no panels; HVAC/skylights/obstructions are fine
   - **Uncertain** — genuinely cannot decide (this is the honest answer)
4. When progress shows **30/30**, click **Export my labels (JSON)**.
   It downloads `labels-<your-handle>.json`.
5. **Send that file back** to Yongpeng, or commit it to the repo under
   `data/benchmark-v1/labels/<your-handle>.json`:
   ```bash
   mkdir -p data/benchmark-v1/labels
   # put labels-<handle>.json there
   git add data/benchmark-v1/labels/
   git commit -m "Add my benchmark labels"
   git push
   ```

Full instructions: [docs/labeling-task.md](labeling-task.md)

## 3. What's already in the repo

| Path | What it is |
|---|---|
| `opencode.json` | Team agent config (no keys; model, permissions, prompts) |
| `data/benchmark-v1/manifest.json` | All 161 candidate images, registered |
| `data/benchmark-v1/labeling/label-standalone.html` | **The labeling tool — use this** |
| `data/benchmark-v1/labeling/subset-30.json` | The 30-case benchmark subset metadata |
| `data/benchmark-v1/results/*.json` | Raw model outputs (gitignored, local) |
| `docs/benchmark-results.md` | Cross-provider comparison table |
| `docs/con-edison-questions.md` | Our 3 questions for the Con Edison clinic |
| `docs/labeling-task.md` | Labeling instructions (English) |
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
- Live labeling tool:
  https://alan12-li.github.io/solarscan-verify-team-1/data/benchmark-v1/labeling/label-standalone.html
- Labeling tool (in repo): `data/benchmark-v1/labeling/label-standalone.html`
- Benchmark results: `docs/benchmark-results.md`
- PRD (course repo): `sims/solarscan-verify/PRD.md` in
  clg236/applied-generative-ai-course-students

## 7. Why GitHub links show source code, and how to view HTML

GitHub deliberately does **not** render `.html` files in the browser
(security: HTML can run scripts on the github.com domain). `github.com/.../blob/...`
and `raw.githubusercontent.com/...` both show the source text.

Our repo is **private**, so htmlpreview.github.io and GitHub Pages (free
tier) do **not** work either. The reliable options:

| Option | How | Use for |
|---|---|---|
| **Download & double-click** (recommended) | Open the blob link → **Download raw file** → double-click the downloaded `.html` | Everything; works offline, no network needed |
| **Local server** (team review on same network) | In the repo root run `python3 -m http.server 8000`, then open `http://localhost:8000/presentation/index.html` | Previewing the presentation together |

**Presentation day:** download `presentation/index.html` ahead of time and
open it in a browser in fullscreen (F11) — do not depend on the venue's
network.
