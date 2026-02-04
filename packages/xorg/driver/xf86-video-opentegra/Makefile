include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/xorg-server-1.15.patch
	touch $@

conf-args += \
	--with-sysroot=$(SYSROOT)

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
