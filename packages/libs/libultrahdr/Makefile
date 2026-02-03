include $(TOP_SRCDIR)/packages/cmake.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/gcc-15.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
