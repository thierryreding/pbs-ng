include $(TOP_SRCDIR)/packages/cmake.mk

srcdir := $(srcdir)/Sources

$(builddir)/tools: | $(builddir)
	mkdir -p $@

$(builddir)/tools/ecc: | $(builddir)/tools
	cd $(builddir)/tools && \
		$(env) cmake $(srcdir)
	cd $(builddir)/tools && \
		$(env) $(MAKE) ecc

$(builddir)/stamp-configure: $(builddir)/tools/ecc

cmake-args += \
	-DECC=$(builddir)/tools/ecc \
	-DCMAKE_BUILD_TYPE=Debug
