# Model cost — measured per-image (2026-08-10)

Real billed cost for **one rooftop image** (511 W 182nd St, 2024 ortho),
all 4 models, temperature 0, same system prompt — measured live via the
OpenRouter API (identical call shape to `demo.html` / `demo_server.py`).

| Model | Prompt tokens | Completion tokens | Cost per image | Cents |
|---|---|---|---|---|
| Gemma 4-26B (open, Apache-2.0) | 336 | 39 | $0.000059 | 0.0059¢ |
| Gemini 3.5 Flash-Lite | 1,150 | 38 | $0.000440 | 0.044¢ |
| Kimi K3 (open) | 269 | 80 | $0.001907 | 0.19¢ |
| GPT-5.5 | 147 | 62 | $0.002595 | 0.26¢ |

OpenRouter list prices used (per 1M tokens): Gemma $0.12/$0.40 ·
Gemini $0.30/$2.50 · Kimi $3/$15 · GPT-5.5 $5/$30 (prompt/completion).

## What this means

- **4 models × 1 roof ≈ $0.005** — half a cent for the full panel.
- **100 roofs × 4 models ≈ $0.50** — less than one unnecessary truck visit.
- **Open-weights are ~44× cheaper than GPT-5.5 per image** (Gemma vs GPT-5.5)
  and were the most honest about doubt (Kimi matched the human 6/6 on real
  NYC roofs; see `docs/nyc-human-validation.md`).
- Cost is **not the blocker** — confident wrong answers on hard roofs are
  (the verification layer's whole reason to exist).

## Method

1. Same JPEG (511 W 182nd St, 2024, ~40 KB) → base64 data URI.
2. One chat completion per model via `https://openrouter.ai/api/v1/chat/completions`
   with the production system prompt, temperature 0, JSON output.
3. Cost = `usage.cost` as reported by OpenRouter (authoritative, includes
   image tokens); list prices cross-checked from `/api/v1/models`.
4. Date: 2026-08-10. Prices may change; this is a snapshot.

Reproduce: `scripts/demo_server.py` uses the same models/prompt; a fresh
run of the calls above re-measures.
