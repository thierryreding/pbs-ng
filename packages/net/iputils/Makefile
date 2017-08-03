include $(TOP_SRCDIR)/packages/common.mk

TARGETS = ping arping

build-args = \
	CC='$(CROSS_COMPILE)gcc' \
	CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)' \
	TARGETS='$(TARGETS)'

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && $(MAKE) $(build-args)
	touch $@

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	install -d $(DESTDIR)$(PREFIX)/bin
	cd $(srcdir) && \
		install -t $(DESTDIR)$(PREFIX)/bin $(TARGETS)
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
