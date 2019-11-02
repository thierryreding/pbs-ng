include $(TOP_SRCDIR)/packages/common.mk

$(builddir): | $(srcdir)
	mkdir -p $@

$(srcdir)/waf: | $(srcdir)
	cd $(srcdir) && ./bootstrap.py

conf-env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)' \
	CC='$(CROSS_COMPILE)gcc' \
	CPPFLAGS='$(CPPFLAGS)' \
	CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)'

conf-args = \
	--out $(builddir) \
	--prefix $(PREFIX)

$(builddir)/stamp-configure: | $(builddir) $(srcdir)/waf
	cd $(srcdir) && \
		$(conf-env) ./waf configure $(conf-args)
	touch $@

build-args = \
	--out $(builddir) \
	--jobs $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(srcdir) && \
		./waf build $(build-args)
	touch $@

install-args = \
	--out $(builddir) \
	--destdir $(DESTDIR)

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(srcdir) && \
		./waf install $(install-args)
	touch $@

install: $(builddir)/stamp-install

.PHONY: install

ifeq ($(FORCE),y)
.PHONY: $(builddir)/stamp-build
endif
