include $(TOP_SRCDIR)/packages/autotools.mk

major = $(word 1, $(subst ., ,$(package.version)))

conf-args += \
	--with-pkg-config-libdir=$(PREFIX)/lib/pkgconfig \
	--with-termlib=tinfo \
	--with-ticlib=tic \
	--disable-stripping \
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
	# don't require -ltinfo when linking with --no-add-needed
	rm -f $(DESTDIR)$(PREFIX)/lib/libncursesw.so && \
		echo 'INPUT(libncursesw.so.$(major) -ltinfo)' \
			> $(DESTDIR)$(PREFIX)/lib/libncursesw.so
	touch $@

install: $(builddir)/stamp-install-compat
