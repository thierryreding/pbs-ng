include $(TOP_SRCDIR)/packages/cmake.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/pcre.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

cmake-args += \
	-DUSE_SHARED=ON
