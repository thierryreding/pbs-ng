include $(TOP_SRCDIR)/packages/autotools.mk

conf-args += \
	--enable-curl-client

conf-vars += \
	ac_cv_prog_have_curl_config=no

$(srcdir)/stamp-patch:
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/out-of-tree.patch
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/expat-backend.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

build-args += \
	BUILDTOOL_CC=$(GCC) \
	BUILDTOOL_CCLD=$(GCC) \
	CPPFLAGS='$(CPPFLAGS)' \
	CFLAGS='$(CFLAGS)' \
	CXXFLAGS='$(CXXFLAGS)' \
	LDFLAGS='$(LDFLAGS)'
