include $(TOP_SRCDIR)/packages/cmake.mk

#
# build a native version of the stringify utility to be used during the
# cross-build later on
#
hostdir = $(CURDIR)/obj-native

$(hostdir):
	mkdir -p $@

$(hostdir)/bin/stringify: | $(hostdir)
	cd $(hostdir) && \
		$(env) cmake -DNO_OPENCL=ON -DNO_CLEW=ON -DNO_PTEX=ON -DOpenGL_GL_PREFERENCE=GLVND $(srcdir)
	cd $(hostdir) && $(env) $(MAKE) -C opensubdiv/tools/stringify

$(builddir)/stamp-configure: $(hostdir)/bin/stringify

$(srcdir)/stamp-patch: | $(srcdir)
	cd $(srcdir) && patch -p1 < $(TOP_SRCDIR)/$(PKGDIR)/patches/tbb-2021.patch
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-patch

#
# use the previously built stringify tool in the cross-build
#
cmake-args += \
	-DSTRINGIFY_LOCATION=$(hostdir)/bin/stringify \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-DNO_OPENCL=ON \ # XXX we really want this enabled
	-DNO_CLEW=ON \
	-DNO_PTEX=ON
