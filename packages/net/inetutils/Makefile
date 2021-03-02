include $(TOP_SRCDIR)/packages/autotools.mk

conf-args += \
	--with-path-procnet-dev=/proc/net/dev

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/fno-common.patch
	#
	# The ftpd.8 manpage has a dependency on the tftpd.c source file and will be rebuilt
	# using help2man (and fail because we're cross-compiling) because we patch the file in
	# the above patch. However, since we do not modify the parameters, there's no need to
	# rebuild the manpage and we can fix this by updating the manpage's timestamp.
	#
	touch $(srcdir)/man/ftpd.8
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
