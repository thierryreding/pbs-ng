include $(TOP_SRCDIR)/packages/build-tools/common.mk

$(builddir): | $(srcdir)
	mkdir -p $@

install-args += \
	--prefix=$(BUILD_TOOLS)

$(builddir)/stamp-install: | $(builddir)
	cd $(builddir) && $(env) python3 -m pip install $(install-args) $(srcdir)
	touch $@

install: $(builddir)/stamp-install

.PHONY: install

ifeq ($(FORCE),y)
.PHONY: $(builddir)/stamp-install
endif
