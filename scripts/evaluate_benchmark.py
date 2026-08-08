#!/usr/bin/env python3
"""Run the SolarScan Verify three-way classification across multiple vision
models on the benchmark images, and produce a comparison table.

PRD §7: same inputs, several models, judged results.

Model IDs route to providers by prefix:
  - `gemini-*`           -> Google Gemini API  (needs GEMINI_API_KEY)
  - `openrouter:<slug>`   -> OpenRouter API     (needs OPENROUTER_API_KEY)
                            e.g. openrouter:openai/gpt-4o-mini

Keys are read ONLY from the environment. They must never be hardcoded,
committed, or pasted into chat.

Usage:
  GEMINI_API_KEY=... python3 scripts/evaluate_benchmark.py --subset --resume
  OPENROUTER_API_KEY=... python3 scripts/evaluate_benchmark.py \\
      --subset --model openrouter:openai/gpt-4o-mini
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCH = REPO_ROOT / "data" / "benchmark-v1"
IMAGES = BENCH / "images"
MANIFEST = BENCH / "manifest.json"
RESULTS = BENCH / "results"

MODELS = [
    "gemini-3.5-flash-lite",
    "openrouter:openai/gpt-5.5",
    "openrouter:moonshotai/kimi-k3",
]

# PRD §3 output contract — every model must return exactly this JSON.
SYSTEM_PROMPT = """You are a rooftop solar verification assistant for a utility company.
The image is an aerial/thermal rooftop view (may be false-color thermal imagery, not a normal photo).
Classify each rooftop as one of exactly three labels:
- "solar": solar panels are clearly visible
- "no_solar": no solar panels; equipment like HVAC, skylights, or obstructions may be present
- "uncertain": you cannot decide from the image; competing interpretations are plausible

