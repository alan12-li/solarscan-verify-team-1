# Labeling Task — SolarScan Verify Benchmark v1

**Time needed:** 15–20 minutes
**Deadline:** before Session 5 (so we can score the models in class)

## What this is

We ran three AI models (Google Gemini, OpenAI GPT-5.5, Moonshot Kimi K3) on
30 rooftop images from a public drone dataset. Each model classified every
roof as `solar` / `no_solar` / `uncertain`. Before we can say which model is
right, we need **ground truth** — what a human actually sees in each image.

Your labels are the ground truth. This is how we measure the models
(accuracy on clear cases, escalation recall on uncertain cases), and it is
the core evidence for the capstone's "multiple models compared on the same
task" deliverable.

## What you need to do

1. **Open the file `label-standalone.html`** (double-click — it works in any
   browser, no install, no account). The file already contains all 30 images,
   so nothing else is needed.
2. **Type your GitHub handle** in the box at the top (e.g. `alan12-li`).
3. **Label every image** with one of three buttons:
   - **Solar** — solar panels are clearly visible
   - **No solar** — no panels; HVAC units, skylights, shadows, obstructions
     are fine here
   - **Uncertain** — you genuinely cannot decide; competing interpretations
     are plausible
4. **Rules:**
   - If you are unsure, choose **Uncertain**. That is the honest answer, and
     it is what we are testing.
   - These are thermal/false-color aerial images — don't expect a normal
     photo look.
   - Notes are optional but welcome for ambiguous cases.
5. When you finish all 30 (progress shows `30/30`), click
   **Export my labels (JSON)**. It downloads a file named
   `labels-<your-handle>.json`.
6. **Send that JSON file back** to Yongpeng (or commit it to the team repo
   under `data/benchmark-v1/labels/`).

## Why your labels matter

- Every image needs **at least 2 people** to agree. Disagreements become
  `uncertain` (we fail toward escalation, per our PRD §5).
- The merged labels become the benchmark's ground truth, which unlocks the
  PRD §6 scorecard (90% clear-case accuracy, 100% escalation recall).
- A refusal to guess is a pass. A confident wrong answer is a finding —
  write it down, that's what Session 5's build log is about.

## Checklist

- [ ] Opened `label-standalone.html` and saw 30 rooftop images
- [ ] Entered my GitHub handle
- [ ] Labeled all 30 images (progress `30/30`)
- [ ] Exported `labels-<handle>.json`
- [ ] Sent the JSON to Yongpeng / committed to the team repo

Questions? Ask in the team chat — include your platform and what you tried.
