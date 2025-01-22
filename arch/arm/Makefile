ARCH = arm

ARCH_LONG = $(ARCH)

ifeq ($(arch.version),armv7-a)
  ARCH_LONG := $(ARCH_LONG)v7
endif

ifeq ($(arch.endian),little)
  ARCH_LONG := $(ARCH_LONG)l
  ENDIAN := little
endif

ifeq ($(arch.endian),big)
  ARCH_LONG := $(ARCH_LONG)b
  ENDIAN := big
endif

ifeq ($(arch.abi),eabi)
  ABI = eabi
endif

ifneq ($(arch.fpu),)
  ABI := $(ABI)hf
endif

VENDOR = unknown
OS = linux
LIBC = gnu

HOST = $(ARCH_LONG)-$(VENDOR)-$(OS)-$(LIBC)$(ABI)

MARCH=$(arch.version)

ifneq ($(arch.fpu),)
  ifeq ($(arch.extensions.neon),y)
    MARCH := $(MARCH)+neon-$(arch.fpu)
  else
    MARCH := $(MARCH)+$(arch.fpu)
  endif
endif

ARCH_CPPFLAGS =
ARCH_ASFLAGS = -march=$(MARCH) -m$(arch.endian)-endian

ARCH_CFLAGS = -O2 -g -marm -march=$(MARCH) -m$(arch.endian)-endian -Uarm

ifneq ($(arch.fpu),)
  ARCH_ASFLAGS += -mfloat-abi=hard
  ARCH_CFLAGS += -mfloat-abi=hard
endif

ifeq ($(arch.abi),eabi)
  ARCH_ASFLAGS += -mabi=aapcs-linux -mno-thumb-interwork
  ARCH_CFLAGS += -mabi=aapcs-linux -mno-thumb-interwork
endif

ARCH_CXXFLAGS = -O2 -g
ARCH_LDFLAGS =

ARCH_LONGDOUBLE_FORMAT = IEEE_DOUBLE_LE
