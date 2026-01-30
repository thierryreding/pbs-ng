include $(TOP_SRCDIR)/packages/cmake.mk
include $(TOP_SRCDIR)/packages/git.mk

cmake-args += \
	-DCL_OFFLINE_COMPILER=$(PREFIX)/bin/llvm-spirv \
	-DCL_LIBCLCXX_DIR=$(SYSROOT)$(PREFIX)/include \
	-DCL_INCLUDE_DIR=$(SYSROOT)$(PREFIX)/include \
	-DCL_LIB_DIR=$(SYSROOT)$(PREFIX)/lib \
	-DCL_CONFORM_LIBRARIES='-lOpenCL' \
	-DCMAKE_ARM_COMPILER=True
