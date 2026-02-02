include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

conf-args += \
	--disable-gssapi

$(builddir)/stamp-cleanup: $(builddir)/stamp-install
	rm -f $(BUILD_TOOLS)/lib/libtirpc.la

install: $(builddir)/stamp-cleanup
