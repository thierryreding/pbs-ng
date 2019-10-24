include $(TOP_SRCDIR)/packages/build-tools/common.mk

$(srcdir)/stamp-patch: | $(srcdir)
	touch $@

conf-args = \
	--prefix=$(BUILD_TOOLS)

$(srcdir)/stamp-configure: $(srcdir)/stamp-patch | $(srcdir)
	cd $(srcdir) && \
		$(env) ./configure $(conf-args)
	touch $@

build-args = \
	-j $(JOBS)

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && \
		$(env) $(MAKE) $(build-args)
	touch $@

install-args =

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		$(env) $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
