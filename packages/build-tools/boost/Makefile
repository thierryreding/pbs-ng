include $(TOP_SRCDIR)/packages/build-tools/common.mk

conf-args = \
	--prefix=$(BUILD_TOOLS)

$(srcdir)/stamp-configure: | $(srcdir)
	cd $(srcdir) && ./bootstrap.sh $(conf-args)
	touch $@

common-args = \
	--layout=system

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && ./b2 $(common-args)
	touch $@

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && ./b2 install $(common-args)
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
