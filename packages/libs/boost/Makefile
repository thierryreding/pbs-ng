include $(TOP_SRCDIR)/packages/common.mk

conf-args = \
	--prefix=$(prefix)

$(srcdir)/stamp-configure: | $(srcdir)
	cd $(srcdir) && ./bootstrap.sh $(conf-args)
	touch $@

$(srcdir)/user-config.jam: $(TOP_SRCDIR)/support/user-config.jam.in | $(srcdir)
	sed 's|@ARCH@|$(ARCH)|;s|@HOST@|$(HOST)|;s|@SYSROOT@|$(SYSROOT)|;s|@OS@|$(OS)|' $< > $@

build-args = \
	--user-config=$(srcdir)/user-config.jam \
	--layout=system

build-vars = \
	toolset=gcc

ifeq ($(ARCH),arm64)
build-vars += \
	architecture=arm \
	address-model=64 \
	abi=aapcs
endif

$(srcdir)/stamp-build: $(srcdir)/stamp-configure $(srcdir)/user-config.jam
	cd $(srcdir) && ./b2 $(build-args) $(build-vars)
	touch $@

install-args = \
	--includedir=$(DESTDIR)$(PREFIX)/include \
	--libdir=$(DESTDIR)$(PREFIX)/lib

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && ./b2 install $(build-args) $(install-args) $(build-vars)
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
