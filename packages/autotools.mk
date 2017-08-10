include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

conf-env = \
	PKG_CONFIG_LIBDIR='$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)$(PREFIX)/share/pkgconfig' \
	PKG_CONFIG_SYSROOT_DIR='$(SYSROOT)'

conf-args = \
	--build=$(BUILD) \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--mandir=$(PREFIX)/share/man \
	--infodir=$(PREFIX)/share/info \
	--localstatedir=/var \
	--sysconfdir=/etc

conf-vars = \
	CPPFLAGS='$(CPPFLAGS)' \
	CXXFLAGS='$(CXXFLAGS)' \
	CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)'

$(builddir)/stamp-configure: | $(builddir)
	cd $(builddir) && \
		$(conf-env) $(srcdir)/configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(builddir)/stamp-build: $(builddir)/stamp-configure
	cd $(builddir) && \
		$(env) $(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)'

$(builddir)/stamp-install: $(builddir)/stamp-build
	cd $(builddir) && \
		$(FAKEROOT) $(MAKE) $(install-args) install
	touch $@

install: $(builddir)/stamp-install

.PHONY: install

ifeq ($(FORCE),y)
.PHONY: $(builddir)/stamp-build
endif

# These are useful if the source directory needs to be exclusively accessed
# for a given build. This can be required if an autotools-based package needs
# to be reconfigured (i.e. using autoreconf). Concurrent builds will mess up
# the source directory if autoreconf runs while another process is running
# the configure script, for example.
#
# To use these, make sure the target that runs autoreconf has a dependency on
# the $(srcdir)/lock target. To ensure that the source directory can be reused
# for new builds again, make sure to make your install: target depend on
# $(srcdir)/unlock.
#
$(srcdir)/pbs.lock:
	lockfile $@

$(srcdir)/lock: $(srcdir)/pbs.lock

$(srcdir)/unlock: $(builddir)/stamp-install
	rm -f $(srcdir)/pbs.lock

.PHONY: $(srcdir)/pbs.lock $(srcdir)/lock $(srcdir)/unlock
