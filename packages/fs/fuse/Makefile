include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/namespace-conflict.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

conf-args += \
	MOUNT_FUSE_PATH=$(PREFIX)/bin
