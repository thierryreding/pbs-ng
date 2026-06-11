include $(TOP_SRCDIR)/packages/common.mk

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) &&  $(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR=$(DESTDIR)

$(srcdir)/stamp-install: | $(srcdir)/stamp-build
	cd $(srcdir) && $(MAKE) $(install-args) install
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
