include $(TOP_SRCDIR)/packages/common.mk

conf-args = \
	--config-cache \
	--build=$(BUILD) \
	--host=$(HOST) \
	--prefix=$(PREFIX) \
	--libdir=$(PREFIX)/lib \
	--mandir=$(PREFIX)/share/man \
	--infodir=$(PREFIX)/share/info \
	--localstatedir=/var \
	--sysconfdir=/etc \
	--with-tlib=ncurses \
	--enable-gui=no

conf-vars = \
	CPPFLAGS='$(CPPFLAGS)' \
	CFLAGS='$(CFLAGS)' \
	LDFLAGS='$(LDFLAGS)'

$(srcdir)/src/auto/config.cache: | $(srcdir)
	echo 'ac_cv_small_wchar_t=yes' > $@
	echo 'vim_cv_toupper_broken=no' >> $@
	echo 'vim_cv_terminfo=yes' >> $@
	echo 'vim_cv_tty_mode=0620' >> $@
	echo 'vim_cv_tty_group=tty' >> $@
	echo 'vim_cv_getcwd_broken=no' >> $@
	echo 'vim_cv_stat_ignores_slash=yes' >> $@
	echo 'vim_cv_memmove_handles_overlap=yes' >> $@
	echo 'vim_cv_tgetent=zero' >> $@

$(srcdir)/stamp-configure: $(srcdir)/src/auto/config.cache
	cd $(srcdir) && $(conf-env) ./configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && $(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)' \
	STRIP=:

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	cd $(srcdir) && $(MAKE) $(install-args) install

install: $(srcdir)/stamp-install

.PHONY: install
