include $(TOP_SRCDIR)/packages/common.mk

KERNELSRC ?= $(CURDIR)/source

common-args = \
	-C '$(KERNELSRC)' \
	-j $(JOBS)

common-vars = \
	CROSS_COMPILE='$(CROSS_COMPILE)' \
	KBUILD_OUTPUT='$(CURDIR)/build' \
	ARCH=$(ARCH)

defconfig = defconfig

ifeq ($(ARCH),arm)
  build-targets = zImage
else
  ifeq ($(ARCH),x86)
    build-targets = bzImage
  else
    build-targets = Image
  endif
endif

build-targets += all
build-targets += modules

install-args = \
	$(common-args)

install-vars = \
	INSTALL_HDR_PATH=$(DESTDIR)$(PREFIX) \
	INSTALL_PATH=$(DESTDIR)/boot \
	INSTALL_MOD_PATH=$(DESTDIR) \
	$(common-vars)

install-targets = \
	headers_install \
	zinstall \
	modules_install

env = env -i PATH=$(PATH) HOME=$(HOME)

$(builddir) $(DESTDIR)/boot:
	mkdir -p $@

$(builddir)/stamp-configure: | $(builddir)
	$(env) $(MAKE) $(common-args) $(common-vars) $(defconfig)
	touch $@

$(builddir)/stamp-build: $(builddir)/stamp-configure
	$(env) $(MAKE) $(common-args) $(common-vars) $(build-targets)
	touch $@

$(builddir)/stamp-install: $(builddir)/stamp-build | $(DESTDIR)/boot
	$(env) $(MAKE) $(install-args) $(install-vars) $(install-targets)
	find $(DESTDIR)$(PREFIX)/include -name .install -o -name ..install.cmd -delete
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
