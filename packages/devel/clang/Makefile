include $(TOP_SRCDIR)/packages/cmake.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

cmake-args += \
	-DLLVM_CONFIG=$(BUILD_TOOLS)/bin/$(HOST)-llvm-config \
	-DLLVM_TABLEGEN_EXE=$(BUILD_TOOLS)/bin/llvm-tblgen \
	-DCLANG_TABLEGEN=$(BUILD_TOOLS)/bin/clang-tblgen \
	-DCMAKE_CROSSCOMPILING=True \
	-DCMAKE_BUILD_TYPE=Release
