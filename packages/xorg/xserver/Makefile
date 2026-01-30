include $(TOP_SRCDIR)/packages/meson.mk

conf-args += \
	--libexecdir $(PREFIX)/lib/xorg-server \
	-Dsuid_wrapper=true \
	-Dxdmcp=false

$(DESTDIR)$(PREFIX)/bin/X: $(builddir)/stamp-install
	ln -sf Xorg $@

install: $(DESTDIR)$(PREFIX)/bin/X
