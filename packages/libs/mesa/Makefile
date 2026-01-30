include $(TOP_SRCDIR)/packages/meson.mk

env += \
	CMAKE=$(BUILD_TOOLS)/bin/cmake \
	PKG_CONFIG_FDO_SYSROOT_RULES=1

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
  gallium-drivers-$(package.option.gallium-drivers.asahi) += asahi
  gallium-drivers-$(package.option.gallium-drivers.crocus) += crocus
  gallium-drivers-$(package.option.gallium-drivers.d3d12) += d3d12
  gallium-drivers-$(package.option.gallium-drivers.ethosu) += ethosu
  gallium-drivers-$(package.option.gallium-drivers.etnaviv) += etnaviv
  gallium-drivers-$(package.option.gallium-drivers.freedreno) += freedreno
  gallium-drivers-$(package.option.gallium-drivers.i915) += i915
  gallium-drivers-$(package.option.gallium-drivers.iris) += iris
  gallium-drivers-$(package.option.gallium-drivers.lima) += lima
  gallium-drivers-$(package.option.gallium-drivers.llvmpipe) += llvmpipe
  gallium-drivers-$(package.option.gallium-drivers.nouveau) += nouveau
  gallium-drivers-$(package.option.gallium-drivers.panfrost) += panfrost
  gallium-drivers-$(package.option.gallium-drivers.r300) += r300
  gallium-drivers-$(package.option.gallium-drivers.r600) += r600
  gallium-drivers-$(package.option.gallium-drivers.radeonsi) += radeonsi
  gallium-drivers-$(package.option.gallium-drivers.rocket) += rocket
  gallium-drivers-$(package.option.gallium-drivers.softpipe) += softpipe
  gallium-drivers-$(package.option.gallium-drivers.svga) += svga
  gallium-drivers-$(package.option.gallium-drivers.tegra) += tegra
  gallium-drivers-$(package.option.gallium-drivers.v3d) += v3d
  gallium-drivers-$(package.option.gallium-drivers.vc4) += vc4
  gallium-drivers-$(package.option.gallium-drivers.virgl) += virgl
  gallium-drivers-$(package.option.gallium-drivers.zink) += zink

  gallium-drivers = $(subst $(empty) $(empty),$(comma),$(gallium-drivers-y))
  conf-args += -Dgallium-drivers=$(gallium-drivers)
else
  conf-args += -Dgallium-drivers=''
endif

ifeq ($(package.option.opencl),y)
  conf-args += -Dgallium-rusticl=true
else
  conf-args += -Dgallium-rusticl=false
endif

ifeq ($(package.option.vulkan-drivers),y)
  vulkan-drivers-$(package.option.vulkan-drivers.amd) += amd
  vulkan-drivers-$(package.option.vulkan-drivers.asahi) += asahi
  vulkan-drivers-$(package.option.vulkan-drivers.broadcom) += broadcom
  vulkan-drivers-$(package.option.vulkan-drivers.freedreno) += freedreno
  vulkan-drivers-$(package.option.vulkan-drivers.gfxstream) += gfxstream
  vulkan-drivers-$(package.option.vulkan-drivers.imagination) += imagination
  vulkan-drivers-$(package.option.vulkan-drivers.intel) += intel
  vulkan-drivers-$(package.option.vulkan-drivers.intel-haswell) += intel_hasvk
  vulkan-drivers-$(package.option.vulkan-drivers.kosmickrisp) += kosmickrisp
  vulkan-drivers-$(package.option.vulkan-drivers.microsoft) += microsoft-experimental
  vulkan-drivers-$(package.option.vulkan-drivers.nouveau) += nouveau
  vulkan-drivers-$(package.option.vulkan-drivers.panfrost) += panfrost
  vulkan-drivers-$(package.option.vulkan-drivers.swrast) += swrast
  vulkan-drivers-$(package.option.vulkan-drivers.tegra) += tegra
  vulkan-drivers-$(package.option.vulkan-drivers.virtio) += virtio

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
	-Dglvnd=enabled \
	-Dllvm=enabled
