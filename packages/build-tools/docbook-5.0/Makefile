include $(TOP_SRCDIR)/packages/build-tools/common.mk

schemadir = $(BUILD_TOOLS)/share/xml/docbook/schema
oasis_url = http://www.oasis-open.org/docbook
docbook_url = http://docbook.org

$(srcdir)/docbook-5.0.xml: $(srcdir)/docbook-%.xml: | $(srcdir)
	xmlcatalog --noout --create $@
	xmlcatalog --noout --add "public" "-//OASIS//DTD DocBook XML $*//EN" "file://$(schemadir)/dtd/$*/docbook.dtd" $@
	for url in $(oasis_url) $(docbook_url); do \
		xmlcatalog --noout --add "system" "$$url/xml/$*/dtd/docbook.dtd" "file://$(schemadir)/dtd/$*/docbook.dtd" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/rng/docbook.rng" "file://$(schemadir)/rng/$*/docbook.rng" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/rng/docbookxi.rng" "file://$(schemadir)/rng/$*/docbookxi.rng" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/rnc/docbook.rnc" "file://$(schemadir)/rnc/$*/docbook.rnc" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/rnc/docbookxi.rnc" "file://$(schemadir)/rnc/$*/docbookxi.rnc" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/xsd/docbook.xsd" "file://$(schemadir)/xsd/$*/docbook.xsd" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/xsd/docbookxi.xsd" "file://$(schemadir)/xsd/$*/docbookxi.xsd" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/xsd/xi.xsd" "file://$(schemadir)/xsd/$*/xi.xsd" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/xsd/xlink.xsd" "file://$(schemadir)/xsd/$*/xlink.xsd" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/xsd/xml.xsd" "file://$(schemadir)/xsd/$*/xml.xsd" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$*/sch/docbook.sch" "file://$(schemadir)/sch/$*/docbook.sch" $@; \
	done

$(srcdir)/dtd/catalog.xml: VERSION = 5.0
$(srcdir)/dtd/catalog.xml:
	xmlcatalog --noout --create $@
	xmlcatalog --noout --add "public" "-//OASIS//DTD DocBook XML $(VERSION)//EN" "docbook.dtd" $@
	xmlcatalog --noout --add "system" "$(oasis_url)/xml/$(VERSION)/dtd/docbook.dtd" "docbook.dtd" $@

$(srcdir)/sch/catalog.xml: VERSION = 5.0
$(srcdir)/sch/catalog.xml:
	xmlcatalog --noout --create $@
	for url in $(docbook_url) $(oasis_url); do \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/sch/docbook.sch" "docbook.sch" $@; \
	done

$(srcdir)/rng/catalog.xml: VERSION = 5.0
$(srcdir)/rng/catalog.xml:
	xmlcatalog --noout --create $@
	for url in $(docbook_url) $(oasis_url); do \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/rng/docbook.rng" "docbook.rng" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/rng/docbookxi.rng" "docbookxi.rng" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/rnc/docbook.rnc" "docbook.rnc" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/rnc/docbookxi.rnc" "docbookxi.rnc" $@; \
	done

$(srcdir)/xsd/catalog.xml: VERSION = 5.0
$(srcdir)/xsd/catalog.xml:
	xmlcatalog --noout --create $@
	for url in $(docbook_url) $(oasis_url); do \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/xsd/docbook.xsd" "docbook.xsd" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/xsd/docbookxi.xsd" "docbookxi.xsd" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/xsd/xlink.xsd" "xlink.xsd" $@ && \
		xmlcatalog --noout --add "uri" "$$url/xml/$(VERSION)/xsd/xml.xsd" "xml.xsd" $@; \
	done

$(srcdir)/stamp-install: $(srcdir)/docbook-5.0.xml
$(srcdir)/stamp-install: $(srcdir)/dtd/catalog.xml
$(srcdir)/stamp-install: $(srcdir)/rng/catalog.xml
$(srcdir)/stamp-install: $(srcdir)/sch/catalog.xml
$(srcdir)/stamp-install: $(srcdir)/xsd/catalog.xml
	cd "$(srcdir)" && \
		mkdir -p "$(schemadir)" && \
		for type in dtd rng sch xsd; do \
			mkdir -p "$(schemadir)/$$type/5.0" && \
			install -m644 $$type/* "$(schemadir)/$$type/5.0"; \
		done && \
		mkdir -p "$(BUILD_TOOLS)/etc/xml" && \
		install -m644 docbook-5.0.xml "$(BUILD_TOOLS)/etc/xml"
	touch $@

$(BUILD_TOOLS)/etc/xml/catalog: $(srcdir)/stamp-install
	test -e $@ || xmlcatalog --noout --create $@
	xmlcatalog --noout --add "delegatePublic" "-//OASIS//ENTITIES DocBook XML" "file://$(BUILD_TOOLS)/etc/xml/docbook-5.0.xml" $@
	xmlcatalog --noout --add "delegatePublic" "-//OASIS//DTD DocBook XML" "file://$(BUILD_TOOLS)/etc/xml/docbook-5.0.xml" $@
	xmlcatalog --noout --add "delegateSystem" "$(oasis_url)" "file://$(BUILD_TOOLS)/etc/xml/docbook-5.0.xml" $@
	xmlcatalog --noout --add "delegateURI" "$(oasis_url)" "file://$(BUILD_TOOLS)/etc/xml/docbook-5.0.xml" $@

install: $(srcdir)/stamp-install $(BUILD_TOOLS)/etc/xml/catalog

.PHONY: install
