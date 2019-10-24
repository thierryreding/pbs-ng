include $(TOP_SRCDIR)/packages/autotools.mk

$(builddir)/stamp-prepare: | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(builddir)/stamp-prepare

conf-args += \
	--with-sysroot=$(SYSROOT)
