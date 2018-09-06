include $(TOP_SRCDIR)/packages/autotools.mk

# make sure to lock the source directory when building from a symlinked
# source, otherwise two concurrent builds might step on each others' toes
ifneq ($(realpath $(srcdir)),$(srcdir))
$(builddir)/stamp-patch: $(srcdir)/lock | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(builddir)/stamp-patch

install: $(srcdir)/unlock
else
$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/glibc-2.28.patch
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
endif

conf-args += \
	--with-sysroot=$(SYSROOT) \
	--disable-rpath
