include $(TOP_SRCDIR)/packages/autotools.mk

ifeq ($(realpath $(srcdir)),$(srcdir))
$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch | $(builddir)
else
$(builddir)/stamp-prepare: | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(builddir)/stamp-prepare
endif

conf-args += \
	--libexecdir=$(PREFIX)/lib \
	--disable-assembler \
	--disable-overlay \
	--disable-shader-debugger \
	--without-libunwind
