include $(TOP_SRCDIR)/packages/autotools.mk

ifeq ($(ARCH),arm64)
  ARCH = aarch64
endif

conf-env += \
	PKG_CONFIG=pkg-config

targets-y += \
	$(ARCH)-linux-user \
	$(ARCH)-softmmu

TARGETS = $(subst $(empty) $(empty),$(comma),$(targets-y))

conf-args += \
	--libexecdir=$(PREFIX)/lib/qemu \
	--cross-prefix=$(CROSS_COMPILE) \
	--extra-cflags='--sysroot $(SYSROOT)' \
	--target-list=$(TARGETS) \
	--enable-virtfs
