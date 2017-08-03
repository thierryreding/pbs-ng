include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/aarch64-regs.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
