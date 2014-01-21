include $(TOP_SRCDIR)/packages/common.mk
include config.mk

srcdir = $(CURDIR)/$(PACKAGE)-$(VERSION)
builddir = $(CURDIR)/obj-$(HOST)

soname = $(basename $(basename $(1)))
CC = $(CROSS_COMPILE)gcc
AWK = awk

VERSION = $(shell $(CC) -dumpversion)

$(builddir):
	mkdir -p $@

srcdir = $(dir $(realpath $(shell $(CC) -print-file-name=libgcc_s.so)))
sysroot = $(shell $(CC) -print-sysroot)

libgcc = $(abspath $(shell $(CC) -print-file-name=libgcc_s.so))
libgcc-static = $(shell $(CC) -print-file-name=libgcc.a)
libgcc-target = $(realpath $(libgcc))

ifeq ($(libgcc),$(libgcc-target))
  libgcc-soname = $(shell $(AWK) '/GROUP/ { print $$3 }' $(libgcc))
else
  libgcc-soname = $(notdir $(libgcc-target))
endif

libssp = $(realpath $(shell $(CC) -print-file-name=libssp.so))
libssp-soname = $(notdir $(call soname,$(libssp)))

libstdcxx = $(realpath $(shell $(CC) -print-file-name=libstdc++.so))
libstdcxx-soname = $(notdir $(call soname,$(libstdcxx)))

$(DESTDIR)$(PREFIX)/lib:
	install -d $@ -m 755

$(builddir)/stamp-install: $(DESTDIR)$(PREFIX)/lib | $(builddir)
	# libgcc
	cp -dp $(srcdir)$(libgcc-soname) $(DESTDIR)$(PREFIX)/lib
	cp -dp $(libgcc) $(DESTDIR)$(PREFIX)/lib
	cp -dp $(libgcc-static) $(DESTDIR)$(PREFIX)/lib
	# libssp
	if test -f "$(libssp)"; then \
		cp -dp $(libssp) $(DESTDIR)$(PREFIX)/lib; \
		cp -dp $(srcdir)$(libssp-soname) $(DESTDIR)$(PREFIX)/lib; \
		cp -dp $(srcdir)libssp.so $(DESTDIR)$(PREFIX)/lib; \
		cp -dp $(srcdir)libssp.a $(DESTDIR)$(PREFIX)/lib; \
	fi
	# libstdc++
	cp -dp $(libstdcxx) $(DESTDIR)$(PREFIX)/lib
	cp -dp $(srcdir)$(libstdcxx-soname) $(DESTDIR)$(PREFIX)/lib
	cp -dp $(srcdir)libstdc++.so $(DESTDIR)$(PREFIX)/lib
	cp -dp $(srcdir)libstdc++.a $(DESTDIR)$(PREFIX)/lib

install: $(builddir)/stamp-install

.PHONY: install
