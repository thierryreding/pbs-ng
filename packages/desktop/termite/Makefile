include $(TOP_SRCDIR)/packages/common.mk

build-args = \
	CXXFLAGS='--sysroot $(SYSROOT)' \
	LDFLAGS='--sysroot $(SYSROOT)'

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && \
		$(env) $(MAKE) -j $(JOBS) $(build-args)
	touch $@

install-args = \
	DESTDIR=$(DESTDIR)

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		$(env) $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
