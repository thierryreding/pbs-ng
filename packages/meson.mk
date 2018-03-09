include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

$(builddir)/cross-compile.txt: $(TOP_SRCDIR)/support/cross-compile.meson | $(builddir)
	sed 's|@OS@|$(OS)|;s|@ARCH@|$(ARCH)|;s|@CPU@|$(CPU)|;s|@ENDIAN@|$(ENDIAN)|;s|@HOST@|$(HOST)|;s|@SYSROOT@|$(SYSROOT)|' $< > $@

env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)' \
	CPPFLAGS='$(CPPFLAGS)' \
	CXXFLAGS='$(CXXFLAGS)' \
	LDFLAGS='$(LDFLAGS)' \
	CFLAGS='$(CFLAGS)' \
	DESTDIR=$(DESTDIR)

conf-args = \
	--prefix $(PREFIX) \
	--libexecdir $(PREFIX)/lib

$(builddir)/stamp-configure: $(builddir)/cross-compile.txt
	$(env) meson --cross-file $< $(conf-args) $(srcdir) $(builddir)
	touch $@

$(builddir)/stamp-build: $(builddir)/stamp-configure
	$(env) ninja -C $(builddir)
	touch $@

$(builddir)/stamp-install: $(builddir)/stamp-build
	$(env) ninja -C $(builddir) install

install: $(builddir)/stamp-install

.PHONY: install
