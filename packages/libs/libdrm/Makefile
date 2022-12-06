include $(TOP_SRCDIR)/packages/meson.mk

ifneq ($(package.option.intel),y)
  conf-args += -Dintel=disabled
else
  conf-args += -Dintel=enabled
endif

ifneq ($(package.option.radeon),y)
  conf-args += -Dradeon=disabled
else
  conf-args += -Dradeon=enabled
endif

ifneq ($(package.option.amdgpu),y)
  conf-args += -Damdgpu=disabled
else
  conf-args += -Damdgpu=enabled
endif

ifneq ($(package.option.nouveau),y)
  conf-args += -Dnouveau=disabled
else
  conf-args += -Dnouveau=enabled
endif

ifneq ($(package.option.vmwgfx),y)
  conf-args += -Dvmwgfx=disabled
else
  conf-args += -Dvmwgfx=enabled
endif

ifneq ($(package.option.omap),y)
  conf-args += -Domap=disabled
else
  conf-args += -Domap=enabled
endif

ifneq ($(package.option.exynos),y)
  conf-args += -Dexynos=disabled
else
  conf-args += -Dexynos=enabled
endif

ifneq ($(package.option.freedreno),y)
  conf-args += -Dfreedreno=disabled
else
  conf-args += -Dfreedreno=enabled
endif

ifneq ($(package.option.tegra),y)
  conf-args += -Dtegra=disabled
else
  conf-args += -Dtegra=enabled
endif

ifneq ($(package.option.vc4),y)
  conf-args += -Dvc4=disabled
else
  conf-args += -Dvc4=enabled
endif

ifneq ($(package.option.etnaviv),y)
  conf-args += -Detnaviv=disabled
else
  conf-args += -Detnaviv=enabled
endif

conf-args += \
	-Dinstall-test-programs=true \
	-Dvalgrind=disabled
