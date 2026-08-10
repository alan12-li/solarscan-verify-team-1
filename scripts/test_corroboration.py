#!/usr/bin/env python3
"""Test the multi-source corroboration branch logic with real models.

Design: we cannot join our 30 benchmark images to NYC records (no addresses),
so we test the BRANCH itself: given a synthetic {model hypothesis, permit
record} pair, does the agent apply the corroboration rule correctly?

Rule under test (docs/multisource-verification.md):
  - permit=Completed + model=no_solar  -> ESCALATE (likely missed panels)
  - permit=absent + model=solar (conf<0.8) -> ESCALATE (possible false pos)
  - permit=absent + model=no_solar -> ACCEPT (records agree)
  - permit=Completed + model=solar -> ACCEPT (records agree)
  - permit=In Progress + model=solar -> ACCEPT with note (partial evidence)
  - records unavailable -> ACCEPT on image alone (PRD §5 fallback)

This tests rule-following, not image classification. Honest scope: the
branch logic, not end-to-end. Run: python3 scripts/test_corroboration.py
"""
import json
import os
import re
import sys
import time
from pathlib import Path

KEYS = {
    "gemini": Path.home() / ".gemini_api_key",
    "openrouter": Path.home() / ".openrouter_api_key",
}
MODELS = [
    ("gemini", "gemini-3.5-flash-lite"),      # baseline
    ("openrouter", "openai/gpt-5.5"),          # best accuracy
]

SYSTEM = (
    "You are the decision step of a rooftop solar verification layer. "
    "Given a MODEL HYPOTHESIS (what a vision model guessed from the roof "
    "image) and a PERMIT RECORD (public NYC solar installation record), "
    "decide whether to ACCEPT the model's answer or ESCALATE to a human "
    "analyst. Respond with JSON only: "
    '{"decision": "accept"|"escalate", "reason": "one short sentence"}. '
    "Rules (apply exactly, thresholds are literal): "
    "1) permit Completed + model no_solar -> escalate (missed panels); "
    "2) no permit + model solar with confidence < 0.8 -> escalate "
    "(possible false positive); "
    "3) records agree (permit Completed + solar, or lookup-OK zero records "
    "+ no_solar) -> accept; "
    "4) lookup unavailable (no parcel id to query) -> accept on image alone; "
    "5) permit In Progress + model solar -> accept with a note. "
    "A person decides on every escalate."
)

CASES = [
    # (id, hypothesis, permit, expected)
    ("c1", "no_solar conf 0.91", "Completed, installed 2019", "escalate"),
    ("c2", "solar conf 0.95", "Completed, installed 2021", "accept"),
    ("c3", "solar conf 0.55", "Lookup OK: zero permit records for parcel", "escalate"),
    ("c4", "no_solar conf 0.88", "Lookup OK: zero permit records for parcel", "accept"),
    ("c5", "solar conf 0.90", "In Progress, filed 2025", "accept"),
    ("c6", "no_solar conf 0.62", "Completed, installed 2017", "escalate"),
    ("c7", "solar conf 0.93", "Completed, installed 2018", "accept"),
    ("c8", "uncertain conf 0.40", "Completed, installed 2020", "escalate"),
    ("c9", "solar conf 0.70", "Lookup unavailable (no parcel id)", "accept"),
    ("c10", "no_solar conf 0.85", "Lookup unavailable (no parcel id)", "accept"),
]


def read_key(name: str) -> str:
    p = KEYS[name]
    if not p.exists():
        print(f"missing key file {p}")
        sys.exit(2)
    return p.read_text().strip()


def ask_model(provider: str, model: str, prompt: str, key: str) -> str:
    if provider == "gemini":
        import urllib.request
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={key}"
        )
        body = json.dumps({
            "systemInstruction": {"parts": [{"text": SYSTEM}]},
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0},
        }).encode()
        req = urllib.request.Request(url, data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        import urllib.request
        url = "https://openrouter.ai/api/v1/chat/completions"
        body = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        }).encode()
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        })
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read())
        text = data["choices"][0]["message"]["content"]
    return text


def extract_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {}


def main() -> int:
    keys = {n: read_key(n) for n in KEYS}
    results = []
    total = 0
    correct = 0
    for provider, model in MODELS:
        for cid, hyp, permit, expected in CASES:
            prompt = (
                f"MODEL HYPOTHESIS: {hyp}\n"
                f"PERMIT RECORD: {permit}\n"
                "What is your decision?"
            )
            total += 1
            try:
                raw = ask_model(provider, model, prompt, keys[provider])
                out = extract_json(raw)
                decision = out.get("decision", "").strip().lower()
            except Exception as e:
                decision = f"error:{type(e).__name__}"
                print(f"  [call error] {model} {cid}: {e}")
            ok = decision == expected
            if ok:
                correct += 1
            results.append({
                "model": model, "case": cid, "hypothesis": hyp,
                "permit": permit, "expected": expected,
                "got": decision, "pass": ok,
            })
            print(f"{'✓' if ok else '✗'} {model} {cid}: "
                  f"expected={expected} got={decision}")
            time.sleep(0.3)

    acc = correct / total if total else 0
    print(f"\nRule-following accuracy: {correct}/{total} = {acc:.0%}")
    out_path = Path("data/benchmark-v1/results/corroboration-branch-test.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "test": "corroboration branch rule-following",
        "models": [m for _, m in MODELS],
        "cases": len(CASES),
        "rule_following_accuracy": round(acc, 3),
        "results": results,
    }, indent=2))
    print(f"wrote {out_path}")
    return 0 if acc == 1.0 else 1


if __name__ == "__main__":
    sys.exit(main())
