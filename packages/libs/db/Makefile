include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

conf-env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

conf-args = \
	--build=$(BUILD) \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--mandir=$(PREFIX)/share/man \
	--infodir=$(PREFIX)/share/info \
	--localstatedir=/var \
	--sysconfdir=/etc

conf-args += \
	--enable-compat185 \
	--enable-shared \
	--enable-static \
	--enable-dbm

conf-vars = \
	CPPFLAGS='$(CPPFLAGS)' \
	CXXFLAGS='$(CXXFLAGS)' \
	CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)' \
	db_cv_atomic=yes

$(builddir)/stamp-configure: | $(builddir)
	cd $(builddir) && \
		$(conf-env) $(srcdir)/dist/configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(env) $(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(FAKEROOT) $(MAKE) $(install-args) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
