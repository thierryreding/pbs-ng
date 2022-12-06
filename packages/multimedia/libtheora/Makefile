include $(TOP_SRCDIR)/packages/autotools.mk

ifeq ($(realpath $(srcdir)),$(srcdir))
$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/autotools.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/libpng-1.6.patch
	cd $(srcdir) && autoreconf --force --install --verbose
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
endif

conf-args += \
	--with-sdl-prefix=$(SYSROOT)$(prefix) \
	--with-sysroot=$(SYSROOT)
