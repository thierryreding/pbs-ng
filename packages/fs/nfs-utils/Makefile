include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/out-of-tree.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/std-sbindir.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/udev-libdir.patch
	cd $(srcdir) && autoreconf --force --install --verbose
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

conf-args += \
	--sbindir=$(PREFIX)/bin \
	--with-rpcgen=$(BUILD_TOOLS)/bin/rpcgen \
	--with-statedir=/var/lib/nfs \
	--with-sysroot=$(SYSROOT) \
	--enable-ipv6 \
	--disable-sbin-override \
	--enable-libmount-mount \
	--enable-mountconfig \
	--without-tcp-wrappers \
	--disable-gss

# needs sqlite3
conf-args += \
	--disable-nfsdcltrack \
	--disable-nfsdcld
