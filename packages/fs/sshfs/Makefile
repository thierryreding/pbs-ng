include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-prepare: | $(srcdir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-prepare

CFLAGS += \
	-D_FILE_OFFSET_BITS=64
