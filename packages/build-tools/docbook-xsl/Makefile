include $(TOP_SRCDIR)/packages/build-tools/common.mk

schemadir = $(BUILD_TOOLS)/share/xml/docbook/schema
oasis_url = http://www.oasis-open.org/docbook
docbook_url = http://docbook.org

$(srcdir)/stamp-install:
	for ns in -nons ''; do \
		install -Dt "$(BUILD_TOOLS)/share/xml/docbook/xsl-stylesheets-$(package.version)$$ns" -m 644 $(srcdir)/docbook-xsl$$ns-$(package.version)/VERSION{,.xsl}; ( \
		shopt -s nullglob; \
		for fn in assembly common eclipse epub epub3 fo highlighting html htmlhelp javahelp lib manpages params profiling roundtrip template website xhtml xhtml-1_1 xhtml5; do \
			install -Dt "$(BUILD_TOOLS)/share/xml/docbook/xsl-stylesheets-$(package.version)$$ns/$$fn" -m 644 $(srcdir)/docbook-xsl$$ns-$(package.version)/$$fn/*.{xml,xsl,dtd,ent}; \
		done \
	) done
	touch $@

$(BUILD_TOOLS)/etc/xml/catalog: $(srcdir)/stamp-install
	test -e $@ || xmlcatalog --nooout --create $@
	for version in $(package.version) current; do \
		for x in rewriteSystem rewriteURI; do \
			xmlcatalog --noout --add rewriteSystem \
				http://cdn.docbook.org/release/xsl/$$version \
				$(BUILD_TOOLS)/share/xml/docbook/xsl-stylesheets-$(package.version) \
				$@ ; \
			xmlcatalog --noout --add rewriteSystem \
				http://cdn.docbook.org/release/xsl-nons/$$version \
				$(BUILD_TOOLS)/share/xml/docbook/xsl-stylesheets-$(package.version)-nons \
				$@; \
			xmlcatalog --noout --add rewriteSystem \
				http://docbook.sourceforge.net/release/xsl-ns/$$version \
				$(BUILD_TOOLS)/share/xml/docbook/xsl-stylesheets-$(package.version) \
				$@; \
			xmlcatalog --noout --add rewriteSystem \
				http://docbook.sourceforge.net/release/xsl/$$version \
				$(BUILD_TOOLS)/share/xml/docbook/xsl-stylesheets-$(package.version)-nons \
				$@; \
		done \
	done

install: $(srcdir)/stamp-install $(BUILD_TOOLS)/etc/xml/catalog

.PHONY: install
