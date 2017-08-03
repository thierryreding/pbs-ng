include $(TOP_SRCDIR)/packages/common.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/xdr-sizeof.patch
	touch $@

$(builddir):
	mkdir -p $@

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--sysconfdir=/etc \
	--disable-gssapi

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(builddir)/stamp-configure: $(srcdir)/stamp-patch | $(builddir)
	cd $(builddir) && \
		$(srcdir)/configure $(conf-args) $(conf-vars)
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
