include $(TOP_SRCDIR)/packages/common.mk

MAJOR = $(word 1,$(subst ., ,$(package.version)))

$(builddir):
	mkdir -p $@

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

$(builddir)/config.cache: | $(builddir)
	echo '# generated for $(HOST)' > $@
	echo 'ac_cv_buggy_getaddrinfo=no' >> $@
	echo 'ac_cv_file__dev_ptmx=yes' >> $@
	echo 'ac_cv_file__dev_ptc=no' >> $@

conf-args = \
	--config-cache \
	--build=$(BUILD) \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--sysconfdir=/etc

conf-args += \
	--without-ensurepip \
	--with-system-expat \
	--with-system-ffi

conf-vars = \
	CPPFLAGS='$(CPPFLAGS)' \
	CFLAGS='$(CFLAGS)' \
	CXXFLAGS='$(CXXFLAGS)' \
	LDFLAGS='$(LDFLAGS)'

$(builddir)/stamp-configure: $(srcdir)/stamp-patch $(builddir)/config.cache | $(builddir)
	cd $(builddir) && \
		$(conf-env) $(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	EXTRA_CFLAGS='$(CFLAGS)' \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(MAKE) $(build-args)
	touch $@

install-args = \
	EXTRA_CFLAGS='$(CFLAGS)' \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(MAKE) $(install-args) install
	ln -sf python$(MAJOR) $(DESTDIR)$(PREFIX)/bin/python
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
