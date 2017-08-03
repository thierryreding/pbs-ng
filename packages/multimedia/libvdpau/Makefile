include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/patches/ltmain-sysroot-2.4.6.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

conf-args += \
	--with-sysroot='$(SYSROOT)'

conf-vars += \
	CXXFLAGS='$(CXXFLAGS)'
