include $(TOP_SRCDIR)/packages/build-tools/python.mk

ifeq ($(realpath $(srcdir)),$(srcdir))
$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/sysroot-default-include-dir.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/gobject-introspection-sysroot.patch
	touch $@

$(builddir)/stamp-install: $(srcdir)/stamp-patch
endif
