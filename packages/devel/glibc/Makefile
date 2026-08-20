include $(TOP_SRCDIR)/packages/autotools.mk

$(builddir)/configparms: | $(builddir)
	echo '# generated' > $@
	echo 'slibdir=$(PREFIX)/lib' >> $@
	echo 'rtlddir=$(PREFIX)/lib' >> $@
	echo 'sbindir=$(PREFIX)/bin' >> $@
	echo 'rootsbindir=$(PREFIX)/bin' >> $@
	touch $@

conf-args += \
	--with-headers=$(SYSROOT)$(PREFIX)/include \
	--libexecdir=$(PREFIX)/lib

conf-vars += \
	ASFLAGS='$(ASFLAGS)'

$(builddir)/stamp-configure: $(builddir)/configparms

$(DESTDIR)/etc/ld.so.conf.d:
	mkdir -p $@

$(DESTDIR)/etc/ld.so.conf:
	echo "include /etc/ld.so.conf.d/*.conf" > $@

$(BUILD_TOOLS)/bin/$(CROSS_COMPILE)ldd: $(TOP_SRCDIR)/support/ldd-sysroot.in
	sed -e 's|@LDD@|$(TOP_SRCDIR)/support/ldd|g' -e 's|@SYSROOT@|$(SYSROOT)|g' $< > $@
	chmod a+x $@

$(builddir)/stamp-post-install: $(builddir)/stamp-install
$(builddir)/stamp-post-install: $(DESTDIR)/etc/ld.so.conf | $(DESTDIR)/etc/ld.so.conf.d
$(builddir)/stamp-post-install: $(BUILD_TOOLS)/bin/$(CROSS_COMPILE)ldd

install: $(builddir)/stamp-post-install
