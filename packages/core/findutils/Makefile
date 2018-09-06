include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/gnulib-update.patch
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

conf-vars += \
	gl_cv_func_wcwidth_works=yes \
	gl_cv_func_stdin=yes
