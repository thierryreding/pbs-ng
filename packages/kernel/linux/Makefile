include $(TOP_SRCDIR)/packages/common.mk
include config.mk

unexport srctree objtree

common-args = \
	-C '$(KERNELSRC)' \
	--no-print-directory \
	-j $(JOBS)

common-vars = \
	CROSS_COMPILE='$(CROSS_COMPILE)' \
	KBUILD_OUTPUT='$(CURDIR)/build' \
	ARCH='$(ARCH)'

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

$(CURDIR)/build $(DESTDIR)/boot:
	mkdir -p $@

configure: $(CURDIR)/build
	$(MAKE) $(common-args) $(common-vars) tegra_defconfig

build: configure
	$(MAKE) $(common-args) $(common-vars) $(build-targets)

install: build | $(CURDIR)/build $(DESTDIR)/boot
	$(MAKE) $(install-args) $(install-vars) $(install-targets)
	find $(DESTDIR)$(PREFIX)/include -name .install -o -name ..install.cmd -delete
