# ncit

NCIt as LinkML YAML and release OWL for Mondo ingest. **Current upstream:** OBO Foundry
`ncit-disorders.owl` (disease/disorder branch) — smaller than the full EVS `Thesaurus.owl`
ZIP; see `docs/plan.md` for restoring the full asserted build.

## Setup

Install dependencies (local validation / `verify` outside Docker):

```bash
uv sync
```

Optional: copy `env/.env.example` to `env/.env` and set `NCIT_MIRROR_URL` if overriding the
default mirror.

## Run

```bash
./odk.sh make all
./odk.sh make MIR=false build
```

Fetch only (same as `make mirror`):

```bash
python scripts/acquire.py
```

## Outputs

| File | Description |
|------|-------------|
| `ncit.yaml` | Primary artefact for Mondo ingest |
| `ncit.owl` | ROBOT component OWL (same as `tmp/transformed-ncit.owl`; release artefact) |
| `reports/` | QC metrics and class counts |

## Docs

| Doc | Contents |
|-----|----------|
| [`docs/plan.md`](docs/plan.md) | Pipeline architecture, field mappings, ID scheme |
| [`docs/release_notes.md`](docs/release_notes.md) | Ontology stats and verification per release |
| [`docs/pipeline_incidents.md`](docs/pipeline_incidents.md) | Pipeline incidents and resolutions |
