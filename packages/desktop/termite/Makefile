include $(TOP_SRCDIR)/packages/common.mk

env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)' \
	CXXFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)' \
	CXX=$(CROSS_COMPILE)g++

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && git submodule init && git submodule sync && \
		git submodule update
	cd $(srcdir) && \
		$(env) $(MAKE) -j $(JOBS)
	touch $@

install-args = \
	DESTDIR=$(DESTDIR)

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		$(env) $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
