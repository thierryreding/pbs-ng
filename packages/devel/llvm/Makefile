include $(TOP_SRCDIR)/packages/cmake.mk

srcdir := $(srcdir)/llvm

TARGET = $(ARCH)

ifeq ($(ARCH),arm64)
  TARGET = AArch64
endif

ifeq ($(ARCH),arm)
  TARGET = ARM
endif

# will exhaust memory and get OOM-killed if run too many parallel jobs
JOBS := 8

cmake-args += \
	-DLLVM_CONFIG_PATH=$(BUILD_TOOLS)/bin/llvm-config \
	-DLLVM_TABLEGEN=$(BUILD_TOOLS)/bin/llvm-tblgen \
	-DLLVM_DEFAULT_TARGET_TRIPLE=$(HOST) \
	-DLLVM_TARGETS_TO_BUILD=$(TARGET) \
	-DLLVM_TARGET_ARCH=$(TARGET) \
	-DLLVM_BUILD_LLVM_DYLIB=ON \
	-DLLVM_LINK_LLVM_DYLIB=ON \
	-DLLVM_ENABLE_RTTI=ON \
	-DCMAKE_CROSSCOMPILING=True \
	-DCMAKE_BUILD_TYPE=Release
