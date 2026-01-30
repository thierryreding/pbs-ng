include $(TOP_SRCDIR)/packages/common.mk

build-args += \
	CROSS=$(CROSS_COMPILE) \
	-j $(JOBS)

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && $(env) $(MAKE) $(build-args)
	touch $@

install-args += \
	DESTDIR=$(DESTDIR) \
	PREFIX=$(PREFIX)

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && $(env) $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
