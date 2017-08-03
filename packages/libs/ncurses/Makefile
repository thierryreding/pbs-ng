include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/gcc-5.1.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

conf-args += \
	--with-pkg-config-libdir=$(PREFIX)/lib/pkgconfig \
	--enable-pc-files \
	--enable-widec \
	--with-normal \
	--with-shared \
	--without-ada \
	--without-cxx

$(builddir)/stamp-install-compat: $(builddir)/stamp-build
	mkdir -p $(DESTDIR)$(PREFIX)/lib/pkgconfig
	for lib in form menu ncurses panel; do \
		echo "INPUT(-l$${lib}w)" > $(DESTDIR)$(PREFIX)/lib/lib$${lib}.so; \
		ln -s $${lib}w.pc $(DESTDIR)$(PREFIX)/lib/pkgconfig/$${lib}.pc; \
	done
	touch $@

install: $(builddir)/stamp-install-compat
