include $(TOP_SRCDIR)/packages/autotools.mk
include config.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/ltmain-sysroot.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

conf-args += \
	--with-sysroot=$(SYSROOT)
