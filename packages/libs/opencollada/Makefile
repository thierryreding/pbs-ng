include $(TOP_SRCDIR)/packages/cmake.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/pcre.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/gcc-13.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

cmake-args += \
	-DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
	-DUSE_SHARED=ON
