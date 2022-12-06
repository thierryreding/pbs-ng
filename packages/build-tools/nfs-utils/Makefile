include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/out-of-tree.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/no-statedir.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/std-sbindir.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/udev-libdir.patch
	cd $(srcdir) && autoreconf --force --install --verbose
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

conf-args += \
	--libexecdir=$(BUILD_TOOLS)/bin \
	--with-modprobedir=$(BUILD_TOOLS)/lib/modprobe.d \
	--disable-sbin-override \
	--with-rpcgen=internal \
	--disable-gss
