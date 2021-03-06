include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

ifeq ($(ARCH),arm64)
  ARCH = aarch64
endif

cross-vars = \
	OS ARCH CPU ENDIAN HOST SYSROOT PREFIX

cross-flags = \
	CPPFLAGS CFLAGS CXXFLAGS LDFLAGS

$(foreach var,$(cross-flags),$(eval flags_$(var) = $$($(var))))
$(foreach var,$(cross-flags),$(eval flags_$(var) = $(patsubst %,'%',$(flags_$(var)))))
$(foreach var,$(cross-flags),$(eval flags_$(var) = $(subst $(space),$(comma) ,$(flags_$(var)))))

$(foreach var,$(cross-vars),$(eval expressions += -e "s|@$(var)@|$$($(var))|g"))
$(foreach var,$(cross-flags),$(eval expressions += -e "s|@$(var)@|$(flags_$(var))|g"))

$(builddir)/cross-compile.txt: $(TOP_SRCDIR)/support/cross-compile.meson | $(builddir)
	sed $(expressions) $< > $@

env = \
	DESTDIR=$(DESTDIR)

conf-args = \
	--prefix $(PREFIX) \
	--libexecdir $(PREFIX)/lib

$(builddir)/stamp-configure: $(builddir)/cross-compile.txt
	$(env) meson --cross-file $< $(conf-args) $(srcdir) $(builddir)
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
