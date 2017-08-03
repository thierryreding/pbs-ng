include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX)

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(builddir)/stamp-configure: | $(builddir)
	cd $(builddir) && \
		$(conf-env) $(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(MAKE) $(build-args)
	touch $@

install-args = \
	-j $(JOBS)

install-vars = \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(MAKE) $(install-args) $(install-vars) install
	ln -s kmod $(DESTDIR)$(PREFIX)/bin/depmod
	ln -s kmod $(DESTDIR)$(PREFIX)/bin/insmod
	ln -s kmod $(DESTDIR)$(PREFIX)/bin/lsmod
	ln -s kmod $(DESTDIR)$(PREFIX)/bin/modinfo
	ln -s kmod $(DESTDIR)$(PREFIX)/bin/modprobe
	ln -s kmod $(DESTDIR)$(PREFIX)/bin/rmmod
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
