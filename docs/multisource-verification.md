# Multi-Source Verification — Beyond the Image Alone

**Date:** 2026-08-10
**Status:** Design + data-source validation ✅ · **Not yet benchmarked** ⚠️
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

1. **Not benchmarked.** Our 30 benchmark images are an anonymized public drone
   dataset with **no addresses/parcels**, so we could not join them to NYC
   records. The multi-source path is designed and its data sources are
   validated, but its accuracy has not been measured.
2. **Permit coverage is not complete.** LL24 records reported installations;
   older or unpermitted systems may be missing. Absence of a permit is
   **not** proof of no solar.
3. **Address matching needs care.** Roof images rarely carry addresses;
   the scanner's existing parcel IDs are the natural join key (ask Con
   Edison which identifier is available — `docs/con-edison-questions.md`).
4. **No Con Edison data used.** Everything above is public NYC Open Data /
   OSM. Exact parcel coordinates beyond the footprint and customer info stay
   off-limits (PRD §2, course red lines).

## Next test (proposed, part of the "limited test")

Take N NYC addresses with known solar status (LL24 `Completed` = positive,
random sample without permits = negative), run the image+context pipeline,
and measure whether the corroboration branch **reduces confident-wrong
answers** and **raises escalation precision** — the two metrics our 30-case
benchmark identified as weak.
