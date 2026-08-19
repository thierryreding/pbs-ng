include $(TOP_SRCDIR)/packages/common.mk

$(builddir)/stamp-build:
	touch $@

$(builddir)/stamp-install: | $(builddir) $(DESTDIR)
	for subdir in etc usr; do \
		cp -a $(TOP_SRCDIR)/$(PKGDIR)/src/$$subdir $(DESTDIR)/$$subdir; \
	done
	touch $@
