include $(TOP_SRCDIR)/packages/autotools.mk

# make sure to lock the source directory when building from a symlinked
# source, otherwise two concurrent builds might step on each others' toes
ifneq ($(realpath $(srcdir)),$(srcdir))
$(builddir)/stamp-patch: $(srcdir)/lock | $(builddir)
	cd $(srcdir) && autoreconf --force --install
	touch $@

$(builddir)/stamp-configure: $(builddir)/stamp-patch

install: $(srcdir)/unlock
endif

conf-args += \
	--with-sysroot=$(SYSROOT)
