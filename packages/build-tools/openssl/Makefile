include $(TOP_SRCDIR)/packages/common.mk

conf-args = \
	--prefix=$(BUILD_TOOLS) \
	shared zlib-dynamic no-docs \
	linux-generic32

$(srcdir)/stamp-configure: | $(srcdir)
	cd $(srcdir) && $(conf-env) ./Configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && $(MAKE) $(build-args)
	touch $@

install-args = \
	MANSUFFIX=ssl

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install

