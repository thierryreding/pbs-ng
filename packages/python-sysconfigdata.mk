ifeq ($(ARCH),arm64)
  ARCH = aarch64
endif

MULTIARCH = $(ARCH)-$(OS)-$(LIBC)$(ABI)

env += \
	_PYTHON_SYSCONFIGDATA_NAME=_sysconfigdata__$(OS)_$(MULTIARCH)
