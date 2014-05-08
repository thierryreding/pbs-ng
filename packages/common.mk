include config.mk

DESTDIR = $(TOP_OBJDIR)/$(PKGDIR)/install
BUILD_TOOLS = $(TOP_OBJDIR)/build-tools
SYSROOT = $(TOP_OBJDIR)/sysroot
PREFIX = /usr

PATH := $(BUILD_TOOLS)/bin:$(PATH)

CROSS_COMPILE = $(HOST)-

builddir = $(CURDIR)/obj-$(HOST)
srcdir = $(CURDIR)/source

JOBS ?= $(NUM_CPUS)

CPPFLAGS += --sysroot=$(SYSROOT)
CFLAGS += --sysroot=$(SYSROOT)
LDFLAGS += --sysroot=$(SYSROOT)
