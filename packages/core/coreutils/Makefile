include $(TOP_SRCDIR)/packages/common.mk
include config.mk

srcdir = $(CURDIR)/$(PACKAGE)-$(VERSION)
builddir = $(CURDIR)/obj-$(HOST)

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/dummy-man.patch
	touch $@

$(builddir):
	mkdir -p $@

$(builddir)/config.cache: $(srcdir)/stamp-patch | $(builddir)
	echo '# generated for $(HOST)' > $@
	echo 'ac_cv_func_canonicalize_file_name=yes' >> $@
	echo 'gl_cv_func_realpath_works=yes' >> $@

conf-args = \
	--config-cache \
	--host=$(HOST) \
	--prefix=$(PREFIX)

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)' \
	PERL=no

$(builddir)/stamp-configure: $(builddir)/config.cache
	cd $(builddir) && \
		$(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	ALL_MANS= \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(MAKE) $(install-args) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
