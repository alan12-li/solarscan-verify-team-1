#!/usr/bin/env python3
"""Select the 30-image labeling subset and generate the labeling tool.

Strategy: prefer the dataset's official test split (held-out, best for a
benchmark) and top up from valid to reach 30.

Outputs:
  data/benchmark-v1/labeling/subset-30.json   (the 30 case ids + metadata)
  data/benchmark-v1/labeling/label.html       (self-contained labeling tool)

Usage:
  python3 scripts/make_labeling_tool.py
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCH = REPO_ROOT / "data" / "benchmark-v1"
IMAGES = BENCH / "images"
LABELING = BENCH / "labeling"
MANIFEST = BENCH / "manifest.json"

SUBSET_SIZE = 30

LABEL_OPTIONS = [
    ("solar", "Solar — panels clearly visible"),
    ("no_solar", "No solar — HVAC/skylights/obstructions, no panels"),
    ("uncertain", "Uncertain — cannot decide from the image"),
]


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    cases = manifest["cases"]

    # Order: test split first, then valid, then train — take first 30.
    order = {"test": 0, "valid": 1, "train": 2}
    cases.sort(key=lambda c: (order.get(c["split"], 9), c["id"]))
    subset = cases[:SUBSET_SIZE]

    LABELING.mkdir(parents=True, exist_ok=True)

    # Copy the subset images into labeling/ (small, committed as previews is
    # overkill — these stay gitignored like images/).
    subset_images = LABELING / "images"
    subset_images.mkdir(exist_ok=True)
    for case in subset:
        src = IMAGES / Path(case["image"]).name
        dst = subset_images / Path(case["image"]).name
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)

    # Record subset metadata (no labels yet)
    subset_meta = {
        "version": "v1",
        "subset_size": len(subset),
        "selection": "test split first, then valid, capped at 30",
        "cases": [
            {
                "id": c["id"],
                "image": f"images/{Path(c['image']).name}",
                "split": c["split"],
                "label": "unlabeled",
                "labelers": [],
            }
            for c in subset
        ],
    }
    (LABELING / "subset-30.json").write_text(json.dumps(subset_meta, indent=2) + "\n")

    # Build the self-contained labeling HTML tool.
    cards = []
    for case in subset_meta["cases"]:
        opts = "".join(
            f'<button type="button" class="opt" data-label="{key}" '
            f'onclick="pick(\'{case["id"]}\', \'{key}\', this)">{label}</button>'
            for key, label in LABEL_OPTIONS
        )
        cards.append(
            f"""
            <div class="card" id="card-{case["id"]}" data-id="{case["id"]}">
              <div class="imgwrap">
                <img src="{case["image"]}" alt="{case["id"]}" loading="lazy">
                <div class="badge">{case["id"]} · {case["split"]}</div>
              </div>
              <div class="opts">{opts}</div>
              <textarea class="notes" placeholder="Notes (optional)"></textarea>
              <div class="status">not labeled</div>
            </div>"""
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SolarScan Verify — Labeling Tool (30 images)</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }}
  h1 {{ font-size: 1.4rem; }}
  .bar {{ position: sticky; top: 0; background: #fff; padding: .5rem 0; border-bottom: 1px solid #ddd; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; margin-top: 1rem; }}
  .card {{ border: 1px solid #ddd; border-radius: 8px; padding: .6rem; }}
  .imgwrap {{ position: relative; }}
  img {{ width: 100%; border-radius: 4px; display: block; }}
  .badge {{ position: absolute; top: .3rem; left: .3rem; background: rgba(0,0,0,.7); color: #fff; padding: .15rem .5rem; border-radius: 4px; font-size: .75rem; }}
  .opts {{ display: flex; flex-direction: column; gap: .3rem; margin: .5rem 0; }}
  .opt {{ padding: .45rem; border: 1px solid #ccc; border-radius: 6px; background: #fafafa; cursor: pointer; text-align: left; font-size: .85rem; }}
  .opt.sel {{ background: #2563eb; color: #fff; border-color: #2563eb; }}
  .notes {{ width: 100%; min-height: 2.2rem; font-size: .8rem; }}
  .status {{ font-size: .75rem; color: #666; }}
  .status.done {{ color: #16a34a; font-weight: 600; }}
  #progress {{ font-weight: 600; }}
  #export {{ margin-top: 1rem; padding: .6rem 1.2rem; font-size: 1rem; }}
</style>
</head>
<body>
<div class="bar">
  <h1>SolarScan Verify — Label 30 rooftop images</h1>
  <p>Rules: <b>solar</b> = panels clearly visible · <b>no_solar</b> = no panels
  (HVAC/skylights/obstructions OK) · <b>uncertain</b> = genuinely cannot
  decide. If unsure, choose <b>uncertain</b>. Progress: <span id="progress">0/30</span></p>
  <p><label>Your GitHub handle: <input id="labeler" placeholder="e.g. alan12-li" style="min-width:10rem"></label></p>
</div>
<div class="grid">
{''.join(cards)}
</div>
<button id="export" onclick="doExport()">Export my labels (JSON)</button>
<script>
const LABELS = {json.dumps([k for k, _ in LABEL_OPTIONS])};
let store = JSON.parse(localStorage.getItem('solarscan-labels') || '{{}}');
function save() {{ localStorage.setItem('solarscan-labels', JSON.stringify(store)); update(); }}
function pick(id, label, btn) {{
  store[id] = store[id] || {{}};
  store[id].label = label;
  save();
  const card = document.getElementById('card-' + id);
  card.querySelectorAll('.opt').forEach(b => b.classList.remove('sel'));
  btn.classList.add('sel');
}}
function update() {{
  let done = 0;
  document.querySelectorAll('.card').forEach(card => {{
    const id = card.dataset.id;
    const st = card.querySelector('.status');
    const notes = card.querySelector('.notes');
    if (store[id] && store[id].label) {{
      done++;
      st.textContent = 'labeled: ' + store[id].label;
      st.className = 'status done';
      card.querySelectorAll('.opt').forEach(b => {{
        b.classList.toggle('sel', b.dataset.label === store[id].label);
      }});
      if (store[id].notes) notes.value = store[id].notes;
    }}
  }});
  document.getElementById('progress').textContent = done + '/30';
}}
document.querySelectorAll('.notes').forEach(t => {{
  t.addEventListener('change', e => {{
    const id = e.target.closest('.card').dataset.id;
    store[id] = store[id] || {{}};
    store[id].notes = e.target.value;
    save();
  }});
}});
document.getElementById('labeler').addEventListener('change', e => {{
  store._labeler = e.target.value; save();
}});
function doExport() {{
  const labeler = document.getElementById('labeler').value || 'unknown';
  const out = {{
    labeler: labeler,
    labels: Object.fromEntries(Object.entries(store).filter(([k]) => !k.startsWith('_'))),
  }};
  const blob = new Blob([JSON.stringify(out, null, 2)], {{type: 'application/json'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'labels-' + labeler + '.json';
  a.click();
}}
update();
</script>
</body>
</html>"""
    (LABELING / "label.html").write_text(html)
    print(f"Wrote {LABELING / 'subset-30.json'}")
    print(f"Wrote {LABELING / 'label.html'}")
    print(f"Images copied to {subset_images}/")
    print(f"\nSelection: {len(subset)} cases "
          f"({sum(1 for c in subset if c['split']=='test')} test, "
          f"{sum(1 for c in subset if c['split']=='valid')} valid)")


if __name__ == "__main__":
    main()
