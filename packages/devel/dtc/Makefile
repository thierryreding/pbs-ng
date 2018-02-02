include $(TOP_SRCDIR)/packages/common.mk

build-args = \
	CC='$(CROSS_COMPILE)gcc' \
	EXTRA_CPPFLAGS='$(CPPFLAGS)' \
	EXTRA_CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)' \
	NO_PYTHON=1 \
	-j $(JOBS)

$(srcdir)/stamp-build:
	cd $(srcdir) && $(env) $(MAKE) $(build-args)

install-args = \
	NO_PYTHON=1 \
	DESTDIR=$(DESTDIR) \
	PREFIX=/usr

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && $(env) $(MAKE) $(install-args) install

install: $(srcdir)/stamp-install

.PHONY: install
