include $(TOP_SRCDIR)/packages/build-tools/common.mk

install-args += \
	--prefix=$(BUILD_TOOLS)

$(builddir)/stamp-install: | $(builddir)
	cd $(builddir) && $(env) python3 -m pip install $(install-args) $(srcdir)
	touch $@
