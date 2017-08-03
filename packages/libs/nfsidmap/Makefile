include $(TOP_SRCDIR)/packages/autotools.mk

$(builddir)/config.cache: | $(builddir)
	echo '# generated for $(HOST)' > $@
	echo 'ac_cv_func_malloc_0_nonnull=yes' >> $@

$(builddir)/stamp-configure: $(builddir)/config.cache

conf-args += \
	--config-cache
