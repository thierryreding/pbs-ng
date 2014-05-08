include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

conf-args = \
	--config-cache \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--with-curses

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(builddir)/config.cache: | $(builddir)
	echo '#generated for $(HOST)' > $@
	echo 'bash_cv_wcwidth_broken=yes' >> $@

$(builddir)/stamp-configure: $(builddir)/config.cache | $(builddir)
	cd $(builddir) && \
		$(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(MAKE) $(install-args) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
