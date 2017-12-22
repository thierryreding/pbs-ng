include $(TOP_SRCDIR)/packages/build-tools/common.mk

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
