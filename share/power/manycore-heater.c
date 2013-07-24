/*
  manycore-heater - stress program for many core 

  Written by  Kazutomo Yoshii <kazutomo@mcs.anl.gov>

  License: GPL
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <assert.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <values.h>
#include <math.h>
#include <omp.h>

int verbose = 0;

static double gettime(void)
{
  struct timeval tv;
  gettimeofday(&tv, 0);
  return (double)tv.tv_sec + (double)tv.tv_usec/1000.0/1000.0;
}

typedef enum {
  HM_MEMCPY=100,
  HM_RANDOM,
  HM_FPU,
  HM_FPUARCH,
} heater_mode_t;

const char* heater_mode_str(heater_mode_t m)
{
  switch(m) {
  case HM_MEMCPY:
    return "MEMCPY";
  case HM_RANDOM:
    return "RANDOM";
  case HM_FPU:
    return "FPU";
  case HM_FPUARCH:
    return "FPUARCH";
  }
  return "UNKNOWN";
}

const char* heater_mode_unit_str(heater_mode_t m)
{
  switch(m) {
  case HM_MEMCPY:
    return "MB/s";
  case HM_RANDOM:
    return "MB/s";
  case HM_FPU:
    return "MFlops";
  case HM_FPUARCH:
    return "MFlops";
  }
  return "UNKNOWN";
}




static void  usage(void)
{
  printf("manycore-heater [options]\n");
  printf("\n");
  printf("-t sec  : timeout in sec.  default=60sec. \n");
  printf("-m mode : memcpy, random, fpu\n");
  printf("-s size : test buffer size per rank in byte. 512 byte is minimum\n");
  printf("-f n    : number of fops(vmadd213pd) each iteration\n");
  printf("-i n    : number of iterations in mic_fma_copy()\n");

}

static unsigned int round_up_to_nearest_power_of_two(unsigned int v)
{
  v--;
  v |= v >> 1;
  v |= v >> 2;
  v |= v >> 4;
  v |= v >> 8;
  v |= v >> 16;
  v++;
  return v;
}


volatile double __attribute ((aligned(64))) dpdata[16];

void  manycore_heater(heater_mode_t mode, unsigned int eachmemsize, int nmadds, int niters, int timeout,
		      const char* hugetlbmnt)
{
  int size, rank, i;
  void* ptr;
  unsigned int totalmemsize = eachmemsize*128;   /* XXX: 128. fix this later */
  double  *results;
  double prepstarttime;
  char hugetlbfn[80];
  int  hugetlbfd;

  prepstarttime = gettime();

  if(hugetlbmnt) {
    snprintf(hugetlbfn,sizeof(hugetlbfn),"%s/mch",hugetlbmnt);
    hugetlbfd = open(hugetlbfn, O_CREAT|O_RDWR, 0755);
    assert(hugetlbfd>0);
    ptr = mmap(0, totalmemsize, PROT_READ|PROT_WRITE, MAP_SHARED, hugetlbfd, 0);
    assert(ptr!=MAP_FAILED);
  } else {
    assert( posix_memalign(&ptr, 1024, totalmemsize ) == 0 );
  }


  memset(ptr, 0, totalmemsize); /* populate the work area. even with
				   all zeros, FPU performance is the same. */

#pragma omp parallel private (rank), shared(size, results)
  {
    extern void set_strict_affinity(int size, int rank);
    rank = omp_get_thread_num();
    size = omp_get_num_threads();

    if(rank == 0)  {
      printf("# of threads = %d\n", size);
      printf("\n");

      results = (double*)malloc( size * sizeof(double) );
    }

    set_strict_affinity(size,rank);
  }

#pragma omp barrier

