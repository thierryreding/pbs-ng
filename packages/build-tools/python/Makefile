include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

conf-args += \
	--with-system-expat \
	--with-system-ffi \
	--with-system-libmpdec \
	--enable-shared

$(BUILD_TOOLS)/bin/python3: $(builddir)/stamp-install

$(BUILD_TOOLS)/bin/python: $(BUILD_TOOLS)/bin/python3
	ln -sf $(basename $<) $@

install: $(BUILD_TOOLS)/bin/python
