#!/usr/bin/env python3
"""Analyze multi-model evaluation results and produce a comparison table.

Before labeling: reports model agreement, label distribution, confidence,
and escalation stats per model.
After labeling (manifest labels filled in): reports accuracy on clear cases
and escalation recall on uncertain cases per PRD §6.

Usage:
  python3 scripts/analyze_results.py
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCH = REPO_ROOT / "data" / "benchmark-v1"
RESULTS = BENCH / "results"
MANIFEST = BENCH / "manifest.json"

LABELS = {"solar", "no_solar", "uncertain"}
ALLOWED_FACTORS = {
    "shading", "orientation", "obstruction", "skylight", "hvac",
    "unusual_layout", "image_quality", "none",
}


def load_results() -> dict[str, dict[str, dict]]:
    out: dict[str, dict[str, dict]] = {}
    for path in sorted(RESULTS.glob("*.json")):
        model = path.stem
        rows = json.loads(path.read_text())
        out[model] = {r["case_id"]: r for r in rows}
    return out


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset", action="store_true",
                        help="Only score cases in the 30-image labeling subset")
    args = parser.parse_args()

    results = load_results()
    manifest = json.loads(MANIFEST.read_text())
    cases = manifest["cases"]
    by_id = {c["id"]: c for c in cases}

    if args.subset:
        sub = json.loads((BENCH / "labeling" / "subset-30.json").read_text())
        subset_ids = {c["id"] for c in sub["cases"]}
        cases = [c for c in cases if c["id"] in subset_ids]
        # Trim each model's results to the subset
        results = {
            m: {cid: r for cid, r in rows.items() if cid in subset_ids}
            for m, rows in results.items()
        }
        print(f"Subset mode: scoring {len(cases)} cases across {len(results)} models\n")

    if not results:
        print("No results yet — run scripts/evaluate_benchmark.py first.")
        return

    models = list(results.keys())
    print(f"Models: {models}\n")
    print(f"{'Metric':<38}" + "".join(f"{m[:18]:>20}" for m in models))

    # 1. Label distribution per model
    dist = {m: Counter(r.get("label", "?") for r in results[m].values()) for m in models}
    print("\n-- Label distribution --")
    for label in LABELS:
        row = f"{label:<38}"
        for m in models:
            row += f"{dist[m].get(label, 0):>20}"
        print(row)

    # 2. Escalation rate (per PRD: escalate when uncertain or conf < 0.6)
    esc = {}
    for m in models:
        n = 0
        for r in results[m].values():
            if r.get("error"):
                continue
            label = r.get("label")
            conf = r.get("confidence", 0)
            if label == "uncertain" or (isinstance(conf, (int, float)) and conf < 0.6):
                n += 1
        esc[m] = n
    total = len(next(iter(results.values())))
    print("\n-- Escalation (uncertain or conf<0.6) --")
    for m in models:
        print(f"{m:<38}{esc[m]:>20} / {total}")

    # 3. Mean confidence per label
    print("\n-- Mean confidence by label --")
    for label in LABELS:
        row = f"{label:<38}"
        for m in models:
            confs = [r.get("confidence", 0) for r in results[m].values()
                     if r.get("label") == label and isinstance(r.get("confidence"), (int, float))]
            row += f"{(sum(confs)/len(confs) if confs else 0):>20.2f}"
        print(row)

    # 4. Cross-model agreement on cases where all models answered
    common = set.intersection(*[set(results[m].keys()) for m in models])
    common = {c for c in common if all(not results[m][c].get("error") for m in models)}
    agree = 0
    for cid in common:
        labs = {results[m][cid].get("label") for m in models}
        if len(labs) == 1:
            agree += 1
    print(f"\n-- Agreement --")
    print(f"Cases all 3 models answered: {len(common)}")
    print(f"All 3 agree on label:        {agree} ({agree/len(common)*100:.0f}%)" if common else "n/a")

    # 5. Difficulty factors used (check enum compliance)
    print("\n-- Difficulty factors (non-enum values flagged) --")
    for m in models:
        factors = Counter()
        bad = Counter()
        for r in results[m].values():
            for f in r.get("difficulty_factors", []) or []:
                if f in ALLOWED_FACTORS:
                    factors[f] += 1
                else:
                    bad[f] += 1
        top = ", ".join(f"{k}:{v}" for k, v in factors.most_common(5))
        print(f"{m}: {top}")
        if bad:
            print(f"    ⚠️ non-enum: {dict(bad)}")

    # 6. Ground-truth scoring (uses data/benchmark-v1/ground-truth.json when
    # available; falls back to manifest labels)
    gt_path = BENCH / "ground-truth.json"
    if gt_path.exists():
        gt_data = json.loads(gt_path.read_text())
        gt_by_id = {c["id"]: c["label"] for c in gt_data["cases"]}
        # Attach ground truth to the cases being scored
        for c in cases:
            if c["id"] in gt_by_id:
                c["label"] = gt_by_id[c["id"]]
        print(f"\n(Using ground truth from {gt_path.name}: "
              f"{gt_data['distribution']}, labelers {gt_data['labelers']})")

    if any(c["label"] != "unlabeled" for c in cases):
        print("\n-- Ground-truth scoring (PRD §6) --")
        clear = [c for c in cases if c["label"] in ("solar", "no_solar")]
        uncertain = [c for c in cases if c["label"] == "uncertain"]
        for m in models:
            correct = sum(1 for c in clear if results[m].get(c["id"], {}).get("label") == c["label"])
            esc_recall = sum(1 for c in uncertain
                             if results[m].get(c["id"], {}).get("label") == "uncertain")
            acc = correct / len(clear) if clear else 0
            rec = esc_recall / len(uncertain) if uncertain else 0
            print(f"{m}: clear-case accuracy {acc:.0%} ({correct}/{len(clear)}), "
                  f"escalation recall {rec:.0%} ({esc_recall}/{len(uncertain)})")
    else:
        print("\n(No ground-truth labels yet — manifest cases are 'unlabeled'."
              "\n Accuracy/escalation-recall scoring unlocks after team labeling.)")


if __name__ == "__main__":
    main()
