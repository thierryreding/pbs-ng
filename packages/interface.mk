# PBS interface

$(builddir):
	mkdir -p $@

# phony targets to make it easy to call these targets
build: $(builddir)/stamp-build
install: $(builddir)/stamp-install
.PHONY: build install

# if a build is forced, mark the build stamp as phony so that is rerun
ifeq ($(FORCE),y)
.PHONY: $(builddir)/stamp-build
endif

# dependency and lifecycle
$(builddir)/stamp-build: | $(builddir)
$(builddir)/stamp-install: $(builddir)/stamp-build
