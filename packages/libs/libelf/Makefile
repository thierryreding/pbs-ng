include $(TOP_SRCDIR)/packages/autotools.mk

conf-args += \
	--disable-debuginfod

ifneq ($(realpath $(srcdir)),$(srcdir))
$(builddir)/stamp-patch: $(srcdir)/lock | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

conf-args += \
	--enable-maintainer-mode

$(builddir)/stamp-configure: $(builddir)/stamp-patch

install: $(srcdir)/unlock
endif
