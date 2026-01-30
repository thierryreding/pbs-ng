include $(TOP_SRCDIR)/packages/common.mk
include $(TOP_SRCDIR)/packages/python-sysconfigdata.mk

env += \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

install-args += \
	--destdir=$(DESTDIR) \
	--prefix=$(PREFIX)

$(srcdir)/stamp-install: | $(srcdir)
	cd $(srcdir) && $(env) python3 -m build --wheel --no-isolation
	cd $(srcdir) && $(env) python3 -m installer $(install-args) dist/*.whl
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
