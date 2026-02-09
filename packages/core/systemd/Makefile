include $(TOP_SRCDIR)/packages/meson.mk

conf-args += \
	-Dversion-tag='$(package.version)-PBS' \
	-Dshared-lib-tag='$(package.version)' \
	-Dsbat-distro='pbs' \
	-Dsbat-distro-summary='Package Build System' \
	-Dsbat-distro-pkgname='core/systemd' \
	-Dsbat-distro-version='$(package.version)' \
	-Dsbat-distro-url='https://pbs-ng.org'

$(builddir)/stamp-install-hwdb: $(builddir)/stamp-install
	$(BUILD_TOOLS)/bin/systemd-hwdb --root $(DESTDIR) update

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
