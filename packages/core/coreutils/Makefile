include $(TOP_SRCDIR)/packages/autotools.mk

$(builddir)/config.cache: | $(builddir)
	echo '# generated for $(HOST)' > $@
	echo 'ac_cv_func_canonicalize_file_name=yes' >> $@
	echo 'gl_cv_func_realpath_works=yes' >> $@

conf-args += \
	--config-cache

conf-vars += \
	PERL=no

$(builddir)/stamp-configure: $(builddir)/config.cache

build-args += \
	ALL_MANS=
