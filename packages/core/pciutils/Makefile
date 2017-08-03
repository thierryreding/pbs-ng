include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

build-args = \
	CROSS_COMPILE='$(CROSS_COMPILE)' \
	IDSDIR='$(PREFIX)/share/hwdata' \
	EXTRA_CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)' \
	PREFIX='$(PREFIX)' \
	HOST='$(HOST)' \
	SHARED=yes \
	ZLIB=yes \
	DNS=no

$(builddir)/stamp-build: $(srcdir)/stamp-patch | $(builddir)
	cd $(srcdir) && $(MAKE) $(build-args)
	touch $@

install-args = \
	IDSDIR='$(PREFIX)/share/hwdata' \
	MANDIR='$(PREFIX)/share/man' \
	SBINDIR='$(PREFIX)/bin' \
	DESTDIR='$(DESTDIR)' \
	PREFIX='$(PREFIX)' \
	SHARED=yes

install-targets = \
	install-lib \
	install

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(srcdir) && $(MAKE) $(install-args) $(install-targets)
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
