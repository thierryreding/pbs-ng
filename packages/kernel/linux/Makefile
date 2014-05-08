include $(TOP_SRCDIR)/packages/common.mk

unexport srctree objtree

KERNELSRC ?= $(CURDIR)/$(PACKAGE)-$(VERSION)

common-args = \
	-C '$(KERNELSRC)' \
	--no-print-directory \
	-j $(JOBS)

common-vars = \
	CROSS_COMPILE='$(CROSS_COMPILE)' \
	KBUILD_OUTPUT='$(CURDIR)/build' \
	ARCH=$(ARCH)

build-targets = \
	zImage \
	modules

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

$(CURDIR)/build $(DESTDIR)/boot:
	mkdir -p $@

configure: $(CURDIR)/build
	$(env) $(MAKE) $(common-args) $(common-vars) tegra_defconfig

build: configure
	$(env) $(MAKE) $(common-args) $(common-vars) $(build-targets)

install: build | $(CURDIR)/build $(DESTDIR)/boot
	$(env) $(MAKE) $(install-args) $(install-vars) $(install-targets)
	find $(DESTDIR)$(PREFIX)/include -name .install -o -name ..install.cmd -delete
