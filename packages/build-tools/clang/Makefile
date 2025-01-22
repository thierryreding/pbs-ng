include $(TOP_SRCDIR)/packages/build-tools/cmake.mk

srcdir := $(srcdir)/clang

# will exhaust memory and get OOM-killed if run too many parallel jobs
JOBS := 8

cmake-args += \
	-DCMAKE_BUILD_TYPE=Release \
	-DLLVM_INCLUDE_TESTS=OFF

$(BUILD_TOOLS)/bin/clang-tblgen: $(builddir)/bin/clang-tblgen
	cp $< $@

$(builddir)/stamp-install: $(BUILD_TOOLS)/bin/clang-tblgen
