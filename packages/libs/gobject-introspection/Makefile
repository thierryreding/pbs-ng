include $(TOP_SRCDIR)/packages/meson.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/sysroot.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

MULTIARCH = $(ARCH)-$(OS)-$(LIBC)$(ABI)

env += _PYTHON_SYSCONFIGDATA_NAME=_sysconfigdata__$(OS)_$(MULTIARCH)

conf-args += \
	-Dgi_cross_pkgconfig_sysroot_path=$(SYSROOT) \
	-Dgi_cross_ldd_wrapper=$(CROSS_COMPILE)ldd \
	-Dgi_cross_binary_wrapper=qemu-sysroot \
	-Dgi_cross_use_prebuilt_gi=true
