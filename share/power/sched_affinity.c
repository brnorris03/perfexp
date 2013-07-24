#define _GNU_SOURCE
#include <sched.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void set_strict_affinity(int size, int rank)
{
  cpu_set_t  cpuset_mask;

  CPU_ZERO(&cpuset_mask);
  CPU_SET(rank, &cpuset_mask);
  //    printf("count=%d\n", CPU_COUNT(&cpuset_mask));
  if ( sched_setaffinity(0, sizeof(cpuset_mask), &cpuset_mask) == -1 ) {
    printf("sched_setaffinity() failed\n");
    exit(1);
  }
#if 0
  {
    int i;
    char buf[1024];

    CPU_ZERO(&cpuset_mask);
    if ( sched_getaffinity(0, sizeof(cpuset_mask), &cpuset_mask) == -1 ) {
      printf("sched_getaffinity() failed\n");
      exit(1);
    }
    memset(buf,0,sizeof(buf));
    for( i=0; i<size; i++ ) {
      if ( CPU_ISSET(i, &cpuset_mask) ) {
	buf[i] = 'o';
      } else
	buf[i] = 'x';
    }
    printf("%03d: %s\n",rank,buf);
  }
#endif
}


#ifdef __TEST_MAIN__

#include <omp.h>

int main()
{
  int rank,size;

#pragma omp barrier

#pragma omp parallel private (size, rank)
  {
    rank = omp_get_thread_num();
    size = omp_get_num_threads();

    if( rank==0 ) {
      printf("size=%d\n",size);
    }
    
    set_strict_affinity(size, rank);
  }

  return 0;
}
#endif
