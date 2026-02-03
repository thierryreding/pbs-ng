include $(TOP_SRCDIR)/packages/meson.mk

env += \
	RUSTFLAGS='-Clink-arg=--sysroot=$(SYSROOT)' \
	RUSTUP_HOME=$(BUILD_TOOLS)/lib/rustup \
	CROSS_COMPILE=$(CROSS_COMPILE) \
	CARGO_HOME=$(BUILD_TOOLS)

conf-args += \
	-Dpixbuf-loader=disabled \
	-Dtriplet=$(HOST)
