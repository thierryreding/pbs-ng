include $(TOP_SRCDIR)/packages/common.mk
include config.mk

$(builddir):
	mkdir -p $@

conf-env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--with-sysroot=$(SYSROOT) \
	--disable-malloc0returnsnull

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)' \
	CPPFLAGS_FOR_BUILD='' \
	CFLAGS_FOR_BUILD='-O2 -g' \
	LDFLAGS_FOR_BUILD=''

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
