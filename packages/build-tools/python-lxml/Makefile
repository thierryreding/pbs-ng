include $(TOP_SRCDIR)/packages/build-tools/common.mk

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && $(env) $(BUILD_TOOLS)/bin/python3 setup.py build
	touch $@

install-args += \
	--prefix=$(BUILD_TOOLS)

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && $(env) $(BUILD_TOOLS)/bin/python3 setup.py install $(install-args)
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
