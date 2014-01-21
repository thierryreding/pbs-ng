include $(TOP_SRCDIR)/packages/common.mk
include config.mk

srcdir = $(CURDIR)/$(PACKAGE)-$(VERSION)
builddir = $(CURDIR)/obj-$(HOST)

$(builddir):
	mkdir -p $@

conf-env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

conf-args = \
	--config-cache \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--disable-gcrypt \
	--disable-gudev

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(builddir)/config.cache: | $(builddir)
	echo '# generated for $(HOST)' > $@
	echo 'ac_cv_func_malloc_0_nonnull=yes' >> $@

$(builddir)/stamp-configure: $(builddir)/config.cache | $(builddir)
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
	-j $(JOBS)

install-vars = \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(MAKE) $(install-args) $(install-vars) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
