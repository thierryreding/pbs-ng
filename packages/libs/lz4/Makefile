# not a proper out-of-tree build,
builddir = $(srcdir)

include $(TOP_SRCDIR)/packages/common.mk

build-args = \
	CC='$(CROSS_COMPILE)gcc' \
	CXX='$(CROSS_COMPILE)g++' \
	CFLAGS='--sysroot $(SYSROOT)' \
	CXXFLAGS='--sysroot $(SYSROOT)'

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && \
		$(MAKE) -j $(JOBS) manuals
	cd $(srcdir) && \
		$(MAKE) $(build-args) -j $(JOBS) all
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)' \
	PREFIX='$(PREFIX)'

$(srcdir)/stamp-install:
	cd $(srcdir) && \
		$(MAKE) $(install-args) install
	touch $@
