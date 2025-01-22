ifeq ($(ARCH),arm64)
  ARCH = aarch64
endif

LONGDOUBLE_FORMAT = $(ARCH_LONGDOUBLE_FORMAT)

meson-vars = \
	OS ARCH CPU ENDIAN HOST SYSROOT PREFIX BUILD_TOOLS LONGDOUBLE_FORMAT

meson-flags = \
	CPPFLAGS CFLAGS CXXFLAGS LDFLAGS

$(foreach var,$(meson-flags),$(eval flags_$(var) = $$($(var))))
$(foreach var,$(meson-flags),$(eval flags_$(var) = $(patsubst %,'%',$(flags_$(var)))))
$(foreach var,$(meson-flags),$(eval flags_$(var) = $(subst $(space),$(comma) ,$(flags_$(var)))))

$(foreach var,$(meson-vars),$(eval expressions += -e "s|@$(var)@|$$($(var))|g"))
$(foreach var,$(meson-flags),$(eval expressions += -e "s|@$(var)@|$(flags_$(var))|g"))

$(builddir)/native.ini: $(TOP_SRCDIR)/support/meson-native.ini | $(builddir)
	sed $(expressions) $< > $@

$(builddir)/cross.ini:: $(TOP_SRCDIR)/support/meson-cross.ini | $(builddir)
	sed $(expressions) $< > $@
