#include <stdio.h>
#include <sys/time.h>
#include <omp.h>
#include "msr.h"


#define rdtsc __native_read_tsc 

static double gettime(void)
{
  struct timeval tv;
  gettimeofday(&tv, 0);
  return (double)tv.tv_sec + (double)tv.tv_usec/1000.0/1000.0;
}

static void flops_vec(void)
{
  unsigned long long start_tsc, elapsed_tsc;
  double start_sec, elapsed_sec;
  int i;
  int n = 1000*1000*200;
  start_sec = gettime();
  start_tsc = rdtsc();

  for(i=0;i<n;i++) {
    asm volatile (
		  "\tvmadd213pd %%v0,%%v1,%%v2\n"   /* 16 flops  per instruction*/
		  "\tvmadd213pd %%v3,%%v4,%%v5\n"   
		  //		  "\tvmadd213pd %%v6,%%v7,%%v8\n"   
		  // "\tvmadd213pd %%v9,%%v10,%%v11\n"   
		  :
		  :
		  : "memory", "%eax", "%edx" /* this is because rdtsc updates edx */
		  );
  }
  elapsed_tsc = rdtsc() - start_tsc;
  elapsed_sec = gettime() - start_sec;

  printf("%lf MHz\n", (double)elapsed_tsc/elapsed_sec/1000.0/1000.0 );
  printf("%llu clocks / %lf sec\n", elapsed_tsc, elapsed_sec);
  printf("%lf  clocks / vadd213pd\n", 
	 (double)elapsed_tsc/(double)n/2.0);
}

/*
  OMP_NUM_THREADS=1 ./flops_test
*/

int main(int argc, char* argv[])
{
  int rank, size;

  rank = native_read_pmc(0);

#pragma omp parallel private (rank), shared(size)
  {
    extern void set_strict_affinity(int size, int rank);
    rank = omp_get_thread_num();
    size = omp_get_num_threads();

    if(rank == 0)  {
      printf("# of threads = %d\n", size);
      printf("\n");
    }
    set_strict_affinity(size,rank);

#pragma omp barrier

    if( rank == 0 ) {
      flops_vec();
    }
  }
  return 0;
}
