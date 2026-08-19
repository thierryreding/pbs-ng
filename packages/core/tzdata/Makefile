# not a proper out-of-tree build,
builddir = $(srcdir)

include $(TOP_SRCDIR)/packages/common.mk

$(srcdir)/stamp-build:
	cd $(srcdir) &&  $(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR=$(DESTDIR)

$(srcdir)/stamp-install:
	cd $(srcdir) && $(MAKE) $(install-args) install
	touch $@
