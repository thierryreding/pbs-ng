include $(TOP_SRCDIR)/packages/meson.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/wayland-core.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
