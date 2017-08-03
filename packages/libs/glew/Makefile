include $(TOP_SRCDIR)/packages/common.mk

build-args = \
	SYSTEM='linux' \
	M_ARCH='$(ARCH)' \
	CC='$(CROSS_COMPILE)gcc' \
	CFLAGS.EXTRA='$(CFLAGS)' \
	CFLAGS.SO='-fPIC' \
	LD='$(CROSS_COMPILE)gcc' \
	LDFLAGS.EXTRA='$(LDFLAGS)' \
	STRIP=''

$(srcdir)/stamp-build:
	cd $(srcdir) && \
		$(env) $(MAKE) $(build-args)
	touch $@

install-args = \
	SYSTEM='linux' \
	M_ARCH='$(ARCH)' \
	GLEW_DEST='$(DESTDIR)$(PREFIX)'

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		$(FAKEROOT) $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
