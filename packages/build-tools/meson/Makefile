include $(TOP_SRCDIR)/packages/build-tools/common.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/find-library-dependencies.patch
	touch $@

$(builddir):
	mkdir -p $@

$(builddir)/stamp-build: $(srcdir)/stamp-patch | $(builddir)
	cd $(srcdir) && python3 setup.py build
	touch $@

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(srcdir) && python3 setup.py install --prefix=$(BUILD_TOOLS)
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
