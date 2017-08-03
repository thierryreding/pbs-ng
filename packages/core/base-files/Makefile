include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

$(builddir)/.install: | $(builddir)
	mkdir -p $(DESTDIR)
	mkdir $(DESTDIR)/boot
	mkdir $(DESTDIR)/dev
	mkdir $(DESTDIR)/etc
	mkdir $(DESTDIR)/home
	mkdir $(DESTDIR)/mnt
	mkdir $(DESTDIR)/opt
	mkdir $(DESTDIR)/proc
	mkdir $(DESTDIR)/root
	mkdir $(DESTDIR)/run
	mkdir $(DESTDIR)/srv
	mkdir $(DESTDIR)/sys
	mkdir $(DESTDIR)/tmp
	mkdir $(DESTDIR)/usr
	mkdir $(DESTDIR)/usr/bin
	mkdir $(DESTDIR)/usr/lib
	mkdir $(DESTDIR)/var

	# files
	dbus-uuidgen --ensure=$(DESTDIR)/etc/machine-id

	echo 'root:$(password):0:0:root:/root:/bin/sh' > $(DESTDIR)/etc/passwd
	echo 'messagebus:x:81:81:messagebus:/var/run/dbus:/bin/false' >> $(DESTDIR)/etc/passwd

	echo 'lock:x:20:' > $(DESTDIR)/etc/group
	echo 'utmp:x:54:' >> $(DESTDIR)/etc/group
	echo 'messagebus:x:81:' >> $(DESTDIR)/etc/group
	echo 'systemd-journal:x:190:' >> $(DESTDIR)/etc/group

	cp -a $(TOP_SRCDIR)/$(PKGDIR)/files/etc/pam.d/* $(DESTDIR)/etc/pam.d

	# symlinks
	ln -sf /proc/self/mounts $(DESTDIR)/etc/mtab
	ln -sf $(PREFIX)/lib/systemd/systemd $(DESTDIR)/sbin/init
	ln -sf /run $(DESTDIR)/var/run
	ln -sf bash $(DESTDIR)/bin/sh

	ln -sf $(PREFIX)/bin $(DESTDIR)/bin
	ln -sf $(PREFIX)/lib $(DESTDIR)/lib

	touch $@

install: $(builddir)/.install

.PHONY: install
