include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

conf-args += \
	--datadir=$(prefix)/share/hwdata
