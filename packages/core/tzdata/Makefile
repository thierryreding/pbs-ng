include $(TOP_SRCDIR)/packages/common.mk

$(builddir):
	mkdir -p $@

TIMEZONES = \
	africa \
	antarctica \
	asia \
	australasia \
	europe \
	northamerica \
	southamerica \
	pacificnew \
	etcetera \
	backward \
	systemv \
	factory

$(TIMEZONES):
	cd $(srcdir) && \
		zic -y ./yearistype -d $(DESTDIR)$(PREFIX)/share/zoneinfo $@

$(builddir)/stamp-install: | $(builddir)
	cd $(srcdir) && \
		zic -y ./yearistype -d $(DESTDIR)$(PREFIX)/share/zoneinfo
	touch $@

install: $(builddir)/stamp-install

.PHONY: install
