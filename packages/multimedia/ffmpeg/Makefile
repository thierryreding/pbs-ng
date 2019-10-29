include $(TOP_SRCDIR)/packages/autotools.mk

conf-args = \
	--prefix=$(PREFIX) \
	--pkg-config=pkg-config \
	--cross-prefix=$(HOST)- \
	--enable-cross-compile \
	--target-os=$(OS) \
	--arch=$(ARCH) \
	--sysroot=$(SYSROOT) \
	--enable-shared \
	--enable-gpl \
	--enable-postproc \
	--enable-swscale \
	--disable-stripping

conf-vars :=
