include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-prepare: | $(srcdir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/config.cache: | $(builddir)
	echo 'glib_cv_stack_grows=no' > $@
	echo 'glib_cv_uscore=no' >> $@
	echo 'ac_cv_func_posix_getpwuid_r=yes' >> $@
	echo 'ac_cv_func_posix_getgrgid_r=yes' >> $@

conf-args += \
	--with-sysroot='$(SYSROOT)' \
	--config-cache

$(builddir)/stamp-configure: $(srcdir)/stamp-prepare $(builddir)/config.cache
