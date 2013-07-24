#include <stdio.h>
#include <assert.h>
#include "s_bitop.h"


int main()
{
  s_bitop_t d;
  int n = 40;
  int i, pos, val;
  int prev;

  assert( s_bitop_alloc(&d, n) == n );

  s_bitop_dump(&d);

  for(i=0;i<n;i++) {
    val = rand()%2;
    pos = rand()%n;

    printf("\nset: pos=%d ",pos);
    prev = s_bitop_set(&d,pos,val);
    printf("%d => %d\n", prev, val);
    s_bitop_dump(&d);
  }

  s_bitop_free(&d);

  return 0;
}
