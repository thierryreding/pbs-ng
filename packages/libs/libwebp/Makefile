include $(TOP_SRCDIR)/packages/autotools.mk

$(builddir)/stamp-patch: | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(builddir)/stamp-patch

conf-args += \
	--with-sysroot=$(SYSROOT) \
	--enable-everything
