include $(TOP_SRCDIR)/packages/common.mk

ifeq ($(realpath $(srcdir)),$(srcdir))
$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/ltmain-sysroot.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
endif

$(builddir):
	mkdir -p $@

conf-env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--with-sysroot=$(SYSROOT)

ifneq ($(package.option.kms),y)
  conf-args += --disable-libkms
else
  conf-args += --enable-libkms
endif

ifneq ($(package.option.intel),y)
  conf-args += --disable-intel
else
  conf-args += --enable-intel
endif

ifneq ($(package.option.vmwgfx),y)
  conf-args += --disable-vmwgfx
else
  conf-args += --enable-vmwgfx
endif

ifneq ($(package.option.radeon),y)
  conf-args += --disable-radeon
else
  conf-args += --enable-radeon
endif

ifneq ($(package.option.nouveau),y)
  conf-args += --disable-nouveau
else
  conf-args += --enable-nouveau
endif

ifneq ($(package.option.omap),y)
  conf-args += --disable-omap-experimental-api
else
  conf-args += --enable-omap-experimental-api
endif

ifneq ($(package.option.exynos),y)
  conf-args += --disable-exynos-experimental-api
else
  conf-args += --enable-exynos-experimental-api
endif

ifneq ($(package.option.freedreno),y)
  conf-args += --disable-freedreno-experimental-api
else
  conf-args += --enable-freedreno-experimental-api
endif

ifneq ($(package.option.tegra),y)
  conf-args += --disable-tegra-experimental-api
else
  conf-args += --enable-tegra-experimental-api
endif

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

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
