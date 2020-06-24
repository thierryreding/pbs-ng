include $(TOP_SRCDIR)/packages/build-tools/cmake.mk

srcdir := $(srcdir)/llvm

cmake-args += \
	-DLLVM_ENABLE_PROJECTS='clang;libcxx;libcxxabi' \
	-DLLVM_BUILD_LLVM_DYLIB=ON \
	-DLLVM_LINK_LLVM_DYLIB=ON \
	-DCMAKE_BUILD_TYPE=Release

$(BUILD_TOOLS)/bin/clang-tblgen: $(builddir)/bin/clang-tblgen
	cp $< $@

$(builddir)/stamp-install: $(BUILD_TOOLS)/bin/clang-tblgen
