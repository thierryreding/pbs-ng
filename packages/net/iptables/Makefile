include $(TOP_SRCDIR)/packages/autotools.mk
include config.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && ln -rs libiptc/linux_list.h include/libiptc
	cd $(srcdir) && autoreconf --force --install
	touch $@

conf-args += \
	--with-sysroot=$(SYSROOT)

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

JOBS := 1
