include $(TOP_SRCDIR)/packages/meson.mk

ifeq ($(realpath $(srcdir)),$(srcdir))
$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/fix-ms-collisions.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/fix-noreturn.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
endif

$(builddir)/stamp-install-hwdb: $(builddir)/stamp-install
	# TODO add build-tools/systemd to get this binary irrespective of
	# whether or not the build system has it installed
	systemd-hwdb --root $(DESTDIR) update

$(builddir)/stamp-install-symlinks: $(builddir)/stamp-install
	ln -sf ../lib/systemd/systemd $(DESTDIR)$(PREFIX)/bin/init
	ln -sf systemctl $(DESTDIR)$(PREFIX)/bin/halt
	ln -sf systemctl $(DESTDIR)$(PREFIX)/bin/poweroff
	ln -sf systemctl $(DESTDIR)$(PREFIX)/bin/reboot
	ln -sf systemctl $(DESTDIR)$(PREFIX)/bin/runlevel
	ln -sf systemctl $(DESTDIR)$(PREFIX)/bin/shutdown
	ln -sf systemctl $(DESTDIR)$(PREFIX)/bin/telinit
	touch $@

install: $(builddir)/stamp-install-hwdb $(builddir)/stamp-install-symlinks