#pragma omp parallel private (rank), shared(size, results)
  {
    double starttime, elapsedtime;
    double res=0.0;
    unsigned long long per_rank_start_addr;
    int  count;
    extern void mic_fma_copy(double* dst, double* src, unsigned int nmadds, int niters);

    rank = omp_get_thread_num();

    per_rank_start_addr = ((unsigned long long)ptr) + (rank*eachmemsize);

    count = 0;

    if( mode == HM_MEMCPY ) {

#pragma omp barrier
      if(rank==0) printf("# HEATER.PREP_TIME=%lf\n", gettime()- prepstarttime);
      sleep(timeout/2);
      if(rank==0) printf("# HEATER.TIME1=%lf\n", gettime()- prepstarttime);

      starttime = gettime();
      for(;;) {
	elapsedtime = gettime() - starttime;
	if( elapsedtime > timeout ) break;

	/*
	{
	  uint64_t *tmpptr;
	  int nelemhalf = eachmemsize/sizeof(uint64_t)/2;
	  tmpptr = (uint64_t*)(per_rank_start_addr);

	  for(i=0;i<nelemhalf;i++) {
	    tmpptr[nelemhalf+i] =  tmpptr[i];
	  }
	}
	*/

	memcpy((double*)(per_rank_start_addr+eachmemsize/2),
	       (double*)(per_rank_start_addr),
	       eachmemsize/2);

	count++;
      }
      if(rank==0) printf("# HEATER.TIME2=%lf\n", gettime()- prepstarttime);

      //     sleep(timeout/2);
      //      if(rank==0) printf("# HEATER.TIME3=%lf\n", gettime()- prepstarttime);

      res = (double)eachmemsize*count/elapsedtime/1024.0/1024.0;
      if(verbose) printf("[%03d]: %lf (MB/s)  et=%lf (sec)  count=%d\n",
	     rank,res,
	     elapsedtime, count);
      
    } else if ( mode == HM_RANDOM ) {
      extern void prep_array_walk(uint64_t *array, int n, int mode, int w);
      extern uint64_t array_walk(uint64_t *array, int n );


      prep_array_walk((uint64_t*)per_rank_start_addr, 
		      eachmemsize/sizeof(uint64_t), 1 , 0 ); /* random */

#pragma omp barrier
      if(rank==0) printf("# HEATER.PREP_TIME=%lf\n", gettime()- prepstarttime);
      sleep(timeout/2);
      if(rank==0) printf("# HEATER.TIME1=%lf\n", gettime()- prepstarttime);

      starttime = gettime();
      for(;;) {
	elapsedtime = gettime() - starttime;
	if( elapsedtime > timeout ) break;
	array_walk((uint64_t*)per_rank_start_addr, eachmemsize/sizeof(uint64_t));
	count++;
      }
      if(rank==0) printf("# HEATER.TIME2=%lf\n", gettime()- prepstarttime);

      // sleep(timeout/2);
      // if(rank==0) printf("# HEATER.TIME3=%lf\n", gettime()- prepstarttime);

      res = (double)eachmemsize*count/elapsedtime/1024.0/1024.0;
      if(verbose) printf("[%03d]: %lf (MB/s)  et=%lf (sec)  count=%d\n",
	     rank,
	     res, 
	     elapsedtime, count);
    } else if ( mode == HM_FPU ) {
      int i;
      double a,b,c,d;

      a = dpdata[ 0];
      b = dpdata[ 1];
      c = dpdata[ 2];
      d = dpdata[ 3];

#pragma omp barrier
      if(rank==0) printf("# HEATER.PREP_TIME=%lf\n", gettime()- prepstarttime);
      sleep(timeout/2);
      if(rank==0) printf("# HEATER.TIME1=%lf\n", gettime()- prepstarttime);

      starttime = gettime();
      for(;;) {

	elapsedtime = gettime() - starttime;
	if( elapsedtime > timeout ) break;
	for(i=0;i<1000;i++) {
	  a += b*c+d;
	}
	count++;
      }
      dpdata[ 0] = a;
      if(rank==0) printf("# HEATER.TIME2=%lf\n", gettime()- prepstarttime);

      //     sleep(timeout/2);
      //     if(rank==0) printf("# HEATER.TIME3=%lf\n", gettime()- prepstarttime);

      res = (double)1000*count*3/elapsedtime/1000.0/1000.0;
      if(verbose) printf("[%03d]: %lf (MFlops) et=%lf (sec)  count=%d val=%lf\n",
	     rank,
	     res,
	     elapsedtime, count, a);
      


#ifdef ENABLE_INTEL_MIC
    } else if ( mode == HM_FPUARCH ) {
      double *dst, *src;
      unsigned long long eachmemoffset=0;

#pragma omp barrier
      if(rank==0) printf("# HEATER.PREP_TIME=%lf\n", gettime()- prepstarttime);
      sleep(timeout/2);
      if(rank==0) printf("# HEATER.TIME1=%lf\n", gettime()- prepstarttime);

      starttime = gettime();
      for(;;) {
	elapsedtime = gettime() - starttime;
	if( elapsedtime > timeout ) break;

	src = (double*)(per_rank_start_addr+eachmemoffset    );
	dst = (double*)(per_rank_start_addr+eachmemoffset+256);
	mic_fma_copy(dst, src, nmadds, niters);  count ++;
	eachmemoffset += 512;
	if( eachmemoffset >= eachmemsize ) eachmemoffset=0;
      }

      if(rank==0) printf("# HEATER.TIME2=%lf\n", gettime()- prepstarttime);

      //      sleep(timeout/2);

      res = (double)16*nmadds*niters*count / elapsedtime / 1000.0 / 1000.0;
      if(verbose) printf("[%03d]: Elapsed=%10.4lf(sec)  DataMoved=%10.4lf(MB/sec)  FOPS=%10.4lf(MFlops)\n",
	     rank,
	     elapsedtime,
	     (double)256*niters*count / elapsedtime / 1000.0 / 1000.0 ,
	     res);
#endif
    } 
    results[rank] = res;
  }

