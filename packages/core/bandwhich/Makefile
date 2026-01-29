include $(TOP_SRCDIR)/packages/common.mk

# rustup 32-bit ARM toolchains aren't endian-specific
ifeq ($(ARCH),arm)
  TARGET := $(ARCH)v7-$(VENDOR)-$(OS)-$(LIBC)$(ABI)
else
  TARGET := $(HOST)
endif

env = \
	RUSTUP_HOME=$(BUILD_TOOLS)/lib/rustup \
	CROSS_COMPILE=$(CROSS_COMPILE) \
	CARGO_HOME=$(BUILD_TOOLS)

build-args = \
	--target $(TARGET) \
	--release --locked

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && $(env) cargo update
	cd $(srcdir) && $(env) cargo build $(build-args)
	touch $@

install-args = \
	--root $(DESTDIR)$(PREFIX) \
	--target $(TARGET) \
	--path .

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && $(env) cargo install $(install-args)
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
