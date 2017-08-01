include $(TOP_SRCDIR)/packages/build-tools/common.mk

$(builddir):
	mkdir -p $@

$(builddir)/stamp-configure: | $(builddir)
	cd $(builddir) && \
		$(env) $(srcdir)/bootstrap --prefix=$(BUILD_TOOLS)
	touch $@

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(env) make -j $(JOBS)
	touch $@

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(env) make install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
