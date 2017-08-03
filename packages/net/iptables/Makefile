include $(TOP_SRCDIR)/packages/autotools.mk
include config.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/ltmain-sysroot.patch
	#cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/out-of-tree.patch
	cd $(srcdir) && autoreconf --force --install
	touch $@

conf-args += \
	--with-sysroot=$(SYSROOT)

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

JOBS := 1
