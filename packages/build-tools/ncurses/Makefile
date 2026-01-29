include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

# allow building with gcc >= 15
CFLAGS += '-std=gnu17'

conf-args += \
	--with-default-terminfo-dir=$(BUILD_TOOLS)/share/terminfo \
	--with-versioned-syms \
	--with-termlib=tinfo \
	--with-ticlib=tic \
	--disable-root-access \
	--disable-root-environ \
	--disable-setuid-environ \
	--disable-stripping \
	--enable-pc-files \
	--enable-widec \
	--with-normal \
	--with-shared
