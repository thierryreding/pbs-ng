include $(TOP_SRCDIR)/packages/autotools.mk

#
# SDL does no longer build against Mesa if GLES1 is enabled. However, if we
# don't enable GLES1 support in Mesa, we can't build the GLES1 tests. Disable
# them.
#
conf-args += \
	--disable-gles1
