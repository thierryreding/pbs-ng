include $(TOP_SRCDIR)/packages/meson.mk

env += CMAKE=$(BUILD_TOOLS)/bin/cmake

ifeq ($(ARCH),arm64)
  ARCH = aarch64
endif

ifneq ($(package.option.debug),y)
  conf-args += --buildtype release
else
  conf-args += --buildtype debug
endif

#
# SDL 2.0.10 fails to build against Mesa's GLES1 headers on 32-bit ARM. Since
# nothing really requires GLES1, let's just disable it.
#
conf-args += \
	-Dgles1=disabled

ifeq ($(package.option.gallium-drivers),y)
  gallium-drivers-$(package.option.gallium-drivers.pl111) += pl111
  gallium-drivers-$(package.option.gallium-drivers.radeonsi) += radeonsi
  gallium-drivers-$(package.option.gallium-drivers.r300) += r300
  gallium-drivers-$(package.option.gallium-drivers.r600) += r600
  gallium-drivers-$(package.option.gallium-drivers.nouveau) += nouveau
  gallium-drivers-$(package.option.gallium-drivers.freedreno) += freedreno
  gallium-drivers-$(package.option.gallium-drivers.swrast) += swrast
  gallium-drivers-$(package.option.gallium-drivers.vc4) += vc4
  gallium-drivers-$(package.option.gallium-drivers.vc5) += vc5
  gallium-drivers-$(package.option.gallium-drivers.etnaviv) += etnaviv
  gallium-drivers-$(package.option.gallium-drivers.imx) += imx
  gallium-drivers-$(package.option.gallium-drivers.tegra) += tegra
  gallium-drivers-$(package.option.gallium-drivers.i915) += i915
  gallium-drivers-$(package.option.gallium-drivers.svga) += svga
  gallium-drivers-$(package.option.gallium-drivers.virgl) += virgl
  gallium-drivers-$(package.option.gallium-drivers.swr) += swr

  gallium-drivers = $(subst $(empty) $(empty),$(comma),$(gallium-drivers-y))
  conf-args += -Dgallium-drivers=$(gallium-drivers)
else
  conf-args += -Dgallium-drivers=''
endif

ifeq ($(package.option.opencl),y)
  conf-args += -Dgallium-opencl=standalone
else
  conf-args += -Dgallium-opencl=disabled
endif

ifeq ($(package.option.vulkan-drivers),y)
  vulkan-drivers-$(package.option.vulkan-drivers.intel) += intel
  vulkan-drivers-$(package.option.vulkan-drivers.amd) += amd

  vulkan-drivers = $(subst $(empty) $(empty),$(comma),$(vulkan-drivers-y))
  conf-args += -Dvulkan-drivers=$(vulkan-drivers)
else
  conf-args += -Dvulkan-drivers=''
endif

ifeq ($(package.option.platforms),y)
  platforms-$(package.option.platforms.android) += android
  platforms-$(package.option.platforms.x11) += x11
  platforms-$(package.option.platforms.wayland) += wayland
  platforms-$(package.option.platforms.haiku) += haiku
  platforms-$(package.option.platforms.windows) += windows

  platforms = $(subst $(empty) $(empty),$(comma),$(platforms-y))
  conf-args += -Dplatforms=$(platforms)
else
  conf-args += -Dplatforms=''
endif

conf-args += -Dbuild-tests=true

conf-args += \
	-Dtexture-float=true \
	-Ddri-drivers='' \
	-Dglvnd=true \
	-Dgallium-omx=disabled \
	-Dllvm=enabled \
	-Dshared-llvm=disabled
