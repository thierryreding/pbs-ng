include config.mk

DESTDIR = $(TOP_OBJDIR)/$(PKGDIR)/install
BUILD_TOOLS = $(TOP_OBJDIR)/build-tools
SYSROOT = $(TOP_OBJDIR)/sysroot
PREFIX = /usr

ACLOCAL_PATH := $(BUILD_TOOLS)/share/aclocal:$(SYSROOT)$(PREFIX)/share/aclocal
PATH := $(BUILD_TOOLS)/bin:$(PATH)

PKG_CONFIG_LIBDIR := $(SYSROOT)$(PREFIX)/lib/pkgconfig
PKG_CONFIG_SYSROOT_DIR := $(SYSROOT)

CROSS_COMPILE = $(HOST)-

builddir = $(CURDIR)/obj-$(HOST)
srcdir = $(CURDIR)/source

JOBS ?= $(NUM_CPUS)

CPPFLAGS += --sysroot $(SYSROOT)
CFLAGS += --sysroot $(SYSROOT)
CXXFLAGS += --sysroot $(SYSROOT)
LDFLAGS += --sysroot $(SYSROOT)

export ACLOCAL_PATH PKG_CONFIG_LIBDIR PKG_CONFIG_SYSROOT_DIR
