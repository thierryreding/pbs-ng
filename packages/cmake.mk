include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

$(builddir)/cross-compile.cmake: $(TOP_SRCDIR)/support/cross-compile.cmake.in | $(builddir)
	sed 's|@ARCH@|$(ARCH)|;s|@HOST@|$(HOST)|;s|@SYSROOT@|$(SYSROOT)|' $< > $@

env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

cmake-args = \
	-DCMAKE_TOOLCHAIN_FILE=$(builddir)/cross-compile.cmake \
	-DCMAKE_INSTALL_PREFIX=$(PREFIX)

$(builddir)/stamp-configure: | $(builddir)/cross-compile.cmake
	cd $(builddir) && \
		$(env) cmake $(cmake-args) $(srcdir)
	touch $@

build-args = \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(env) $(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(env) $(MAKE) $(install-args) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
