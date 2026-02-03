include $(TOP_SRCDIR)/packages/cmake.mk
include $(TOP_OBJDIR)/packages/devel/python/export.mk

cmake-args += \
	-DPython_INCLUDE_DIR=$(BUILD_TOOLS)/include/python$(PYTHON_MAJOR).$(PYTHON_MINOR) \
	-DPython_EXECUTABLE=FILEPATH:$(BUILD_TOOLS)/bin/python \
	-Dpystring_ROOT=$(SYSROOT)$(PREFIX) \
	-Dexpat_ROOT=$(SYSROOT)$(PREFIX)
