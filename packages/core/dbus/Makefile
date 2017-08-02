include $(TOP_SRCDIR)/packages/autotools.mk

conf-args += \
	--with-systemdsystemunitdir=$(PREFIX)/lib/systemd/system \
	--libexec=$(PREFIX)/lib/dbus-1.0 \
	--enable-systemd \
	--without-x

SYSUSERS = $(DESTDIR)$(PREFIX)/lib/sysusers.d

$(SYSUSERS):
	mkdir -p $@

$(SYSUSERS)/dbus.conf: | $(SYSUSERS)
	echo 'u messagebus - - -' > $@

install: $(SYSUSERS)/dbus.conf
