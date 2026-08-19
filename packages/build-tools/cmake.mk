include $(TOP_SRCDIR)/packages/build-tools/common.mk

env = \
	PKG_CONFIG_LIBDIR='$(BUILD_TOOLS)/lib/pkgconfig'

cmake-args = \
	-DCMAKE_INSTALL_PREFIX=$(BUILD_TOOLS)

$(builddir)/stamp-configure: | $(builddir)
	cd $(builddir) && \
		$(env) cmake $(cmake-args) $(srcdir)
	touch $@

build-args = \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(env) $(MAKE) $(build-args)
	touch $@

install-args =

$(builddir)/stamp-install:
	cd $(builddir) && \
		$(env) $(MAKE) $(install-args) install
	touch $@
