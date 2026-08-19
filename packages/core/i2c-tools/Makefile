# not a proper out-of-tree build,
builddir = $(srcdir)

include $(TOP_SRCDIR)/packages/common.mk

common-args = \
	PREFIX='$(PREFIX)'

build-args = \
	CC='$(CROSS_COMPILE)gcc' \
	CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)' \
	$(common-args)

$(srcdir)/stamp-build:
	cd $(srcdir) && $(MAKE) -j $(JOBS) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)' \
	$(common-args)

$(srcdir)/stamp-install:
	cd $(srcdir) && $(MAKE) $(install-args) install
	touch $@
