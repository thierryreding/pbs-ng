include $(TOP_SRCDIR)/packages/cmake.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/buildfix.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/gcc-13.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

cmake-args += \
	-DBUILD_RECORDER=0 \
	-DUSE_FRIBIDI=0 \
	-DUSE_WIIUSE=0
