include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/libdir.patch
	cd $(srcdir) && autoreconf --force --install --verbose
	touch $@

conf-args += \
	--with-sysroot=$(SYSROOT)

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
