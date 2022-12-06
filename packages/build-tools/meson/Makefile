include $(TOP_SRCDIR)/packages/build-tools/common.mk

ifeq ($(realpath $(srcdir)),$(srcdir))
$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/sysroot-default-include-dir.patch
	touch $@

$(builddir)/stamp-build: $(srcdir)/stamp-patch
endif

$(builddir):
	mkdir -p $@

$(builddir)/stamp-build: | $(builddir)
	cd $(srcdir) && python3 setup.py build
	touch $@

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(srcdir) && python3 setup.py install --prefix=$(BUILD_TOOLS)
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
