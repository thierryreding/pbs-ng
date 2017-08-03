include $(TOP_SRCDIR)/packages/common.mk

TMPFILES = $(DESTDIR)$(PREFIX)/lib/tmpfiles.d
FACTORY = $(DESTDIR)$(PREFIX)/share/factory

$(DESTDIR)/etc $(DESTDIR)$(PREFIX)/lib $(TMPFILES) $(FACTORY)/etc $(builddir):
	mkdir -p $@

#$(DESTDIR)$(PREFIX)/lib/os-release: | $(DESTDIR)$(PREFIX)/lib
$(DESTDIR)/etc/os-release: | $(DESTDIR)/etc
	echo 'NAME="PBS Linux"' > $@
	echo 'ID="pbs"' >> $@
	echo 'PRETTY_NAME="PBS Linux v$(package.version)"' >> $@
	echo 'ANSI_COLOR="0;36"' >> $@

#$(TMPFILES)/factory.conf: | $(TMPFILES)
#	echo 'L /etc/hostname - - - -' > $@
#	echo 'L /etc/locale.conf - - - -' >> $@
#	echo 'C /etc/passwd - - - -' >> $@
#	echo 'C /etc/group - - - -' >> $@
#	echo 'C /etc/shadow - - - -' >> $@
#
#$(FACTORY)/etc/hostname: | $(FACTORY)/etc
#	echo 'tegra' > $@
#
#$(FACTORY)/etc/locale.conf: | $(FACTORY)/etc
#	echo 'LANG=en_IE.UTF-8' > $@
#
#$(FACTORY)/etc/passwd: | $(FACTORY)/etc
#	#echo 'root:x:0:0:root:/root:/bin/bash' > $@
#	cp $(TOP_SRCDIR)/$(PKGDIR)/passwd $@
#
#$(FACTORY)/etc/group: | $(FACTORY)/etc
#	cp $(TOP_SRCDIR)/$(PKGDIR)/group $@
#
#$(FACTORY)/etc/shadow: | $(FACTORY)/etc
#	echo 'root:$$6$$BB55PEFALFjy8xcC$$T5pxeOwhnjao4Qp5d7MiN54B/6QgE4noCfBcK5ENAUDEjaUB57idlJ5vcDZqR4oDMkqkA9GMYVkjcp1sYnsHK.::::::::' > $@
#
#FILES = \
#	$(DESTDIR)$(PREFIX)/lib/os-release \
#	$(TMPFILES)/factory.conf \
#	$(FACTORY)/etc/hostname \
#	$(FACTORY)/etc/locale.conf \
#	$(FACTORY)/etc/passwd \
#	$(FACTORY)/etc/group \
#	$(FACTORY)/etc/shadow

$(DESTDIR)/etc/ld.so.cache:
	ln -sf ../run/ld.so.cache $@

FILES = \
	$(DESTDIR)/etc/os-release \
	$(DESTDIR)/etc/ld.so.cache

$(builddir)/stamp-install: $(FILES) | $(builddir)
	cp -a $(TOP_SRCDIR)/$(PKGDIR)/src/etc $(DESTDIR)
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
