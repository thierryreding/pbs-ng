include $(TOP_SRCDIR)/packages/common.mk

# we need to override PKGDIR when calling the glew's make because it will
# otherwise try to reuse the PBS' PKGDIR variable to point at the target
# directory for pkg-config files

build-args = \
	SYSTEM='linux' \
	M_ARCH='$(ARCH)' \
	CC='$(CROSS_COMPILE)gcc' \
	CFLAGS.EXTRA='$(CFLAGS)' \
	CFLAGS.SO='-fPIC' \
	LD='$(CROSS_COMPILE)gcc' \
	LDFLAGS.EXTRA='$(LDFLAGS)' \
	PKGDIR='$(DESTDIR)$(PREFIX)/lib/pkgconfig' \
	STRIP=''

$(srcdir)/stamp-build:
	cd $(srcdir) && \
		$(env) $(MAKE) $(build-args)
	touch $@

install-args = \
	SYSTEM='linux' \
	M_ARCH='$(ARCH)' \
	PKGDIR='$(DESTDIR)$(PREFIX)/lib/pkgconfig' \
	GLEW_DEST='$(DESTDIR)$(PREFIX)'

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		$(FAKEROOT) $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
