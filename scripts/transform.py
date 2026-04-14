#!/usr/bin/env python3
"""
Serialize NCI Thesaurus (EVS asserted OWL) component → schema-conformant YAML.

Reads ROBOT output (P97→IAO:0000115, P90→hasExactSynonym, xref fix). Class IRIs use the EVS
namespace `http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C…` expressed as CURIEs `NCIT:C…`.

Input:  tmp/transformed-ncit.owl
Output: ncit.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from rdflib import OWL, RDF, RDFS, Graph, Literal, URIRef
from rdflib.namespace import DCTERMS, SKOS, Namespace

OBOINOWL = Namespace("http://www.geneontology.org/formats/oboInOwl#")
OBO = Namespace("http://purl.obolibrary.org/obo/")

NCIT_IRI_PREFIX = "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#"
NCIT_CURIE_PREFIX = "NCIT:"

DEFINITION = OBO["IAO_0000115"]
OWL_DEPRECATED_PROP = OWL.deprecated


def is_ncit_class_iri(iri: str) -> bool:
    if not iri.startswith(NCIT_IRI_PREFIX):
        return False
    frag = iri[len(NCIT_IRI_PREFIX) :]
    return len(frag) > 0 and frag[0] == "C"


def iri_to_curie(iri: str) -> str:
    if iri.startswith(NCIT_IRI_PREFIX):
        return NCIT_CURIE_PREFIX + iri[len(NCIT_IRI_PREFIX) :]
    return iri


def _literal_values(g: Graph, subj: URIRef, pred) -> list[str]:
    out: list[str] = []
    for o in g.objects(subj, pred):
        if isinstance(o, Literal):
            val = str(o).strip()
            if val:
                out.append(val)
    return sorted(set(out))


def _uri_or_literal_values(g: Graph, subj: URIRef, pred) -> list[str]:
    out: list[str] = []
    for o in g.objects(subj, pred):
        if isinstance(o, (Literal, URIRef)):
            val = str(o).strip()
            if val:
                out.append(val)
    return sorted(set(out))


def collect_ncit_class_iris(g: Graph) -> set[str]:
    out: set[str] = set()
    for s in g.subjects(RDF.type, OWL.Class):
        if isinstance(s, URIRef):
            iri = str(s)
            if is_ncit_class_iri(iri):
                out.add(iri)
    return out


def get_direct_ncit_parents(g: Graph, subj: URIRef, known: set[str]) -> list[str]:
    parents: list[str] = []
    for o in g.objects(subj, RDFS.subClassOf):
        if isinstance(o, URIRef):
            oiri = str(o)
            if oiri in known:
                parents.append(iri_to_curie(oiri))
    return sorted(parents)


def extract_ontology_document(g: Graph) -> dict:
    doc: dict = {}
    for ont in g.subjects(RDF.type, OWL.Ontology):
        if not isinstance(ont, URIRef):
            continue
        lbl = g.value(ont, RDFS.label)
        if lbl:
            doc["title"] = str(lbl)
        ver = g.value(ont, OWL.versionInfo)
        if ver:
            doc["version"] = str(ver)
        dct = g.value(ont, DCTERMS.title)
        if dct:
            doc["dcterms_title"] = str(dct)
        break

    if "title" not in doc:
        doc["title"] = "NCI Thesaurus"
    if "version" not in doc:
        doc["version"] = "unknown"
    return doc


def extract_terms(g: Graph) -> list[dict]:
    known = collect_ncit_class_iris(g)
    terms: list[dict] = []

    for iri in sorted(known):
        subj = URIRef(iri)
        curie = iri_to_curie(iri)

        label_node = g.value(subj, RDFS.label)
        if label_node is None:
            continue
        label = str(label_node).strip()
        if not label:
            continue

        dep_node = g.value(subj, OWL_DEPRECATED_PROP)
        is_deprecated = dep_node is not None and str(dep_node).strip().lower() == "true"

        defn_node = g.value(subj, DEFINITION)
        definition = str(defn_node).strip() if defn_node else None

        exact_syns = _literal_values(g, subj, OBOINOWL.hasExactSynonym)

        parent_curies = get_direct_ncit_parents(g, subj, known)
        is_root = len(parent_curies) == 0

        term: dict = {"id": curie, "label": label}
        if is_deprecated:
            term["deprecated"] = True
        if definition:
            term["definition"] = definition
        if exact_syns:
            term["exact_synonyms"] = [{"synonym_text": s} for s in exact_syns]
        if not is_root:
            term["parents"] = parent_curies

        for key, pred in (
            ("related_synonyms", OBOINOWL.hasRelatedSynonym),
            ("narrow_synonyms", OBOINOWL.hasNarrowSynonym),
            ("broad_synonyms", OBOINOWL.hasBroadSynonym),
        ):
            vals = _literal_values(g, subj, pred)
            if vals:
                term[key] = [{"synonym_text": s} for s in vals]

        xrefs = _uri_or_literal_values(g, subj, OBOINOWL.hasDbXref)
        for key, pred in (
            ("skos_exact_match", SKOS.exactMatch),
            ("skos_broad_match", SKOS.broadMatch),
            ("skos_narrow_match", SKOS.narrowMatch),
            ("skos_related_match", SKOS.relatedMatch),
        ):
            vals = _uri_or_literal_values(g, subj, pred)
            if vals:
                term[key] = vals

        if xrefs:
            existing = term.get("skos_exact_match", [])
            term["skos_exact_match"] = sorted(set(existing + xrefs))

        terms.append(term)

    return terms


def transform(input_path: Path, output_path: Path) -> None:
    print(f"Parsing component OWL: {input_path}", file=sys.stderr)
    g = Graph()
    g.parse(str(input_path))

    doc = extract_ontology_document(g)
    terms = extract_terms(g)

    active = sum(1 for t in terms if not t.get("deprecated"))
    deprecated = sum(1 for t in terms if t.get("deprecated"))
    print(
        f"Extracted {len(terms)} NCIT classes ({active} active, {deprecated} deprecated)",
        file=sys.stderr,
    )

    doc["terms"] = terms

    class QuotedDumper(yaml.Dumper):
        pass

    QuotedDumper.add_representer(
        str,
        lambda dumper, data: dumper.represent_scalar("tag:yaml.org,2002:str", data, style="'")
        if any(c in data for c in ",:{}")
        else dumper.represent_scalar("tag:yaml.org,2002:str", data),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        yaml.dump(
            doc,
            fh,
            Dumper=QuotedDumper,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )

    print(f"Written: {output_path}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Serialize NCIT component OWL → schema YAML")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    if not args.schema.exists():
        print(f"Error: schema file not found: {args.schema}", file=sys.stderr)
        sys.exit(1)

    transform(args.input, args.output)


if __name__ == "__main__":
    main()
