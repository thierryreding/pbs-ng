include $(TOP_SRCDIR)/packages/build-tools/common.mk

env = \
	PKG_CONFIG_LIBDIR=$(BUILD_TOOLS)/lib/pkgconfig

$(builddir):
	mkdir -p $@

$(srcdir)/stamp-patch: | $(srcdir)
	touch $@

conf-args = \
	--prefix=$(BUILD_TOOLS)

conf-vars = \
	CFLAGS='-I$(BUILD_TOOLS)/include' \
	LDFLAGS='-L$(BUILD_TOOLS)/lib'

$(builddir)/stamp-configure: $(srcdir)/stamp-patch | $(builddir)
	cd $(builddir) && \
		$(env) $(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(env) $(MAKE) $(build-args)
	touch $@

install-args =

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(env) $(MAKE) $(install-args) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
