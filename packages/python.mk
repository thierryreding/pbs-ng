include $(TOP_SRCDIR)/packages/common.mk

ifeq ($(ARCH),arm64)
  ARCH = aarch64
endif

MULTIARCH = $(ARCH)-$(OS)-$(LIBC)$(ABI)

env += \
	_PYTHON_SYSCONFIGDATA_NAME=_sysconfigdata__$(OS)_$(MULTIARCH)

env += \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && $(env) python3 setup.py build $(build-args)
	touch $@

install-args += \
	--prefix=$(PREFIX) \
	--root=$(DESTDIR)

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && $(env) python3 setup.py install $(install-args)
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
