include $(TOP_SRCDIR)/packages/common.mk

install-args = \
	FIRMWAREDIR='$(PREFIX)/lib/firmware' \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-build:
	touch $@

$(builddir)/stamp-install:
	cd $(srcdir) && $(MAKE) $(install-args) install
	cd $(srcdir) && $(MAKE) $(install-args) dedup
	touch $@

version:
	@cd $(srcdir) && $(MAKE) version

.PHONY: version
