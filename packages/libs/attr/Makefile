include $(TOP_SRCDIR)/packages/common.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/ltmain-sysroot.patch
	touch $@

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX)

conf-vars = \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)' \
	INSTALL_GROUP=root \
	INSTALL_USER=root

$(srcdir)/stamp-configure: $(srcdir)/stamp-patch
	cd $(srcdir) && \
		$(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && \
		$(MAKE)

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		DIST_ROOT='$(DESTDIR)' $(MAKE) $(install-args) install install-lib install-dev
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
