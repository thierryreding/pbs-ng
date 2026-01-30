# out-of-tree builds don't work currently
builddir = $(srcdir)

include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

$(srcdir)/stamp-configure: $(srcdir)/stamp-patch

conf-env += \
	CC=$(CROSS_COMPILE)gcc \
	PLATFORM=$(ARCH) \
	COMPILER=gcc
