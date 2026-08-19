include $(TOP_SRCDIR)/packages/common.mk
include $(TOP_SRCDIR)/packages/meson-support.mk

MESON = meson
NINJA = ninja

env = \
	QEMU_LD_PREFIX=$(SYSROOT) \
	DESTDIR=$(DESTDIR)

conf-args = \
	--native-file $(builddir)/native.ini \
	--cross-file $(builddir)/cross.ini \
	--libexecdir $(PREFIX)/lib \
	--prefix $(PREFIX)

$(builddir)/stamp-configure: $(builddir)/native.ini $(builddir)/cross.ini
	$(env) $(MESON) setup $(conf-args) $(srcdir) $(builddir)
	touch $@

$(builddir)/stamp-build: $(builddir)/stamp-configure
	$(env) $(NINJA) -C $(builddir) $(build-args)
	touch $@

$(builddir)/stamp-install:
	$(env) $(FAKEROOT) $(NINJA) -C $(builddir) install
