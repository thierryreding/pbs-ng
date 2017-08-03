include $(TOP_SRCDIR)/packages/autotools.mk

$(builddir)/stamp-patch: | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(builddir)/stamp-patch

conf-args += \
	--with-sysroot=$(SYSROOT) \
	--without-dri-drivers \
	--with-gallium-drivers=swrast,nouveau,tegra \
	--with-egl-platforms=x11,wayland,drm \
	--enable-gles1 \
	--enable-gles2 \
	--enable-gbm

ifneq ($(package.option.debug),y)
  conf-args += --disable-debug
else
  conf-args += --enable-debug
endif

# prevent the host systems llvm-config script from messing with us
conf-vars += LLVM_CONFIG=no
