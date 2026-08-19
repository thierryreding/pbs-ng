include $(TOP_SRCDIR)/packages/build-tools/common.mk

env = \
	DESTDIR=$(DESTDIR)

conf-args = \
	-Dpkg_config_path=$(BUILD_TOOLS)/lib/pkgconfig:$(BUILD_TOOLS)/share/pkgconfig \
	--libexecdir $(BUILD_TOOLS)/lib \
	--prefix $(BUILD_TOOLS)

$(builddir)/stamp-configure: | $(builddir)
	$(env) meson setup $(conf-args) $(srcdir) $(builddir)
	touch $@

$(builddir)/stamp-build: $(builddir)/stamp-configure
	$(env) ninja -C $(builddir)
	touch $@

$(builddir)/stamp-install:
	$(env) $(FAKEROOT) ninja -C $(builddir) install
