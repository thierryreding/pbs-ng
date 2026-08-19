# not a proper out-of-tree build
builddir = $(srcdir)

include $(TOP_SRCDIR)/packages/common.mk
include $(TOP_SRCDIR)/packages/python-sysconfigdata.mk

env += \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

install-args += \
	--prefix=$(PREFIX) \
	--root=$(DESTDIR)

$(srcdir)/stamp-install:
	cd $(srcdir) && $(env) python3 -m pip install $(install-args) .
	touch $@
