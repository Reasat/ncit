# Release notes (NCIT)

## 2026-04-14 (scaffold verification)

- **EVS / NCIt build:** `26.03e` (from `owl:versionInfo` in source ontology; mirrored in `ncit.yaml` `version`).
- **Terms:** 211,072 total (205,508 active, 5,564 deprecated); unique IDs 211,072; broken parent refs 0.
- **ROBOT metrics (final `ncit.owl`):** class count 211,072; axiom count 646,315 (extended JSON in `reports/metrics.json`).
- **Top-level descendant counts** (`reports/top-level-counts.tsv`): Disease, Disorder or Finding (C7057) 35,173; Disease or Disorder (C2991) 7,085; Neoplasm (C3262) 400.
- **linkml-validate:** PASS.
- **verify.py:** PASS.
- **OWL note:** `ncit.owl` is a copy of the ROBOT component file `tmp/transformed-ncit.owl` (not `linkml-owl` output); see `docs/pipeline_incidents.md`.