#pragma omp barrier

  /* statistics */
  {
    double total = 0.0, max = 0.0, min = MAXDOUBLE;
    double av = 0.0, sd = 0.0, tmp = 0.0;
    
    for(i=0;i<size;i++) {
      total += results[i];
      if( results[i] > max ) max = results[i];
      if( results[i] < min ) min = results[i];
    }
    av = total/(double)size;
    tmp = 0.0;
    for(i=0;i<size;i++) {
      tmp += (results[i]-av) * (results[i]-av);
    }
    tmp = tmp / (double)size;
    sd = sqrt(tmp);

    printf("# HEATER.%-7s(%6s): AGG=%9.2lf  MEAN=%8.2lf  MIN=%8.2lf  MAX=%8.2lf  SD=%8.2lf\n",
	   heater_mode_str(mode),
	   heater_mode_unit_str(mode),
	   total, 
	   av, 
	   min, max, sd);

#if 0
    printf("# %s.MEAN=%lf\n", heater_mode_str(mode), av);
    printf("# %s.MAX=%lf\n", heater_mode_str(mode), max);
    printf("# %s.MIN=%lf\n", heater_mode_str(mode), min);
    printf("# %s.SD=%lf\n", heater_mode_str(mode), sd);
#endif
  }
    
  if(hugetlbmnt) {
    munmap(ptr, totalmemsize);
    close(hugetlbfd);
    unlink(hugetlbfn) ;
  } else
    free(ptr);

  free(results);

  return;
} 



int main(int argc, char* argv[])
{
  int opt;
  unsigned int eachmemsize = 32*1024;
  int timeout = 10;
  heater_mode_t mode = HM_MEMCPY;
  /* XXX: these are MIC specific. clean up later */
  int nmadds= 800*1000*1000/14; /* MIC vector instruction calling counts. 0 means no FPU ops. */
  int niters = 1;  /* the number of iterations  */
  char *hugetlbmnt=NULL;

  while ((opt = getopt(argc, argv, "hm:s:f:t:i:H:")) != -1) {
    switch (opt) {
    case 'H':
      hugetlbmnt = strdup(optarg);
      break;
    case 'h':
      usage();
      exit(0);
      break;
    case 's':
      eachmemsize = atoi(optarg);
      break;
    case 'f':
      nmadds = atoi(optarg);
      break;
    case 't':
      timeout = atoi(optarg);
      break;
    case 'i':
      niters = atoi(optarg);
      break;
    case 'm':
      switch( optarg[0] ) {
      case 'm':
	mode = HM_MEMCPY;
	break;
      case 'r':
	mode = HM_RANDOM;
	break;
      case 'f':
	mode = HM_FPU;
	break;
      case 'F':
	mode = HM_FPUARCH;
	break;
      }
      break;
    default:
      usage();
    }
  }
  eachmemsize = round_up_to_nearest_power_of_two(eachmemsize);
  if( eachmemsize<512 )  eachmemsize  = 512;
  if( eachmemsize>8*1024*1024 )  eachmemsize  = 8*1024*1024;

  printf("mode:        %s\n", heater_mode_str(mode) );
  printf("eachmemsize: %d bytes\n", eachmemsize);
  printf("nmadds:      %d counts\n", nmadds);
  printf("niters:      %d counts\n", niters);
  printf("timeout:     %d sec\n", timeout);
  if(hugetlbmnt) {
    printf("hugetlbmnt:  %s\n", hugetlbmnt);
  }

  dpdata[ 0] = 0.0;
  dpdata[ 1] = 0.0;
  dpdata[ 2] = 0.0;
  dpdata[ 3] = 1.0;

  manycore_heater(mode, eachmemsize, nmadds, niters, timeout,hugetlbmnt);

  puts("[done]");

  return 0;
}
