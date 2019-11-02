include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/ltmain-sysroot.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/aarch64.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch | $(builddir)

conf-args += \
	--with-sysroot=$(SYSROOT)
