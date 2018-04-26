include $(TOP_SRCDIR)/packages/common.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

$(builddir):
	mkdir -p $@

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--with-sysroot=$(SYSROOT)

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
