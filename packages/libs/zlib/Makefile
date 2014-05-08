include $(TOP_SRCDIR)/packages/common.mk

conf-env = \
	CC='$(CROSS_COMPILE)gcc' \
	CFLAGS='--sysroot $(SYSROOT)'

conf-args = \
	--prefix=$(PREFIX) \

$(srcdir)/stamp-configure:
	cd $(srcdir) && \
		$(conf-env) ./configure $(conf-args)
	touch $@

build-args = \
	-j $(JOBS)

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && \
		$(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)'

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && \
		fakeroot $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
