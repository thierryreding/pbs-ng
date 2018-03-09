include $(TOP_SRCDIR)/packages/cmake.mk

TARGET = $(ARCH)

ifeq ($(ARCH),arm64)
  TARGET = AArch64
endif

ifeq ($(ARCH),arm)
  TARGET = ARM
endif

cmake-args += \
	-DLLVM_TABLEGEN=$(BUILD_TOOLS)/bin/llvm-tblgen \
	-DLLVM_DEFAULT_TARGET_TRIPLE=$(HOST) \
	-DLLVM_TARGETS_TO_BUILD=$(TARGET) \
	-DLLVM_TARGET_ARCH=$(TARGET) \
	-DLLVM_BUILD_LLVM_DYLIB=ON \
	-DLLVM_LINK_LLVM_DYLIB=ON \
	-DLLVM_ENABLE_RTTI=ON \
	-DCMAKE_CROSSCOMPILING=True \
	-DCMAKE_BUILD_TYPE=Release

$(BUILD_TOOLS)/bin/$(HOST)-llvm-config: $(TOP_SRCDIR)/$(PKGDIR)/llvm-config.in
	$(SED) 's|@SYSROOT@|$(SYSROOT)|;s|@PREFIX@|$(PREFIX)|;s|@VERSION@|$(package.version)|;s|@SOURCE_ROOT@|$(srcdir)|' $< > $@
	chmod a+x $@

$(builddir)/stamp-install: $(BUILD_TOOLS)/bin/$(HOST)-llvm-config
