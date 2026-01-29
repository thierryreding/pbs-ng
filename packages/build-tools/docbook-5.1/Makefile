include $(TOP_SRCDIR)/packages/build-tools/common.mk

schemadir = $(BUILD_TOOLS)/share/xml/docbook/schema
oasis_url = http://www.oasis-open.org/docbook
docbook_url = http://docbook.org

$(srcdir)/docbook-5.1.xml: $(srcdir)/docbook-%.xml: | $(srcdir)
	xmlcatalog --noout --create $@
	for url in $(oasis_url) $(docbook_url); do \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/rng/docbook.rng" "file://$(schemadir)/rng/$*/docbook.rng" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/rng/docbookxi.rng" "file://$(schemadir)/rng/$*/docbookxi.rng" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/rnc/docbook.rnc" "file://$(schemadir)/rnc/$*/docbook.rnc" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/rnc/docbookxi.rnc" "file://$(schemadir)/rnc/$*/docbookxi.rnc" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/sch/docbook.sch" "file://$(schemadir)/rng/$*/docbook.sch" $@; \
	done

$(srcdir)/schemas/rng/catalog.xml: VERSION = 5.1
$(srcdir)/schemas/rng/catalog.xml:
	xmlcatalog --noout --create $@
	for url in $(oasis_url) $(docbook_url); do \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/rng/docbook.rng" "docbook.rng" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/rng/docbookxi.rng" "docbookxi.rng" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/rng/docbook.rnc" "docbook.rnc" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/rng/docbookxi.rnc" "docbookxi.rnc" $@; \
	done

$(srcdir)/schemas/sch/catalog.xml: VERSION = 5.1
$(srcdir)/schemas/sch/catalog.xml:
	xmlcatalog --noout --create $@
	for url in $(oasis_url) $(docbook_url); do \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/sch/docbook.sch" "docbook.sch" $@; \
	done

$(srcdir)/stamp-install: $(srcdir)/docbook-5.1.xml
$(srcdir)/stamp-install: $(srcdir)/schemas/rng/catalog.xml
$(srcdir)/stamp-install: $(srcdir)/schemas/sch/catalog.xml
	cd "$(srcdir)/schemas" && \
		mkdir -p "$(schemadir)" && \
		for type in rng sch; do \
			mkdir -p "$(schemadir)/$$type/5.1" && \
			install -m644 $$type/* "$(schemadir)/$$type/5.1"; \
		done
	cd "$(srcdir)" && \
		mkdir -p "$(BUILD_TOOLS)/etc/xml" && \
		install -m644 docbook-5.1.xml "$(BUILD_TOOLS)/etc/xml"
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
