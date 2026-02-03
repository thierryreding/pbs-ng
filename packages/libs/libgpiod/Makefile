include $(TOP_SRCDIR)/packages/autotools.mk

$(srcdir)/configure: | $(srcdir)
	cd $(srcdir) && NOCONFIGURE=1 ./autogen.sh

$(builddir)/stamp-configure: $(srcdir)/configure

conf-args += \
	--with-sysroot=$(SYSROOT) \
	--enable-tools

# XXX Remove this workaround? The build suddenly started happening with
# libgpiod v2.2 and this fixes it.
conf-args += \
	--disable-dependency-tracking
