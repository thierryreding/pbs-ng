include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

$(builddir)/configparms: | $(builddir)
	echo '# generated' > $@
	echo 'slibdir=$(PREFIX)/lib' >> $@
	echo 'rtlddir=$(PREFIX)/lib' >> $@
	echo 'sbindir=$(PREFIX)/bin' >> $@
	echo 'rootsbindir=$(PREFIX)/bin' >> $@
	touch $@

conf-args = \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--libexecdir=$(PREFIX)/lib \
	--with-headers=$(SYSROOT)$(PREFIX)/include

conf-vars = \
	ASFLAGS='$(ASFLAGS)' \
	CPPFLAGS='$(CPPFLAGS)' \
	CXXFLAGS='$(CXXFLAGS)' \
	CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)'

$(builddir)/stamp-configure: $(builddir)/configparms
	cd $(builddir) && \
		$(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

$(builddir)/stamp-build: $(builddir)/stamp-configure | $(builddir)
	cd $(builddir) && \
		$(MAKE) -j $(JOBS)
	touch $@

$(builddir)/stamp-install: $(builddir)/stamp-build | $(builddir)
	cd $(builddir) && \
		$(MAKE) -j $(JOBS) DESTDIR=$(DESTDIR) install
	touch $@

$(DESTDIR)/etc/ld.so.conf.d:
	mkdir -p $@

$(DESTDIR)/etc/ld.so.conf:
	echo "include /etc/ld.so.conf.d/*.conf" > $@

install: $(builddir)/stamp-install $(DESTDIR)/etc/ld.so.conf | $(DESTDIR)/etc/ld.so.conf.d

.PHONY: install
