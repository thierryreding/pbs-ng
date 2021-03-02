include $(TOP_SRCDIR)/packages/common.mk

$(builddir) $(DESTDIR):
	mkdir -p $@

$(builddir)/stamp-install: | $(builddir) $(DESTDIR)
	mkdir -p $(DESTDIR)$(PREFIX)/lib && \
		cp -a $(srcdir)/lib/nvidia/* $(DESTDIR)$(PREFIX)/lib
	mkdir -p $(DESTDIR)/etc/ld.so.conf.d && \
		cp -a $(srcdir)/etc/ld.so.conf.d/000_cuda.conf $(DESTDIR)/etc/ld.so.conf.d && \
		cp -a $(srcdir)/etc/ld.so.conf.d/989_cuda-11.conf $(DESTDIR)/etc/ld.so.conf.d
	mkdir -p $(DESTDIR)$(PREFIX)/lib/xorg/modules && \
		cp -a $(srcdir)/xorg/* $(DESTDIR)$(PREFIX)/lib/xorg/modules
	mkdir -p $(DESTDIR)$(PREFIX)/local/cuda && \
		cp -a $(srcdir)/cuda/* $(DESTDIR)$(PREFIX)/local/cuda
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
