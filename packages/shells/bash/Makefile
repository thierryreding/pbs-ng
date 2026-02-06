include $(TOP_SRCDIR)/packages/autotools.mk

$(builddir)/config.cache: | $(builddir)
	echo '# generated for $(HOST)' > $@
	echo 'bash_cv_job_control_missing=present' >> $@

conf-args += \
	--config-cache

$(builddir)/stamp-configure: $(builddir)/config.cache

$(builddir)/stamp-post-install: $(builddir)/stamp-install
	ln -s bash $(DESTDIR)$(PREFIX)/bin/sh
	touch $@

install: $(builddir)/stamp-post-install