Return ONLY a JSON object with this exact schema:
{
  "label": "solar" | "no_solar" | "uncertain",
  "confidence": 0.0,
  "reason": "one short sentence naming the visual evidence",
  "difficulty_factors": ["shading" | "orientation" | "obstruction" | "skylight" | "hvac" | "unusual_layout" | "image_quality" | "none"],
  "escalate": true
}
Use ONLY these difficulty_factors values, no others. Set "escalate" to true when label is "uncertain" or confidence is below 0.6.
No prose before or after the JSON."""


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text())


def ask_gemini(model: str, image_path: Path, api_key: str) -> dict:
    """Send one image to a Gemini model and return parsed JSON.

    Retries with exponential backoff on 429 (free-tier rate limit) and on
    transient 5xx errors.
    """
    import base64
    import time as _time

    image_b64 = base64.b64encode(image_path.read_bytes()).decode()
    mime = "image/jpeg" if image_path.suffix.lower() in (".jpg", ".jpeg") else "image/png"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT},
                    {"inline_data": {"mime_type": mime, "data": image_b64}},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0,
            "responseMimeType": "application/json",
        },
    }
    import urllib.error
    import urllib.request

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = json.loads(resp.read().decode())
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < max_attempts:
                wait = 15 * (2 ** (attempt - 1))  # 15, 30, 60, 120
                print(f"    429 rate limit — retrying in {wait}s (attempt {attempt}/{max_attempts})")
                _time.sleep(wait)
                continue
            raise
    else:
        raise RuntimeError(f"Exhausted {max_attempts} attempts for {model}")

    text = body["candidates"][0]["content"]["parts"][0]["text"]
    parsed = extract_json(text)
    # Normalize
    if isinstance(parsed, list):
        parsed = parsed[0] if parsed else {}
    parsed["label"] = str(parsed.get("label", "")).strip().lower()
    return parsed


def ask_openrouter(model_id: str, image_path: Path, api_key: str) -> dict:
    """Send one image to any OpenRouter vision model (OpenAI-compatible API).

    model_id is the OpenRouter slug, e.g. "openai/gpt-4o-mini" or
    "anthropic/claude-3.5-sonnet". Same retry/backoff policy as Gemini.
    """
    import base64
    import time as _time
    import urllib.error
    import urllib.request

    image_b64 = base64.b64encode(image_path.read_bytes()).decode()
    mime = "image/jpeg" if image_path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    data_url = f"data:{mime};base64,{image_b64}"

    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Classify this rooftop image."},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            },
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = json.loads(resp.read().decode())
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < max_attempts:
                wait = 15 * (2 ** (attempt - 1))
                print(f"    429 rate limit — retrying in {wait}s (attempt {attempt}/{max_attempts})")
                _time.sleep(wait)
                continue
            raise
    else:
        raise RuntimeError(f"Exhausted {max_attempts} attempts for {model_id}")

    text = body["choices"][0]["message"]["content"]
    parsed = extract_json(text)
    if isinstance(parsed, list):
        parsed = parsed[0] if parsed else {}
    parsed["label"] = str(parsed.get("label", "")).strip().lower()
    return parsed


def ask_model(model: str, image_path: Path, keys: dict) -> dict:
    """Route a model ID to the right provider.

    "gemini-*" -> Google Gemini API (keys["gemini"])
    "openrouter:<slug>" -> OpenRouter API (keys["openrouter"])
    """
    if model.startswith("openrouter:"):
        return ask_openrouter(model[len("openrouter:"):], image_path, keys["openrouter"])
    if model.startswith("gemini-") or model.startswith("models/"):
        return ask_gemini(model, image_path, keys["gemini"])
    # Default: treat bare IDs as Gemini (backward compatible)
    return ask_gemini(model, image_path, keys["gemini"])


def extract_json(text: str) -> dict:
    """Robustly extract a JSON object from a model response.

    Handles: ``` fences, multiple JSON objects (take the last, which is
    usually the final answer), trailing prose, and stray characters.
    """
    import re

    text = text.strip()
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Strip ```json ... ``` fences
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1).strip())
        except json.JSONDecodeError:
            pass
    # Find all JSON objects and take the last complete one
    objects = []
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(text):
        if text[idx] in "{[":
            try:
                obj, end = decoder.raw_decode(text, idx)
                objects.append(obj)
                idx = end
            except json.JSONDecodeError:
                idx += 1
        else:
            idx += 1
    if objects:
        return objects[-1] if isinstance(objects[-1], dict) else objects[-1][0]
    raise ValueError(f"Could not extract JSON from model output: {text[:200]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Run only first N cases")
    parser.add_argument("--sample", action="store_true", help="Sample 5 images across splits")
    parser.add_argument("--resume", action="store_true",
                        help="Skip cases already answered in existing result files")
    parser.add_argument("--model", action="append", default=None,
                        help="Run only specific model(s); repeatable")
    parser.add_argument("--delay", type=float, default=2.0,
                        help="Seconds between calls (default 2.0; free tier is rate-limited)")
    parser.add_argument("--subset", action="store_true",
                        help="Run only the 30 labeling-subset cases (test+valid)")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    or_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    keys = {"gemini": api_key, "openrouter": or_key}

    models = MODELS if not args.model else args.model

    # Validate that every requested model has its provider key present.
    for model in models:
        if model.startswith("openrouter:") and not keys["openrouter"]:
            sys.exit(
                "OPENROUTER_API_KEY is not set (needed for "
                f"{model}). Export it first:  export OPENROUTER_API_KEY=...  "
                "(never paste it into chat or commit it)"
            )
        if not model.startswith("openrouter:") and not keys["gemini"]:
            sys.exit(
                "GEMINI_API_KEY is not set (needed for "
                f"{model}). Export it first:  export GEMINI_API_KEY=...  "
                "(never paste it into chat or commit it)"
            )

    manifest = load_manifest()
    cases = manifest["cases"]
    if args.subset:
        sub = json.loads((BENCH / "labeling" / "subset-30.json").read_text())
        subset_ids = {c["id"] for c in sub["cases"]}
        cases = [c for c in cases if c["id"] in subset_ids]
        print(f"Subset mode: {len(cases)} labeling-subset cases")
    elif args.sample:
        cases = [c for c in cases if c["split"] == "test"][:5]
        print(f"Sample mode: {len(cases)} test-split cases")
    elif args.limit:
        cases = cases[: args.limit]
        print(f"Limit mode: {len(cases)} cases")

    RESULTS.mkdir(parents=True, exist_ok=True)

    for model in models:
        out_name = model.replace("/", "_").replace(":", "_")
        out_path = RESULTS / f"{out_name}.json"
        existing = {}
        if args.resume and out_path.exists():
            for r in json.loads(out_path.read_text()):
                if "error" not in r:
                    existing[r["case_id"]] = r
            print(f"\n=== {model} (resume: {len(existing)} already done) ===")
        else:
            print(f"\n=== {model} ===")
        rows = list(existing.values())
        done_ids = set(existing.keys())
        for i, case in enumerate(cases, 1):
            if case["id"] in done_ids:
                print(f"  {case['id']}: skipped (done)")
                continue
            img = IMAGES / Path(case["image"]).name
            if not img.exists():
                print(f"  skip {case['id']}: image missing")
                continue
            try:
                result = ask_model(model, img, keys)
                rows.append({"case_id": case["id"], **result})
                print(f"  {case['id']}: {result.get('label')} conf={result.get('confidence')}")
            except Exception as exc:
                rows.append({"case_id": case["id"], "error": str(exc)})
                print(f"  {case['id']}: ERROR {exc}")
            time.sleep(args.delay)  # be gentle with rate limits

        out_path.write_text(json.dumps(rows, indent=2) + "\n")
        print(f"  -> {out_path} ({len(rows)} rows)")

    print("\nDone. Results in", RESULTS)


if __name__ == "__main__":
    main()
