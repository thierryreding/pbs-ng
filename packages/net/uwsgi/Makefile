include $(TOP_SRCDIR)/packages/common.mk

env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)' \
	CC='$(CROSS_COMPILE)gcc' \
	CPP='$(CROSS_COMPILE)cpp' \
	OBJCOPY='$(CROSS_COMPILE)objcopy' \
	APPEND_CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

plugins = \
	corerouter \
	http \
	python

plugins-list = \
	$(subst $(empty) $(empty),$(comma) $(empty),$(plugins))

plugindir = $(PREFIX)/lib/uwsgi

$(srcdir)/buildconf/pbs.ini: $(TOP_SRCDIR)/$(PKGDIR)/pbs.ini | $(srcdir)
	sed 's|@PLUGINS@|$(plugins-list)|;s|@PLUGINDIR@|$(plugindir)|' $< > $@

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

$(srcdir)/stamp-build: $(srcdir)/stamp-patch $(srcdir)/buildconf/pbs.ini
	cd $(srcdir) && $(env) python uwsgiconfig.py --build pbs
	touch $@

$(srcdir)/stamp-install-core: $(srcdir)/stamp-build
	install -m 755 -d $(DESTDIR)$(PREFIX)/bin
	install -m 755 $(srcdir)/uwsgi $(DESTDIR)$(PREFIX)/bin
	touch $@

$(DESTDIR)$(plugindir):
	install -m 755 -d $@

$(DESTDIR)$(plugindir)/%_plugin.so: $(srcdir)/stamp-build | $(DESTDIR)$(plugindir)
	install -m 755 $(srcdir)/$*_plugin.so $@

mkplugin = $(DESTDIR)$(plugindir)/$(1)_plugin.so
install-plugins = $(foreach plugin,$(plugins),$(call mkplugin,$(plugin)))

$(srcdir)/stamp-install: $(srcdir)/stamp-install-core $(install-plugins)
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
