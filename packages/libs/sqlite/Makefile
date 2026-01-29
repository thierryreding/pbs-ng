include $(TOP_SRCDIR)/packages/autotools.mk

#
# This is a bit complicated. On one hand we want to reuse the common
# autotools build snippet, but we want to run it in a subdirectory that
# will be created during a preparation step.
#
# So we redirect srcdir to the subdirectory for autotools.mk and then
# we need to make sure that the stamp-prepare target uses the old source
# directory.
#
topdir := $(srcdir)
srcdir := $(srcdir)/mkpkg_tmp_dir

$(topdir)/stamp-prepare: | $(topdir)
	cd $(topdir) && ./configure && $(MAKE) amalgamation-tarball
	cd $(srcdir) && $(MAKE) distclean
	touch $@

$(builddir)/stamp-configure: $(CURDIR)/source/stamp-prepare
