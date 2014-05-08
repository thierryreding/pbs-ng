include $(TOP_SRCDIR)/packages/common.mk

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX)

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(builddir):
	mkdir -p $@

$(builddir)/stamp-configure: | $(builddir)
	cd $(builddir) && \
		$(srcdir)/configure $(conf-args) $(conf-vars)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(MAKE) -j $(JOBS)

install-args = \
	DESTDIR='$(DESTDIR)' \
	-j $(JOBS)

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(MAKE) $(install-args) install

install: $(builddir)/stamp-install

.PHONY: install
