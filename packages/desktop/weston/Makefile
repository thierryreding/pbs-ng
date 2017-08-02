include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

$(builddir)/stamp-patch: | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(builddir)/stamp-patch

conf-env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--libexecdir=$(PREFIX)/lib/weston \
	--with-sysroot=$(SYSROOT) \
	--enable-clients \
	--enable-demo-clients-install

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(builddir)/stamp-configure: | $(builddir)
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
