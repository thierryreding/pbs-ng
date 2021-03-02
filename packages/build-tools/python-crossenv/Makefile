include $(TOP_SRCDIR)/packages/build-tools/common.mk

#$(srcdir)/stamp-patch: | $(srcdir)
#	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
#	touch $@

$(builddir):
	mkdir -p $@

$(builddir)/stamp-build: | $(builddir)
	cd $(srcdir) && python3 setup.py build
	touch $@

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(srcdir) && python3 setup.py install --prefix='$(BUILD_TOOLS)'
	$(BUILD_TOOLS)/bin/python3 -m crossenv --sysroot '$(SYSROOT)' \
		'$(SYSROOT)$(PREFIX)/bin/python3' '$(BUILD_TOOLS)/python'
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
