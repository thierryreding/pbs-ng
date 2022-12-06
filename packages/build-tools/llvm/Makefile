include $(TOP_SRCDIR)/packages/build-tools/cmake.mk

srcdir := $(srcdir)/llvm

# will exhaust memory and get OOM-killed if run too many parallel jobs
JOBS := 8

cmake-args += \
	-DLLVM_BUILD_LLVM_DYLIB=ON \
	-DLLVM_LINK_LLVM_DYLIB=ON \
	-DCMAKE_BUILD_TYPE=Release
