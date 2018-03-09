include $(TOP_SRCDIR)/packages/cmake.mk

cmake-args += \
	-DLLVM_CONFIG=$(BUILD_TOOLS)/bin/$(HOST)-llvm-config \
	-DCLANG_TABLEGEN=$(BUILD_TOOLS)/bin/clang-tblgen \
	-DCMAKE_CROSSCOMPILING=True \
	-DCMAKE_BUILD_TYPE=Release
