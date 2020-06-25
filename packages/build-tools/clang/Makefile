include $(TOP_SRCDIR)/packages/build-tools/cmake.mk

cmake-args += \
	-DCMAKE_BUILD_TYPE=Release

$(BUILD_TOOLS)/bin/clang-tblgen: $(builddir)/bin/clang-tblgen
	cp $< $@

$(builddir)/stamp-install: $(BUILD_TOOLS)/bin/clang-tblgen
