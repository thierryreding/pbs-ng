include $(TOP_SRCDIR)/packages/meson.mk

env += \
	PKG_CONFIG_FDO_SYSROOT_RULES=1

# gobject-introspection builds currently don't work
conf-args += \
	-Dintrospection=disabled \
	-Dgobject=enabled \
	-Ddocs=disabled
