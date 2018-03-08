include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/configure:
	cd $(srcdir) && $(conf-env) ./autogen.sh

$(builddir)/config.cache: | $(builddir)
	echo '# generated for $(HOST)' > $@
	echo 'ac_cv_func_malloc_0_nonnull=yes' >> $@

conf-args += \
	--with-sysroot=$(SYSROOT) \
	--config-cache \
	--enable-tools

$(builddir)/stamp-configure: $(srcdir)/configure $(builddir)/config.cache
