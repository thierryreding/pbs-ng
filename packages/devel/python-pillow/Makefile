include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

#
# Ensure that the cross-compilation Python interpreter is used, so that the
# correct cross-compiler is picked up to build extensions.
#
env += \
	PATH='$(BUILD_TOOLS)/python/cross/bin:$(PATH)' \

common-args = \
	build_ext --disable-platform-guessing

$(builddir)/stamp-build: | $(builddir)
	cd $(srcdir) && $(env) python3 setup.py $(common-args)
	touch $@

install-args = \
	install --prefix=$(PREFIX) --root=$(DESTDIR)

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(srcdir) && $(env) python3 setup.py $(common-args) $(install-args)
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
