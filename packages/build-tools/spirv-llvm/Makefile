include $(TOP_SRCDIR)/packages/build-tools/cmake.mk

#$(srcdir)/stamp-patch: | $(srcdir)
#	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/constant-function-pointer-intel.patch
#	touch $@

cmake-args += \
	-DLLVM_EXTERNAL_SPIRV_HEADERS_SOURCE_DIR=$(BUILD_TOOLS)/include/spirv

#$(builddir)/stamp-configure: $(srcdir)/stamp-patch

build-args += \
	all llvm-spirv

$(BUILD_TOOLS)/bin/llvm-spirv: | $(builddir)/stamp-build
	cp $(builddir)/tools/llvm-spirv/llvm-spirv $@

$(builddir)/stamp-install: $(BUILD_TOOLS)/bin/llvm-spirv
