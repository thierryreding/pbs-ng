include $(TOP_SRCDIR)/packages/common.mk
include config.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/no-rpath.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/extra-cflags.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/engines-path.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/fix-pod-syntax.patch
	touch $@

conf-args = \
	--cross-compile-prefix=$(HOST)- \
	--prefix=$(PREFIX) \
	--openssldir=/etc/ssl \
	shared zlib-dynamic \
	linux-generic32

$(srcdir)/stamp-configure: $(srcdir)/stamp-patch
	cd $(srcdir) && \
		$(conf-env) ./Configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	EXTRA_CPPFLAGS='--sysroot $(SYSROOT)' \
	EXTRA_CFLAGS='--sysroot $(SYSROOT)'

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && \
		$(MAKE) $(build-args)
	touch $@

install-args = \
	EXTRA_CPPFLAGS='--sysroot $(SYSROOT)' \
	EXTRA_CFLAGS='--sysroot $(SYSROOT)' \
	MANDIR=$(PREFIX)/share/man \
	MANSUFFIX=ssl \
	INSTALL_PREFIX='$(DESTDIR)'

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		fakeroot $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
