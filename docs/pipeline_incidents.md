# Pipeline incidents (NCIT)

Record unexpected failures, tool quirks, and deviations from the standard mondo-source-ingest template.

## linkml-runtime inlined list + commas

If `linkml-validate` or loading YAML fails on synonym strings containing commas, the known `linkml_runtime` inlining bug may apply. The `make dependencies` target installs `linkml` / `linkml-runtime` from the `linkml/linkml` monorepo `main` branch inside the ODK container (see root `Makefile`). Document the upstream fix here when released.

## Initial scaffold

- **2026-04-14:** Repository created with EVS stable `Thesaurus.OWL.zip` URL and ROBOT rename of `P90`/`P97` to standard oboInOwl / IAO predicates.

## ROBOT Java heap (large ontology)

- First `robot` component build hit `OutOfMemoryError` with default heap. Run Docker with `-e ROBOT_JAVA_ARGS=-Xmx24G -e JAVA_OPTS=-Xmx24G` (see `odk.sh`).

## linkml-owl vs release OWL

- `linkml-owl` re-serialisation from YAML for ~211k classes did not complete in reasonable time. The Makefile copies `tmp/transformed-ncit.owl` to `ncit.owl` instead — the same graph consumed by `transform.py`, so YAML and OWL stay aligned.
