# not a proper out-of-tree build
builddir = $(srcdir)

include $(TOP_SRCDIR)/packages/common.mk

env += \
	CC='$(CROSS_COMPILE)gcc' \
	AR='$(CROSS_COMPILE)ar' \
	CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)'

$(srcdir)/stamp-configure: | $(srcdir)
	cd $(srcdir) && $(env) ./configure
	touch $@

build-args = \
	HOSTCC='gcc' \
	CBUILD_CFLAGS='-O2 -g' \
	DESTDIR='$(DESTDIR)' \
	PREFIX='$(PREFIX)' \
	SBINDIR='$(PREFIX)/bin' \
	-j $(JOBS)

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && $(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)' \
	PREFIX='$(PREFIX)' \
	SBINDIR='$(PREFIX)/bin'

$(srcdir)/stamp-install:
	cd $(srcdir) && $(MAKE) $(install-args) install
	touch $@
