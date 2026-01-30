# out-of-tree builds are currently broken
builddir = $(srcdir)

include $(TOP_SRCDIR)/packages/autotools.mk

$(builddir)/stamp-prepare: | $(srcdir)
	cd $(srcdir) && autoreconf --force --install --verbose
	touch $@

conf-args += \
	--with-system-luajit \
	--with-system-ck \
	--without-mysql

conf-vars += \
	ac_cv_prog_XSLTPROC=false

$(srcdir)/stamp-configure: $(srcdir)/stamp-prepare
