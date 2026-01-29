include $(TOP_SRCDIR)/packages/common.mk

$(srcdir)/stamp-install: | $(srcdir)
	cd $(srcdir) && \
		install -Dm 644 nuklear.h -t "$(DESTDIR)$(PREFIX)/include"
	touch $@

install: $(srcdir)/stamp-install
