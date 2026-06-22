include $(TOP_SRCDIR)/packages/cmake.mk

srcdir := $(srcdir)/libclc

#
# Note that we override cmake-args here because we don't want to pull in any
# of the cross-compilation arguments at this point. This is because we don't
# actually compile any code in libclc but rather compile built-ins using the
# LLVM/clang compiler infrastructure.
#
cmake-args = \
	-DLLVM_CONFIG=$(BUILD_TOOLS)/bin/llvm-config \
	-DCMAKE_INSTALL_PREFIX=$(PREFIX) \
	-DCMAKE_BUILD_TYPE=Release
