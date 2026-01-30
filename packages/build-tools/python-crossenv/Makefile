include $(TOP_SRCDIR)/packages/build-tools/python.mk

$(srcdir)/stamp-createenv: $(srcdir)/stamp-install
	$(BUILD_TOOLS)/bin/python3 -m crossenv --sysroot '$(SYSROOT)' \
		'$(SYSROOT)$(PREFIX)/bin/python3' '$(BUILD_TOOLS)/python'
	touch $@

install: $(srcdir)/stamp-createenv
