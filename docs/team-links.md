# SolarScan Verify — Team Link Pack

Everything a teammate needs, in one place. Repo is **PUBLIC** — never push
keys, personal data, or Con Edison data.

---

## 🔗 Core links

| What | Link |
|---|---|
| **Team repo** | https://github.com/alan12-li/solarscan-verify-team-1 |
| **Labeling tool (live)** | https://alan12-li.github.io/solarscan-verify-team-1/data/benchmark-v1/labeling/label-standalone.html |
| **Presentation (live)** | https://alan12-li.github.io/solarscan-verify-team-1/presentation/ |
| **Team guide** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/TEAM-GUIDE.md |
| **Benchmark results** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/benchmark-results.md |
| **Prototype fit (brief compliance)** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/prototype-fit.md |
| **Multi-source verification** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/multisource-verification.md |
| **Labeling progress** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/labeling-progress.md |
| **Labeling task instructions** | https://github.com/alan12-li/solarscan-verify-team-1/blob/main/docs/labeling-task.md |
| **PRD (course repo)** | https://github.com/clg236/applied-generative-ai-course-students/blob/main/sims/solarscan-verify/PRD.md |

---

## ✅ Your action items

### 1. Accept the GitHub invite (if you haven't)

Check your GitHub notifications (bell icon) or open the invitation link from
the chat. Without accepting, you cannot push.

### 2. Label 30 rooftop images (~15 min) — current bottleneck

1. Open the **labeling tool** link above (works in any browser, no install).
2. Type your **GitHub handle** in the box.
3. For each image: **Solar** / **No solar** / **Uncertain**
   (if unsure, choose Uncertain — that is the honest answer).
4. When progress shows **30/30**, click **Export my labels (JSON)**.
5. Send the downloaded `labels-<your-handle>.json` to Yongpeng, or commit it:
   ```bash
   mkdir -p data/benchmark-v1/labels
   # put labels-<your-handle>.json in that folder
   git add data/benchmark-v1/labels/
   git commit -m "Add my benchmark labels"
   git push
   ```

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
