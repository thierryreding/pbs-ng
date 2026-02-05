include $(TOP_SRCDIR)/packages/common.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

build-args = \
	AR='$(CROSS_COMPILE)ar' \
	CC='$(CROSS_COMPILE)gcc' \
	EXTRA_CFLAGS='$(CFLAGS)' \
	-j $(JOBS)

$(srcdir)/stamp-build: $(srcdir)/stamp-patch
	cd $(srcdir) && $(MAKE) $(build-args)
	touch $@

install-args = \
	PREFIX=$(PREFIX) \
	DESTDIR=$(DESTDIR)

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && fakeroot $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
