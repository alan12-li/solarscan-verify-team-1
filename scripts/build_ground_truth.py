#!/usr/bin/env python3
"""Build the final benchmark ground truth from merged labeler files.

Rule (PRD §5, labels/README.md): majority vote among labelers; a tie
becomes "uncertain" (fail toward escalation).

Usage:
  python3 scripts/build_ground_truth.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCH = REPO_ROOT / "data" / "benchmark-v1"
LABELS = BENCH / "labels"
SUBSET = BENCH / "labeling" / "subset-30.json"
OUT = BENCH / "ground-truth.json"

VALID = {"solar", "no_solar", "uncertain"}


def main() -> int:
    subset = json.loads(SUBSET.read_text())
    ids = [c["id"] for c in subset["cases"]]

    label_files = sorted(LABELS.glob("*.json"))
    labelers = []
    per_case: dict[str, dict[str, str]] = {}
    for path in label_files:
        data = json.loads(path.read_text())
        labeler = data.get("labeler", path.stem)
        labelers.append(labeler)
        for cid, entry in data.get("labels", {}).items():
            lbl = entry.get("label", "")
            if lbl not in VALID:
                print(f"WARN {labeler}: invalid label {lbl!r} for {cid}")
            per_case.setdefault(cid, {})[labeler] = lbl

    cases = []
    ties = []
    for cid in ids:
        votes = per_case.get(cid, {})
        valid_votes = {lbl for lbl in votes.values() if lbl in VALID}
        if not valid_votes:
            print(f"ERROR {cid}: no valid labels ({votes})")
            return 2
        from collections import Counter as _C
        tally = _C(lbl for lbl in votes.values() if lbl in VALID)
        top_count = tally.most_common(1)[0][1]
        winners = {lbl for lbl, n in tally.items() if n == top_count}
        if len(winners) == 1:
            final = winners.pop()
        else:
            final = "uncertain"  # tie -> escalate
            ties.append({"case_id": cid, "votes": votes, "tally": dict(tally)})
        cases.append({"id": cid, "label": final, "labelers": sorted(votes)})

    from collections import Counter
    dist = Counter(c["label"] for c in cases)
    out = {
        "version": "v1",
        "created": "2026-08-08",
        "labelers": labelers,
        "rule": "majority vote; ties become uncertain",
        "image_count": len(cases),
        "distribution": dict(dist),
        "ties_resolved_as_uncertain": ties,
        "cases": cases,
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Wrote {OUT}")
    print(f"  labelers: {labelers}")
    print(f"  distribution: {dict(dist)}")
    print(f"  ties -> uncertain: {len(ties)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
