include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/no-rpath.patch
	touch $@

$(builddir)/config.cache: | $(builddir)
	echo '# generated for $(HOST)' > $@
	echo 'bash_cv_wcwidth_broken=yes' >> $@

conf-args += \
	--config-cache \
	--with-curses

$(builddir)/stamp-configure: $(srcdir)/stamp-patch $(builddir)/config.cache

build-args += \
	SHLIB_LIBS='-lncurses'
