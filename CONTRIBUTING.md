# Contributing to SolarScan Verify

Team collaboration rules for the Con Edison capstone repository.
Adapted from the course repository's CONTRIBUTING.md.

## 1. Branch and sync

Keep `main` clean. Do all work on a branch named after you and the task:

```text
git switch main
git pull
git switch -c work/<github-handle>/<short-task-name>
```

Examples: `work/alan12-li/labeling`, `work/tanapreuk/results-table`.

## 2. Know what is public

This repository is private, but treat it as public. Never commit:

- API keys, passwords, tokens, `.env` files, auth files, or provider
  credentials — each teammate uses their own key, and keys never enter the
  repo, chat, or screenshots;
- customer information, exact infrastructure locations, network topology,
  partner documents, or operational Con Edison data;
- grades, NYU IDs, email addresses, or private feedback;
- identifiable recordings, faces, interviews, or private business data.

Use public, synthetic, consented, de-identified, or explicitly authorized
evidence only. Raw media stays outside Git; commit manifests/descriptions.

## 3. Review the agent's work

Before approving a commit:

```text
git status --short
git diff
```

Then commit with a one-line message describing one coherent change:

```text
git add <files>
git commit -m "Describe one coherent change"
git push -u origin HEAD
```

Show the diff to a teammate (or in the PR) before it lands on `main`.

## 4. Pull requests

- One coherent change per pull request.
- Explain what changed, what evidence/tests you used, what remains uncertain,
  and what a reviewer should inspect.
- The agent may draft the PR text; the author verifies and approves it.
- Do not merge your own PR without a teammate's review.

## 5. Current ground rules

- **Labels:** every benchmark image needs ≥2 agreeing labelers; disagreements
  become `uncertain`. Commit your labels as
  `data/benchmark-v1/labels/<handle>.json`.
- **Data:** regenerate with `scripts/` rather than committing raw media;
  verify image integrity before labeling.
- **Keys:** never shared, never committed. If you think a key leaked, say so
  immediately — the team stops work until it is replaced.
- **Agent config:** `opencode.json` at the repo root is the shared team
  config; propose changes via PR.
