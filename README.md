# SolarScan Verify

Con Edison capstone — **Solar Scanner Optimization** brief
Applied Generative AI in Business · SHBI-GB 7151 · Summer 2026

> ⚠️ **This repository is PUBLIC.** Everything pushed here is visible to
> anyone. Never commit keys, credentials, personal data, or operational
> Con Edison data. See [CONTRIBUTING.md](CONTRIBUTING.md) §2.

## Quick start (for teammates)

> **Read [docs/TEAM-GUIDE.md](docs/TEAM-GUIDE.md) first** — setup, your
> labeling task, and everything in the repo, in one place.
> **Full link pack: [docs/team-links.md](docs/team-links.md)**

1. Accept the GitHub invite, then clone this repo.
2. OpenCode loads `opencode.json` automatically from the repo root —
   connect **your own** OpenRouter key (never share keys).
3. **Your task: label 30 images** — open
   `data/benchmark-v1/labeling/label-standalone.html` and follow
   [docs/labeling-task.md](docs/labeling-task.md).
4. Reproduce the model comparison: `docs/benchmark-results.md` and the
   scripts under `scripts/`.

**Live pages (GitHub Pages):**
- Presentation: <https://alan12-li.github.io/solarscan-verify-team-1/presentation/>
- Labeling tool: <https://alan12-li.github.io/solarscan-verify-team-1/data/benchmark-v1/labeling/label-standalone.html>

## Team

- Yongpeng Li (alan12-li)
- Praewa Udomlertsakul (pointpraewa)
- Kenji Tannady (ktannady22)
- Tanapat Boontuam (tanapreuk)
- Victor Chan (Vchan5526)

## Proposal

**SolarScan Verify** is a generative-AI verification system designed to improve Con Edison's existing rooftop solar scanner. Rather than replacing the current system, it focuses on the difficult or low-confidence cases where complex New York City rooftops — HVAC units, skylights, shadows, obstructions, unusual layouts — may be mistaken for solar panels.

A multimodal AI agent reviews these ambiguous cases using rooftop imagery plus contextual data (building footprints, permit and public building information, roof geometry, historical imagery). The system evaluates why a rooftop is difficult to classify, detects change over time, and assesses shading, orientation, obstructions, and overall roof suitability.

Each building is classified as **solar / no solar / uncertain**, with unclear cases escalated for human review. Goal: improve accuracy, reduce unnecessary manual verification, and make Con Edison's scanning more scalable, reliable, and informative.

## Data boundary

This repository is private, but course rules still apply. Do **not** commit:

- Class/API keys, passwords, tokens, `.env` files, or credentials of any kind
- Customer information, exact infrastructure locations, network topology, or partner-only documents
- Operational Con Edison data, identifiable field media, faces, or private business data
- Grades, NYU IDs, email addresses, attendance, or private feedback

Use public, synthetic, consented, de-identified, or explicitly authorized evidence only. Raw media stays outside Git; commit de-identified manifests or descriptions when permitted.

## Repository layout

- `docs/` — proposal, decisions, results, prototype-fit, build-log evidence
  (start with `docs/team-links.md`)
- `data/` — public/synthetic datasets and manifests (no raw private media)
- `src/` — prototype code
- `presentation/` — the Session 6 HTML presentation
