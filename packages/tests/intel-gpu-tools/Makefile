include $(TOP_SRCDIR)/packages/meson.mk

ifneq ($(realpath $(srcdir)),$(srcdir))
version:
	@cd $(srcdir) && git describe --abbrev=12 | sed s/igt-gpu-tools-//
endif

conf-args += \
	-Dbuild_chamelium=true
