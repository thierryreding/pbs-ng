include $(TOP_SRCDIR)/packages/autotools.mk

conf-args += \
	--disable-gles-tests \
	--enable-cgc

version:
	@cd $(srcdir) && git describe --abbrev=12 --always --tags
