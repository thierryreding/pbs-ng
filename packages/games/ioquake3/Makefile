include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

env = env -i PATH='$(PATH)' \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

common-args += \
	COPYDIR='$(DESTDIR)$(PREFIX)/lib/ioquake3' \
	DEFAULT_BASEDIR='$(PREFIX)/lib/ioquake3' \
	COPYBINDIR='$(DESTDIR)$(PREFIX)/bin' \
	BUILD_DIR='$(builddir)' \
	BUILD_RENDERER_OPENGL2=1 \
	PLATFORM=linux \
	FULLBINEXT='' \
	ARCH=$(ARCH) \
	NO_STRIP=1

build-args += \
	$(common-args) \
	CC='$(CROSS_COMPILE)gcc' \
	PKG_CONFIG='pkg-config' \
	CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)' \
	-j $(JOBS)

$(builddir)/stamp-build: | $(builddir)
	cd $(srcdir) && \
		$(env) $(MAKE) $(build-args) release
	touch $@

install-args += \
	$(common-args) \
	-j $(JOBS)

$(builddir)/stamp-install: $(builddir)/stamp-build
	mkdir -p '$(DESTDIR)$(PREFIX)/lib/ioquake3' && \
		mkdir -p '$(DESTDIR)$(PREFIX)/bin'
	cd $(srcdir) && \
		$(env) $(MAKE) $(install-args) copyfiles
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
