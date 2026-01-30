include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/glibc-2.43.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
