include $(TOP_SRCDIR)/packages/common.mk
include config.mk

srcdir = $(CURDIR)/Mesa-$(VERSION)
builddir = $(CURDIR)/obj-$(HOST)

$(srcdir)/stamp-patch:
	cd $(srcdir) && PATH=/home/thierry.reding/src/pbs.git/build/venice2/rootfs/build-tools/bin:$$PATH autoreconf --force --install
	#cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/ltmain-sysroot.patch
	touch $@

$(builddir):
	mkdir -p $@

conf-env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--sysconfdir=/etc \
	--with-sysroot=$(SYSROOT) \
	--without-dri-drivers \
	--with-gallium-drivers=swrast \
	--with-egl-platforms=x11,wayland,drm \
	--enable-gallium-egl \
	--enable-gallium-gbm \
	--enable-gles1 \
	--enable-gles2 \
	--enable-gbm

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(builddir)/stamp-configure: $(srcdir)/stamp-patch | $(builddir)
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
