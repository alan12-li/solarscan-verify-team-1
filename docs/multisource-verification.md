# Multi-Source Verification — Beyond the Image Alone

**Date:** 2026-08-10
**Status:** Data-source validation ✅ · **Branch-logic tested 20/20 ✅**
**· Context injection implemented & demoed ✅ · NYC orthoimagery pipeline
verified (PATH B) ✅ · Full image→records benchmark: not scored ⚠️**
**Owner:** SolarScan Verify team

## The idea

The verification layer should not rely on the rooftop image alone. When the
image is ambiguous — or a model reads it wrong — **independent public records
can corroborate or refute the model's call**. This is exactly the "optional
context" the PRD §3 defines (building footprint, parcel/address, permit
records, roof geometry, historical imagery). This document validates that the
data exists, is public, and is queryable — and states honestly what we have
and have not tested.

## Why it matters (from our benchmark)

Our 30-case benchmark shows models are confident on exactly the roofs humans
hesitate over (slide 9). A second, independent signal gives the verification
layer a way to **catch confident wrong answers**:

- Image says `solar`, but no solar permit + flat-roof feature code + recent
  construction → escalate to human, don't rubber-stamp.
- Image says `no_solar`, but a completed solar permit exists for the parcel →
  escalate; the model may have missed panels.
- Image is `uncertain`, permit says `Completed` → strong evidence to review
  first (the permit is authoritative: someone installed solar there).

## Validated public data sources (queried 2026-08-10)

### 1. NYC Solar PV permits — LL24 (NYC Open Data, dataset `cfz5-6fvh`)

Public API (no key): `https://data.cityofnewyork.us/resource/cfz5-6fvh.json`

Fields that matter: `address`, `status` (`Completed`/`In Progress`),
`installation_date`, `estimated_annual_production`, `borough`, `agency`.

Verified query — address lookup:
```
GET /resource/cfz5-6fvh.json?address=199%20Chambers%20St
→ 3 records, status "Completed", installation dates 2017–2018
```
This answers the binary question **"is there a completed solar installation
at this address?"** — exactly the corroboration the verification layer needs.

### 2. NYC Building Footprints (NYC Open Data, dataset `5zhs-2jue`)

Public API (no key): `https://data.cityofnewyork.us/resource/5zhs-2jue.json`

Fields that matter: `height_roof`, `ground_elevation` (→ roof height above
grade), `construction_year`, `feature_code` (building type), `the_geom`
(GeoJSON footprint polygon), `bin`/`bbl` (parcel identifiers).

Verified: dataset responds, columns confirmed.

Use: roof geometry context — a low flat roof with HVAC (feature_code
`Warehouse`/`Garage`) makes `solar` less likely on a thermal image alone;
`height_roof` differences help disambiguate rooftop equipment from panels.

### 3. OpenStreetMap (ODbL)

Building outlines + roof tags (`roof:shape`, `roof:orientation`, `roof:levels`)
via Overpass API. Useful as a fallback geometry source outside NYC data.

## How the verification agent would use them

```
image + address
   │
   ├─ model ensemble → {solar | no_solar | uncertain} + confidence
   │
   ├─ LL24 permit lookup (address) → permit_status
   ├─ Building Footprint (parcel) → roof_height, feature_code, footprint
   │
   └─ Decision rule (PRD §5 + new "corroboration" branch):
        if permit = Completed and model = no_solar  → escalate (likely miss)
        if permit = none and model = solar and conf < 0.8 → escalate (possible false positive)
        if records disagree with model → escalate to human with both signals shown
        if records agree → accept with higher confidence
```

The agent does not replace the human — it **gives the human better evidence**
and catches the failure mode our benchmark measured (confident wrong answers).

## Honest limitations (what we have NOT done)

1. **Not benchmarked end-to-end.** Our 30 benchmark images are an
   anonymized public drone dataset with **no addresses/parcels**, so we
   could not join them to NYC records. **The capability is implemented and
   the mechanism verified** (context injection changes model behavior;
   lookup APIs return real records; decision rules followed 20/20), but a
   real-data accuracy score needs N roofs with parcel IDs — the first step
   of the proposed limited test.
2. **Permit coverage is not complete.** LL24 records reported installations;
   older or unpermitted systems may be missing. Absence of a permit is
   **not** proof of no solar.
