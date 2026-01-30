include $(TOP_SRCDIR)/packages/common.mk

ifeq ($(ARCH),arm64)
  ARCH = aarch64
endif

MULTIARCH = $(ARCH)-$(OS)-$(LIBC)$(ABI)

MAJOR = $(word 1,$(subst ., ,$(package.version)))
MINOR = $(word 2,$(subst ., ,$(package.version)))

$(builddir):
	mkdir -p $@

$(builddir)/config.cache: | $(builddir)
	echo '# generated for $(HOST)' > $@
	echo 'ac_cv_buggy_getaddrinfo=no' >> $@
	echo 'ac_cv_file__dev_ptmx=yes' >> $@
	echo 'ac_cv_file__dev_ptc=no' >> $@

$(CURDIR)/export.mk:
	echo "PYTHON_MAJOR := $(MAJOR)"  > $@
	echo "PYTHON_MINOR := $(MINOR)" >> $@

conf-args = \
	--config-cache \
	--build=$(BUILD) \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--sysconfdir=/etc

conf-args += \
	--with-build-python=$(BUILD_TOOLS)/bin/python \
	--without-ensurepip \
	--with-system-libmpdec \
	--with-system-expat \
	--with-system-ffi \
	--enable-shared

conf-vars = \
	CPPFLAGS='$(CPPFLAGS)' \
	CFLAGS='$(CFLAGS)' \
	CXXFLAGS='$(CXXFLAGS)' \
	LDFLAGS='$(LDFLAGS)'

$(builddir)/stamp-configure: $(builddir)/config.cache $(CURDIR)/export.mk | $(builddir)
	cd $(builddir) && \
		$(conf-env) $(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	EXTRA_CFLAGS='$(CFLAGS)' \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(MAKE) $(build-args)
	touch $@

install-args = \
	EXTRA_CFLAGS='$(CFLAGS)' \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(MAKE) $(install-args) install
	ln -sf python$(MAJOR) $(DESTDIR)$(PREFIX)/bin/python
	touch $@

# install sysconfigdata file for cross-compilation of modules
SYSCONFIGDATA = _sysconfigdata__$(OS)_$(MULTIARCH).py

$(BUILD_TOOLS)/lib/python$(MAJOR).$(MINOR)/$(SYSCONFIGDATA): $(builddir)/build/lib.$(OS)-$(ARCH)-$(MAJOR).$(MINOR)/$(SYSCONFIGDATA)
	$(BUILD_TOOLS)/bin/python $(TOP_SRCDIR)/support/export-sysconfigdata $(SYSROOT) $< $@

$(builddir)/stamp-install: $(BUILD_TOOLS)/lib/python$(MAJOR).$(MINOR)/$(SYSCONFIGDATA)

install: $(builddir)/stamp-install

.PHONY: install
