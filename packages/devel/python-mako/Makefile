include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

$(builddir)/stamp-build: | $(builddir)
	cd $(srcdir) && python3 setup.py build
	touch $@

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(srcdir) && python3 setup.py install --root=$(DESTDIR) \
		--prefix=$(PREFIX)
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
