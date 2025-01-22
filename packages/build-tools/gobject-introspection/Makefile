include $(TOP_SRCDIR)/packages/build-tools/meson.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/sysroot.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

$(BUILD_TOOLS)/bin/g-ir-scanner: $(TOP_SRCDIR)/support/g-ir-scanner.in $(builddir)/stamp-install
	mv $(BUILD_TOOLS)/bin/g-ir-scanner $(BUILD_TOOLS)/bin/g-ir-scanner.real
	sed -e 's|@HOST@|$(HOST)|' -e 's|@SYSROOT@|$(SYSROOT)|' $< > $@
	chmod a+x $@

install: $(BUILD_TOOLS)/bin/g-ir-scanner
