include $(TOP_SRCDIR)/packages/common.mk

build-args += \
	CC='$(CROSS_COMPILE)gcc' \
	CXX='$(CROSS_COMPILE)g++' \
	OBJDUMP='$(CROSS_COMPILE)objdump' \
	-j $(JOBS)

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && $(MAKE) $(build-args)
	touch $@

install-args += \
	CC='$(CROSS_COMPILE)gcc' \
	CXX='$(CROSS_COMPILE)g++' \
	OBJDUMP='$(CROSS_COMPILE)objdump' \
	DESTDIR='$(DESTDIR)'

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
