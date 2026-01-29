include $(TOP_SRCDIR)/packages/build-tools/common.mk

# rustup 32-bit ARM toolchains aren't endian-specific
ifeq ($(ARCH),arm)
  TARGET := $(ARCH)v7-$(VENDOR)-$(OS)-$(LIBC)$(ABI)
else
  TARGET := $(HOST)
endif

env = \
	RUSTUP_HOME=$(BUILD_TOOLS)/lib/rustup \
	RUSTUP_INIT_SKIP_PATH_CHECK=yes \
	CARGO_HOME=$(BUILD_TOOLS)

install-args = \
	--default-toolchain 1.91 \
	--default-host $(BUILD) \
	--target $(TARGET) \
	--no-modify-path \
	-y

$(srcdir)/stamp-install: | $(srcdir)
	cd $(srcdir) && $(env) ./rustup-init.sh $(install-args)
	touch $@

$(BUILD_TOOLS)/.cargo:
	mkdir -p $@

$(BUILD_TOOLS)/.cargo/config.toml: | $(BUILD_TOOLS)/.cargo
	echo "[target.$(HOST)]" > $@
	echo "linker = \"$(HOST)-gcc\"" >> $@
	echo "ar = \"$(HOST)-ar\"" >> $@

install: $(BUILD_TOOLS)/.cargo/config.toml $(srcdir)/stamp-install

.PHONY: install
