include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

$(srcdir)/stamp-prepare: | $(srcdir)
	cd $(srcdir) && autoreconf --force --install --verbose
	touch $@

$(builddir)/stamp-configure: $(srcdir)/stamp-prepare

conf-args += \
	--disable-liblastlog2 \
	--disable-mount \
	--disable-su \
	--disable-wall

$(builddir)/stamp-cleanup: $(builddir)/stamp-install
	# libtool will sometimes try to link against build libraries, so
	# remove the libtool archives to prevent that
	rm -f $(BUILD_TOOLS)/lib/lib{blkid,fdisk,mount,smartcols,uuid}.la
	touch $@

install: $(builddir)/stamp-cleanup
