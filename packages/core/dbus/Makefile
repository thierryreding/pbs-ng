include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libexec=$(PREFIX)/lib/dbus-1.0 \
	--localstatedir=/var \
	--sysconfdir=/etc \
	--without-x

conf-args += \
	--with-systemdsystemunitdir=/usr/lib/systemd/system

conf-vars = \
	CPPFLAGS='--sysroot $(SYSROOT)' \
	CFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(builddir)/stamp-configure: | $(builddir)
	cd $(builddir) && \
		$(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

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
