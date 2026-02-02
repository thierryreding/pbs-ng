include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

conf-args += \
	--with-python=$(BUILD_TOOLS)

$(builddir)/stamp-postinstall: $(builddir)/stamp-install
	rm -f $(BUILD_TOOLS)/lib/libxml2.la

install: $(builddir)/stamp-postinstall
