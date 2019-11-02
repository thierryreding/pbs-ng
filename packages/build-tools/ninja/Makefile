include $(TOP_SRCDIR)/packages/build-tools/common.mk

$(builddir):
	mkdir -p $@

$(builddir)/stamp-build: | $(builddir)
	cd $(builddir) && \
		$(env) $(srcdir)/configure.py --bootstrap
	touch $@

$(BUILD_TOOLS)/bin:
	install -m 755 -d $(BUILD_TOOLS)/bin

$(builddir)/stamp-install: $(builddir)/stamp-build | $(BUILD_TOOLS)/bin
	cd $(builddir) && \
		install -m 755 -D ninja $(BUILD_TOOLS)/bin
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
