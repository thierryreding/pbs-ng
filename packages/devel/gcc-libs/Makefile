include $(TOP_SRCDIR)/packages/common.mk

CC = $(shell env -i PATH=$(PATH) which $(CROSS_COMPILE)gcc)
soname = $(basename $(basename $(1)))
AWK = awk

VERSION = $(shell $(CC) -dumpversion)

$(builddir):
	mkdir -p $@

srcdir = $(dir $(realpath $(shell $(CC) -print-file-name=libgcc_s.so)))
sysroot = $(shell $(CC) -print-sysroot)

libgcc = $(abspath $(shell $(CC) -print-file-name=libgcc_s.so))
libgcc-static = $(shell $(CC) -print-file-name=libgcc.a)
libgcc-target = $(realpath $(libgcc))

libatomic = $(abspath $(shell $(CC) -print-file-name=libatomic.so))
libatomic-static = $(shell $(CC) -print-file-name=libatomic.a)
libatomic-target = $(realpath $(libatomic))
libatomic-soname = $(call soname,$(libatomic-target))

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
	# libatomic
	cp -dp $(libatomic) $(DESTDIR)$(PREFIX)/lib
	cp -dp $(libatomic-target) $(DESTDIR)$(PREFIX)/lib
	cp -dp $(libatomic-soname) $(DESTDIR)$(PREFIX)/lib
	cp -dp $(libatomic-static) $(DESTDIR)$(PREFIX)/lib

install: $(builddir)/stamp-install

version:
	@$(CC) -dumpversion

.PHONY: install
