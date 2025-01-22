include $(TOP_SRCDIR)/packages/cmake.mk

srcdir := $(srcdir)/clang

# will exhaust memory and get OOM-killed if run too many parallel jobs
JOBS := 8

cmake-args += \
	-DLLVM_TABLEGEN_EXE=$(BUILD_TOOLS)/bin/llvm-tblgen \
	-DCLANG_TABLEGEN=$(BUILD_TOOLS)/bin/clang-tblgen \
	-DCMAKE_CROSSCOMPILING=True \
	-DCMAKE_BUILD_TYPE=Release \
	-DLLVM_INCLUDE_TESTS=OFF
