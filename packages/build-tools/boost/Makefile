include $(TOP_SRCDIR)/packages/build-tools/common.mk

conf-args = \
	--prefix=$(prefix)

$(srcdir)/stamp-configure: | $(srcdir)
	cd $(srcdir) && ./bootstrap.sh $(conf-args)
	touch $@

build-args = \
	--layout=system

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && ./b2 $(build-args)
	touch $@

install-args = \
	--includedir=$(BUILD_TOOLS)/include \
	--libdir=$(BUILD_TOOLS)/lib

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && ./b2 install $(build-args) $(install-args)
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
