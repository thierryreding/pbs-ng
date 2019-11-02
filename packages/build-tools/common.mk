include config.mk

BUILD_TOOLS = $(TOP_OBJDIR)/build-tools
SYSROOT = $(TOP_OBJDIR)/sysroot

ACLOCAL_PATH := $(BUILD_TOOLS)/share/aclocal
LD_RUN_PATH := $(BUILD_TOOLS)/lib:$(LD_RUN_PATH)
PATH := $(BUILD_TOOLS)/bin:$(PATH)

PKG_CONFIG_LIBDIR := $(BUILD_TOOLS)/lib/pkgconfig

builddir = $(CURDIR)/obj-native
srcdir = $(CURDIR)/source

JOBS ?= $(NUM_CPUS)

export ACLOCAL_PATH LD_RUN_PATH PKG_CONFIG_LIBDIR
