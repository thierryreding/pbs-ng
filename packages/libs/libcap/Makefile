include $(TOP_SRCDIR)/packages/common.mk
include config.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

$(builddir):
	mkdir -p $@

build-args = \
	prefix=$(PREFIX) \
	lib=lib \
	BUILD_CC='gcc' \
	CC='$(CROSS_COMPILE)gcc' \
	EXTRA_CFLAGS='--sysroot $(SYSROOT)' \
	EXTRA_LDFLAGS='--sysroot $(SYSROOT)' \
	RAISE_SETFCAP=no \
	PAM_CAP=no

$(builddir)/stamp-build: $(srcdir)/stamp-patch | $(builddir)
	cd $(srcdir) && \
		$(MAKE) $(build-args)

install-args = \
	prefix=$(PREFIX) \
	lib=lib \
	DESTDIR='$(DESTDIR)' \
	RAISE_SETFCAP=no \
	PAM_CAP=no

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(srcdir) && \
		$(MAKE) $(install-args) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
