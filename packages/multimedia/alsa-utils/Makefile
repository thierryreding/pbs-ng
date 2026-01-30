include $(TOP_SRCDIR)/packages/autotools.mk

# XXX point to $(BUILD_TOOLS)/etc/xml/catalog once docbook support is enabled
env += XML_CATALOG_FILES=/etc/xml/catalog

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/const-correctness.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
