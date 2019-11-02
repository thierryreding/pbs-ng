include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/config-h.patch
	touch $@

$(builddir)/config.cache: | $(builddir)
	echo '# generated for $(HOST)' > $@
	echo 'ac_cv_func_malloc_0_nonnull=yes' >> $@
	echo 'ac_cv_func_realloc_0_nonnull=yes' >> $@

conf-args += \
	--sbindir=$(PREFIX)/bin \
	--libdir=$(PREFIX)/lib \
	--bindir=$(PREFIX)/bin \
	--exec-prefix=/ \
	--config-cache

$(builddir)/stamp-configure: $(srcdir)/stamp-patch $(builddir)/config.cache
