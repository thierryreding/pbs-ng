include $(TOP_SRCDIR)/packages/autotools.mk

ifeq ($(realpath $(srcdir)),$(srcdir))
$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch | $(builddir)
else
$(builddir)/stamp-prepare: | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(builddir)/stamp-prepare
endif

conf-args += \
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
  conf-args += --disable-freedreno
else
  conf-args += --enable-freedreno
endif

ifneq ($(package.option.tegra),y)
  conf-args += --disable-tegra-experimental-api
else
  conf-args += --enable-tegra-experimental-api
endif

conf-args += \
	--enable-install-test-programs
