include $(TOP_SRCDIR)/packages/autotools.mk

conf-args += \
	--sbindir=$(PREFIX)/bin \
	--libexecdir=$(PREFIX)/lib/ssh \
	--with-privsep-user=nobody \
	--sysconfdir=/etc/ssh \
	--disable-strip

$(DESTDIR)$(PREFIX)/lib/systemd/system:
	mkdir -p $@

$(DESTDIR)$(PREFIX)/lib/systemd/system/sshd.service: $(TOP_SRCDIR)/$(PKGDIR)/sshd.service | $(DESTDIR)$(PREFIX)/lib/systemd/system
	cp $< $@

$(DESTDIR)/etc/tmpfiles.d:
	mkdir -p $@

$(DESTDIR)/etc/tmpfiles.d/sshd.conf: $(TOP_SRCDIR)/$(PKGDIR)/sshd.conf | $(DESTDIR)/etc/tmpfiles.d
	cp $< $@

$(builddir)/stamp-install: $(DESTDIR)$(PREFIX)/lib/systemd/system/sshd.service
$(builddir)/stamp-install: $(DESTDIR)/etc/tmpfiles.d/sshd.conf
