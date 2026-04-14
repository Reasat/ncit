# ncit

NCI Thesaurus (EVS asserted OWL) as LinkML YAML and LinkML-derived OWL for Mondo ingest.

## Setup

Install dependencies (local validation / `verify` outside Docker):

```bash
uv sync
```

## Run

```bash
./odk.sh make all
./odk.sh make MIR=false build
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
