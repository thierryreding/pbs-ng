include $(TOP_SRCDIR)/packages/common.mk
include config.mk

builddir = $(CURDIR)/obj-$(HOST)

$(builddir) $(DESTDIR):
	mkdir -p $@

password = $(shell $(TOP_SRCDIR)/scripts/mkpasswd root)

$(builddir)/stamp-install: | $(builddir) $(DESTDIR)
	# directories
	install -d $(DESTDIR)/bin -m 755
	install -d $(DESTDIR)/dev -m 755
	install -d $(DESTDIR)/etc -m 755
	install -d $(DESTDIR)/etc/pam.d -m 755
	install -d $(DESTDIR)/media -m 755
	install -d $(DESTDIR)/mnt -m 755
	install -d $(DESTDIR)/proc -m 555
	install -d $(DESTDIR)/root -m 750
	install -d $(DESTDIR)/run -m 755
	install -d $(DESTDIR)/sbin -m 755
	install -d $(DESTDIR)/sys -m 555
	install -d $(DESTDIR)/tmp -m 1777
	install -d $(DESTDIR)/usr -m 755
	install -d $(DESTDIR)/var -m 755
	install -d $(DESTDIR)/var/lib -m 755
	install -d $(DESTDIR)/var/log -m 755

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

	touch $@

install: $(builddir)/stamp-install

.PHONY: install
