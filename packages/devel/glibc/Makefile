include $(TOP_SRCDIR)/packages/common.mk
include config.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/make-4.patch
	touch $@

patch: $(builddir)/stamp-patch

$(builddir):
	mkdir -p $@

$(builddir)/configparms: | $(builddir)
	echo '# generated' > $@
	#echo 'slibdir=$(PREFIX)/lib' >> $@
	echo 'sbindir=$(PREFIX)/bin' >> $@
	echo 'rootsbindir=$(PREFIX)/bin' >> $@
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch $(builddir)/configparms
	cd $(builddir) && \
		$(srcdir)/configure \
			--host=$(HOST) \
			--prefix=$(PREFIX) \
			--libexecdir=$(PREFIX)/lib \
			--with-headers=$(SYSROOT)$(PREFIX)/include \
			--enable-obsolete-rpc
	touch $@

configure: $(builddir)/stamp-configure

$(builddir)/stamp-build: $(builddir)/stamp-configure | $(builddir)
	cd $(builddir) && \
		$(MAKE) -j $(JOBS)
	touch $@

build: $(builddir)/stamp-build

$(builddir)/stamp-install: $(builddir)/stamp-build | $(builddir)
	cd $(builddir) && \
		$(MAKE) -j $(JOBS) DESTDIR=$(DESTDIR) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: patch configure build install
