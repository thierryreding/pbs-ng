include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

$(builddir)/stamp-install: | $(builddir) $(DESTDIR)
	@echo "Installing for $(package.option.soc)"
	cp -a $(TOP_SRCDIR)/$(PKGDIR)/src/* $(DESTDIR)
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
