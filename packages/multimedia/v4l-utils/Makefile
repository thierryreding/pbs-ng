include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-prepare: | $(srcdir)
	cd $(srcdir) && autoreconf --force --install --verbose
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-prepare

conf-args += \
	--with-sysroot=$(SYSROOT) \
	--disable-rpath
