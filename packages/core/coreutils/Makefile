include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/recursive-variable.patch
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/config.cache: | $(builddir)
	echo '# generated for $(HOST)' > $@
	echo 'ac_cv_func_canonicalize_file_name=yes' >> $@
	echo 'gl_cv_func_realpath_works=yes' >> $@

conf-args += \
	--config-cache

conf-vars += \
	PERL=no

$(builddir)/stamp-configure: $(srcdir)/stamp-patch $(builddir)/config.cache

build-args += \
	ALL_MANS=
