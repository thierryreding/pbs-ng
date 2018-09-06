include $(TOP_SRCDIR)/packages/common.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

build-args = \
	CC='$(CROSS_COMPILE)gcc' \
	EXTRA_CFLAGS='$(CFLAGS)'

$(srcdir)/stamp-build: $(srcdir)/stamp-patch
	cd $(srcdir) && $(MAKE) $(build-args)
	touch $@

install-args = \
	prefix=$(DESTDIR)$(PREFIX)

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
