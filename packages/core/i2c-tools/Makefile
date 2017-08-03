include $(TOP_SRCDIR)/packages/common.mk

common-args = \
	prefix='$(PREFIX)' \
	sbindir='$$(prefix)/bin'

build-args = \
	CC='$(CROSS_COMPILE)gcc' \
	CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)' \
	$(common-args)

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && $(MAKE) -j $(JOBS) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)' \
	$(common-args)

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
