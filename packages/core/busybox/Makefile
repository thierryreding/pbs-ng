include $(TOP_SRCDIR)/packages/common.mk
include config.mk

common-args = \
	-j $(JOBS)

common-vars = \
	ARCH=$(ARCH) \
	CROSS_COMPILE=$(CROSS_COMPILE) \
	EXTRA_CPPFLAGS='--sysroot $(SYSROOT)' \
	EXTRA_CFLAGS='--sysroot $(SYSROOT)' \
	EXTRA_LDFLAGS='--sysroot $(SYSROOT)' \
	KBUILD_OUTPUT=$(builddir)

conf-args = $(common-args)
conf-vars = $(common-vars)

build-args = $(common-args)
build-vars = $(common-vars)

install-args = $(common-args)
install-vars = \
	CONFIG_PREFIX='$(DESTDIR)' \
	$(common-vars)

$(builddir):
	mkdir -p $@

$(builddir)/stamp-configure: | $(builddir)
	cd $(srcdir) && \
		$(MAKE) $(conf-args) $(conf-vars) defconfig
	touch $@

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(srcdir) && \
		$(MAKE) $(build-args) $(build-vars)
	touch $@

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(srcdir) && \
		$(MAKE) $(install-args) $(install-vars) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: configure build install
