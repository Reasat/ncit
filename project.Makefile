# NCIT — temporary mirror: OBO Foundry NCIT disorders branch extract (smaller than full EVS ZIP).
# Reinstate EVS `Thesaurus.OWL.zip` when ready: see docs/plan.md.

NCIT_MIRROR_URL ?= http://purl.obolibrary.org/obo/ncit/ncit-disorders.owl

ifeq ($(MIR),true)
$(RAW_OWL): | $(TMP_DIR)
	python $(SCRIPTS_DIR)/acquire.py --url "$(NCIT_MIRROR_URL)" -o "$(RAW_OWL)"
	@echo "Downloaded: $@"
endif

# ROBOT: normalize, rename NCIT editor predicates to OBO/oboInOwl, fix xref prefixes, strip
$(OUTPUT_OWL): $(MIRROR_OWL) \
		$(CONFIG_DIR)/property-map.sssom.tsv \
		$(CONFIG_DIR)/properties.txt \
		$(SPARQL_DIR)/fix_xref_prefixes.ru
	$(ROBOT) remove -i $(MIRROR_OWL) --select imports \
		rename --mappings $(CONFIG_DIR)/property-map.sssom.tsv \
			--allow-missing-entities true --allow-duplicates true \
		query --update $(SPARQL_DIR)/fix_xref_prefixes.ru \
		remove -T $(CONFIG_DIR)/properties.txt --select complement --select properties --trim true \
		annotate \
			--ontology-iri $(URIBASE)/mondo/sources/$(SOURCE).owl \
			--version-iri $(URIBASE)/mondo/sources/$(TODAY)/$(SOURCE).owl \
		-o $@
	@echo "Build complete: $@"
