include $(TOP_SRCDIR)/packages/meson.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/post-install.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

conf-args += \
	-Dlauncher-permissions=disabled

SYSUSERS = $(DESTDIR)$(PREFIX)/lib/sysusers.d

$(SYSUSERS):
	mkdir -p $@

$(SYSUSERS)/dbus.conf: | $(SYSUSERS)
	echo 'u messagebus - - -' > $@

install: $(SYSUSERS)/dbus.conf
