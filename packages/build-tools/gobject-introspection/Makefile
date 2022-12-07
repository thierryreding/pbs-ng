include $(TOP_SRCDIR)/packages/build-tools/meson.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/sysroot.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
