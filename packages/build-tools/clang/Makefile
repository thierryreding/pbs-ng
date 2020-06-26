include $(TOP_SRCDIR)/packages/build-tools/cmake.mk

srcdir := $(srcdir)/clang

cmake-args += \
	-DCMAKE_BUILD_TYPE=Release

$(BUILD_TOOLS)/bin/clang-tblgen: $(builddir)/bin/clang-tblgen
	cp $< $@

$(builddir)/stamp-install: $(BUILD_TOOLS)/bin/clang-tblgen
