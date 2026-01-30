include $(TOP_SRCDIR)/packages/common.mk

$(builddir) $(DESTDIR):
	mkdir -p $@

$(builddir)/stamp-install: | $(builddir) $(DESTDIR)
	mkdir -p $(DESTDIR)$(PREFIX)/lib/firmware && \
		cp -a $(srcdir)/firmware/gv11b $(DESTDIR)$(PREFIX)/lib/firmware
	mkdir -p $(DESTDIR)$(PREFIX)/lib && \
		cp -a $(srcdir)/lib/nvidia/* $(DESTDIR)$(PREFIX)/lib
	mkdir -p $(DESTDIR)$(PREFIX)/share && \
		cp -a $(srcdir)/share/glvnd $(DESTDIR)$(PREFIX)/share
	mkdir -p $(DESTDIR)/etc/ld.so.conf.d && \
		cp $(srcdir)/etc/ld.so.conf.d/nvidia-l4t-jetson.conf $(DESTDIR)/etc/ld.so.conf.d
	mkdir -p $(DESTDIR)/etc/X11/xorg.conf.d && \
		cp $(srcdir)/etc/X11/xorg.conf.d/tegra-drm-outputclass.conf $(DESTDIR)/etc/X11/xorg.conf.d
	mkdir -p $(DESTDIR)$(PREFIX)/lib/xorg/modules && \
		cp -a $(srcdir)/xorg/* $(DESTDIR)$(PREFIX)/lib/xorg/modules
	mkdir -p $(DESTDIR)$(PREFIX)/local/cuda && \
		cp -a $(srcdir)/cuda/* $(DESTDIR)$(PREFIX)/local/cuda
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
