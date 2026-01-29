include $(TOP_SRCDIR)/packages/common.mk

SUBDIRS = \
	CPP/7zip/Bundles/Alone2

build-args = \
	CROSS_COMPILE=$(CROSS_COMPILE) \
	DISABLE_RAR=1 \
	-j $(JOBS)

$(srcdir)/stamp-build: | $(srcdir)
	cd $(srcdir) && for subdir in "$(SUBDIRS)"; do \
		$(env) $(MAKE) -C $$subdir -f ../../cmpl_gcc.mak $(build-args); \
	done
	touch $@

install-args += \
	DEST_DIR=$(DESTDIR) \
	DEST_HOME=$(PREFIX) \
	DEST_MAN=$(PREFIX)/share/man

$(srcdir)/stamp-install: $(srcdir)/stamp-build
	install -d $(DESTDIR)$(PREFIX)/bin
	install -m 755 -t $(DESTDIR)$(PREFIX)/bin $(srcdir)/CPP/7zip/Bundles/Alone2/b/g/7zz
	touch $@

install: $(srcdir)/stamp-install

.PHONY: install
