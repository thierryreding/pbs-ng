include $(TOP_SRCDIR)/packages/meson.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

env += \
	RUSTFLAGS='-Clink-arg=--sysroot=$(SYSROOT)' \
	RUSTUP_HOME=$(BUILD_TOOLS)/lib/rustup \
	CROSS_COMPILE=$(CROSS_COMPILE) \
	CARGO_HOME=$(BUILD_TOOLS) \
	TARGET=$(HOST)

conf-args += \
	-Dlibglycin-gtk4=false \
	-Dtriplet=$(HOST) \
	-Dtests=false
