include $(TOP_SRCDIR)/packages/meson.mk

conf-args += \
	--libexecdir $(PREFIX)/lib/xorg-server \
	-Dxdmcp=false

$(DESTDIR)$(PREFIX)/bin/X: $(builddir)/stamp-install
	ln -s Xorg $@

install: $(DESTDIR)$(PREFIX)/bin/X
