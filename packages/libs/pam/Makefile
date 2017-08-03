include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

conf-env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--with-sysroot='$(SYSROOT)' \
	--disable-regenerate-docu \
	--disable-rpath \
	--disable-db

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(builddir)/stamp-configure: | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	cd $(builddir) && \
		$(conf-env) $(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(MAKE) -j $(JOBS)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)' \
	-j $(JOBS)

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(MAKE) $(install-args) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
