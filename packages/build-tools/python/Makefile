include $(TOP_SRCDIR)/packages/build-tools/autotools.mk

conf-args += \
	--with-system-expat \
	--with-system-ffi \
	--with-system-libmpdec \
	--enable-shared

$(BUILD_TOOLS)/bin/python3: $(builddir)/stamp-install
	# make sure pip is up-to-date
	$(BUILD_TOOLS)/bin/pip3 install --upgrade pip

$(BUILD_TOOLS)/bin/python: $(BUILD_TOOLS)/bin/python3
	ln -sf $(basename $<) $@

install: $(BUILD_TOOLS)/bin/python
