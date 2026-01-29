include $(TOP_SRCDIR)/packages/build-tools/common.mk

schemadir = $(BUILD_TOOLS)/share/xml/docbook/schema
oasis_url = http://www.oasis-open.org/docbook
docbook_url = http://docbook.org

$(srcdir)/stamp-install:
	mkdir -p $(schemadir)/xml-dtd-$(package.version)
	cd $(srcdir) && \
		cp -dr docbook.cat *.dtd ent/ *.mod $(schemadir)/xml-dtd-$(package.version)
	#cd "$(srcdir)" && \
	#	mkdir -p "$(schemadir)" && \
	#	for type in dtd rng sch xsd; do \
	#		mkdir -p "$(schemadir)/$$type/5.0" && \
	#		install -m644 $$type/* "$(schemadir)/$$type/5.0"; \
	#	done && \
	#	mkdir -p "$(BUILD_TOOLS)/etc/xml" && \
	#	install -m644 docbook-5.0.xml "$(BUILD_TOOLS)/etc/xml"
	touch $@

$(BUILD_TOOLS)/etc/xml:
	mkdir -p $@

$(BUILD_TOOLS)/etc/xml/docbook-xml: | $(BUILD_TOOLS)/etc/xml
$(BUILD_TOOLS)/etc/xml/docbook-xml: $(srcdir)/stamp-install
	test -e $@ || xmlcatalog --noout --create $@
	xmlcatalog --noout --add "public" \
		"-//OASIS//DTD DocBook XML V$(package.version)//EN" \
		"$(oasis_url)/xml/$(package.version)/docbookx.dtd" \
		$@
	# XXX
	xmlcatalog --noout --add "rewriteSystem" \
		"$(oasis_url)/xml/$(package.version)" \
		$(schemadir)/xml-dtd-$(package.version) \
		$@
	xmlcatalog --noout --add "rewriteURI" \
		"$(oasis_url)/xml/$(package.version)" \
		$(schemadir)/xml-dtd-$(package.version) \
		$@

$(BUILD_TOOLS)/etc/xml/catalog: $(BUILD_TOOLS)/etc/xml/docbook-xml
	test -e $@ || xmlcatalog --noout --create $@
	xmlcatalog --noout --add "delegatePublic" \
		"-//OASIS//ENTITIES DocBook XML" \
		"file://$(BUILD_TOOLS)/etc/xml/docbook-xml" \
		$@
	xmlcatalog --noout --add "delegatePublic" \
		"-//OASIS/DTD DocBook XML" \
		"file://$(BUILD_TOOLS)/etc/xml/docbook-xml" \
		$@
	xmlcatalog --noout --add "delegateSystem" \
		"$(oasis_url)/" \
		"file://$(BUILD_TOOLS)/etc/xml/docbook-xml" \
		$@
	xmlcatalog --noout --add "delegateURI" \
		"$(oasis_url)/" \
		"file://$(BUILD_TOOLS)/etc/xml/docbook-xml" \
		$@

install: $(srcdir)/stamp-install $(BUILD_TOOLS)/etc/xml/catalog

.PHONY: install
