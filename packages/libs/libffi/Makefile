include $(TOP_SRCDIR)/packages/common.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/remove-libtool-ldflags.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/libdir.patch
	touch $@

$(builddir):
	mkdir -p $@

conf-env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--libexecdir=$(PREFIX)/lib \
	--with-sysroot=$(SYSROOT)

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(builddir)/stamp-configure: $(srcdir)/stamp-patch | $(builddir)
	cd $(srcdir) && autoreconf
	cd $(builddir) && \
		$(conf-env) $(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		fakeroot $(MAKE) $(install-args) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
