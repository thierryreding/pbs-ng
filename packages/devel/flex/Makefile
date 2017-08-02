include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX)

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)' \
	ac_cv_func_malloc_0_nonnull=yes \
	ac_cv_func_realloc_0_nonnull=yes

$(builddir)/stamp-configure: | $(builddir)
	cd $(builddir) && \
		$(conf-env) $(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(MAKE) -j $(JOBS)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)' \
	-j $(JOBS)

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(MAKE) $(install-args) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
