# SolarScan Verify — Team Link Pack

Everything a teammate needs, in one place. Repo is **PUBLIC** — never push
keys, personal data, or Con Edison data.

---

## 🔗 Core links

| What | Link |
|---|---|
| **Team repo** | https://github.com/alan12-li/solarscan-verify-team-1 |
| **Presentation (live)** | https://alan12-li.github.io/solarscan-verify-team-1/presentation/ |
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

### 1. Accept the GitHub invite (if you haven't)

Check your GitHub notifications (bell icon) or open the invitation link from
the chat. Without accepting, you cannot push.

### 2. Review the results (labeling is complete)

All 5 teammates labeled the 30-image set. Ground truth is locked (majority
vote) and the final deck is based on 6 real NYC roofs:

1. Open the **Presentation (live)** link above — 10 slides, self-contained.
2. Read `docs/nyc-human-validation.md` (model vs human on real roofs).
3. Read `docs/benchmark-results.md` and `docs/value-for-conedison.md`.
4. Scripts under `scripts/` reproduce every number (no keys needed for
   review; model calls need your own API key).

### 3. Connect your own OpenRouter key in OpenCode

`/connect` → OpenRouter → your own key ($5 credit + $5 limit, name it
`stern-course-agent`). **Never share keys.**

### 4. Prove your agent can operate the repo

The capstone requires each member to make **one commit through their own
agent**. Your label commit (step 2) counts.

---

## 📊 Where we stand

- Benchmark: 30 images (public CC drone dataset), ground truth locked from
  2 labelers; 5 disagreements → `uncertain`
- Models compared: GPT-5.5, Gemini 3.5 Flash-Lite (baseline), Kimi K3
  (open-weights), Gemma 4 26B (open-weights)
- Result: no model meets PRD §6 targets yet (best clear-case accuracy 84%,
  best escalation recall 40%) — that is the finding we present

## ⚠️ Public-repo rules (short version)

- No API keys, passwords, tokens, `.env`
- No personal data (NYU IDs, emails, photos of people)
- No Con Edison operational data
- Public/synthetic data only
