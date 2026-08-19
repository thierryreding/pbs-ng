# not a proper out-of-tree build,
builddir = $(srcdir)

include $(TOP_SRCDIR)/packages/common.mk

conf-args = \
	--cross-compile-prefix=$(HOST)- \
	--prefix=$(PREFIX) \
	--openssldir=/etc/ssl \
	shared zlib-dynamic \
	linux-generic32 \
	'$(CFLAGS)'

$(srcdir)/stamp-configure:
	cd $(srcdir) && \
		$(conf-env) ./Configure $(conf-args) $(conf-vars)
	touch $@

build-args = \
	-j $(JOBS)

$(srcdir)/stamp-build: $(srcdir)/stamp-configure
	cd $(srcdir) && \
		$(MAKE) $(build-args)
	touch $@

install-args = \
	DESTDIR='$(DESTDIR)' \
	MANSUFFIX=ssl

$(srcdir)/stamp-install:
	cd $(srcdir) && \
		$(MAKE) $(install-args) install
	touch $@
