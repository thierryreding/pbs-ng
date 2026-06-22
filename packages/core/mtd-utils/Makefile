include $(TOP_SRCDIR)/packages/autotools.mk

# mtd-utils 2.3.0 tarballs are missing some data files needed for the tests
# also, as of OpenSSL, some of the ENGINE_* APIs are no longer available, so
# disable the crypto support for now
conf-args += \
	--without-crypto \
	--without-tests
