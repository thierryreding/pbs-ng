include $(TOP_SRCDIR)/packages/autotools.mk

ifeq ($(realpath $(srcdir)),$(srcdir))
$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/patches/ltmain-sysroot-2.4.2.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch
endif

conf-args += \
	--with-sysroot='$(SYSROOT)'
