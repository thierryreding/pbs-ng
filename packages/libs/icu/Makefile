include $(TOP_SRCDIR)/packages/autotools.mk

hostdir := $(CURDIR)/obj-$(BUILD)

host-build-args = \
	-j $(JOBS)

$(hostdir):
	mkdir -p $@

host-conf-env = \
	PKG_CONFIG_LIBDIR=$(BUILD_TOOLS)/lib/pkgconfig

host-conf-args = \
	--prefix=$(BUILD_TOOLS)

$(hostdir)/stamp-configure: | $(hostdir)
	cd $(hostdir) && \
		$(host-conf-env) $(srcdir)/configure $(host-conf-args)
	touch $@

$(hostdir)/stamp-build: $(hostdir)/stamp-configure
	cd $(hostdir) && $(host-env) $(MAKE) $(host-build-args)
	touch $@

$(builddir)/stamp-configure: $(hostdir)/stamp-build

srcdir := $(srcdir)/icu4c/source

conf-args += \
	--with-cross-build=$(hostdir)
