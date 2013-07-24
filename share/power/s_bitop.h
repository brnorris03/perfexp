/*
  simple damn straight bit ops

 */
#ifndef __S_BITOP_DEFINED__
#define __S_BITOP_DEFINED__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct {
  uint8_t* p;
  int   n;
} s_bitop_t;


/*
  return n on success, otherwise -1 on error
 */
inline int s_bitop_alloc(s_bitop_t* d, int n)
{
  if(!d) return -1;

  if( (n%8)!=0 ) return -1;

  d->n = n;
  d->p = (uint8_t*)malloc( (n/8)+1 );
  if( !d->p ) return -1;

  memset(d->p,0x0, (n/8)+1);

  return n;
}

inline void s_bitop_free(s_bitop_t *d)
{
  if( d && d->p ) free(d->p);
}

inline int s_bitop_get(s_bitop_t *d,int nth)
{
  if(!d) return -1;


  return ((d->p[nth/8])>>(7-(nth&0x7)))&1;
}

inline int s_bitop_set(s_bitop_t *d,int nth,int val)
{
  int ret;

  if(!d) return -1;

  ret = s_bitop_get(d,nth);

  if(val==0) {
    (d->p[nth/8]) &= (~(1<<(7-(nth&0x7))));
  } else if (val==1 ) {
    (d->p[nth/8]) |= (1<<(7-(nth&0x7)));
  } else {
    return -1;
  }

  return ret;
}

inline int s_bitop_count(s_bitop_t *d,int val)
{
  int ret=0;
  int i;

  if(!d) return -1;

  for(i=0;i<d->n;i++) {
    if( s_bitop_get(d,i) == val ) ret++;
  }

  return ret;
}


inline int s_bitop_count_setbits(unsigned char v)
{
  int ret;
  ret = 
    ((v&0x01)>0) + ((v&0x02)>0) + ((v&0x04)>0) + ((v&0x08)>0) +
    ((v&0x10)>0) + ((v&0x20)>0) + ((v&0x40)>0) + ((v&0x80)>0) ;
  return ret;
}


/*
  find nth 1bit or 0bit and return the position
  nth: 1 base

  return -1 if not found
 */
inline int s_bitop_find_nth(s_bitop_t *d,int nth,int val)
{
  int posinblock=0;
  int pos = -1;
  int i,j;

  if( nth > s_bitop_count(d,val) ) return -1;

  // puts("");
  for(i=0;i<(d->n)/8;i++) {
    unsigned char tmp;

    tmp = d->p[i];
  
    if(val==0) tmp = ~tmp;
    /*
    printf(":: i=%d tmp=%02x nth=%d  posonval=%d + count=%d\n",
    	   i, tmp, nth, posinblock, s_bitop_count_setbits(tmp));
    */
    if( nth <= (posinblock + s_bitop_count_setbits(tmp)) ) {
      int offset = 0;
      for(j=0;j<8;j++) {
	if( s_bitop_get(d,i*8+j)==val )  {
	  offset ++;
	  if( nth == (posinblock + offset) ) {
	    pos = i*8+j;
	    break;
	  }
	}
      }
    }
    posinblock += s_bitop_count_setbits(tmp);
  }

  return pos;
}


inline void s_bitop_dump(s_bitop_t *d)
{
  int i;
  printf("[dump] p=%p n=%d: ", d->p, d->n );
  for(i=0;i<(d->n/8)+1*((d->n%8)>0);i++) {
    printf("%02x ",d->p[i]);
  }
  printf("\n");

  printf("count: 1bits=%d 0bits=%d all=%d\n", 
	 s_bitop_count(d,1), 
	 s_bitop_count(d,0),
	 s_bitop_count(d,1)+s_bitop_count(d,0));

  for(i=0;i<d->n;i++) {
    if((i%10)==0)   printf("%d", (i/10)%10 );
    else            printf(" ");
  }
  printf("\n");
  for(i=0;i<d->n;i++) {
    printf("%d", i%10 );
  }
  printf("\n");

  for(i=0;i<d->n;i++) {
    if(s_bitop_get(d,i)) printf("o");
    else                 printf(".");
  }
  printf("\n");

  /*
  printf("1bits positions: ");
  for(i=0;i<s_bitop_count(d,1);i++) {
    printf("%d ",s_bitop_find_nth(d,i+1,1));
  }
  printf("\n");
  */
}


#endif

