#!/usr/bin/env python3
"""Verify that the labeling-tool images are byte-identical to the evaluation
images (the ones sent to the models).

Run before labeling or after re-running fetch_benchmark.py, to guarantee the
human labels and the model outputs refer to the same pixels.

Usage:
  python3 scripts/verify_image_integrity.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCH = REPO_ROOT / "data" / "benchmark-v1"
IMAGES = BENCH / "images"
LABELING_IMAGES = BENCH / "labeling" / "images"
SUBSET = BENCH / "labeling" / "subset-30.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not SUBSET.exists():
        print(f"Missing {SUBSET} — run scripts/make_labeling_tool.py first.")
        return 2

    subset = json.loads(SUBSET.read_text())
    cases = subset["cases"]
    print(f"Checking {len(cases)} subset images: images/ vs labeling/images/")

    mismatches: list[str] = []
    missing: list[str] = []
    for case in cases:
        name = Path(case["image"]).name
        eval_img = IMAGES / name
        label_img = LABELING_IMAGES / name
        if not eval_img.exists():
            missing.append(f"{case['id']}: eval image missing {eval_img}")
            continue
        if not label_img.exists():
            missing.append(f"{case['id']}: labeling image missing {label_img}")
            continue
        if sha256(eval_img) != sha256(label_img):
            mismatches.append(case["id"])

    for msg in missing:
        print(f"  MISSING {msg}")
    for cid in mismatches:
        print(f"  MISMATCH {cid} — labeling image differs from eval image")

    if missing or mismatches:
        print(f"\nFAIL: {len(missing)} missing, {len(mismatches)} mismatched "
              f"of {len(cases)}. Re-run make_labeling_tool.py to resync.")
        return 1

    print(f"\nPASS: all {len(cases)} images byte-identical "
          f"(SHA-256 match). Labels and model outputs refer to the same pixels.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
