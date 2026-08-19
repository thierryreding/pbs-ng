include $(TOP_SRCDIR)/packages/common.mk

$(builddir)/stamp-build:
	touch $@

$(builddir)/stamp-install: | $(DESTDIR)
	@echo "Installing for $(package.option.soc)"
	for subdir in common $(package.option.soc); do \
		cp -a $(TOP_SRCDIR)/$(PKGDIR)/src/$$subdir/* $(DESTDIR); \
	done
	touch $@
