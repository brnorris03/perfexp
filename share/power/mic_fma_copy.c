/* 
   A FMA copy function for Intel MIC(Aurbrey Isle) specific 

   If nloop is large enough, this will be a FPU stress.  
   With nloop = freq/14, it runs around 1 sec.

   This also acts as 256 byte copy routine if nloop is 0.

   This function returns the total elapsed cycles, including load/store.

   dst: pointer to a 256-byte aligned buffer
        double va[8], vb[8], vc[8], vd[8]

   src: pointer to a 256-byte aligned buffer 
        double ve[8], vf[8], vg[8], vh[8]

   nloop_fma : loop count for vmadd213pd 

   if nloop > 0: 
     va[] => vd[]
     repeat nloop:  va[] * vb[] + vc[] => va[]
     va[] => ve[], vb[] => vf[], vc[] => vg[], vd[] => vh[]

   if nloop == 0:
     va[] => ve[], vb[] => vf[], vc[] => vg[], vd[] => vh[]


  Written by  Kazutomo Yoshii <kazutomo@mcs.anl.gov>

  License: GPL

  Hardware information on Intel MIC stress test program 

  MIC arch info
  30 cores are active
  four hardware thread per core
  L1:  32KB, 64-byte in linesize, 8-way, one cycle latency
  L2: 256KB, 64-byte in linesize, 8-way, 14 cycle at idle, up to 20-30 cycles
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

#include "msr.h"



void mic_fma_copy(double* dst, double* src, unsigned int nmadds, int niters)
{
  int i;
  
  for(i=0;i<niters;i++) {
    asm volatile (
		  "\tvloadq  %0, %%v0\n"
		  "\tvloadq  %1, %%v1\n"
		  "\tvloadq  %2, %%v2\n"
		  "\tvloadq  %3, %%v3\n" /* this loads is for benchmark purpose */
		  "\tmov %8, %%eax\n"
		  "\ttestl %%eax, %%eax\n"  /* if nloop is zero, skip FPU ops */
		  "\tje 2f\n"  
		  "\tvloadq  %0, %%v3\n" /* preserve va. already in cache line, so this only adds one cycle */
		  "\tnop\n"
		  ".align 8\n"
		  "1:\n"
		  "\tvmadd213pd %%v2,%%v1,%%v0\n"   /* 16 flops. takes 14~ cycles by my measurement  */
		  "\tnop\n"
		  "\tnop\n"
		  "\tnop\n"
		  "\tnop\n"
		  "\tdec %%eax\n"
		  "\tjne 1b\n"
		  "2:\n"
		  "\tvstoreq %%v0,%4\n"
		  "\tvstoreq %%v1,%5\n"
		  "\tvstoreq %%v2,%6\n"
		  "\tvstoreq %%v3,%7\n"
		  : "+m"(*(src+0)), "+m"(*(src+8)), "+m"(*(src+16)), "+m"(*(src+24)), 
		    "+m"(*(dst+0)), "+m"(*(dst+8)), "+m"(*(dst+16)), "+m"(*(dst+24))
		  : "Ir"(nmadds)
		  : "memory", "%eax", "%edx" /* this is because rdtsc updates edx */
		  );
  }
}


#ifdef __TEST_MAIN__

#include <sys/time.h>
static double gettime(void)
{
  struct timeval tv;

  gettimeofday(&tv, 0);

  return (double)tv.tv_sec + (double)tv.tv_usec/1000.0/1000.0;

}


int main()
{
  char __attribute ((aligned(256)))   src[256];
  char __attribute ((aligned(256)))   dst[256];
  double *va,*vb,*vc,*vd;
  double *ve,*vf,*vg,*vh;
  double st0, et0;
  unsigned long long  tsc_total, tsc_st;
  unsigned long n=0;
  int nfops=0;
  int i;
  
  printf("src:%p\n",src);
  printf("dst:%p\n",dst);

  va = (double*)(src+  0);
  vb = (double*)(src+ 64);
  vc = (double*)(src+128);
  vd = (double*)(src+192);

  ve = (double*)(dst+  0);
  vf = (double*)(dst+ 64);
  vg = (double*)(dst+128);
  vh = (double*)(dst+192);
  
  for(i=0;i<8;i++) {
    va[i] = (double)(1.0);
    vb[i] = (double)(1.0);
    vc[i] = (double)(i);
    vd[i] = 0.0;
  }

  /*
    latency bench
   */
  n = 2*(800*1000*1000)/40; /* loads/stores in mic_fma_copy() takes around 40 cycles at least and
			       cpu runs at 800MHz, which n yields that mic_fma_copy with nfops=0 takes >2sec */


  memset(src,0,sizeof(src));
  memset(dst,0,sizeof(dst));

  for(nfops=0; nfops<3; nfops++) {
    printf("\n== [latency nfops=%d] ========================================\n",nfops); 

    st0 = gettime();
    tsc_st =  __native_read_tsc();
    mic_fma_copy((double*)dst,(double*)src,nfops,n);

    tsc_total = __native_read_tsc() - tsc_st;
    et0 = gettime() - st0;
    printf("%lf cycles/iter,  elapsed %lf sec, %lf MHz  \n",
	   (double)tsc_total/(double)n,
	   et0,
	   (double)tsc_total/et0/1000.0/1000.0
	   );
  }

  return 0;

  puts("\n== [copy] ========================================"); 
  for(i=0;i<8;i++) printf("%2d: %12.1lf %12.1lf %12.1lf %12.1lf\n",i, va[i], vb[i], vc[i], vd[i] ); 
  memset(dst,0,sizeof(dst));
  mic_fma_copy((double*)dst,(double*)src,0,1);
  puts(""); for(i=0;i<8;i++) printf("%2d: %12.1lf %12.1lf %12.1lf %12.1lf\n",i, ve[i], vf[i], vg[i], vh[i] );

  puts("\n== [fma] ========================================"); 
  for(i=0;i<8;i++) printf("%2d: %12.1lf %12.1lf %12.1lf %12.1lf\n",i, va[i], vb[i], vc[i], vd[i] ); 
  memset(dst,0,sizeof(dst));
  mic_fma_copy((double*)dst,(double*)src,1,1);
  puts(""); for(i=0;i<8;i++) printf("%2d: %12.1lf %12.1lf %12.1lf %12.1lf\n",i, ve[i], vf[i], vg[i], vh[i] );
  /* validation */
  for(i=0;i<8;i++) {
    if( ve[i] != (vg[i]+vh[i]) ) {
      printf("Error at %d\n", i);
      exit(1);
    }
  }

  puts("\n== [fma2] ========================================"); 
  for(i=0;i<8;i++) printf("%2d: %12.1lf %12.1lf %12.1lf %12.1lf\n",i, va[i], vb[i], vc[i], vd[i] ); 
  memset(dst,0,sizeof(dst));

  nfops = 800*1000*1000/14;
  mic_fma_copy((double*)dst,(double*)src,nfops,1);
  puts(""); for(i=0;i<8;i++) printf("%2d: %12.1lf %12.1lf %12.1lf %12.1lf\n",i, ve[i], vf[i], vg[i], vh[i] );


  return 0;
}

#endif 

