include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/perl-5.26.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
