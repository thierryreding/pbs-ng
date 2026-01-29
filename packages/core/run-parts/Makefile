include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-prepare: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/conditional-docs.patch
	cd $(srcdir) && autoreconf --force --install --verbose
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-prepare
