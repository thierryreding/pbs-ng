include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/libressl-2.7.0.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
