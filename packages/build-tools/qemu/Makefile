include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

ifeq ($(ARCH),arm64)
  ARCH = aarch64
endif

conf-args += \
	--target-list=$(ARCH)-linux-user

$(BUILD_TOOLS)/bin/qemu-sysroot: $(TOP_SRCDIR)/support/qemu-sysroot.in
	sed -e 's|@ARCH@|$(ARCH)|g' -e 's|@SYSROOT@|$(SYSROOT)|g' $< > $@
	chmod a+x $@

install: $(BUILD_TOOLS)/bin/qemu-sysroot
