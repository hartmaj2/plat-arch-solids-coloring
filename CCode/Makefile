# Simple Makefile for the C++ orbit counter.
#
# Default target builds with OpenMP if available. On macOS the system
# clang ships without OpenMP, so we fall back to a plain single-threaded
# build there.

CXX      ?= c++
CXXSTD    = -std=c++17
OPT       = -O3 -DNDEBUG -march=native
WARN      = -Wall -Wextra -Wno-unused-parameter

UNAME_S  := $(shell uname -s)

# Try to detect OpenMP support.
ifeq ($(UNAME_S),Darwin)
  # On macOS try Homebrew libomp if present.
  ifneq ($(wildcard /opt/homebrew/opt/libomp/include/omp.h),)
    OMP_CFLAGS = -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include
    OMP_LIBS   = -L/opt/homebrew/opt/libomp/lib -lomp
  else ifneq ($(wildcard /usr/local/opt/libomp/include/omp.h),)
    OMP_CFLAGS = -Xpreprocessor -fopenmp -I/usr/local/opt/libomp/include
    OMP_LIBS   = -L/usr/local/opt/libomp/lib -lomp
  else
    OMP_CFLAGS =
    OMP_LIBS   =
  endif
else
  OMP_CFLAGS = -fopenmp
  OMP_LIBS   = -fopenmp
endif

CXXFLAGS  = $(CXXSTD) $(OPT) $(WARN) $(OMP_CFLAGS)
LDFLAGS   = $(OMP_LIBS)

all: orbits

orbits: orbits.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f orbits *.o

.PHONY: all clean
