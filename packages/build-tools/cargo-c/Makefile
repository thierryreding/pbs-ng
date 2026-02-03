include $(TOP_SRCDIR)/packages/build-tools/common.mk

env += \
	RUSTUP_HOME=$(BUILD_TOOLS)/lib/rustup \
	CARGO_HOME=$(BUILD_TOOLS)

$(srcdir)/stamp-install: | $(srcdir)
	cargo install --path $(srcdir) --root $(BUILD_TOOLS)
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
