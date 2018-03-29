include $(TOP_SRCDIR)/packages/meson.mk

ifneq ($(package.option.kms),y)
  conf-args += -Dlibkms=false
else
  conf-args += -Dlibkms=true
endif

ifneq ($(package.option.intel),y)
  conf-args += -Dintel=false
else
  conf-args += -Dintel=true
endif

ifneq ($(package.option.radeon),y)
  conf-args += -Dradeon=false
else
  conf-args += -Dradeon=true
endif

ifneq ($(package.option.amdgpu),y)
  conf-args += -Damdgpu=false
else
  conf-args += -Damdgpu=true
endif

ifneq ($(package.option.nouveau),y)
  conf-args += -Dnouveau=false
else
  conf-args += -Dnouveau=true
endif

ifneq ($(package.option.vmwgfx),y)
  conf-args += -Dvmwgfx=false
else
  conf-args += -Dvmwgfx=true
endif

ifneq ($(package.option.omap),y)
  conf-args += -Domap=false
else
  conf-args += -Domap=true
endif

ifneq ($(package.option.exynos),y)
  conf-args += -Dexynos=false
else
  conf-args += -Dexynos=true
endif

ifneq ($(package.option.freedreno),y)
  conf-args += -Dfreedreno=false
else
  conf-args += -Dfreedreno=true
endif

ifneq ($(package.option.tegra),y)
  conf-args += -Dtegra=false
else
  conf-args += -Dtegra=true
endif

ifneq ($(package.option.vc4),y)
  conf-args += -Dvc4=false
else
  conf-args += -Dvc4=true
endif

ifneq ($(package.option.etnaviv),y)
  conf-args += -Detnaviv=false
else
  conf-args += -Detnaviv=true
endif

conf-args += \
	-Dinstall-test-programs=true \
	-Dvalgrind=false
