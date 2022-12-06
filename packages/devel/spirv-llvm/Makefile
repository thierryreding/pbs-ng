include $(TOP_SRCDIR)/packages/cmake.mk

$(srcdir)/stamp-patch: | $(srcdir)
	#cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/constant-function-pointer-intel.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

cmake-args += \
	-DLLVM_EXTERNAL_SPIRV_HEADERS_SOURCE_DIR=$(SYSROOT)$(PREFIX)/include/spirv \
	-DBUILD_SHARED_LIBS=ON \
	-DCMAKE_BUILD_TYPE=Debug \
	-DCMAKE_POSITION_INDEPENDENT_CODE=ON \
	-DCMAKE_SKIP_RPATH=ON \
	-Wno-dev
