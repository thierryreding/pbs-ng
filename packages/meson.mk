include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

ifeq ($(ARCH),arm64)
  ARCH = aarch64
endif

meson-vars = \
	OS ARCH CPU ENDIAN HOST SYSROOT PREFIX BUILD_TOOLS

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

env = \
	DESTDIR=$(DESTDIR)

conf-args = \
	--native-file $(builddir)/native.ini \
	--cross-file $(builddir)/cross.ini \
	--libexecdir $(PREFIX)/lib \
	--prefix $(PREFIX)

$(builddir)/stamp-configure: $(builddir)/native.ini $(builddir)/cross.ini
	$(env) meson setup $(conf-args) $(srcdir) $(builddir)
	touch $@

$(builddir)/stamp-build: $(builddir)/stamp-configure
	$(env) ninja -C $(builddir)
	touch $@

$(builddir)/stamp-install: $(builddir)/stamp-build
	$(env) $(FAKEROOT) ninja -C $(builddir) install

install: $(builddir)/stamp-install

.PHONY: install

ifeq ($(FORCE),y)
.PHONY: $(builddir)/stamp-build
endif
