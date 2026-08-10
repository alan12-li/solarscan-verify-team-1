#!/usr/bin/env python3
"""Fetch NYC rooftop orthoimagery for multi-source verification (PATH B).

Technical validation pipeline (2026-08-10): proves the end-to-end chain
  Building Footprints (BBL+coords) -> NYC Orthos 2018 tile -> model classify

Data (all public):
  - Building Footprints: NYC Open Data `5zhs-2jue` (CC/ODbL-ish, public)
  - Orthoimagery: NYC Orthos 2018 MapServer (public, CC BY 4.0)
  - Solar permits: LL24 `cfz5-6fvh` (join needs an address — Con Edison step)

Usage:
  python3 scripts/fetch_nyc_roofs.py --count 20 --z 19 --out /tmp/nyc_roofs

Honest scope: this downloads roof imagery + building attributes and can
classify them, but the 20-image benchmark has NO ground truth yet (that
needs labelers) and the permit join needs real addresses (Con Edison data
step). It is a mechanism proof, not an accuracy result.
"""
import argparse
import json
import math
import time
import urllib.parse
import urllib.request
from pathlib import Path

TILES = ("https://tiles.arcgis.com/tiles/yG5s3afENB5iO9fj/arcgis/rest/"
         "services/NYC_Orthos_2018/MapServer/tile")
FOOTPRINTS = "https://data.cityofnewyork.us/resource/5zhs-2jue.json"
UA = {"User-Agent": "solarscan-verify-capstone"}


def get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def latlon_to_tile(lat: float, lon: float, z: int) -> tuple[int, int]:
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    lat_rad = math.radians(lat)
    y = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return int(x), int(y)


def fetch_footprints(limit: int = 30) -> list[dict]:
    params = {
        "$where": "base_bbl like '1%'",  # Manhattan
        "$select": "bin,base_bbl,height_roof,feature_code,the_geom",
        "$limit": str(limit),
    }
    url = FOOTPRINTS + "?" + urllib.parse.urlencode(params)
    return json.loads(get(url))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--z", type=int, default=19,
                        help="zoom level (19 ~= 0.5 m/px roof detail)")
    parser.add_argument("--out", type=Path, default=Path("/tmp/nyc_roofs"))
    args = parser.parse_args()

    rows = fetch_footprints(limit=max(args.count * 2, 30))
    print(f"footprints fetched: {len(rows)} (Manhattan)")
    args.out.mkdir(parents=True, exist_ok=True)

    manifest = []
    used = 0
    for row in rows:
        if used >= args.count:
            break
        geom = row.get("the_geom", {})
        polys = geom.get("coordinates", [])
        if not polys or not polys[0]:
            continue
        ring = polys[0][0]
        lon = sum(p[0] for p in ring) / len(ring)
        lat = sum(p[1] for p in ring) / len(ring)
        bin_id = row["bin"]
        bbl = row["base_bbl"]

        x, y = latlon_to_tile(lat, lon, args.z)
        try:
            img = get(f"{TILES}/{args.z}/{y}/{x}")
        except Exception as e:
            print(f"  {bin_id}: tile ERR {type(e).__name__}")
            continue
        if img[:3] != b"\xff\xd8\xff":
            print(f"  {bin_id}: not JPEG ({len(img)} B)")
            continue

        fname = args.out / f"mn_{bin_id}_bbl{bbl}_z{args.z}.jpg"
        fname.write_bytes(img)
        manifest.append({
            "bin": bin_id, "bbl": bbl,
            "height_roof": row.get("height_roof"),
            "feature_code": row.get("feature_code"),
            "tile_xyz": [args.z, x, y], "lat": lat, "lon": lon,
            "image": fname.name,
        })
        print(f"  {bin_id} bbl={bbl} roof={row.get('height_roof')} "
              f"fc={row.get('feature_code')} -> {fname.name} ({len(img)//1024} KB)")
        used += 1
        time.sleep(0.3)

    (args.out / "manifest.json").write_text(json.dumps({
        "source": "NYC Orthos 2018 (CC BY 4.0) + Building Footprints (5zhs-2jue)",
        "scope": "MECHANISM PROOF — no ground truth, no accuracy claim",
        "zoom": args.z,
        "roofs": manifest,
    }, indent=2))
    print(f"\ndownloaded {used} roofs -> {args.out}; manifest written")


if __name__ == "__main__":
    main()
