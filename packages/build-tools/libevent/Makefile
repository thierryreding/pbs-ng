include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

$(srcdir)/stamp-prepare: | $(srcdir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-prepare

$(builddir)/stamp-cleanup: $(builddir)/stamp-install
	rm -f $(BUILD_TOOLS)/lib/libevent_core.la

install: $(builddir)/stamp-cleanup
