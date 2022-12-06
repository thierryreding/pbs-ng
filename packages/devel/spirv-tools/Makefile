include $(TOP_SRCDIR)/packages/cmake.mk

#$(srcdir)/stamp-patch: | $(srcdir)
#	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/build-fix.patch
#	touch $@
#
#$(builddir)/stamp-configure: $(srcdir)/stamp-patch

cmake-args += \
	-DSPIRV-Headers_SOURCE_DIR="$(SYSROOT)$(PREFIX)"
