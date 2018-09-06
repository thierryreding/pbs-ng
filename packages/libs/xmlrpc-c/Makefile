include $(TOP_SRCDIR)/packages/autotools.mk

builddir = $(srcdir)

conf-args += \
	--enable-curl-client

conf-vars += \
	ac_cv_prog_have_curl_config=no

build-args += \
	CC_FOR_BUILD=$(GCC) \
	CFLAGS_FOR_BUILD='-O2 -g' \
	LDFLAGS_FOR_BUILD='' \
	CPPFLAGS='$(CPPFLAGS)' \
	CFLAGS='$(CFLAGS)' \
	CXXFLAGS='$(CXXFLAGS)' \
	LDFLAGS='$(LDFLAGS)'
