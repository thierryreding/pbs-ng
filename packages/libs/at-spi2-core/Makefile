include $(TOP_SRCDIR)/packages/meson.mk

env += \
	PKG_CONFIG_FDO_SYSROOT_RULES=1

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/introspection.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
