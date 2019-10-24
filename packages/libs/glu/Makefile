include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/NULL.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
