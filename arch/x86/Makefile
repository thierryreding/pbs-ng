ARCH = $(arch)
ARCH_LONG = $(arch.generation)
ENDIAN = little

VENDOR = unknown
OS = linux
LIBC = gnu

ARCH_GEN = $(subst _,-,$(arch.generation))
ARCH_CPU = $(arch.cpu)

ifneq ($(filter core-i7 core-i9,$(arch.cpu)),)
  ARCH_CPU = corei7
endif

HOST = $(ARCH_LONG)-$(VENDOR)-$(OS)-$(LIBC)

ARCH_CPPFLAGS =
ARCH_ASFLAGS =
ARCH_CFLAGS = -march=$(ARCH_GEN) -mtune=$(ARCH_CPU) -O2 -g
ARCH_CXXFLAGS = -march=$(ARCH_GEN) -mtune=$(ARCH_CPU) -O2 -g
ARCH_LDFLAGS =
