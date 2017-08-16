include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-prepare: | $(srcdir)
	cp $(BUILD_TOOLS)/share/gettext/config.rpath $(srcdir)/
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-prepare

conf-args += \
	MOUNT_FUSE_PATH=$(PREFIX)/bin
