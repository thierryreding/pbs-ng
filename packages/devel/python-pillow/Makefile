include $(TOP_SRCDIR)/packages/python.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/cross-compile.patch
	touch $@

$(srcdir)/stamp-build: $(srcdir)/stamp-patch

common-args = \
	build_ext \
	--disable-platform-guessing \
	--debug

build-args = \
	$(common-args)

install-args = \
	$(common-args) \
	install \
	--prefix $(PREFIX) \
	--root=$(DESTDIR)
