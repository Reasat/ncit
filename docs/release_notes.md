# Release notes (NCIT)

## 2026-04-24 (disorders mirror + ingest alignment)

- **Upstream (temporary):** `http://purl.obolibrary.org/obo/ncit/ncit-disorders.owl` (OBO edition disease/disorder branch).
- **Terms (smoke build on disorders OWL, 2026-04-24):** 22,379 total (0 deprecated in that run); full `make all` in CI refreshes `ncit.yaml` / `ncit.owl` release assets.
- **Acquire:** `scripts/acquire.py` implements mirror download (`make mirror` calls it); optional `NCIT_MIRROR_URL` / `NCIT_RAW_OWL`.
- **Reports:** `sparql/count_classes_by_top_level.sparql` lists both EVS `#C…` and OBO `NCIT_C…` top-level IRIs so `make reports` works for either mirror (disorders extract may only populate some rows, e.g. C7057 absent).
- **Dependencies:** `pyproject.toml` / `uv.lock` use `linkml-owl==0.5.0` to match `make dependencies` in ODK.
- **linkml-validate / verify.py:** expected PASS after a full pipeline run on the disorders mirror.

## 2026-04-14 (scaffold verification)

- **EVS / NCIt build:** `26.03e` (from `owl:versionInfo` in source ontology; mirrored in `ncit.yaml` `version`).
- **Terms:** 211,072 total (205,508 active, 5,564 deprecated); unique IDs 211,072; broken parent refs 0.
- **ROBOT metrics (final `ncit.owl`):** class count 211,072; axiom count 646,315 (extended JSON in `reports/metrics.json`).
- **Top-level descendant counts** (`reports/top-level-counts.tsv`): Disease, Disorder or Finding (C7057) 35,173; Disease or Disorder (C2991) 7,085; Neoplasm (C3262) 400.
- **linkml-validate:** PASS.
- **verify.py:** PASS.
- **OWL note:** `ncit.owl` is a copy of the ROBOT component file `tmp/transformed-ncit.owl` (not `linkml-owl` output); see `docs/pipeline_incidents.md`.
