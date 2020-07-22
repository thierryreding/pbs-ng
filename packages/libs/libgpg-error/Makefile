include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/pkg-config.patch
	cd $(srcdir) && autoreconf --force --install --verbose
	touch $@

conf-args += \
	--with-sysroot=$(SYSROOT)

conf-vars += \
	AWK='$(AWK) --non-decimal-data'

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
