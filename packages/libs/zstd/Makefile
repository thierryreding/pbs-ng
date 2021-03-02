include $(TOP_SRCDIR)/packages/common.mk

build-args = \
	CC='$(CROSS_COMPILE)gcc' \
	CXX='$(CROSS_COMPILE)g++' \
	CFLAGS='--sysroot $(SYSROOT)' \
	CXXFLAGS='--sysroot $(SYSROOT)'

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && \
		$(MAKE) -j $(JOBS) manual
	cd $(srcdir) && \
		$(MAKE) $(build-args) -j $(JOBS) programs
	cd $(srcdir) && \
		$(MAKE) $(build-args) -j $(JOBS) all
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)' \
	PREFIX='$(PREFIX)'

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		$(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
