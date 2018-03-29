include $(TOP_SRCDIR)/packages/common.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/llvm-bindir.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/llvm-cxxflags.patch
	touch $@

env += \
	LD_LIBRARY_PATH=$(BUILD_TOOLS)/lib

conf-args += \
	--with-llvm-config=$(BUILD_TOOLS)/bin/$(HOST)-llvm-config \
	--with-llvm-cxxflags='-I$(BUILD_TOOLS)/include' \
	--with-llvm-bindir=$(BUILD_TOOLS)/bin \
	--prefix=$(PREFIX)

$(srcdir)/stamp-configure: $(srcdir)/stamp-patch
	cd $(srcdir) && \
		./configure.py $(conf-args)
	touch $@

build-args += \
	-j $(JOBS)

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && \
		$(env) $(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR=$(DESTDIR)

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		$(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install

ifeq ($(FORCE),y)
.PHONY: $(srcdir)/stamp-build
endif
