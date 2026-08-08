# labels/

Human ground-truth labels for the benchmark subset.

Each teammate commits their exported labels here as
`<github-handle>.json`, produced by the labeling tool
(`data/benchmark-v1/labeling/label-standalone.html` → "Export my labels").

Rules:
- File name = your GitHub handle, e.g. `alan12-li.json`.
- Every image needs ≥2 agreeing labelers; disagreements become `uncertain`.
- Never edit someone else's labels file; add your own.
