include $(TOP_SRCDIR)/packages/autotools.mk

# make sure to lock the source directory when building from a symlinked
# source, otherwise two concurrent builds might get in each others' way
ifneq ($(realpath $(srcdir)),$(srcdir))
$(builddir)/stamp-prepare: $(srcdir)/lock | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(builddir)/stamp-prepare

install: $(srcdir)/unlock

version:
	@cd $(srcdir) && git describe --abbrev=12 | sed s/intel-gpu-tools-//
endif

conf-vars += \
	ac_cv_prog_XMLRPC_C_CONFIG=no

conf-args += \
	--libexecdir=$(PREFIX)/lib \
	--disable-shader-debugger \
	--enable-chamelium
