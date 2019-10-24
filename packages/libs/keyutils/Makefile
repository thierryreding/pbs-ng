include $(TOP_SRCDIR)/packages/common.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/symlinks.patch
	touch $@

build-args = \
	CC='$(CROSS_COMPILE)gcc' \
	CFLAGS='$(CFLAGS) -Wall -Werror' \
	LDFLAGS='$(LDFLAGS)' \
	USRLIBDIR='$(PREFIX)/lib' \
	SBINDIR='$(PREFIX)/sbin' \
	BINDIR='$(PREFIX)/bin' \
	LIBDIR='$(PREFIX)/lib' \
	-j $(JOBS)

$(srcdir)/stamp-build: $(srcdir)/stamp-patch
	cd $(srcdir) && \
		$(MAKE) $(build-args)
	touch $@

install-args = \
	USRLIBDIR='$(PREFIX)/lib' \
	SBINDIR='$(PREFIX)/sbin' \
	BINDIR='$(PREFIX)/bin' \
	LIBDIR='$(PREFIX)/lib' \
	DESTDIR='$(DESTDIR)'

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		fakeroot $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
