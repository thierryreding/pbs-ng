include $(TOP_SRCDIR)/packages/meson.mk

ifeq ($(realpath $(srcdir)),$(srcdir))
$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/tests.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
endif

conf-args += \
	-Ddocs=false
