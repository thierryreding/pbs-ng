include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	cd $(srcdir) && autoreconf --force --install --verbose
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

conf-args += \
	--sbindir=$(PREFIX)/bin \
	--with-statedir=/var/lib/nfs \
	--enable-ipv6 \
	--enable-libmount-mount \
	--enable-mountconfig \
	--disable-nfsdcld \
	--disable-nfsdcltrack \
	--disable-gss \
	--without-tcp-wrappers \
	--with-rpcgen=internal
