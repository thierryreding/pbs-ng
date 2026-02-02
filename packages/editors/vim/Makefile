include $(TOP_SRCDIR)/packages/autotools.mk

conf-args += \
	--config-cache \
	--with-tlib=ncurses \
	--enable-gui=no

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

install-args += \
	STRIP=:
