#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <assert.h>
#include <sys/time.h>
#include <values.h>
#include <math.h>
#include <omp.h>

#include "msr.h"
#define  rdtsc  __native_read_tsc

static double gettime(void)
{
  struct timeval tv;
  gettimeofday(&tv, 0);
  return (double)tv.tv_sec + (double)tv.tv_usec/1000.0/1000.0;
}


uint64_t getcylclespersec(void)
{
  uint64_t s_tsc, e_tsc;
  double   s_time;

  s_time = gettime();
  s_tsc  = rdtsc();
  while( gettime()-s_time < 1.0 ) ; /* makes core busy, so tsc drift */
  e_tsc = rdtsc();

  return e_tsc-s_tsc;
}

static uint64_t CPU_HZ;

static void guess_cpu_hz(void)
{
  int i;
  double HZ=0.0;
  for(i=0;i<3;i++) HZ += (double)getcylclespersec();
  CPU_HZ = (uint64_t)(HZ/(double)i);
}


typedef struct {
  uint64_t  start;
  uint64_t  duration;
} detour_t;

#define N_DETOURS_PER_CORE 200

static void  usage(void)
{
  printf("recnoise [options]\n");
  printf("\n");
  printf("-p prefix : if no prefix specified, it doesn't save data\n");
}


static void  recordnoise(int timeout_sec, int threhold_us, const char* prefix)
{
#pragma omp parallel 
  {
  uint64_t start;
  uint64_t current, prev, td, min,max;
  uint64_t elapsed, noisesum;
  int idx = 0;
  int size, rank;
  uint64_t timeout;
  uint64_t threshold;
  detour_t detours[N_DETOURS_PER_CORE];

  memset(detours, 0, sizeof(detours));

  rank = omp_get_thread_num();
  size = omp_get_num_threads();


  set_strict_affinity(size,rank);

#pragma omp barrier
  guess_cpu_hz();
  timeout = timeout_sec*CPU_HZ;
  threshold = CPU_HZ*threhold_us/1000/1000;


  printf("[%03d] CPU_HZ=   %lu\n", rank, CPU_HZ);
  printf("[%03d] timeout=  %lu\n", rank, timeout);
  printf("[%03d] threshold=%lu\n", rank, threshold);

#pragma omp barrier

  min = timeout;
  max = 0;
  noisesum = 0;
  current = start=rdtsc();
  while(rdtsc()-start<timeout) {
    prev = current;
    current = rdtsc();
    td = current-prev;
    if( td>threshold ) {
      noisesum += td;
      detours[idx].start = current;
      detours[idx].duration= td;

      idx++;
      if( N_DETOURS_PER_CORE <= idx ) break;
    }
    if(td<min) min = td;
    if(td>max) max = td;
  }
  elapsed = rdtsc() - start;

#pragma omp barrier

  printf("[%03d] elapsed=  %lu\n", rank,elapsed);
  printf("[%03d] noisesum= %lu\n", rank,noisesum);
  printf("[%03d] max=      %lu\n", rank,max);
  printf("[%03d] min=      %lu\n", rank,min);
  //  printf("[%03%d] idx=      %d\n",idx);

  if(prefix) {
    char fn[256];
    FILE* fp;
    snprintf(fn, sizeof(fn), "%s%03d.txt",prefix,rank);
    fp = fopen(fn, "w");
    if( fp ) {
      int i;

      fprintf(fp,"# rank=%d\n", rank);
      fprintf(fp,"# CPU_HZ=%lu\n", CPU_HZ);
      fprintf(fp,"# timeout=%lu\n", timeout);
      fprintf(fp,"# threshold=%lu\n",  threshold);
      fprintf(fp,"# elapsed=%lu\n",elapsed);
      fprintf(fp,"# noisesum=%lu\n",noisesum);
      fprintf(fp,"# max=%lu\n",max);
      fprintf(fp,"# min=%lu\n",min);
      fprintf(fp,"# idx=%d\n", idx);
      fprintf(fp,"# start=%lu\n",detours[0].start);
      fprintf(fp,"#\n");
      
      for(i=0;i<N_DETOURS_PER_CORE;i++) {
	fprintf(fp,"%lu %lu\n", detours[i].start-detours[0].start, detours[i].duration);
      }
      fclose(fp);
    } else {
      printf("what happened? can't open %s\n",fn);
    }
  }


  }
}


int main(int argc, char* argv[])
{
  int opt;
  char* prefix=NULL;
  int threhold_us = 1;
  int timeout = 30;

  while ((opt = getopt(argc, argv, "hp:")) != -1) {
    switch (opt) {
    case 'h':
      usage();
      exit(0);
      break;
    case 'p':
      prefix = strdup(optarg);
      break;
    }
  }


  recordnoise(timeout, threhold_us, prefix);

  return 0;
}
