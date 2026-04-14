# NCIT (NCI Thesaurus) Mondo source ingest

## Upstream

- **Publisher:** NCI Enterprise Vocabulary Services (EVS).
- **Asserted OWL:** stable “current” ZIP URL (always tracks the latest monthly build):
  `https://evs.nci.nih.gov/ftp1/NCI_Thesaurus/Thesaurus.OWL.zip`
- **Inside the ZIP:** `Thesaurus.owl` — primary EVS OWL2 representation (asserted is-a and roles as edited).
- **Release identifier:** `owl:versionInfo` on the ontology (e.g. `26.03e`), matching EVS `ReadMe.txt` and the download page.

The inferred build (`ThesaurusInf.OWL.zip`) is not used here; it targets UMLS/Metathesaurus import and excludes retired concepts.

## ID scheme

- **Class IRIs:** `http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#` + fragment `C` + digits (e.g. `#C3262`).
- **YAML / OWL CURIEs:** `NCIT:C3262` with prefix `NCIT:` → the EVS namespace above (required for `linkml-owl`).

This matches the authoritative EVS file, not the OBO Foundry PURL form (`http://purl.obolibrary.org/obo/NCIT_C…`).

## Pipeline

1. **Mirror:** download `Thesaurus.OWL.zip`, extract `Thesaurus.owl` → `tmp/ncit_raw.owl`.
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
4. **Transform (`scripts/transform.py`):** rdflib read → YAML `ncit.yaml` (all `owl:Class` in the EVS namespace with a non-empty `rdfs:label`; direct `rdfs:subClassOf` parents only; restrictions ignored for `parents`).
5. **Validate:** `linkml-validate` on `ncit.yaml`.
6. **Verify:** `scripts/verify.py`.
7. **OWL:** copy `tmp/transformed-ncit.owl` → top-level `ncit.owl` (same graph the transform read; `linkml-owl` re-materialisation is omitted at this scale — ~200k+ classes).

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

`sparql/count_classes_by_top_level.sparql` counts descendants under illustrative high-level NCIT classes:

- `C7057` — Disease, Disorder or Finding (ontology root for that branch)
- `C2991` — Disease or Syndrome (child of C7057)
- `C3262` — Neoplasm

## Versioning

- **YAML `version`:** taken from `owl:versionInfo` on the source ontology block (EVS release tag).

## CI / release

- **Release workflow:** weekly cron + `workflow_dispatch` + push to `main` when pipeline paths change. Adjust in `.github/workflows/release.yml` if a different cadence is needed.
