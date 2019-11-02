include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

conf-args += \
	--without-ensurepip \
	--with-system-expat \
	--with-system-ffi \
	--enable-shared

$(BUILD_TOOLS)/bin/python3: $(builddir)/stamp-install

$(BUILD_TOOLS)/bin/python: $(BUILD_TOOLS)/bin/python3
	ln -sf $(basename $<) $@

install: $(BUILD_TOOLS)/bin/python
