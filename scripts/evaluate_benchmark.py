#!/usr/bin/env python3
"""Run the SolarScan Verify three-way classification across multiple Gemini
models on the benchmark images, and produce a comparison table.

PRD §7: same inputs, several models, judged results.

Models (all vision-capable, via the user's own Gemini API key):
  - gemini-2.5-flash
  - gemini-2.5-flash-lite
  - gemini-2.5-pro

The API key is read ONLY from the GEMINI_API_KEY environment variable.
It must never be hardcoded, committed, or pasted into chat.

Usage:
  GEMINI_API_KEY=<key> python3 scripts/evaluate_benchmark.py [--limit N] [--sample]
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
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
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
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        sys.exit(
            "GEMINI_API_KEY is not set. Export it first:  export GEMINI_API_KEY=...  "
            "(never paste it into chat or commit it)"
        )

    models = MODELS if not args.model else args.model

    manifest = load_manifest()
    cases = manifest["cases"]
    if args.sample:
        cases = [c for c in cases if c["split"] == "test"][:5]
        print(f"Sample mode: {len(cases)} test-split cases")
    elif args.limit:
        cases = cases[: args.limit]
        print(f"Limit mode: {len(cases)} cases")

    RESULTS.mkdir(parents=True, exist_ok=True)

    for model in models:
        out_path = RESULTS / f"{model.replace('/', '_')}.json"
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
                result = ask_gemini(model, img, api_key)
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
