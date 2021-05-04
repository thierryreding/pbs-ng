include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-prepare: | $(srcdir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

conf-args += \
	--with-sysroot='$(SYSROOT)'

$(builddir)/stamp-configure: $(srcdir)/stamp-prepare
