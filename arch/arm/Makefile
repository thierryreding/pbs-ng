ARCH = arm

ifeq ($(arch.version),armv7-a)
  ARCH_LONG = $(ARCH)v7
endif

ifeq ($(arch.endian),little)
  ARCH_LONG := $(ARCH_LONG)l
endif

ifeq ($(arch.endian),big)
  ARCH_LONG := $(ARCH_LONG)b
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

CFLAGS = -marm -march=$(arch.version) -m$(arch.endian)-endian -Uarm

ifneq ($(arch.fpu),)
  CFLAGS += -mfloat-abi=hard
endif

ifeq ($(arch.abi),eabi)
  CFLAGS += -mabi=aapcs-linux -mno-thumb-interwork
endif
