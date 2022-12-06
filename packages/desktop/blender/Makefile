include $(TOP_SRCDIR)/packages/cmake.mk

PYTHON_VERSION = $(shell $(BUILD_TOOLS)/bin/python $(TOP_SRCDIR)/scripts/python-version.py)

$(srcdir)/stamp-patch: | $(srcdir)
	#cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

$(builddir)/build-tools: | $(builddir)
	mkdir $@

$(builddir)/stamp-host-tools: $(srcdir)/stamp-patch | $(builddir)/build-tools
	cd $(builddir)/build-tools && \
		cmake -DCMAKE_INSTALL_PREFIX=$(BUILD_TOOLS) \
			-DPYTHON_INCLUDE_DIRS=$(BUILD_TOOLS)/include/python$(PYTHON_VERSION) \
			-DPYTHON_LIBRARY=python$(PYTHON_VERSION) \
			-DPYTHON_LIBPATH=$(BUILD_TOOLS)/lib \
			-DPYTHON_VERSION=$(PYTHON_VERSION) \
			-DWITH_PYTHON_INSTALL=off \
			-DWITH_MOD_OCEANSIM=off \
			-DWITH_POTRACE=off \
			-DWITH_CYCLES_EMBREE=off \
			-DWITH_CYCLES=off \
			$(srcdir)
	cd $(builddir)/build-tools && \
		$(MAKE) -j $(JOBS) datatoc datatoc_icon makesdna makesrna msgfmt
	touch $@

env += \
	LD_LIBRARY_PATH=$(BUILD_TOOLS)/lib

$(builddir)/stamp-configure: $(builddir)/stamp-host-tools

#
# WITH_OPENCOLORID currently breaks the build for unknown reasons
# WITH_DOC_MANPAGE needs a native blender binary to generate
#
cmake-args += \
	-C$(srcdir)/build_files/cmake/config/blender_release.cmake \
	-DDATATOC_PATH=$(builddir)/build-tools/bin/datatoc \
	-DDATATOC_ICON_PATH=$(builddir)/build-tools/bin/datatoc_icon \
	-DMAKESDNA_PATH=$(builddir)/build-tools/bin/makesdna \
	-DMAKESRNA_PATH=$(builddir)/build-tools/bin/makesrna \
	-DMSGFMT_PATH=$(builddir)/build-tools/bin/msgfmt \
	-DPYTHON_INCLUDE_DIRS=$(SYSROOT)$(PREFIX)/include/python$(PYTHON_VERSION) \
	-DPYTHON_LIBRARY=python$(PYTHON_VERSION) \
	-DPYTHON_LIBPATH=$(SYSROOT)$(PREFIX)/lib \
	-DPYTHON_VERSION=$(PYTHON_VERSION) \
	-DOPENSUBDIV_ROOT_DIR=$(SYSROOT)$(PREFIX) \
	-DWITH_INSTALL_PORTABLE=OFF \
	-DWITH_PYTHON_INSTALL=OFF \
	-DWITH_OPENCOLORIO=OFF \
	-DWITH_DOC_MANPAGE=OFF \
	-DWITH_SYSTEM_GLEW=ON

ifneq ($(ARCH),x86)
cmake-args += \
	-DWITH_CYCLES_EMBREE=off
endif
