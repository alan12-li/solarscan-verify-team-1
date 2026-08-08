#!/usr/bin/env python3
"""Download benchmark source imagery and build the benchmark manifest skeleton.

SolarScan Verify — benchmark v1 pipeline (reproducible).

Sources:
  1. HuggingFace: Francesco/solar-panels-taxvb (CC license, 640x640 drone
     rooftop imagery, Roboflow RF100). Provides real rooftop imagery.
  2. Synthetic: generated later by src/generate_synthetic.py (team-generated,
     full label control) for the uncertain cases.

Outputs:
  data/benchmark-v1/images/        (gitignored — raw media stays out of Git)
  data/benchmark-v1/manifest.json  (committed — the ground truth)

Usage:
  python3 scripts/fetch_benchmark.py
"""

from __future__ import annotations

import json
import tarfile
import tempfile
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCH = REPO_ROOT / "data" / "benchmark-v1"
IMAGES = BENCH / "images"
MANIFEST = BENCH / "manifest.json"

HF_DATASET = "Francesco/solar-panels-taxvb"
HF_TARBALL = (
    f"https://huggingface.co/datasets/{HF_DATASET}/resolve/main/dataset.tar.gz"
)


def source_split_from_path(tarball_path: str) -> str:
    """Recover train/test/valid split from the tarball path."""
    for split in ("train", "test", "valid"):
        if f"/{split}/" in tarball_path:
            return split
    return "unknown"


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)

    cases = []
    with tempfile.TemporaryDirectory() as tmp:
        tarball_path = Path(tmp) / "dataset.tar.gz"
        print(f"Downloading {HF_DATASET} ...")
        urllib.request.urlretrieve(HF_TARBALL, tarball_path)
        print(f"  saved ({tarball_path.stat().st_size / 1e6:.1f} MB)")

        with tarfile.open(tarball_path, "r:gz") as tar:
            jpgs = [m for m in tar.getmembers() if m.name.endswith(".jpg")]
            print(f"  {len(jpgs)} images in tarball")

            for i, member in enumerate(sorted(jpgs, key=lambda m: m.name), start=1):
                f = tar.extractfile(member)
                if f is None:
                    continue
                name = f"sv-{i:04d}.jpg"
                (IMAGES / name).write_bytes(f.read())
                cases.append(
                    {
                        "id": f"sv-{i:04d}",
                        "image": f"images/{name}",
                        "label": "unlabeled",  # team labels these
                        "difficulty_factors": [],
                        "source": f"hf:{HF_DATASET}",
                        "split": source_split_from_path(member.name),
                        "notes": "",
                    }
                )

    manifest = {
        "version": "v1",
        "created": "2026-08-08",
        "image_count": len(cases),
        "target_distribution": {
            "solar": 35,
            "no_solar": 35,
            "uncertain": 30,
        },
        "labeling_rule": (
            ">=2 team members agree; disagreements become 'uncertain'"
        ),
        "sources": {
            f"hf:{HF_DATASET}": {"license": "cc", "count": len(cases)},
            "synthetic": {"license": "team-generated", "count": 0},
        },
        "cases": cases,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"\nWrote {MANIFEST}")
    print(f"  {len(cases)} images registered, all labels 'unlabeled'")
    print("  Next: team labels the images, then labels go into manifest.json")


if __name__ == "__main__":
    main()
