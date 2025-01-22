include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

install-args = \
	FIRMWAREDIR='$(PREFIX)/lib/firmware' \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-install: | $(builddir)
	cd $(srcdir) && $(MAKE) $(install-args) install
	cd $(srcdir) && $(MAKE) $(install-args) dedup
	touch $@

install: $(builddir)/stamp-install

version:
	@cd $(srcdir) && $(MAKE) version

.PHONY: install version
