include $(TOP_SRCDIR)/packages/common.mk

$(builddir) $(DESTDIR):
	mkdir -p $@

password = $(shell $(TOP_SRCDIR)/scripts/mkpasswd root)

$(builddir)/stamp-install: | $(builddir) $(DESTDIR)
	# directories
	install -d $(DESTDIR)/boot -m 755
	install -d $(DESTDIR)/dev -m 755
	install -d $(DESTDIR)/etc -m 755
	install -d $(DESTDIR)/etc/pam.d -m 755
	install -d $(DESTDIR)/home -m 755
	install -d $(DESTDIR)/media -m 755
	install -d $(DESTDIR)/media/disk -m 755
	install -d $(DESTDIR)/mnt -m 755
	install -d $(DESTDIR)/opt -m 755
	install -d $(DESTDIR)/proc -m 555
	install -d $(DESTDIR)/root -m 750
	install -d $(DESTDIR)/run -m 755
	install -d $(DESTDIR)/srv -m 755
	install -d $(DESTDIR)/sys -m 555
	install -d $(DESTDIR)/tmp -m 1777
	install -d $(DESTDIR)/usr -m 755
	install -d $(DESTDIR)/usr/bin -m 755
	install -d $(DESTDIR)/usr/lib -m 755
	install -d $(DESTDIR)/usr/sbin -m 755
	install -d $(DESTDIR)/var -m 755
	install -d $(DESTDIR)/var/cache -m 755
	install -d $(DESTDIR)/var/lib -m 755
	install -d $(DESTDIR)/var/log -m 755
	install -d $(DESTDIR)/var/spool -m 755

	# files
	dbus-uuidgen --ensure=$(DESTDIR)/etc/machine-id

	for file in passwd group; do \
		cp $(TOP_SRCDIR)/$(PKGDIR)/files/etc/$$file $(DESTDIR)/etc/$$file; \
	done

	cp -a $(TOP_SRCDIR)/$(PKGDIR)/files/etc/pam.d/* $(DESTDIR)/etc/pam.d

	cp $(TOP_SRCDIR)/$(PKGDIR)/files/etc/nsswitch.conf $(DESTDIR)/etc/nsswitch.conf
	cp $(TOP_SRCDIR)/$(PKGDIR)/files/etc/os-release $(DESTDIR)/etc/os-release
	cp $(TOP_SRCDIR)/$(PKGDIR)/files/etc/securetty $(DESTDIR)/etc/securetty
	cp $(TOP_SRCDIR)/$(PKGDIR)/files/etc/shells $(DESTDIR)/etc/shells

	# symlinks
	ln -sf usr/bin $(DESTDIR)/bin
	ln -sf usr/lib $(DESTDIR)/lib
	ln -sf usr/bin $(DESTDIR)/sbin

	ln -sf /proc/self/mounts $(DESTDIR)/etc/mtab
	ln -sf $(PREFIX)/lib/systemd/systemd $(DESTDIR)/sbin/init
	ln -sf /run $(DESTDIR)/var/run
	ln -sf bash $(DESTDIR)/bin/sh

	touch $@

install: $(builddir)/stamp-install

.PHONY: install
