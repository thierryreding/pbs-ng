include $(TOP_SRCDIR)/packages/common.mk

build-args = \
	CC='$(CROSS_COMPILE)gcc' \
	CFLAGS='$(CFLAGS)' \
	STRIP='$(CROSS_COMPILE)strip' \
	-j $(JOBS)

$(srcdir)/stamp-build:
	cd $(srcdir) && \
		$(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)' \
	sbindir=$(PREFIX)/bin

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		fakeroot $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
