# SolarScan Verify — Team Link Pack

Everything a teammate needs, in one place. Repo is **PUBLIC** — never push
keys, personal data, or Con Edison data.

---

## 🔗 Core links

| What | Link |
|---|---|
| **Team repo** | https://github.com/alan12-li/solarscan-verify-team-1 |
| **Presentation (live)** | https://alan12-li.github.io/solarscan-verify-team-1/presentation/ |
| **🎯 NYC 6-roof labeling tool** | https://alan12-li.github.io/solarscan-verify-team-1/data/nyc-validation/label-nyc.html |
| **Team guide** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/TEAM-GUIDE.md |
| **Benchmark results** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/benchmark-results.md |
| **NYC human validation** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/nyc-human-validation.md |
| **Prototype fit (brief compliance)** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/prototype-fit.md |
| **Multi-source verification** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/multisource-verification.md |
| **Value for Con Edison** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/value-for-conedison.md |
| **Labeling progress** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/labeling-progress.md |
| **Labeling task instructions** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/labeling-task.md |
| **PRD (course repo)** | https://github.com/clg236/applied-generative-ai-course-students/blob/main/sims/solarscan-verify/PRD.md |

---

## ✅ Your action items

### 1. 🎯 NEW: Label 6 real NYC roofs (~2 min) — one teammate needed

We upgraded the human validation to **3 labelers** (majority vote). One
teammate (Victor or Praewa — whoever is available) please do this:

1. Open the **NYC 6-roof labeling tool** link at the top of this page.
2. Type your GitHub handle → look at each of the 6 roof images (public NYC
   orthoimagery) → click **Solar / No solar / Uncertain**.
3. Click **⬇ Export my labels (JSON)** → save the file.
4. Push it to `data/nyc-validation/labels/<your-handle>.json` (via your
   agent: "save this file as data/nyc-validation/labels/<handle>.json and
   commit"), or just send the JSON to Yongpeng.

Your labels are stored only in your browser until you export — nothing is
uploaded automatically. This upgrades the deck from "1 labeler" to
"3 labelers, majority vote" for the demo tomorrow.

### 2. Accept the GitHub invite (if you haven't)

Check your GitHub notifications (bell icon) or open the invitation link from
the chat. Without accepting, you cannot push.

### 3. Review the results

The final deck is based on **6 real NYC roofs** (12 slides, self-contained):

1. Open the **Presentation (live)** link above — 12 slides, self-contained.
2. Read `docs/nyc-human-validation.md` (model vs human on real roofs).
3. Read `docs/benchmark-results.md` and `docs/value-for-conedison.md`.
4. Scripts under `scripts/` reproduce every number (no keys needed for
   review; model calls need your own API key).

### 4. Connect your own OpenRouter key in OpenCode

`/connect` → OpenRouter → your own key ($5 credit + $5 limit, name it
`stern-course-agent`). **Never share keys.**

### 5. Prove your agent can operate the repo

The capstone requires each member to make **one commit through their own
agent**. Your label commit (step 1) counts.

---

## 📊 Where we stand

- Benchmark: 30 images (public CC drone dataset), ground truth locked from
  5 labelers, majority vote (14 solar / 16 no_solar / 0 uncertain)
- Models compared: GPT-5.5, Gemini 3.5 Flash-Lite (baseline), Kimi K3
  (open-weights), Gemma 4 26B (open-weights)
- NYC validation: 6 real Manhattan roofs, human labels vs 4 models — Kimi
  6/6, Gemini 5/6, Gemma 5/6, GPT-5.5 4/6; **upgrading to 3 labelers now**

## ⚠️ Public-repo rules (short version)

- No API keys, passwords, tokens, `.env`
- No personal data (NYU IDs, emails, photos of people)
- No Con Edison operational data
- Public/synthetic data only
