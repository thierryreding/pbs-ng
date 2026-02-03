include config.mk

empty :=
comma := ,
space := $(empty) $(empty)

DESTDIR = $(TOP_OBJDIR)/$(PKGDIR)/install
BUILD_TOOLS = $(TOP_OBJDIR)/build-tools
SYSROOT = $(TOP_OBJDIR)/sysroot
PREFIX = /usr

ACLOCAL_PATH := $(BUILD_TOOLS)/share/aclocal:$(SYSROOT)$(PREFIX)/share/aclocal
LD_LIBRARY_PATH := $(BUILD_TOOLS)/lib
PATH := $(BUILD_TOOLS)/bin:$(PATH)

PKG_CONFIG_LIBDIR := $(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig
PKG_CONFIG_SYSROOT_DIR := $(SYSROOT)

CROSS_COMPILE = $(HOST)-

builddir ?= $(CURDIR)/obj-$(HOST)
srcdir = $(CURDIR)/source

JOBS ?= $(NUM_CPUS)

ASFLAGS = $(ARCH_ASFLAGS)
CPPFLAGS = $(ARCH_CPPFLAGS) --sysroot=$(SYSROOT)
CFLAGS += $(ARCH_CFLAGS) --sysroot=$(SYSROOT)
CXXFLAGS += $(ARCH_CXXFLAGS) --sysroot=$(SYSROOT)
LDFLAGS += $(ARCH_LDFLAGS) --sysroot=$(SYSROOT)

export ACLOCAL_PATH LD_LIBRARY_PATH PKG_CONFIG_LIBDIR PKG_CONFIG_SYSROOT_DIR
