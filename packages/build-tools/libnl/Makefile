include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

$(srcdir)/stamp-prepare: | $(builddir)
	cd $(srcdir) && autoreconf --force --install --verbose
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-prepare

$(builddir)/stamp-post-install: $(builddir)/stamp-install
	rm -f $(BUILD_TOOLS)/lib/libnl-genl-3.la
	rm -f $(BUILD_TOOLS)/lib/libnl-3.la
	touch $@

install: $(builddir)/stamp-post-install
