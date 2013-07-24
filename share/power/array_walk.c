/*
  Array walk memory stress

  Written by Kazutomo Yoshii <kazutomo@mcs.anl.gov>
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include "s_bitop.h"

/*
  n: the number of elements in an uint64_t array (0 .. INT_MAX)

  mode:
  0: sequantial
  1: random
  2: stride

  w: stride width
 */
void prep_array_walk(uint64_t *array, int n, int mode, int w)
{
  int  i,j;

  if( mode == 0 ) {
      for(i=0;i<n;i++) array[i] = (i+1)%n;
  } else if( mode == 1 ) {
    /* fake random */
    int point_to, candidate;

    for(i=0; i<n; i++ ) {
      array[i] = (uint64_t)-1;
    }

    /* we can pick other than the first  */
    point_to = (rand()%(n-1))+1;
    array[0] = point_to;
    //printf("== array[0] = %d\n", point_to);

    for(i=0; i<(n-1); i++ ) {
      if( i==(n-2) ) { /* this is the last item. */
	array[point_to] = 0; /* back to array[0] */
	//printf("== array[%d] = %d # lst\n", point_to, 0);

      } else {
	/* find a candidate */
	candidate = (rand()%(n-1))+1;
	while( candidate == point_to ) {
	  candidate = (rand()%(n-1))+1;
	}

	if( array[candidate] != (uint64_t)-1 ) {
	  int off = (rand()%(n-1))+1;
	  int pos;

	  for(j=1; j<n-1; j++ ) {
	    pos = ((off+j)%(n-1))+1;
	    if( array[pos] == (uint64_t)-1 
		&& pos != point_to ) {

	      candidate = pos; 
	      break;
	    }
	  }
	  assert( j<(n-1) );
	}
	//printf("== array[%d] = %d\n", point_to, candidate);
	array[point_to] = candidate;
	point_to = candidate;
      }
    }

#ifdef NEED_TO_BE_OPTIMIZED
    s_bitop_t d = {0,0};
    uint64_t  *p64;
    int i, idx, n_0bits, pos;
    int dice, n_p64, pos_p64, pos_p8=0;
    idx = 0;
    n_0bits   = n;

    assert( s_bitop_alloc(&d, n) == n );

    /* assume that d->p is 64-byte aligned and d->n is multiples of 64 */
    p64 = (uint64_t*)d.p;
    n_p64 = n_0bits/64;

    for(;;) {
      s_bitop_set(&d,idx,1);

      n_0bits --;

      // s_bitop_dump(&d);

      if( n_0bits > 0 ) {
	// pos = s_bitop_find_nth(&d,(rand()%n_0bits)+1,0); // this is too slow
	
	/* find the next 64-bit slot */
	dice = rand()%n_p64;
	pos_p64 = dice;
	if( p64[dice] != (uint64_t)-1 ) {
	  pos_p64 = dice;
	} else {
	  for(i=0;i<n_p64;i++) {
	    pos_p64=(dice+1+i)%n_p64;
	    if( p64[pos_p64] != (uint64_t)-1 ) {
	      break;
	    }
	  }
	  if(i==n_p64) {  /* unlikely */
	    printf("Could not find the next 64-bit slot! n_0bits=%d\n",n_0bits);
	    exit(1);
	  }
	}
	// printf("** pos_p64=%d\n",pos_p64);

	/* find the next 8-bit slot */
	dice = rand()%8;
	pos_p8 = (pos_p64*8) + dice;
	if( d.p[pos_p8] == (uint8_t)-1 ) {
	  for(i=0;i<8;i++) {
	    if( d.p[pos_p64*8 + ((1+dice+i)%8)] != (uint8_t)-1 ) {
	      pos_p8 = pos_p64*8 + ((1+dice+i)%8);
	      break;
	    }
	  }
	  if(i==8) { /* unlikely */
	    printf("Could not find the next 8-bit slot! n_0bits=%d\n",n_0bits);
	    exit(1);
	  }
	}


	/* find the next single bit */
	dice = rand()%8;
	pos = pos_p8*8+dice;
	// printf("*** pos_p8=%d pos=%d\n",pos_p8,pos);
	if( s_bitop_get(&d,pos) == 1 ) {
	  for(i=0;i<8;i++) {
	    //printf("**** pos=%d %d\n",pos_p8*8 + ((dice+1+i)%8), s_bitop_get(&d, pos_p8*8 + ((dice+1+i)%8) ));

	    if( s_bitop_get(&d, pos_p8*8 + ((dice+1+i)%8) ) == 0 ) {
	      pos = pos_p8*8 + ((dice+1+i)%8);
	      break;
	    }
	  }
	  if(i==8) { /* unlikely */
	    printf("Could not find the next single slot! n_0bits=%d\n",n_0bits);
	    exit(1);
	  }
	}
	//printf("**** pos=%d\n",pos);

	array[idx] = pos;
	idx = pos;
      } else {
	array[idx] = 0;
	break;
      }
    }
    s_bitop_free(&d);
    //    for(i=0;i<n;i++)       printf("%3d: %3d\n",i,(int)array[i]);

#endif // DAMN_SLOW_BUT_UNICURSAL

  } else if ( mode == 2 ) {
    for(i=0;i<n;i++) {
      array[i] = (i+w)%n;
    }
  }
}

uint64_t array_walk(uint64_t *array, int n )
{
  int i;
  uint64_t idx, ret = 0;
  idx = array[0];
  ret = ret + idx;
  for(i=1;i<n;i++) {
    idx = array[idx]; 
    ret = ret + idx;
  }
  return ret;
}


uint64_t array_walk_marking(uint64_t *array, int n )
{
  int i;
  uint64_t idx, ret = 0;
  s_bitop_t d = {0,0};
  assert( s_bitop_alloc(&d, n) == n );

  idx = array[0];
  s_bitop_set(&d, 0 , 1);
  ret = ret + idx;
  for(i=1;i<n;i++) {
    s_bitop_set(&d, idx, 1);
    idx = array[idx];
    ret = ret + idx;
  }

  s_bitop_dump(&d);

  s_bitop_free(&d);

  return ret;
}



#ifdef __TEST_MAIN__

#include <sys/time.h>
#include <assert.h>
#include <string.h>

static double gettime(void)
{
  struct timeval tv;
  gettimeofday(&tv, 0);
  return (double)tv.tv_sec + (double)tv.tv_usec/1000.0/1000.0;
}



int main(int argc, char* argv[])
{
  uint64_t ret;
  uint64_t *arrayptr;
  double st,et;
  int n = (32*1024)/4/sizeof(uint64_t);
  int i;

  if( argc>= 2 ) {
    n = atoi(argv[1]);
  }
  printf("n=%d  (%lu bytes)\n", n, n*sizeof(uint64_t));

  assert( posix_memalign((void**)&arrayptr, 1024, n*sizeof(uint64_t) ) == 0 );
  memset(arrayptr, 0, n*sizeof(uint64_t));



  for(i=0;i<2;i++) {
    printf("\narray_walk mode=%d\n",i);
    st = gettime();
    prep_array_walk(arrayptr, n, i, 0 );
    et = gettime() - st;
    printf("prep=%lf(sec)\n", et);

    st = gettime();
    ret = array_walk(arrayptr,n);
    et = gettime() - st;
    printf("et=%lf(sec) ret=%lu\n", et,ret);
  }

  /*
  prep_array_walk(arrayptr, n, 1, 0 );
  array_walk_marking(arrayptr,n);
  */

  return 0;
}
#endif
