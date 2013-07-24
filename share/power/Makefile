T=MIC

ifeq "$(T)" "MIC"

CC=icc
GCC=/usr/linux-l1om-4.7/bin/x86_64-l1om-linux-gcc

OBJS_ARCH=mic_fma_copy.o
CFLAGS=-Wall -O2 -DENABLE_INTEL_MIC -mmic -openmp
CFLAGS_GCC=-Wall -O2 -DENABLE_INTEL_MIC
LIBS=-lm
# gcc openmp flags: -fopenmp  .. -lgomp -lpthread
else
CFLAGS=-Wall -O2 -fopenmp
GCC=gcc  # for inline asm
CC=gcc
LIBS=-lgomp -lpthread -lm
endif



all: manycore-heater

sched_affinity.o : sched_affinity.c
	$(CC)  -c $(CFLAGS) $<

mic_fma_copy.o: mic_fma_copy.c msr.h
	$(GCC) -c $(CFLAGS_GCC) $<

array_walk.o: array_walk.c s_bitop.h
	$(CC)  -c $(CFLAGS) $<

manycore-heater: manycore-heater.c sched_affinity.o array_walk.o $(OBJS_ARCH)
	$(CC)  $(CFLAGS) -o $@ $^  $(LIBS)

recnoise: recnoise.c sched_affinity.o
	$(CC)  $(CFLAGS) -o $@ $^  $(LIBS)


#
# local test
#
mic_fma_copy_test : mic_fma_copy.c msr.h
	$(GCC) $(CFLAGS) -D__TEST_MAIN__ -o $@ $<

array_walk_test: array_walk.c s_bitop.h
	$(CC)  $(CFLAGS) -D__TEST_MAIN__ -o $@ $<

s_bitop_test : s_bitop_test.c s_bitop.h
	$(CC)  $(CFLAGS) -D__TEST_MAIN__ -o $@ $<


flops_test: flops.c sched_affinity.o
	$(CC)  $(CFLAGS) $(CFLAGS_ARCH) -o $@ $^ $(LIBS)

#
#
#

clean:
	rm -f manycore-heater  
	rm -f mic_fma_copy_test array_walk_test  s_bitop_test flops_test
	rm -f *.o a.out
	rm -f ODMTrace.txt


