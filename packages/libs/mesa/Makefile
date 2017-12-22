include $(TOP_SRCDIR)/packages/autotools.mk

# make sure to lock the source directory when building from a symlinked
# source, otherwise two concurrent builds might step on each others' toes
ifneq ($(realpath $(srcdir)),$(srcdir))
$(builddir)/stamp-patch: $(srcdir)/lock | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(builddir)/stamp-patch

install: $(srcdir)/unlock
endif

conf-args += \
	--with-sysroot=$(SYSROOT) \
	--without-dri-drivers \
	--with-gallium-drivers=swrast,nouveau,tegra \
	--with-platforms=x11,wayland,drm \
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
