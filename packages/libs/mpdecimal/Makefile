include $(TOP_SRCDIR)/packages/common.mk

env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

conf-args = \
	--build=$(BUILD) \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--with-sysroot=$(SYSROOT)

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(srcdir)/stamp-configure: | $(srcdir)
	cd $(srcdir) && \
		$(env) ./configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && \
		$(env) $(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)'

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		fakeroot $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
