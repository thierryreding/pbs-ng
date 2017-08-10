include $(TOP_SRCDIR)/packages/autotools.mk

# make sure to lock the source directory when building from a symlinked
# source, otherwise two concurrent builds might step on each others' toes
ifeq ($(realpath $(srcdir)),$(srcdir))
$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/opentegra.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
else
$(builddir)/stamp-patch: $(srcdir)/lock
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(builddir)/stamp-patch

install: $(srcdir)/unlock
endif

conf-args += \
	--with-sysroot=$(SYSROOT) \
	--enable-glamor

conf-vars += \
	xorg_cv_MONOTONIC_CLOCK=yes

$(builddir)/stamp-cleanup: $(builddir)/stamp-install
	find $(DESTDIR) -name '*.la' -delete
	touch $@

install: $(builddir)/stamp-cleanup