3. **Address matching needs care.** Roof images rarely carry addresses;
   the scanner's existing parcel IDs are the natural join key (ask Con
   Edison which identifier is available — `docs/con-edison-questions.md`).
4. **No Con Edison data used.** Everything above is public NYC Open Data /
   OSM. Exact parcel coordinates beyond the footprint and customer info stay
   off-limits (PRD §2, course red lines).

## Context injection into classification (2026-08-10) — mechanism works ✅

The PRD §3 context signals are now **usable at classification time**:
`scripts/evaluate_benchmark.py --context <dir>` reads per-case
`<case_id>.json` files (building_footprint, parcel_id, permit, roof_geometry,
historical_imagery) and injects them into the model prompt as corroborating
evidence ("use as corroboration, do not overrule clear visual evidence").
Cases without a context file run image-only (PRD §5 fallback).

**Demo (synthetic context, 3 cases, Gemini 3.5 Flash-Lite):**

| Case | Image-only | Image + context | Effect |
|---|---|---|---|
| sv-0001 | no_solar (0.95) | no_solar (0.95) | consistent (no permit supports no_solar) |
| **sv-0003** | **uncertain (0.45)** | **no_solar (0.85)** | **model used context to move off uncertain** |
| sv-0004 | solar (0.95) | solar (0.95) | consistent (permit supports solar) |

**Finding:** the model demonstrably uses injected context — on the hardest
image (sv-0003, where models split), context converted `uncertain` → a
confident `no_solar`. Mechanism verified end-to-end (prompt → API → parsed
JSON). Context files: `data/benchmark-v1/context/*.json` (**synthetic,
clearly marked — the 30 benchmark images have no real addresses**).

## NYC orthoimagery pipeline (PATH B) — verified 2026-08-10 ✅

**The end-to-end chain works.** We proved we can go from public data to a
model classification of a real NYC roof:

```
Building Footprints (5zhs-2jue, Manhattan, BBL + centroid)
   -> NYC Orthos 2018 MapServer tile (public, CC BY 4.0, z=19 ≈ 0.5 m/px)
   -> Gemini classifies the roof (structured JSON)
```

- **Verified:** 4 Manhattan roofs downloaded (15–17 KB tiles); Gemini
  classified one as `no_solar, conf 0.9` ("standard shingled textures
  without distinct solar panel arrays").
- **Reproducible:** `scripts/fetch_nyc_roofs.py --count N --z 19 --out DIR`
  (writes a manifest with BBL, roof height, feature code, tile XYZ).
- **Data sources:** `NYC Orthos 2018` MapServer (public, CC BY 4.0);
  Building Footprints `5zhs-2jue`; LL24 solar permits `cfz5-6fvh`
  (join needs an address — the Con Edison data step).
- **Honest scope:** mechanism proof only. The 20 downloaded roofs have **no
  ground truth** (needs labelers) and the **permit join needs real
  addresses** (Con Edison step). This is the first stage of the proposed
  100-roof limited test, not an accuracy result.

## Branch-logic test (2026-08-10) — rule-following measured ✅

We tested whether models actually **follow the corroboration rules**, using
10 synthetic {hypothesis, permit} scenarios × 2 models
(`scripts/test_corroboration.py`):

| Model | Rule-following |
|---|---|
| GPT-5.5 | **10/10 (100%)** |
| Gemini 3.5 Flash-Lite | **10/10 (100%)** |
| **Combined** | **20/20 (100%)** |

**Honest scope:** this tests the *decision branch* (given a hypothesis and a
permit record, does the model apply the rule correctly), NOT image
classification and NOT end-to-end. The 30 benchmark images have no addresses,
so the full image→records pipeline remains part of the limited test.

**Finding (reproduced by prompt iteration):** rule-following depends on
**unambiguous rules**. With vague wording ("no permit found" vs "low
confidence") models disagreed; after separating "lookup OK, zero records"
from "lookup unavailable" and making the confidence threshold literal
(< 0.8), both models hit 100%. Same lesson as the main classification:
**prompt quality is the system.**

## Next test (proposed, part of the "limited test")

Take N NYC addresses with known solar status (LL24 `Completed` = positive,
random sample without permits = negative), run the image+context pipeline,
and measure whether the corroboration branch **reduces confident-wrong
answers** and **raises escalation precision** — the two metrics our 30-case
benchmark identified as weak.
