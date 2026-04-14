# NCIT — NCI Thesaurus asserted OWL from EVS (stable “current” ZIP).

# Authoritative asserted release: unversioned alias always tracks the latest monthly build.
THESAURUS_ZIP_URL ?= https://evs.nci.nih.gov/ftp1/NCI_Thesaurus/Thesaurus.OWL.zip

ifeq ($(MIR),true)
$(RAW_OWL): | $(TMP_DIR)
	curl -fsSL -o $(TMP_DIR)/Thesaurus.OWL.zip $(THESAURUS_ZIP_URL)
	unzip -o -q $(TMP_DIR)/Thesaurus.OWL.zip Thesaurus.owl -d $(TMP_DIR)
	mv -f $(TMP_DIR)/Thesaurus.owl $@
	@echo "Downloaded and extracted: $@"
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
