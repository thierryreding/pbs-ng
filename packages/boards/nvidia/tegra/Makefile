include $(TOP_SRCDIR)/packages/common.mk

$(builddir) $(DESTDIR):
	mkdir -p $@

$(builddir)/stamp-install: | $(builddir) $(DESTDIR)
	@echo "Installing for $(package.option.soc)"
	for subdir in common $(package.option.soc); do \
		cp -a $(TOP_SRCDIR)/$(PKGDIR)/src/$$subdir/* $(DESTDIR); \
	done
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
