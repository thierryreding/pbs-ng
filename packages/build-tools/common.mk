include config.mk

BUILD_TOOLS = $(TOP_OBJDIR)/build-tools
SYSROOT = $(TOP_OBJDIR)/sysroot
#
# Note that this is the prefix on the host, in case we ever need it during
# the build process of build tools. BUILD_TOOLS is the correct prefix to use
# on the build system.
#
PREFIX = /usr

ACLOCAL_PATH := $(BUILD_TOOLS)/share/aclocal
LD_RUN_PATH := $(BUILD_TOOLS)/lib:$(LD_RUN_PATH)
LD_LIBRARY_PATH := $(BUILD_TOOLS)/lib
PATH := $(BUILD_TOOLS)/bin:$(PATH)

PKG_CONFIG_LIBDIR := $(BUILD_TOOLS)/lib/pkgconfig

builddir = $(CURDIR)/obj-native
srcdir = $(CURDIR)/source

JOBS ?= $(NUM_CPUS)

export ACLOCAL_PATH LD_RUN_PATH LD_LIBRARY_PATH PKG_CONFIG_LIBDIR
