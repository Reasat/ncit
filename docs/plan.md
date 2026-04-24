# NCIT (NCI Thesaurus) Mondo source ingest

## Upstream

- **Temporary mirror:** OBO Foundry NCIT disorders extract (Disease or Disorder branch):
  `http://purl.obolibrary.org/obo/ncit/ncit-disorders.owl` — smaller than the full asserted EVS drop; used until the large-file pipeline is restored.
- **Planned / authoritative asserted OWL:** NCI EVS stable “current” ZIP (tracks latest monthly build):
  `https://evs.nci.nih.gov/ftp1/NCI_Thesaurus/Thesaurus.OWL.zip` — extract `Thesaurus.owl` as `tmp/ncit_raw.owl`.
- **Release identifier (EVS):** `owl:versionInfo` on the ontology (e.g. `26.03e`). The disorders extract uses `owl:versionIRI` under `…/ncit/releases/…`.

The inferred build (`ThesaurusInf.OWL.zip`) is not used here; it targets UMLS/Metathesaurus import and excludes retired concepts.

## ID scheme

- **EVS class IRIs:** `http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#` + fragment `C` + digits (e.g. `#C3262`).
- **OBO edition class IRIs (current mirror):** `http://purl.obolibrary.org/obo/NCIT_C` + digits (e.g. `NCIT_C100012`).
- **YAML CURIEs:** `NCIT:C…` in both cases (required for `linkml-owl`).

## Pipeline

1. **Mirror / acquire:** `scripts/acquire.py` (or `make mirror`) downloads `ncit-disorders.owl` from the PURL above → `tmp/ncit_raw.owl` (temporary; replace with EVS ZIP extract when scaling to full NCIT). Override with `NCIT_MIRROR_URL` / `--url`.
2. **Mirror normalize:** `robot merge … odk:normalize` → `tmp/mirror-ncit.owl`.
3. **Component (ROBOT):**
   - Drop imports.
   - **Rename** EVS synonym/definition predicates to standard annotations:
     - `…#P97` → `obo:IAO_0000115`
     - `…#P90` → `oboInOwl:hasExactSynonym`
   - **SPARQL:** `sparql/fix_xref_prefixes.ru` (NBSP strip + common xref prefix normalisation).
   - **Property allowlist** (`config/properties.txt`): keep labels, definitions, synonyms, xrefs, subset, skos matches, etc.; drop NCIT-specific editorial noise not needed for Mondo.
   - **Annotate** component ontology IRI / version IRI.
   - Output: `tmp/transformed-ncit.owl`.
4. **Transform (`scripts/transform.py`):** rdflib read → YAML `ncit.yaml` (all `owl:Class` in the NCIT class IRI scheme with a non-empty `rdfs:label`; direct `rdfs:subClassOf` parents only; restrictions ignored for `parents`).
5. **Validate:** `linkml-validate` on `ncit.yaml`.
6. **Verify:** `scripts/verify.py`.
7. **OWL:** copy `tmp/transformed-ncit.owl` → top-level `ncit.owl` (same graph the transform read; `linkml-owl` re-materialisation is omitted at full NCIT scale — ~200k+ classes; the disorders extract is smaller).

## Field mappings

| Source (post-ROBOT) | Schema slot |
|---------------------|-------------|
| `rdfs:label` | `label` |
| `obo:IAO_0000115` (from P97) | `definition` |
| `oboInOwl:hasExactSynonym` (from P90) | `exact_synonyms` |
| `oboInOwl:hasDbXref` (+ normalisation) | merged into `skos_exact_match` |
| `skos:*Match` | respective `skos_*_match` slots |
| `owl:deprecated` | `deprecated` |
| Direct `rdfs:subClassOf` to another NCIT class | `parents` |

## Reports

`sparql/count_classes_by_top_level.sparql` counts descendants under illustrative high-level NCIT classes (each listed as **both** EVS `#C…` and OBO `NCIT_C…` IRIs so `make reports` works for either mirror):

- `C7057` — Disease, Disorder or Finding (ontology root for that branch)
- `C2991` — Disease or Syndrome (child of C7057)
- `C3262` — Neoplasm

## Versioning

- **YAML `version`:** taken from `owl:versionInfo` on the source ontology block when present (EVS release tag). The disorders extract may omit it (`unknown` until we parse `owl:versionIRI` or similar).

## CI / release

- **Release workflow:** weekly cron + `workflow_dispatch` + push to `main` when pipeline paths change. Adjust in `.github/workflows/release.yml` if a different cadence is needed.
